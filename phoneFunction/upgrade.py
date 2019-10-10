# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-10

from config.usr_data import phone_list


def auto_upgrade(phones: list, fw_path: str=None):
    for phone in phones:
        url = 'http://{usr}:{pwd}@{ip}/auto_provision.htm'.format(usr=phone.usr, pwd=phone.pwd, ip=phone.ip)
        r = phone.requests_get(url, 'Auto Upgrade')
        print(r[1])


auto_upgrade(phone_list)
