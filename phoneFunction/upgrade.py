# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-10

from config.usr_data import phone_list
from PhoneLib.htek_phone_conf import log
import re
import time
import sys
import os


def ping(phone_list: list):
    # return_code是一个十六位二进制的数转为十进制，如ping一个无效ip时返回512；但真正的状态码是十六位二进制去掉低八位后，再转成十进制
    # 例如512 对应是 0000001000000000，去掉后八位是 00000010，再转为十进制，为2
    # 参考链接：https://blog.csdn.net/c453787298/article/details/23844907
    for phone in phone_list:
        return_code = os.system('ping -c 1 -w 1 %s' % phone.ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
        ex_int = int('{:016b}'.format(return_code)[0:-8], 2)
        print(ex_int)
        if ex_int:
            return False
        else:
            return True


# ping('www.baidu.com')


def auto_upgrade(phones: list, fw_path: str = None, upgrade_mode: str = '1'):
    """
    对一个话机列表进行升级
    在升级前获取其config path 路径，以便在升级完成后恢复
    :param phones: 要执行升级操作的话机的列表
    :param fw_path: 升级rom存放的服务器路径
    :param upgrade_mode: 升级模式
    :return: 留存的config server path
    """

    upgrade_executed_list = []
    upgrade_unexecuted_list = []

    for phone in phones:
        url = 'http://{usr}:{pwd}@{ip}/auto_provision.htm'.format(usr=phone.usr, pwd=phone.pwd, ip=phone.ip)
        r = phone.requests_get(url, 'Auto Upgrade')
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
                            phone.error_prompt(sys._getframe().f_lineno)
                            config_path = 'Blank'
                        # print(config_path)
                    else:
                        continue
                # for循环结束，设置升级所需的P值并重启升级
                # 设置 fw server path
                phone.set_p_value('P192', fw_path)
                # 设置 config server path
                phone.set_p_value('P237', '%NULL%')
                # 设置 upgrade protocol
                phone.set_p_value('P212', upgrade_mode)
                # 以防万一，关闭 PnP
                phone.set_p_value('P20165', '0')
                # 以防万一，关闭 DHCP Option
                phone.set_p_value('P145', '0')
                phone.reboot()

                upgrade_executed_list.append(phone.ip)

        else:
            upgrade_unexecuted_list.append(phone.ip)

    return config_path, upgrade_executed_list, upgrade_unexecuted_list


def check_fw(phones: list, boot_info: str, rom_info: str, img_info: str):
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
    for phone in phones:
        phone_failed_list = []
        index_url = 'http://{usr}:{pwd}@{ip}/index.htm'.format(usr=phone.usr, pwd=phone.pwd, ip=phone.ip)
        r_index = phone.requests_get(index_url, 'check fw')
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
                    check_success_list.append(phone.ip)
                else:
                    for failed_check in {(boot_check, 'boot'), (rom_check, 'rom'), (img_check, 'img')}:
                        if failed_check[0] == 0:
                            pat = r'({failed_check}--.*?)(?=<br>)'.format(failed_check=failed_check[1])
                            real_info = re.findall(pat, lines[cnt], flags=re.IGNORECASE)
                            if real_info:
                                # print(real_info[0])
                                phone_failed_list.append(real_info[0])
                            else:
                                phone_failed_list.append('{failed_check} may be failed.'.format(failed_check=failed_check[1]))
                    if len(phone_failed_list) == 0:
                        log.info('On {ip}, all fw info checked success.')
                    else:
                        log.info(
                            'On {ip}, failed info is {failed_list}'.format(ip=phone.ip, failed_list=phone_failed_list))
                    check_failed_list.append((phone.ip, phone_failed_list))

    log.info('All need to check: %s, FW check success: %s, check failed: %s' % (len(phone_list), len(check_success_list), len(check_failed_list)))

    fw_check_dir['success'] = check_success_list
    fw_check_dir['failed'] = check_failed_list
    return fw_check_dir

    # auto_upgrade(phone_list)


boot_if = '2.0.5.20(2019-03-07 14:52:00) | 2.0.4.4(2018-01-20 13:33:00)'
rom_if = '2.0.4.4.81(2019-09-21 15:30:00)'
img_if = '2.0.4.4.81(2019-09-21 15:30:00)'
result = check_fw(phone_list, boot_if, rom_if, img_if)
print(result)
print(result['failed'])
if len(result['failed']) == 0:
    print('All success.')
else:
    print(result['failed'][0])
    print(result['failed'][0][0])
    print(result['failed'][0][1])
# print(check_fw.__doc__)
