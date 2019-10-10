# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-08
from PhoneLib.htek_phone_conf import log


log.info('hello')


def make_call(phone_a, phone_b):
    result = phone_a.dial(phone_b.ext)
    return result


def answer_call(phone):
    result = phone.answer('speaker')
    return result


def on_hook_call(phone):
    result = phone.end_call('speaker')
    return result


def set_idle(phone):
    result = phone.set_idle_status()
    return result


def sleep_call(phone):
    result = phone.keep_call(3)
    return result


def basic_call(phone_a, phone_b):
    cnt_success = 0
    failed_list = []
    if phone_a.dial(phone_b.ext) == 200:
        cnt_success += 1
    else:
        cnt_success -= 1
        failed_list.append('phone_a dial failed.')
    if phone_b.answer('f1') == 200:
        cnt_success += 1
    else:
        cnt_success -= 1
        failed_list.append('phone_b answer failed.')
    if phone_b.end_call('f4') == 200:
        cnt_success += 1
    else:
        cnt_success -= 1
        failed_list.append('phone_b end call failed.')

    if cnt_success == 3:
        return True
    else:
        return failed_list


def transfer_flow(phone_a, phone_b, phone_c):
    phone_a.dial(phone_b.ext)
    phone_b.transfer(phone_c)


