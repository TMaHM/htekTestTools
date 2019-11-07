# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-10

from config.usr_data import *
import logging
import re
import sys
import os


class Logger:

    def __init__(self, echo: bool = False, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        import time

        # log及截屏文件存放目录
        log_dir = r'./upgrade_log/'
        info_path = log_dir + r'info.log'
        debug_path = log_dir + r'debug.log'
        # 当天的月，日
        now_month = time.ctime().split(' ')[1]
        now_date = time.ctime().split(' ')[2]

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            open(info_path, 'w').close()
            open(debug_path, 'w').close()
        else:
            if not os.path.exists(info_path):
                open(info_path, 'w').close()
                open(debug_path, 'w').close()
            else:
                info_size = os.path.getsize(info_path)
                debug_size = os.path.getsize(debug_path)
                if info_size / 1024 ** 2 > 5:
                    log.info('---Backup info.log because large than 5M.----')
                    os.rename(info_path, '{dir}backup/info_bak_{month}{date}.log'.format(dir=log_dir, month=now_month,
                                                                                         date=now_date))
                    open(info_path, 'w').close()
                else:
                    pass
                if debug_size / 1024 ** 2 > 5:
                    log.info('---Backup debug.log because large than 5M---')
                    os.rename(debug_path, '{dir}backup/debug_bak_{month}{date}.log'.format(dir=log_dir, month=now_month,
                                                                                           date=now_date))
                    open(debug_path, 'w').close()
                else:
                    pass

        self.logger_debug = logging.getLogger(info_path)
        self.logger_info = logging.getLogger(debug_path)
        self.logger_debug.setLevel(logging.DEBUG)
        self.logger_info.setLevel(logging.INFO)
        fmt_info = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fmt_debug = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置终端日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt_info)
        sh.setFormatter(fmt_debug)
        sh.setLevel(clevel)
        # 设置文件日志
        fh_info = logging.FileHandler(info_path)
        fh_debug = logging.FileHandler(debug_path)
        fh_info.setFormatter(fmt_info)
        fh_debug.setFormatter(fmt_debug)
        fh_info.setLevel(Flevel)
        fh_debug.setLevel(Flevel)
        if echo:
            self.logger_info.addHandler(sh)
            self.logger_debug.addHandler(sh)
        self.logger_info.addHandler(fh_info)
        self.logger_debug.addHandler(fh_debug)

    def debug(self, message):
        self.logger_debug.debug(message)

    def info(self, message):
        self.logger_info.info(message)

    def war(self, message):
        self.logger_info.warning(message)

    def error(self, message):
        self.logger_info.error(message)


log = Logger(echo=False)


