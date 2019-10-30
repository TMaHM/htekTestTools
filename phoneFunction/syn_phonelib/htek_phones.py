# Written by Stephen

import time
import re
import sys
import requests
import traceback

from PhoneLib.htek_phone_conf import *


class Phone(TestUrl):

    def __init__(self, ip: str, extension: str, line=1, model: str = 'uc926e', usr: str = 'admin', pwd: str = 'admin'):
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
        self.model = model
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
                log.debug('Try to execute [%s] on %s, url is --> %s' % (func_name, self.ext, url))
                if r.status_code == 200:
                    log.debug('Execute %s success [%s].' % (func_name, url))
                    try:
                        return r.status_code, r.content.decode()
                    except UnicodeDecodeError:
                        log.debug(traceback.format_exc())
                        return r.status_code, r.content
                elif r.status_code == 401:
                    # log.error('Execute %s Failed. %s return 401...Retry now...' % (name, url))
                    cnt_retry += 1
                elif r.status_code == 404:
                    log.debug('404 Not Found --> %s' % url)
                    return 404, 'Not Found'
                else:
                    log.error(
                        'Execute %s on %s Failed. %s return %s...' % (func_name, self.ext, url, r.status_code))
                    return r.status_code, 'Get Failed'

            except requests.ConnectionError:
                log.error('Execute %s on %s Failed. Get %s connection error...' % (func_name, self.ext, url))
                log.debug(traceback.format_exc())
                return 500, '%s Connection Error...' % url

        log.error('Auth Failed on %s, Return code is %s, please verify it ...' % (self.ip, r.status_code))
        return r.status_code, 'Auth Failed'

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
            url = '%s/download_xml_cfg' % self.url_prefix
            log.info('Prepare config files %s...' % url)
            prepare_file = self.requests_get(url, self._func_name())
            if prepare_file[0] is 200:
                f.write(prepare_file[1])
                print('Configuration file prepared.')
                log.info('Prepare config files %s success.' % url)
            else:
                print('Configuration file prepare failed...')
                log.error('Prepare config files %s failed.' % url)

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

        if status is 'idle':
            url_check_status = self.url_idle_status
            pat_return_code = r'(?<=<CheckGuiStatus>)(\d)(?=</CheckGuiStatus>)'
        else:
            code = phone_status(status)
            pat_return_code = r'(?<=<Return>)(\d)(?=</Return>)'
            url_check_status = '%s%s' % (self.url_status, code)

        while retry_times < MAX_CHECK_TIMES:
            return_code = self.requests_get(url_check_status, self._func_name())
            if return_code[0] == 200:
                result = re.findall(pat_return_code, return_code[1])
                if result == ['0']:
                    log.info('Check status [%s] on %s success after %s time(s).' % (status, self.ip, retry_times))
                    return check_success
                elif result == ['1']:
                    retry_times += 1
                    log.debug('Current status of %s on %s: %s' % (self.ext, self.ip, return_code[1]))
                    time.sleep(0.5)
                    continue
                else:
                    log.error('Unknown Status...')
                    log.error(return_code[1].encode())
                    self.screen_shot(self._func_name())
                    return check_failed
            elif return_code[0] == 401:
                log.error('Return 401. Retry Now! - %s time(s).' % (return_code[0], retry_times))
                log.debug('Current status of %s on %s: %s' % (self.ext, self.ip, return_code[1]))
                time.sleep(0.5)
                retry_times += 1
                continue
            else:
                log.error('Return code is %s, Request Terminated.' % return_code[0])
                return check_failed

        log.error('Check status [%s] on %s Failed!' % (status, self.ext))
        log.error('Return code is %s, Return content is \n%s' % (return_code[0], return_code[1]))
        screen_cap = self.screen_shot('%s_%s' % (self._func_name(), status))
        return check_failed

    def dial(self, dst_ext: str, ):
        """
        Phone(A) dial Phone(B)'s extension
        :param dst_ext: Destination Extension
        :return: 200->success; 400->get error; 500->connection error
        """

        # 定义拨号url，使用ActionURL方式拨号
        log.info('%s try to dial %s' % (self.ext, dst_ext))
        url_dial = '%s/Phone_ActionURL&Command=1&Number=%s&Account=%s' % (self.url_prefix, dst_ext, str(self.line))
        r_dial = self.requests_get(url_dial, self._func_name())
        if r_dial[0] == 200:
            time.sleep(1)
            if self.check_status('outgoing'):
                log.info('%s dialed %s success.' % (self.ext, dst_ext))
                return 200
            else:
                log.info('Function Check Status Failed.')
                return 400
        elif r_dial[0] == 500:
            log.info('Function Dial return %s %s...' % (r_dial[0], r_dial[1]))
            return 500
        else:
            log.info('Function Dial return %s %s...' % (r_dial[0], r_dial[1]))
            return 400

    def answer(self, cmd: str = 'SPEAKER'):
        """
        Phone(A) answers the call
        :param cmd: str F1, SPEAKER or OK
        :return: 200->success; 400->get error; 500->connection error
        """
        if self.check_status('ringing') is True:
            url_answer = '%s%s' % (self.url_keyboard, cmd.upper())
            r_answer = self.requests_get(url_answer, self._func_name())
            if r_answer[0] == 200:
                self.keep_call(2)
                if self.check_status('talking') is True:
                    log.info('%s(%s) answered success.' % (self.ext, self.ip))
                    return 200
                else:
                    log.error('%s Check status failed...But the scripts will continue.' % self.ext)
                    return 400
            else:
                log.error('%s(%s) answered failed.' % (self.ext, self.ip))
                return 500

    def hold(self):
        """
        hold 方法
        :return: 200 Success or 400 False
        """
        url_hold = '%s%s' % (self.url_keyboard, 'F_HOLD')
        self.requests_get(url_hold, self._func_name())
        if self.check_status('hold') == 200:
            log.info('%s(%s) is now hold the call.' % (self.ext, self.ip))
            return 200
        else:
            log.error('%s(%s) hold the call failed.' % (self.ext, self.ip))
            return 400

    def keep_call(self, seconds: int):
        """
        保持通话方法
        实际上是将time.sleep以更易读的方式展现
        :param seconds: int 秒
        :return: 返回keep的时间
        """
        log.info('%s keep the call for %s seconds.' % (self.ext, seconds))
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
            cnt = 0
            for line in islice(cfg_file, lk_start_line, lk_end_line):
                # print(line)
                cnt += 1
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

            matched_key_value = re.findall(pat_key_type, linecache.getline(self.cfg_file, lk_start_line + cnt))
            if matched_key_value:
                real_key_value = matched_key_value[0]
            else:
                real_key_value = ''

            matched_key_label = re.findall(pat_key_type, linecache.getline(self.cfg_file, lk_start_line + cnt + 1))
            if matched_key_label:
                real_key_label = matched_key_label[0]
            else:
                real_key_label = ''

            matched_key_account = re.findall(pat_key_type, linecache.getline(self.cfg_file, lk_start_line + cnt + 2))
            for k, v in key_acc_code_dir.items():
                if matched_key_account[0] == v:
                    real_key_account = k
                else:
                    continue

            key_property = {'type': '%s' % real_key_type,
                            'value': '%s' % real_key_value,
                            'account': '%s' % real_key_account,
                            'label': '%s' % real_key_label}
            log.info('Check LineKey_%s properties return: %s' % (line_key_num[0], key_property))

            cfg_file.close()
            if real_key_type is not None:
                return key_property
            else:
                log.info(real_key_type)
                return 'Key Type mismatched.'
        #
        except BaseException:
            log.debug(traceback.format_exc())
            log.info('Input line key [ %s ] mismatched, need to check.' % key.upper())

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
                log.error(
                    'Key %s Type [%s] can not match with key_type_code_dir, please check.' % (key_line, key_type))
                return 404

            if key_mode in key_mode_code_dir:
                pc_key_mode = key_mode_code_dir[key_mode]
            else:
                log.error(
                    'Key %s Mode [%s] can not match with key_mode_code_dir, please check.' % (key_line, key_mode))
                return 404

            key_acc = 'ACCOUNT%s' % key_acc
            if key_acc in key_acc_code_dir:
                pc_key_acc = key_acc_code_dir[key_acc]
            else:
                log.error(
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
            log.info('Variable [Line] is None, it is Invalid. To use this method, please refer:')
            log.info('set_key(key_line=1, key_type=\'blf\', key_value=\'8724\', key_acc=1')
            return 401

    def set_p_value(self, p_value: str, option: str):
        url_set_pv = '{}{}={}'.format(self.url_setting, p_value.upper(), option)
        result = self.requests_get(url_set_pv, ('Set P Value {}'.format(p_value)))
        if result[0] == 200:
            log.info('%s(%s) set %s as %s success.' % (self.ext, self.ip, p_value, option))
            return 200
        else:
            log.info('%s(%s) set %s as %s failed.' % (self.ext, self.ip, p_value, option))
            return 400

    def press_key(self, cmd: str):
        """
        按键方法
        具体按键请参见【自动化测试Action URI说明V3.3】
        :param cmd:
        :return: 200 Success or 400 False
        """
        url_press_key = self.url_keyboard + cmd.upper()
        r_press_k = self.requests_get(url_press_key, (self._func_name(), cmd))
        if r_press_k[0] == 200:
            time.sleep(0.6)
            log.info('%s(%s) press %s' % (self.ext, self.ip, cmd.upper()))
            return 200
        else:
            log.info('%s(%s) press %s failed...' % (self.ext, self.ip, cmd.upper()))
            return 400

    def transfer(self, target, mod='BT'):
        """
        用于执行 Transfer 的方法
        当前话机必须已处在一路通话中
        该方法只执行transfer，这意味着最后一步是按下Transfer以完成此功能，而不是完成整个transfer业务
        所以，在实际使用时，除了Attended Transfer外，都需要在transfer后让目标接起
        :param target: 另一个Phone对象，即 Transfer 的对象
        :param mod: str Transfer的模式，当前支持 BT， SAT， AT
        :return: 200 Success
                 404 Not Found
                 405 Permission Denied
                 481 Remote Error
        """
        if isinstance(target, Phone) is not True:
            log.error(
                'Transfer method need a Phone(type class) as parameter.\n'
                'But the recieved parameter is type: %s' % type(target))
            return 405
        else:
            pass

        if mod.upper() in ('BT', 'AT', 'SAT'):
            pass
        else:
            log.error('Method Error, should be one of (BT, AT, SAT).')
            return 405

        if self.check_status('talking') is True:
            pass
        else:
            log.error('No call here -> %s' % self.ext)
            return 404

        self.press_key('f_transfer')
        for number in target.ext:
            self.press_key(number)

        if mod == 'AT':
            log.info(
                '{executor} execute [Attended Transfer] to {target}'.format(executor=self.ext, target=target.ext))
            self.press_key('OK')
            if target.answer() == 200:
                self.press_key('f_transfer')
                return 200
            else:
                log.error('Target %s answer failed.' % target.ext)
                return 481
        elif mod == 'SAT':
            log.info('{executor} execute [Semi-Attended Transfer] to {target}'.format(executor=self.ext,
                                                                                      target=target.ext))
            self.press_key('OK')
            if phone.check_status('ringing') is True:
                self.press_key('f_transfer')
                return 200
            else:
                log.error('Target %s is not in ringing status.' % target.ext)
                return 481
        elif mod == 'BT':
            log.info('{executor} execute [Blind Transfer] to {target}'.format(executor=self.ext, target=target.ext))
            self.press_key('f_transfer')
            return 200
        else:
            log.error('Transfer mod error --> ' + mod)
            return 405

    def press_exp_key(self, cmd: str):
        """
        扩展板按键方法，具体的按键请参看htek_phone_conf中的字典 exp_key_dir
        :param cmd: str range: [L1 - L20]
        :return: 200 Success or 400 False
        """
        # 如果cmd不在字典exp_key_dir中，直接返回400
        if cmd.upper() not in exp_key_dir:
            log.info('cmd [%s] can not match with exp_key_dir, please check.' % cmd)
            return 400

        for k, v in exp_key_dir.items():
            if cmd.upper() != k:
                continue
            elif cmd.upper() == k:
                url_exp_key = self.url_keyboard + v
                r_exp_key = self.requests_get(url_exp_key, self._func_name())
                if r_exp_key[0] == 200:
                    time.sleep(1)
                    log.info(self.ip + ' trigger Expansion ' + cmd)
                    return 200
                else:
                    log.error(self.ip + ' trigger Expansion' + cmd + 'failed...')
                    return 400

    def end_call(self, cmd: str = 'X'):
        """
        结束当前通话，默认使用X键.
        :param cmd: str range: [F4, SPEAKER or X]
        :return: 200 Success or 400 False
        """

        url_end = self.url_keyboard + cmd.upper()
        r_end = self.requests_get(url_end, self._func_name())
        if r_end[0] == 200:
            time.sleep(2)
            if self.check_status('idle'):
                log.info(self.ip + ' end the call with ' + cmd)
                return 200
            else:
                self.screen_shot(self._func_name())
                log.error(self.ip + ' end call failed with ' + cmd)
                return 400
        else:
            log.error(self.ip + ' Return ' + str(r_end[0]) + ', End call failed.')
            return 400

    def flexible_seating(self, method: str = None, solution: str = None, aid: int = 0, number: str = None,
                         pwd: str = None, ):
        """
        Broadsoft 平台的 Flexible Seating 登入登出功能
        在登入或者登出后，通过图片对比的方法判断是否执行成功
        :param method: srt, 要执行的操作, In or Out
        :param aid: int, 默认值为0, 一般也为0
        :param number: str, 登入时需要的User ID
        :param pwd: str, 登入时需要的Password
        :return: 成功返回200； 操作成功，但图片对比失败返回400； 输入的method不匹配返回500； 其他返回request_get的返回值，如401
        """

        if method.upper() is 'In':
            url_flx_s = self.url_drd_prefix + 'GUESTIN:aid=%s&number=%s&password=%s' % (aid, number, pwd)
        elif method.upper() is 'OUT':
            url_flx_s = self.url_drd_prefix + 'GUESTOUT'
        else:
            log.info('Flexible Seating method must be specified as In or Out, but you set it as %s' % method)
            return 500

        r_flex_s = self.requests_get(url_flx_s, self._func_name())
        if r_flex_s[0] == 200:
            log.info('Operation Flexible Seating Guest {method} success.'.format(method=method))
            # 截屏(成功返回路径，失败返回失败码)
            captured_img = self.screen_shot('flx_{}'.format(method))
            # 临时图片路径
            temp_img = '{tmp_path}/temp_img.jpg'.format(tmp_path=IMG_TEMP_PATH)
            # 正确图片路径
            standard_img = '{path}/{solution}_{model}_flx_{method}.jpg'.format(path=IMG_STANDARD_PATH,
                                                                               solution=self.solution.lower(),
                                                                               model=self.model.lower(),
                                                                               method=method.lower())
            # 截屏裁剪部分相对于截屏的像素点元组
            try:
                crop_pixel = pixel_dir['flx_{}'.format(method.lower())][self.model.lower()][solution.lower()]
            except KeyError:
                log.error('Key Error, can not search on pixel_dir.')
                log.debug(traceback.format_exc())
                return 500

            if captured_img.isdigit() is not True:
                cropping_img(captured_img, temp_img, crop_pixel)
                result = comparing_img(temp_img, standard_img)
                if result is not None and result <= 10:
                    log.info('%s on %s execute Flexible Seating Guest %s Success.' % (self.ext, self.ip, method))
                    return 200
                else:
                    log.error('%s on %s execute Flexible Seating Guest %s Failed.' % (self.ext, self.ip, method))
                    return 400

        else:
            log.error('%s return %s, [Flexible Guest %s] failed.' % (self.ip, r_flex_s[0], method.upper()))
            return r_flex_s[0]

    def acd(self, method: str = None, solution: str = None, aid: int = 0):
        method = method.upper()
        if method in ('IN', 'OUT',):
            url_acd_method = '{drd_pre}ACD:LOG{method}:aid=0'.format(drd_pre=self.url_drd_prefix, method=method)
        elif method in ('AVAILABLE', 'WRAPUP'):
            url_acd_method = '{drd_pre}ACD:{method}:aid=0'.format(drd_pre=self.url_drd_prefix, method=method)
        elif method in ('UNAVAILABLE', 'DISPCODE'):
            url_acd_method = '{drd_pre}ACD:{method}'
        else:
            log.error('ACD operation method dismatched, please check [%s].' % method)
            return 500

        r_acd = self.requests_get(url_acd_method, self._func_name())
        if r_acd[0] == 200:
            log.info('Operation ACD {method} success, checking status...'.format(method=method))
            captured_img = self.screen_shot('acd_{}'.format(method))
            temp_img = '{tmp_path}/temp_img.jpg'.format(tmp_path=IMG_TEMP_PATH)
            standard_img = '{path}/{solution}_{model}_acd_{method}.jpg'.format(path=IMG_STANDARD_PATH,
                                                                               solution=solution.lower(),
                                                                               model=self.model.lower(),
                                                                               method=method.lower())
            # print(standard_img)
            # 截屏裁剪部分相对于截屏的像素点元组
            try:
                crop_pixel = pixel_dir['acd_{}'.format(method.lower())][self.model.lower()][solution.lower()]
            except KeyError:
                log.error('Key Error, can not search on pixel_dir.')
                log.debug(traceback.format_exc())
                return 500
            # 如果截屏成功，打开后进行裁剪，存为临时文件temp_img并和正确的图片进行对比
            if captured_img.isdigit() is not True:  # not True 说明返回了截屏文件路径
                cropping_img(captured_img, temp_img, crop_pixel)
                result = comparing_img(temp_img, standard_img)
                # print(result)
                # 如何完全一致为0，但截屏可能存在10以内的误差
                if result is not None and result <= 10:
                    log.info('Check success. %s on %s execute ACD %s Success.' % (self.ext, self.ip, method))
                    return 200
                else:
                    log.error('Check Failed. %s ACD status on %s can not be judged.' % (self.ext, self.ip))
                    return 400
        else:
            log.error('%s return %s, Operation [ACD %s] failed.' % (self.ip, r_acd[0], method.upper()))
            return r_acd[0]

    def set_idle_status(self):
        """
        设置 idle 态，不需要参数
        首先会尝试drd=RETURNIDLE接口，但此接口没有合入所有分支，所以如果404，则尝试通过按下SPEAKER
        :return: 200 Success
                401 Auth Failed
                404 Not Found
                500 Connection Error
        """
        url_return_idle = self.url_prefix + '/drd=RETURNIDLE'
        r_return_idle = self.requests_get(url_return_idle, self._func_name())

        if self.check_status('idle'):
            log.info('%s is already on [idle] status.' % self.ext)
            return 200
        else:
            if r_return_idle[0] == 200:
                log.info('%s set [idle] status success.' % self.ip)
            elif r_return_idle[0] == 404:
                log.error('%s has not merged, try press [Speaker] to return to idle.' % url_return_idle)
                self.press_key('speaker')
                if self.check_status('idle'):
                    return 200
                else:
                    self.press_key('speaker')
                    if self.check_status('idle'):
                        return 200
                    else:
                        log.error('%s Return to Idle status failed.' % self.ext)
                        return 400
            elif r_return_idle[0] == 401:
                log.info('%s return 401, please check.' % self.ip)
                return 401
            else:
                log.error('%s return %s, set [idle] status failed.' % (url_return_idle, r_return_idle[0]))
                return 500

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
            log.info(self.ip + str(mem_info))
            return 200
        else:
            log.error(self.ip + 'Get memory failed, return ' + str(r_mem[0]))
            return 400

    def screen_shot(self, screen_name):
        """
        Capture the LCD screenShot when check status returns False
        :param screen_name: 调用截屏的功能的名称，用以拼接成完整的名称对存储的截屏命名
        :return: 返回一个元组
                成功：200，包含完整路径的文件名
                认证失败：401，Auth Failed
                URL不匹配：404，Not Found
                连接出错：500，Connection Error
        """
        retry = 0
        url_screen_cap = self.url_screenshot

        while retry < 2:
            # 避免因为第一次get返回401导致截屏失败
            cur_time = time.strftime("%m%d_%H%M%S", time.localtime())
            stored_screen = '%s/%s_%s.jpg' % (log.screen_dir, screen_name, cur_time)
            screen_file = open(stored_screen, 'wb')
            try:
                r_screen_shot = requests.get(url_screen_cap, timeout=5)
                if r_screen_shot.status_code == 200:
                    screen_file.write(r_screen_shot.content)
                    log.info('Capture ScreenShot Success: %s' % stored_screen)
                    return 200, stored_screen
                elif r_screen_shot.status_code == 401:
                    if retry < 1:
                        log.info('Capture ScreenShot Return 401, will try again')
                        retry += 1
                    else:
                        log.info('Capture ScreenShot Failed Because Auth Error. Please check!')
                        screen_file.close()
                        return 401, 'Password Error.'
                elif r_screen_shot.status_code == 404:
                    log.info('Capture ScreenShot Failed Because Resource Not Found.')
                    return 404, 'URL Not Found.'
                else:
                    log.info(
                        'Capture Failed Because Unknown Reason. Return Code is %s' % r_screen_shot.status_code)
                    return 500, 'Connection Failed.'

            except requests.ConnectionError:
                log.info('Connection Failed. URL -> [%s]' % url_screen_cap)
                log.debug(traceback.format_exc())
                return 500

    def reboot(self):
        """
        重启话机
        :return: 执行成功返回 200， 否则返回 HTTP返回码
        """
        url_restart = self.url_keyboard + 'Reboot'
        r_reboot = self.requests_get(url_restart, self._func_name())
        if r_reboot[0] == 200:
            log.info('{phone} reboot success.'.format(phone=self.ip))
            return r_reboot[0]
        else:
            log.error('{phone} reboot failed, return code is {code}'.format(phone=self.ip, code=r[0]))
            return r_reboot[0]

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
            'file:%s, lines:%s, input fine for continue or exit for terminate the script: ' % (filename, line_num))
        if cmd == 'fine':
            log.war('Continuing execute script manually.')
            pass
        elif cmd == 'exit':
            log.error('Error prompted, script terminated manually.')
            sys.exit()
        else:
            self.error_prompt(filename, line_num)


