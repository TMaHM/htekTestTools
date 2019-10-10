# Written by Stephen
# 该文件在更新后需要同步到 ./venv/lib/python3.5/site-packages/PhoneLib/htek_phones.py

import time
import re
import sys
import requests

from data.conf import *


class Phone(TestUrl):
    log = Logger(echo=False)

    def __init__(self, ip: str, extension: str, line=1, usr='admin', pwd='admin'):
        TestUrl.__init__(self, ip, usr, pwd)

        """
        Initializing the Phone's IP, Extension, Web username and Web password
        and import class Url() use for getting the AutoTest URL
        :param ip: str Phone's IP
        :param extension: str Phone's Extension
        :param usr: str Phone's web username
        :param pwd: str Phone's web password
        """
        self.ip = ip
        self.ext = extension
        self.line = line
        self.usr = usr
        self.pwd = pwd
        self.cfg_file = 'cfg%s.xml' % self.ip.replace('.', '_')

    def requests_get(self, url: str, func_name):
        """
        简化其他方法中调用requests的流程
        除了capture screen外，都直接或间接使用该方法
        :param url: get的url
        :param func_name: 当前运行的方法名，由方法_func_name提供
        :return: 成功返回元祖(status_code, content.decode()); 失败返回错误提示
        """
        cnt_retry = 0

        while cnt_retry <= 2:
            try:
                r = requests.get(url, timeout=5)
                self.log.debug('Try to execute [%s] on %s, url is --> %s' % (func_name, self.ext, url))
                if r.status_code == 200:
                    self.log.debug('Execute %s success [%s].' % (func_name, url))
                    try:
                        return r.status_code, r.content.decode()
                    except UnicodeDecodeError:
                        return r.status_code, r.content
                elif r.status_code == 401:
                    # self.log.error('Execute %s Failed. %s return 401...Retry now...' % (name, url))
                    cnt_retry += 1
                elif r.status_code == 404:
                    self.log.debug('404 Not Found --> %s' % url)
                    return 404, 'Not Found'
                else:
                    self.log.error(
                        'Execute %s on %s Failed. %s return %s...' % (func_name, self.ext, url, r.status_code))
                    return r.status_code, 'Get Failed'

            except requests.ConnectionError:
                self.log.error('Execute %s on %s Failed. Get %s connection error...' % (func_name, self.ext, url))
                return 500, '%s Connection Error...' % url

        self.log.error('Auth Failed, please verify it ...')
        return 401, 'Auth Failed'

    @staticmethod
    def _func_name():
        # 返回当前运行的方法名，作为requests_get方法的参数->name
        import inspect
        return inspect.stack()[1][3]

    @staticmethod
    def _get_p_value_of_lk(line_num: int):
        """
        通过传入的line key的序号，找出其对应的所有设置项的P值
        :param line_num: 要查询P值的line key的序号
        :return: 以字典形式返回line key对应的所有设置项的P值
        """
        pv_of_line = {}
        lk_num = 'linekey%s' % line_num
        pv_of_line['type'] = line_key_dir[lk_num]['type']
        pv_of_line['mode'] = line_key_dir[lk_num]['mode']
        pv_of_line['value'] = line_key_dir[lk_num]['value']
        pv_of_line['label'] = line_key_dir[lk_num]['label']
        pv_of_line['acc'] = line_key_dir[lk_num]['acc']
        pv_of_line['ext'] = line_key_dir[lk_num]['ext']
        return pv_of_line

    def prepare_cfg_file(self):
        # 准备cfg.xml文件，主要提供给方法get_line_key使用
        print('Preparing configuration files, please wait...')
        with open(self.cfg_file, 'w+', encoding='utf-8') as f:
            url = '%s/download_xml_cfg' % self.prefix
            self.log.info('Prepare config files %s...' % url)
            prepare_file = self.requests_get(url, self._func_name())
            if prepare_file[0] is 200:
                f.write(prepare_file[1])
                print('Configuration file prepared.')
                self.log.info('Prepare config files %s success.' % url)
            else:
                print('Configuration file prepare failed...')
                self.log.error('Prepare config files %s failed.' % url)

    def check_status(self, status: str):
        """
        在达到最大检查次数前，如果状态检查失败，间隔0.5s重复执行
        超时截图并返回失败
        :param status: str 要检查的状态
        :return: True or False
        """
        check_failed = False
        check_success = True
        retry_times = 0
        pat_return_code = r'(?<=<Return>)(\d)(?=</Return>)'
        code = phone_status(status)
        url_check_status = '%s%s' % (self.url_status, code)

        while retry_times < MAX_CHECK_TIMES:
            return_code = self.requests_get(url_check_status, self._func_name())
            if return_code[0] == 200:
                result = re.findall(pat_return_code, return_code[1])
                if result == ['0']:
                    self.log.info('Check status [%s] on %s success after %s time(s).' % (status, self.ip, retry_times))
                    return check_success
                elif result == ['1']:
                    retry_times += 1
                    self.log.debug('Current status of %s on %s: %s' % (self.ext, self.ip, return_code[1]))
                    time.sleep(0.5)
                    continue
                else:
                    self.log.error('Unknown Status...')
                    self.log.error(return_code[1].encode())
                    self.screen_shot(self._func_name())
                    return check_failed
            else:
                self.log.error('Return %s. Retry Now! - %s time(s).' % (return_code[0], retry_times))
                self.log.debug('Current status of %s on %s: %s' % (self.ext, self.ip, return_code[1]))
                time.sleep(0.5)
                retry_times += 1
                continue

        self.log.error('Check status [%s] Failed!' % status)
        screen_cap = self.screen_shot('%s_%s' % (self._func_name(), status))
        if screen_cap == 200:
            return check_failed
        elif screen_cap == 401:
            return 401
        elif screen_cap == 404:
            return 404
        elif screen_cap == 500:
            return 500
        else:
            pass

    def dial(self, dst_ext: str, ):
        """
        Phone(A) dial Phone(B)'s extension
        :param dst_ext: Destination Extension
        :return: 200->success; 400->get error; 500->connection error
        """

        # 定义拨号url，使用ActionURL方式拨号
        self.log.info('%s try to dial %s' % (self.ext, dst_ext))
        url_dial = '%s/Phone_ActionURL&Command=1&Number=%s&Account=%s' % (self.prefix, dst_ext, str(self.line))
        r_dial = self.requests_get(url_dial, self._func_name())
        if r_dial[0] == 200:
            time.sleep(1)
            if self.check_status('outgoing'):
                self.log.info('%s dialed %s success.' % (self.ext, dst_ext))
                return 200
            else:
                self.log.info('Function Check Status Failed.')
                return 400
        elif r_dial[0] == 500:
            self.log.info('Function Dial return %s %s...' % (r_dial[0], r_dial[1]))
            return 500
        else:
            self.log.info('Function Dial return %s %s...' % (r_dial[0], r_dial[1]))
            return 400

    def answer(self, cmd: str = 'f1, speaker, ok'):
        """
        Phone(A) answers the call
        :param cmd: str F1, SPEAKER or OK
        :return: 200->success; 400->get error; 500->connection error
        """
        if self.check_status('ringing') is True:
            url_answer = '%s%s' % (self.keyboard, cmd.upper())
            r_answer = self.requests_get(url_answer, self._func_name())
            if r_answer[0] == 200:
                self.keep_call(2)
                if self.check_status('talking') is True:
                    self.log.info('%s answered by %s.' % (self.ip, cmd.upper()))
                    self.keep_call(1)
                    return 200
                else:
                    self.log.error('Check status failed...But the scripts will continue.')
                    return 400
            else:
                self.log.error('%s answer failed.' % self.ip)
                return 500

    def hold(self):
        """
        hold 方法
        :return: 200 Success or 400 False
        """
        url_hold = '%s%s' % (self.keyboard, 'F_HOLD')
        self.requests_get(url_hold, self._func_name())
        if self.check_status('hold') == 200:
            self.log.info('%s(%s) is now hold the call.' % (self.ext, self.ip))
            return 200
        else:
            self.log.error('%s(%s) hold the call failed.' % (self.ext, self.ip))
            return 400

    def keep_call(self, seconds: int):
        """
        保持通话方法
        实际上是将time.sleep以更易读的方式展现
        :param seconds: int 秒
        :return: 返回keep的时间
        """
        self.log.info('%s keep the call on for %s seconds.' % (self.ext, seconds))
        time.sleep(seconds)
        return seconds

    def get_line_key(self, key):
        """
        :param key: 指定要获取状态的LineKey，变量范围L1-L36
        :return: 返回指定的LineKey的属性字典
        :如L1->{'type': 'LINE', 'value': 'None', 'label': '8724 | Stephen Yu', 'account': 'ACCOUNT1'}
        """
        import linecache
        from itertools import islice

        self.prepare_cfg_file()

        # 为避免每次遍历整个cfg.xml文件，因此写死了开始行和结尾行
        lk_start_line = 1616
        lk_end_line = 1866
        real_key_type = None
        real_key_account = None

        try:
            line_key_num = re.findall(r'\d+', key)

            pat_line_key = r'LineKey%s_Type' % line_key_num[0]
            pat_key_type = r'(?<=>).*(?=<)'
            cfg_file = open(self.cfg_file, encoding='utf-8')
            for line in islice(cfg_file, lk_start_line, lk_end_line):
                # print(line)
                if pat_line_key in line:
                    matched_key_type_code = re.findall(pat_key_type, line)
                    if matched_key_type_code:
                        for k, v in key_type_code_dir.items():
                            if matched_key_type_code[0] == v:
                                real_key_type = k
                            else:
                                continue
                    else:
                        continue
                else:
                    continue

            matched_key_value = re.findall(pat_key_type, linecache.getline(self.cfg_file, lk_start_line + 2))
            if matched_key_value:
                real_key_value = matched_key_value[0]
            else:
                real_key_value = ''

            matched_key_label = re.findall(pat_key_type, linecache.getline(self.cfg_file, lk_start_line + 3))
            if matched_key_label:
                real_key_label = matched_key_label[0]
            else:
                real_key_label = ''

            matched_key_account = re.findall(pat_key_type, linecache.getline(self.cfg_file, lk_start_line + 4))
            for k, v in key_acc_code_dir.items():
                if matched_key_account[0] == v:
                    real_key_account = k
                else:
                    continue

            key_property = {'type': '%s' % real_key_type,
                            'value': '%s' % real_key_value,
                            'account': '%s' % real_key_account,
                            'label': '%s' % real_key_label}
            self.log.info('Check LineKey_%s properties return: %s' % (line_key_num[0], key_property))

            cfg_file.close()
            if real_key_type is not None:
                return key_property
            else:
                self.log.info(real_key_type)
                return 'Key Type mismatched.'
        #
        except BaseException:
            self.log.info('Input line key [ %s ] mismatched, need to check.' % key.upper())

    def set_line_key(self, key_line: int = None, key_type: str = None, key_mode: str = 'default', key_value: str = '',
                     key_label: str = '', key_acc: int = 1, key_ext: str = ''):
        """
        设置 line key
        :param key_line: int 要设置的line key的序号，如 key_line=1
        :param key_type: str 要设置的line key的类型，如 key_type='blf'，所有的key_type 请参见 conf.py 中 key_type_code_dir
        :param key_mode: str 要设置的line key的模式，如 key_mode='lock'，[default, lock, float]
        :param key_value: str 要设置的line key的值，如 key_value='8724'，如果不设置则为空
        :param key_label: str 要设置的line key的标签， 如 key_label='Test Key 1'
        :param key_acc: int 要设置的line key所属的 Account，如 key_acc=1
        :param key_ext: str 要设置的line key的 extension，一般配合 Call Park 类型使用，如 key_ext='*98'
        :return: [200: Success, 400: Failed, 500: Connection Error]
        """

        if key_line is not None:
            # 获取line key的P值字典
            pv_line = self._get_p_value_of_lk(key_line)
            # 获取传入各参数对应的code
            key_type = key_type.strip().upper()

            # 判断key type, mode, account是否在字典中。如果在，获取其对应的code；如果不在，对line key的设置没有意义，直接返回404
            if key_type in key_type_code_dir:
                pc_key_type = key_type_code_dir[key_type]
            else:
                self.log.error(
                    'Key %s Type [%s] can not match with key_type_code_dir, please check.' % (key_line, key_type))
                return 404

            if key_mode in key_mode_code_dir:
                pc_key_mode = key_mode_code_dir[key_mode]
            else:
                self.log.error(
                    'Key %s Mode [%s] can not match with key_mode_code_dir, please check.' % (key_line, key_mode))
                return 404

            key_acc = 'ACCOUNT%s' % key_acc
            if key_acc in key_acc_code_dir:
                pc_key_acc = key_acc_code_dir[key_acc]
            else:
                self.log.error(
                    'Key %s Mode [%s] can not match with key_mode_code_dir, please check.' % (key_line, key_acc))
                return 404

            # 调用set_p_value方法发送设置P值请求
            if self.set_p_value(pv_line['type'], pc_key_type) != 200:
                result = False
            elif self.set_p_value(pv_line['mode'], pc_key_mode) != 200:
                result = False
            elif self.set_p_value(pv_line['value'], key_value) != 200:
                result = False
            elif self.set_p_value(pv_line['label'], key_label) != 200:
                result = False
            elif self.set_p_value(pv_line['acc'], pc_key_acc) != 200:
                result = False
            elif self.set_p_value(pv_line['ext'], key_ext) != 200:
                result = False
            else:
                result = True
            return result
        else:
            self.log.info('Variable [Line] is None, it is Invalid. To use this method, please refer:')
            self.log.info('set_key(key_line=1, key_type=\'blf\', key_value=\'8724\', key_acc=1')
            return 401

    def set_p_value(self, p_value: str, option: str):
        url_set_pv = '{}{}={}'.format(self.setting, p_value.upper(), option)
        result = self.requests_get(url_set_pv, ('Set P Value {}'.format(p_value)))
        if result[0] == 200:
            self.log.info('%s(%s) set %s as %s success.' % (self.ext, self.ip, p_value, option))
            return 200
        else:
            self.log.info('%s(%s) set %s as %s failed.' % (self.ext, self.ip, p_value, option))
            return 400

    def press_key(self, cmd: str):
        """
        按键方法
        具体按键请参见【自动化测试Action URI说明V3.3】
        :param cmd:
        :return: 200 Success or 400 False
        """
        url_press_key = self.keyboard + cmd.upper()
        r_press_k = self.requests_get(url_press_key, (self._func_name(), cmd))
        if r_press_k[0] == 200:
            time.sleep(0.5)
            self.log.info('%s(%s) press %s' % (self.ext, self.ip, cmd.upper()))
            return 200
        else:
            self.log.info('%s(%s) press %s failed...' % (self.ext, self.ip, cmd.upper()))
            return 400

    def transfer(self, phone, mod='BT'):
        """
        用于执行 Transfer 的方法
        :param phone: 另一个Phone对象，即 Transfer 的对象
        :param mod: str Transfer的模式，当前支持 BT， SAT， AT
        :return:
        """
        if type(phone) is not 'class':
            print('transfer method need a class Phone as its parameter.')
            sys.exit(-1)
        else:
            pass

        self.press_key('f_transfer')
        for number in phone.ext:
            self.press_key(number)

        if mod == 'AT':
            self.press_key('pound')
            if phone.answer('speaker'):
                self.keep_call(3)
                self.press_key('f1')
        elif mod == 'SAT':
            self.press_key('pound')
            if phone.check_status('ringing'):
                self.press_key('f1')
        elif mod == 'BT':
            self.press_key('f1')
        else:
            self.log.error('Transfer mod error --> ' + mod)

    def press_exp_key(self, cmd: str):
        """
        扩展板按键方法
        :param cmd: str range: [L1 - L20]
        :return: 200 Success or 400 False
        """
        # 如果cmd不在字典exp_key_dir中，直接返回400
        if cmd.upper() not in exp_key_dir:
            self.log.info('cmd [%s] can not match with exp_key_dir, please check.' % cmd)
            return 400

        for k, v in exp_key_dir.items():
            if cmd.upper() != k:
                continue
            elif cmd.upper() == k:
                url_exp_key = self.keyboard + v
                r_exp_key = self.requests_get(url_exp_key, self._func_name())
                if r_exp_key[0] == 200:
                    time.sleep(1)
                    self.log.info(self.ip + ' trigger Expansion ' + cmd)
                    return 200
                else:
                    self.log.error(self.ip + ' trigger Expansion' + cmd + 'failed...')
                    return 400

    def end_call(self, cmd: str = 'f4, speaker, x'):
        """
        Phone(A) end the call.
        :param cmd: str range: [F4, SPEAKER or X]
        :return: 200 Success or 400 False
        """

        url_end = self.keyboard + cmd.upper()
        r_end = self.requests_get(url_end, self._func_name())
        if r_end[0] == 200:
            time.sleep(2)
            if self.check_status('idle'):
                self.log.info(self.ip + ' The call ended with ' + cmd)
                return 200
            else:
                self.screen_shot(self._func_name())
                self.log.error(self.ip + ' end call failed with ' + cmd)
                return 400
        else:
            self.log.error(self.ip + ' Return ' + str(r_end[0]) + ', End call failed.')
            return 400

    def set_idle_status(self, model: str = 'normal'):
        """
        设置 idle 态，不需要参数
        :return: 200 Success or 400 False
        """
        # if model is 'normal':
        #     url_return_idle = self.press_key('x')
        #     r_return_idle = self.requests_get(url_return_idle, self._func_name())
        #
        #
        # elif model is 'drd':

        url_return_idle = self.prefix + '/drd=RETURNIDLE'
        r_return_idle = self.requests_get(url_return_idle, self._func_name())
        if r_return_idle[0] == 200:
            self.log.info(self.ip + ' set [idle] status in ' + self.ip + ' success.')
        elif r_return_idle[0] == 404:
            self.log.error('%s has not merged, try press [F4] twice to return to idle.' % url_return_idle)
            self.press_key('f4')
            time.sleep(0.5)
            self.press_key('f4')
            time.sleep(2)
        elif r_return_idle[0] == 401:
            self.log.info('401? Are you sure?')
        else:
            self.log.error('%s return %s' % (url_return_idle, r_return_idle[0]))
            return 400

        if self.check_status('idle'):
            self.log.info('Return to Idle status success.')
            return 200
        else:
            self.log.error('Return to Idle status failed.')
            return 400

    def get_memory(self):
        """
        Get Phone(A)'s memory info
        :return: 200 Success or 400 False
        """
        pat_un_tag = r'(?<=\>)(.*)(?=\<)'
        url_memory = self.url_get_memory
        r_mem = self.requests_get(url_memory, self._func_name())
        if r_mem[0] == 200:
            mem_info = re.findall(pat_un_tag, r_mem[0])
            print(mem_info, time.time())
            self.log.info(self.ip + str(mem_info))
            return 200
        else:
            self.log.error(self.ip + 'Get memory failed, return ' + str(r_mem[0]))
            return 400

    def screen_shot(self, screen_name):
        """
        Capture the LCD screenShot when check status returns False
        :param screen_name: 在调用时传入
        :return: 200 Success or 401 Auth Failed or 404 Not Found or 500 Connection Error
        """
        retry = 0
        url_screen_cap = self.screenshot

        while retry < 2:
            # 避免因为第一次get返回401导致截屏失败
            cur_time = time.strftime("%m%d_%H%M%S", time.localtime())
            stored_screen = '%s%s_%s.jpg' % (self.log.screen_dir, screen_name, cur_time)
            screen_file = open(stored_screen, 'wb')
            try:
                r_screen_shot = requests.get(url_screen_cap, timeout=5)
                if r_screen_shot.status_code == 200:
                    screen_file.write(r_screen_shot.content)
                    self.log.info('Capture ScreenShot Success: %s' % stored_screen)
                    break
                elif r_screen_shot.status_code == 401:
                    if retry < 1:
                        self.log.info('Capture ScreenShot Return 401, will try again')
                        retry += 1
                    else:
                        self.log.info('Capture ScreenShot Failed Because Auth Error. Please check!')
                        screen_file.close()
                        return 401
                elif r_screen_shot.status_code == 404:
                    self.log.info('Capture ScreenShot Failed Because Resource Not Found.')
                    return 404
                else:
                    self.log.info(
                        'Capture Failed Because Unknown Reason. Return Code is %s' % r_screen_shot.status_code)

            except requests.ConnectionError:
                self.log.info('Connection Failed. URL -> [%s]' % url_screen_cap)
                return 500

    def error_prompt(self, filename, line_num):
        """
        用于在检查状态错误时中断脚本，依据用户的输入进行下一步动作：
        继续执行 或 停止运行
        :param filename: 当前运行的脚本名
        :param line_num: 错误发送所在行
        :return:
        """
        import sys
        cmd = input(
            'file:%s, lines:%s, input fine for continue or exit for terminate the test: ' % (filename, line_num))
        if cmd == 'fine':
            self.log.war('Check Status Error, Continue AutoTest manually.')
            pass
        elif cmd == 'exit':
            self.log.error('Check Status Error, Terminate AutoTest manually.')
            sys.exit()
        else:
            self.error_prompt(filename, line_num)
