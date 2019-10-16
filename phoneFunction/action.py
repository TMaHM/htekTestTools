# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-08
import time
from config.conf import Logger


# 拨号
def make_call(phone_a, phone_b):
    result = phone_a.dial(phone_b.ext)
    return result


# 应答
def answer_call(phone_b):
    result = phone_b.answer('f1')


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


# 基本呼叫并且应答挂机
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


# 挂机
def end_call(phone):
    result = phone.press_key('F4')
    return result


# 话机按键执行保持
def hold_the_call(phone):
    result = phone.press_key('F2')
    return result


# 使用按键恢复通话，前置条件必须为保持状态
def resume_the_hold(phone):
    result = phone.press_key('F2')
    return result


# 用于设置时间间隔
def wait(seconds: int):
    time.sleep(seconds)
    return True


# 基础Blind Transfer
def blind_transfer_call(phone_1, phone_2):
    phone_1.transfer(phone_2, mod='BT')
    return True


# AT Transfer
def AT_transfer_call(phone_1, phone_2):
    phone_1.transfer(phone_2, mod='AT')
    return True


# SAT Transfer
def SAT_transfer_call(phone_1, phone_2):
    phone_1.transfer(phone_2, mod='SAT')
    return True


# 将话机状态回味为IDLE
def set_phones_idle(phone_list: list):

    idle_success = 0
    for i in phone_list:
        phone_i = phone_list.pop(i)
        result = phone_i.set_idle_status
        if result is not 200:
            Logger.error("Set %s to Idle failed!" % phone_i)
        else:
            idle_success += 1

    if idle_success == len(phone_list):
        return True
    else:
        return False