def ping(phone_list: list):
    # return_code是一个十六位二进制的数转为十进制，如ping一个无效ip时返回512；但真正的状态码是十六位二进制去掉低八位后，再转成十进制
    # 例如512 对应是 0000001000000000，去掉后八位是 00000010，再转为十进制，为2
    # 参考链接：https://blog.csdn.net/c453787298/article/details/23844907
    for _phone in phone_list:
        return_code = os.system('ping -c 1 -w 1 %s' % _phone.ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
        ex_int = int('{:016b}'.format(return_code)[0:-8], 2)
        print(ex_int)
        if ex_int:
            return False
        else:
            return True


# ping('www.baidu.com')

def store_config_path(_phone):
    url = 'http://{usr}:{pwd}@{ip}/auto_provision.htm'.format(usr=_phone.usr, pwd=_phone.pwd, ip=_phone.ip)
    r = _phone.requests_get(url, 'Store Config Path')
    if r[0] == 200:
        with open('temp_file', 'w', encoding='utf-8') as f:
            f.write(r[1])
        with open('temp_file', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            cnt = 0
            for line in lines:
                cnt += 1
                if 'config_server_path' in line:
                    pat_result = re.findall(r'(?<=value=\")(.*)(?=\"\sname)', lines[cnt])
                    if pat_result:
                        config_path = pat_result[0]
                    else:
                        log.error(
                                'Can not pattern to config server path, please check {line}. '
                                'BTW, the path will be cleared.'.format(line=lines[cnt]))
                        _phone.error_prompt(sys._getframe().f_lineno)
                        config_path = 'Blank'
                    # print(config_path)
                else:
                    continue
            return config_path


def auto_upgrade(phones: tuple, fw_path: str = None, upgrade_mode: str = '1'):
    """
    对一个话机列表进行升级
    在升级前获取其config path 路径，以便在升级完成后恢复
    :param phones: 要执行升级操作的话机的列表
    :param fw_path: 升级rom存放的服务器路径
    :param upgrade_mode: 升级模式, 默认为'1', 即http
    :return: 留存的config server path
    """
    # 在fw_path为空的情况下, 提示用户输入
    # 目前直接回车会往下运行, 即如果一定要为空, 那么可以接受fw_path为空. 后面看看是否要限制.
    while fw_path is None:
        fw_path = input('Firmware Server Path is None, please write the path: ')

    upgrade_executed_list = []
    upgrade_unexecuted_list = []
    phone_info_dir = {}
    for _phone in phones:
        config_path = store_config_path(_phone)
        phone_info_dir[_phone.ip] = {}
        phone_info_dir[_phone.ip]['config_path'] = config_path
        # 设置 fw server path
        phone_info_dir[_phone.ip]['fw_set_flag'] = 1 if _phone.set_p_value('P192', fw_path) == 200 else 0
        # 设置 config server path
        phone_info_dir[_phone.ip]['cfg_set_flag'] = 1 if _phone.set_p_value('P237', '%NULL%') == 200 else 0
        # 设置 upgrade protocol
        phone_info_dir[_phone.ip]['up_mode_set_flag'] = 1 if _phone.set_p_value('P212', upgrade_mode) == 200 else 0
        # 以防万一，关闭 PnP
        phone_info_dir[_phone.ip]['pnp_set_flag'] = 1 if _phone.set_p_value('P20165', '0') == 200 else 0
        # 以防万一，关闭 DHCP Option
        phone_info_dir[_phone.ip]['option_set_flag'] = 1 if _phone.set_p_value('P145', '0') == 200 else 0
        # phone_info_dir[phone.ip]['reboot_flag'] = 1 if phone.set_p_value('P192', fw_path) == 200 else 0
        for flag in phone_info_dir[_phone.ip].values():
            if flag in (1, config_path):
                upgrade_executed_list.append(_phone.ip)
            else:
                upgrade_unexecuted_list.append(_phone.ip)

    return set(upgrade_executed_list), set(upgrade_unexecuted_list), phone_info_dir


def check_fw(phones: tuple, boot_info: str, rom_info: str, img_info: str):
    """
    根据给定的fw信息，检查指定设备是否匹配
    :param phones: 待检查的话机列表
    :param boot_info: fw中boot的version和时间信息，如果有多个boot信息，请使用 | 进行分割
                        如 boot_if = ('2.0.4.4(2018-01-20 13:33:00)|2.0.4.4(2018-01-20 13:33:33)')
    :param rom_info: fw中rom的version和时间信息
    :param img_info: fw中img的version和时间信息
    :return: 返回检查成功和失败设备的字典 result{'success:[success list], 'failed':[failed list]}
            result['success']:可以得到检查成功设备列表，result['failed']为检查失败的设备(ip+失败项)元祖的列表;
            因此，result['failed'][0]为检查失败的第一台设备，
            result['failed'][0][0]为该设备IP,
            result['failed'][0][1]为该设备真实的fw信息与给定检查信息不匹配的项
    """
    # 检查话机是否升级到指定版本
    boot_info_list = []
    tmp_boot_info_list = boot_info.split('|')
    print(tmp_boot_info_list)
    for boot in tmp_boot_info_list:
        boot_info = 'BOOT--{boot_ver}'.format(boot_ver=boot.strip())
        boot_info_list.append(boot_info)
    rom_info = 'ROM--{rom_ver}'.format(rom_ver=rom_info)
    img_info = 'IMG--{img_ver}'.format(img_ver=img_info)

    fw_check_dir = {}
    check_success_list = []
    check_failed_list = []
    for _phone in phones:
        phone_failed_list = []
        index_url = 'http://{usr}:{pwd}@{ip}/index.htm'.format(usr=_phone.usr, pwd=_phone.pwd, ip=_phone.ip)
        r_index = _phone.requests_get(index_url, 'check fw')
        if r_index[0] == 200:
            with open('temp_file', 'w', encoding='utf-8') as f:
                f.write(r_index[1])
            with open('temp_file', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                cnt = 0
                for line in lines:
                    cnt += 1
                    if 'firmware_version' in line:
                        # 只要话机的boot信息和给定的boot信息中的一个匹配，就将boot_check置为1并退出循环
                        for boot in boot_info_list:
                            if boot in lines[cnt]:
                                boot_check = 1
                                break
                            else:
                                boot_check = 0
                        rom_check = 1 if (rom_info in lines[cnt]) else 0
                        img_check = 1 if (img_info in lines[cnt]) else 0
                        break
                if {boot_check, rom_check, img_check} == {1, 1, 1}:
                    check_success_list.append(_phone.ip)
                else:
                    for failed_check in {(boot_check, 'boot'), (rom_check, 'rom'), (img_check, 'img')}:
                        if failed_check[0] == 0:
                            pat = r'({failed_check}--.*?)(?=<br>)'.format(failed_check=failed_check[1])
                            real_info = re.findall(pat, lines[cnt], flags=re.IGNORECASE)
                            if real_info:
                                # print(real_info[0])
                                phone_failed_list.append(real_info[0])
                            else:
                                phone_failed_list.append(
                                        '{failed_check} may be failed.'.format(failed_check=failed_check[1]))
                    if len(phone_failed_list) == 0:
                        log.info('On {ip}, all fw info checked success.')
                    else:
                        log.info(
                                'On {ip}, failed info is {failed_list}'.format(ip=_phone.ip,
                                                                               failed_list=phone_failed_list))
                    check_failed_list.append((_phone.ip, phone_failed_list))

    log.info('All need to check: %s, FW check success: %s, check failed: %s' % (
        len(phones), len(check_success_list), len(check_failed_list)))

    fw_check_dir['success'] = check_success_list
    fw_check_dir['failed'] = check_failed_list
    return fw_check_dir


phone_list_1 = (daily_uc923_1, daily_uc923_2, daily_uc912e_1, daily_uc926e_1, daily_uc912g_1)
auto_upgrade(phone_list_1, 'http://10.3.2.242:8080/rom/withOutBoot/')
for phone in phone_list_1:
    phone.reboot()