def cropping_img(crop_img, temp_img_path, pixel_tuple):
    """
    打开截屏文件，裁剪后返回存放路径
    :param crop_img: 截屏文件，也就是要进行裁剪的原图
    :param temp_img_path: 裁剪下来的图片的存放路径
    :param pixel_tuple: 像素点元组(top, left, bottom, right)
    :return: 裁剪结果的存放路径
    """

    from PIL import Image

    # 打开截屏文件
    crop_img = Image.open(crop_img)
    # 裁剪
    try:
        cropped = crop_img.crop(pixel_tuple)
    except ValueError:
        log.error('Value Error: Pixel tuple should be 4 elements.')
        log.debug(traceback.format_exc())
        return False
    # 裁剪结果存入temp_img_path路径
    cropped.save(temp_img_path)
    return True


def comparing_img(img_file, img_original):
    """
    对比原理：
    1. histogram()返回图片像素点的列表
    2. list(map(lambda a,b:(a-b)**2, h1, h2)返回的是h1,h2中元素一一相减后结果的平方的列表
    3. 将上面得到的列表值相加后，除以原始图片的像素点列表长度
    4. 最后通过math.sqrt()做一次开方运算
    参考链接：https://www.jianshu.com/p/3d608bf33fe2
    :param img_file: 要进行对比的图片
    :param img_original: 原始的，正确的图片
    :return: 返回float型对比结果，为0.0说明完全一致，数值越大，相差越大
    """
    from PIL import Image
    import math
    import operator
    from functools import reduce

    try:
        img_new = Image.open(img_file)
        img_ori = Image.open(img_original)
    except FileNotFoundError:
        log.error('Image File Not Exist')
        log.debug(traceback.format_exc())
        return None

    h_new = img_new.histogram()
    h_ori = img_ori.histogram()

    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h_new, h_ori))) / len(h_ori))
    return result
