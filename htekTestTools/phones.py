# Written by Stephen

import time
import re

from docs.conf import *


class Phone(TestUrl):

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

    def requests_get(self, url: str, name):
        """
        简化其他方法中调用requests的流程
        :param url: get的url
        :param name: 当前运行的方法名，由方法_func_name提供
        :return: 成功返回元祖(status_code, content.decode()); 失败返回错误提示
        """
        import requests
        cnt_retry = 0

        while cnt_retry <= 1:
            try:
                r = requests.get(url, timeout=5)
                log.debug('Try to execute [%s] on %s, url is --> %s' % (name, self.ext, url))
                if r.status_code == 200:
                    log.debug('Execute %s success [%s].' % (name, url))
                    try:
                        return r.status_code, r.content.decode()
                    except UnicodeDecodeError:
                        return r.status_code, r.content
                elif r.status_code == 401:
                    # log.error('Execute %s Failed. %s return 401...Retry now...' % (name, url))
                    cnt_retry += 1
                elif r.status_code == 404:
                    log.debug('404 Not Found --> %s' % url)
                    return 404, 'Not Found'
                else:
                    log.error('Execute %s on %s Failed. %s return %s...' % (name, self.ext, url, r.status_code))
                    return r.status_code, 'Get Failed'

            except requests.ConnectionError:
                log.error('Execute %s on %s Failed. Get %s connection error...' % (name, self.ext, url))
                return 500, '%s Connection Error...' % url

        log.error('Auth Failed, please verify it ...' )
        return 401, 'Auth Failed'

    @staticmethod
    def _func_name():
        # 返回当前运行的方法名，作为requests_get方法的参数->name
        import inspect
        return inspect.stack()[1][3]

    def prepare_cfg_file(self):
        # 准备cfg.xml文件，主要提供给方法get_line_key和set_line_key使用
        print('Preparing configuration files, please wait...')
        with open(self.cfg_file, 'w+', encoding='utf-8') as f:
            url = '%s/download_xml_cfg' % self.prefix
            log.info('Prepare config files %s...' % url)
            prepare_file = self.requests_get(url, self._func_name())
            if prepare_file[0] is 200:
                f.write(prepare_file[1])
                print('Configuration file prepared.')
                log.info('Prepare config files %s success.' % url)
            else:
                print('Configuration file prepare failed...')
                log.error('Prepare config files %s failed.' % url)

    def check_status(self, status):
        check_failed = False
        check_success = True
        retry_times = 0
        pat_return_code = r'(?<=<Return>)(\d)(?=</Return>)'
        code = phone_status(status)
        url_check_status = '%s%s' % (self.url_status, code)
        while retry_times < max_check_times:
            return_code = self.requests_get(url_check_status, self._func_name())
            if return_code[0] == 200:
                result = re.findall(pat_return_code, return_code[1])
                if result == ['0']:
                    log.info('Check status [%s] on %s success after %s time(s).' % (status, self.ip, retry_times))
                    return check_success
                elif result == ['1']:
                    retry_times += 1
                    time.sleep(0.5)
                    continue
                else:
                    log.error('Unknown Status...')
                    log.error(return_code[1].encode())
                    self.screen_shot(self._func_name())
                    return check_failed
            else:
                log.error('Return %s. Retry Now! - %s time(s).' % (return_code[0], retry_times))
                time.sleep(0.5)
                retry_times += 1
                continue

        log.error('Check status [%s] Failed!' % status)
        self.screen_shot('%s_%s' % (self._func_name(), status))
        return check_failed

    def dial(self, dst_ext: str, isnew:bool=True):
        """
        Phone(A) dial Phone(B)'s extension
        :param dst_ext: Destination Extension
        :return: 200->success; 400->get error; 500->connection error
        """

        # 定义拨号url，使用ActionURL方式拨号
        # url_dial = '%s/Phone_ActionURL&Command=1&Number=%s&%s' % (self.prefix, dst_ext, account)
        
        if isnew:
            line_key = 'l%s' % self.line
            self.press_key(line_key)
        else:
            pass
        time.time()
        for num in dst_ext:
            self.press_key(num)
        self.press_key('f1')

        log.info('%s dial %s success.' % (self.ext, dst_ext))
        return True


    def answer(self, cmd: str = 'f1, speaker, ok'):
        """
        Phone(A) answers the call
        :param cmd: str F1, SPEAKER or OK
        :return: 200->success; 400->get error; 500->connection error
        """
        if self.check_status('ringing'):
            url_answer = '%s%s' % (self.keyboard, cmd.upper())
            r_answer = self.requests_get(url_answer, self._func_name())
            if r_answer[0] == 200:
                self.keep_call(2)
                if self.check_status('talking'):
                    log.info('%s answered by %s.' % (self.ip, cmd.upper()))
                    self.keep_call(1)
                    return 200
                else:
                    log.error('Check status failed...But the scripts will continue.')
                    return 400
            else:
                log.error('%s answer failed.' % self.ip)
                return 500

    def hold(self):
        url_hold = '%s%s' % (self.keyboard, 'F_HOLD')
        self.requests_get(url_hold, self._func_name())
        if self.check_status('hold'):
            log.info('%s(%s) is now hold the call.' % (self.ext, self.ip))
        else:
            log.error('%s(%s) hold the call failed.' % (self.ext, self.ip))

    def keep_call(self, seconds: int):
        log.info('%s keep the call on for %s senconds.' % (self.ext, seconds))
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
            for k, v in key_account_code_dir.items():
                if matched_key_account[0] == v:
                    real_key_account = k
                else:
                    continue

            key_property = {'type'   : '%s' % real_key_type,
                            'value'  : '%s' % real_key_value,
                            'account': '%s' % real_key_account,
                            'label'  : '%s' % real_key_label}
            log.info('Check LineKey_%s properties return: %s' % (line_key_num[0], key_property))

            cfg_file.close()
            if real_key_type is not None:
                return key_property
            else:
                log.info(real_key_type)
                return 'Key Type mismatched.'
        #
        except BaseException:
            log.info('Input line key [ %s ] mismatched, need to check.' % key.upper())

    def set_line_key(self, key, k_type, value, account='Account1', label=''):
        import linecache
        from itertools import islice
        # 格式化 k_type 和 account 字符串，采用全大写形式
        key_type_upper = k_type.upper()
        account_upper = account.upper()

        # 准备字符串用来在xml文件中匹配，找出传入的key对应的type/value/account/label所在的行
        # 例如LineKey1_Type
        pat_key_type = dsskey_dir[key]['type']
        pat_key_value = dsskey_dir[key]['value']
        pat_key_account = dsskey_dir[key]['account']
        pat_key_label = dsskey_dir[key]['label']

        # 准备字符串用来在找到的行中，将对应的P值找出
        pat_pv = r'(?<=<)(P\d+)'

        # 在key_type_code_dir和key_account_code_dir字典中找到传入的k_type和account对应的值
        # 如N/A - 0
        pc_key_type = key_type_code_dir[key_type_upper]
        pc_key_account = key_account_code_dir[account_upper]

        cfg_xml_file = r'%s/cfg.xml' % os.path.dirname(__file__)
        cnt_line = 0
        lk_start_line = 1616
        lk_end_line = 1866

        with open(cfg_xml_file, 'r', encoding='utf-8') as f:
            for line in islice(f, lk_start_line, lk_end_line):
                cnt_line += 1
                matched_key_type = re.findall(pat_key_type, line, flags=re.IGNORECASE)
                if matched_key_type:
                    pv_key_type = re.findall(pat_pv, line)[0]
                    url_set_key_type = '%s%s=%s' % (self.setting, pv_key_type, pc_key_type)
                    r_key_type = self.requests_get(url_set_key_type, self._func_name())
                    if r_key_type[0] == 200:
                        log.info('%s set %s as %s success.' % (self.ip, key, k_type))
                    else:
                        log.info('%s set %s as %s failed.' % (self.ip, key, k_type))

                    value_line = linecache.getline(cfg_xml_file, lk_start_line + cnt_line + 2)
                    label_line = linecache.getline(cfg_xml_file, lk_start_line + cnt_line + 3)
                    account_line = linecache.getline(cfg_xml_file, lk_start_line + cnt_line + 4)
                    key_value = re.findall(pat_key_value, value_line, flags=re.IGNORECASE)
                    if key_value:
                        pv_key_value = re.findall(pat_pv, value_line)[0]
                        url_set_key_value = r'%s%s=%s' % (self.setting, pv_key_value, value)
                        r_key_value = self.requests_get(url_set_key_value, self._func_name())
                        if r_key_value[0] == 200:
                            log.info('%s set %s value as %s success.' % (self.ip, key, value))
                        else:
                            log.info('%s set %s value as %s failed. %s' % (self.ip, key, value, url_set_key_value))

                    key_account = re.findall(pat_key_account, account_line, flags=re.IGNORECASE)
                    if key_account:
                        pv_key_account = re.findall(pat_pv, account_line)[0]
                        url_set_key_account = '%s%s=%s' % (self.setting, pv_key_account, pc_key_account)
                        r_key_account = self.requests_get(url_set_key_account, self._func_name())
                        if r_key_account[0] == 200:
                            log.info('%s set %s account as %s success.' % (self.ip, key, account))
                        else:
                            log.info('%s set %s account as %s success.' % (self.ip, key, account))

                    key_label = re.findall(pat_key_label, label_line, flags=re.IGNORECASE)
                    if key_label:
                        pv_key_label = re.findall(pat_pv, label_line)[0]
                        url_set_key_label = '%s%s=%s' % (self.setting, pv_key_label, label)
                        if label != '':
                            r_key_label = self.requests_get(url_set_key_label, self._func_name())
                            if r_key_label[0] != 200:
                                log.info(self.ip + ' set label failed.')
                            else:
                                pass

    def set_p_value(self, p_value, option):
        url_set_pv = '{}{}={}'.format(self.setting, p_value.upper(), option)
        result = self.requests_get(url_set_pv, ('Set P Value {}'.format(p_value)))
        if result[0] == 200:
            log.info('%s(%s) set %s as %s success.' % (self.ext, self.ip, p_value, option))
            return 200
        else:
            log.info('%s(%s) set %s as %s failed.' % (self.ext, self.ip, p_value, option))
            return 400

    def press_key(self, cmd):
        url_press_key = self.keyboard + cmd.upper()
        r_pr_k = self.requests_get(url_press_key, (self._func_name(),cmd))
        if r_pr_k[0] == 200:
            time.sleep(0.5)
            log.info('%s(%s) press %s' % (self.ext, self.ip, cmd.upper()))
            return 200
        else:
            log.info('%s(%s) press %s failed...' % (self.ext, self.ip, cmd.upper()))
            return 400

    def transfer(self, phone, mod='BT'):
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
            log.error('Transfer mod error --> ' + mod)

    def exp_blf(self, cmd):
        for k, v in exp_blf_dir.items():

            if cmd.upper() != k:
                continue
            elif cmd.upper() == k:
                url_exp_key = self.keyboard + v
                r_exp_key = self.requests_get(url_exp_key, self._func_name())
                if r_exp_key[0] == 200:
                    time.sleep(1)
                    log.info(self.ip + ' trigger Expansion ' + cmd)
                    return 200
                else:
                    log.error(self.ip + ' trigger Expansion' + cmd + 'failed...')
                    return 400

    def end_call(self, cmd: str='f4, speaker, x'):
        """
        Phone(A) end the call.
        :param cmd: str F4, SPEAKER or X
        :return: True or False
        """

        url_end = self.keyboard + cmd.upper()
        r_end = self.requests_get(url_end, self._func_name())
        if r_end[0] == 200:
            time.sleep(2)
            if self.check_status('idle'):
                log.info(self.ip + ' The call ended with ' + cmd)
                return 200
            else:
                self.screen_shot(self._func_name())
                log.error(self.ip + ' end call failed with ' + cmd)
                return 400
        else:
            log.error(self.ip + ' Return ' + str(r_end[0]) + ', End call failed.')
            return 400

    def set_idle_status(self):
        url_return_idle = self.prefix + '/drd=RETURNIDLE'
        r_return_idle = self.requests_get(url_return_idle, self._func_name())
        if r_return_idle[0] == 200:
            log.info(self.ip + ' set [idle] status in ' + self.ip + ' success.')
        elif r_return_idle[0] == 404:
            log.error('%s has not merged, try press [F4] twice to return to idle.' % url_return_idle)
            self.press_key('f4')
            time.sleep(0.5)
            self.press_key('f4')
            time.sleep(2)
        else:
            log.error('%s return %s' % (url_return_idle, r_return_idle[0]))

        if self.check_status('idle'):
            log.info('Return to Idle status success.')
            return 200
        else:
            log.error('Return to Idle status failed.')
            return 400

    def get_memory(self):
        """
        Get Phone(A)'s memory info
        :return: True or False
        """

        pat_un_tag = r'(?<=\>)(.*)(?=\<)'
        url_memory = self.url_get_memory
        r_mem = self.requests_get(url_memory, self._func_name())
        if r_mem[0] == 200:
            mem_info = re.findall(pat_un_tag, r_mem[0])
            print(mem_info, time.time())
            log.info(self.ip + str(mem_info))
            return 200
        else:
            log.error(self.ip + 'Get memory failed, return ' + str(r_mem[0]))
            return 400

    def screen_shot(self, screen_name):
        """
        Capture the LCD screenShot when check status returns False
        :param screen_name: 在调用时传入
        :return: True or False
        """
        retry = 0

        url_screen_shot = self.screenshot
        while retry < 2:
            r_screen_shot = self.requests_get(url_screen_shot, self._func_name())
            if r_screen_shot[0] == 200:
                cur_time = time.strftime("%m%d_%H%M%S", time.localtime())
                stored_screen = '%s%s_%s.jpg' % (log.screen_dir, screen_name, cur_time)
                with open(stored_screen, 'wb') as f:
                    f.write(r_screen_shot[1])
                    log.info('Capture ScreenShot Success: %s' % stored_screen)
                    break
        else:
            log.error('Capture ScreenShot failed.')

    def error_prompt(self, filename, lineno):
        import sys
        cmd = input('file:%s, lines:%s, input fine for continue or exit for terminate the test: ' % (filename, lineno))
        if cmd == 'fine':
            log.war('Check Status Error, Continue AutoTest manually.')
            pass
        elif cmd == 'exit':
            log.error('Check Status Error, Terminate AutoTest manually.')
            sys.exit()
        else:
            self.error_prompt(filename, lineno)


