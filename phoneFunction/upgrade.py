# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-10

from config.usr_data import phone_list
from PhoneLib.htek_phone_conf import log
import re
import time
import sys
import os


def ping(ip):
    # return_code是一个十六位二进制的数转为十进制，如ping一个无效ip时返回512；但真正的状态码是十六位二进制去掉低八位后，再转成十进制
    # 例如512 对应是 0000001000000000，去掉后八位是 00000010，再转为十进制，为2
    # 参考链接：https://blog.csdn.net/c453787298/article/details/23844907
    return_code = os.system('ping -c 1 -w 1 %s' % ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
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
                            log.error('Can not pattern to config server path, please check {line}. BTW, the path will be cleared.'.format(line=lines[cnt]))
                            phone.error_prompt(sys._getframe().f_lineno)
                            config_path = 'Blank'
                        # print(config_path)
                    else:
                        continue

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

    return config_path


def check_fw(phones: list, boot_info: str, rom_info: str, img_info: str):
    # 检查话机是否升级到指定版本
    boot_info = 'BOOT--{boot_ver}'.format(boot_ver=boot_info)
    rom_info = 'ROM--{rom_ver}'.format(rom_ver=rom_info)
    img_info = 'IMG--{img_ver}'.format(img_ver=img_info)

    check_success_list = []
    check_failed_list = []
    for phone in phones:
        index_url = 'http://{usr}:{pwd}@{ip}/index.htm'.format(usr=phone.usr, pwd=phone.pwd, ip=phone.ip)
        r_index = phone.requests_get(index_url)
        if r_index[0] == 200:
            with open('temp_file', 'w', encoding='utf-8') as f:
                f.write(r_index[1])
            with open('temp_file', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                cnt = 0
                for line in lines:
                    cnt += 1 if (boot_info in line) else 0
                    cnt += 1 if (rom_info in line) else 0
                    cnt += 1 if (img_info in line) else 0
                if cnt == 3:
                    check_success_list.append(phone.ip)
                else:
                    check_failed_list.append(phone.ip)
    log.info('FW check success: %s, check failed: %s' % (len(check_success_list), len(check_failed_list)))

    return check_success_list, check_failed_list


                # auto_upgrade(phone_list)