class Phone3cx(Phone):

    # def _func_name(self):
    #     import inspect
    #     return inspect.stack()[1][3]

    def transfer(self, phone, mod='BT'):
        self.press_key('f_transfer')
        for number in phone.ext:
            self.press_key(number)

        if mod == 'AT':
            self.press_key('pound')
            if phone.answer('speaker'):
                self.keep_call(3)
                self.press_key('f1')
                if phone.check_status('talking'):
                    log.info('%s transferred the call to %s' % (self.ext, phone.ext))
        elif mod == 'SAT':
            log.war('On 3cx, it is not recommended using Semi-Attended Transfer.')
            pass
        elif mod == 'BT':
            self.press_key('f1')
            if phone.check_status('ringing'):
                log.info('%s transferred the call to %s' % (self.ext, phone.ext))
        else:
            log.error('Transfer mod error --> ' + mod)

    def set_3cx_status(self, status):

        def dial_service(code):
            line_key = 'l%s' % self.line
            self.press_key(line_key)
            for num in code:
                self.press_key(num)
            self.press_key('pound')
            if self.check_status('talking'):
                log.info('%s dial service code [%s] success.' % (self.ext, code))
                time.sleep(4)
                if self.check_status('idle'):
                    log.info('%s return to idle.' % self.ext)
                    return True
                else:
                    return False

        if status.upper() == 'AWAY':
            log.info('Set %s(%s) status on 3cx to %s' % (self.ext, self.ip, status))
            if dial_service('*31'):
                return True
            else:
                return False

        elif status.upper() == 'DND':
            log.info('Set %s(%s) status on 3cx to %s' % (self.ext, self.ip, status))
            if dial_service('*32'):
                return True
            else:
                return False

        elif status.upper() == 'NODND':
            log.info('Set %s(%s) status on 3cx to %s' % (self.ext, self.ip, status))
            if dial_service('*60'):
                return True
            else:
                return False

        elif status.upper() == 'LUNCH':
            log.info('Set %s(%s) status on 3cx to %s' % (self.ext, self.ip, status))
            if dial_service('*33'):
                return True
            else:
                return False

        elif status.upper() == 'BUSINESS':
            log.info('Set %s(%s) status on 3cx to %s' % (self.ext, self.ip, status))
            if dial_service('*34'):
                return True
            else:
                return False

        elif status.upper() == 'AVAILABLE':
            log.info('Set %s(%s) status on 3cx to %s' % (self.ext, self.ip, status))
            if dial_service('*30'):
                return True
            else:
                return False
