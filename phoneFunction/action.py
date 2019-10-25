# -*- coding: UTF-8 -*-
# Written by Stephen
# 2019-10-08
from PhoneLib.htek_phone_conf import log
import time


def action_make_call(phone_a, phone_b):
    result = phone_a.dial(phone_b.ext)
    return result


def action_answer_call(phone):
    result = phone.answer('speaker')
    return result


def action_on_hook_call(phone):
    result = phone.end_call('x')
    return result


def action_set_idle(phone):
    result = phone.set_idle_status()
    return result


def action_sleep_call(phone):
    result = phone.keep_call(3)
    return result


def action_press_key(phone, key):
    if key.isdigit():
        for k in key:
            phone.press_key(k)
    else:
        phone.press_key(key)


# 话机按键执行保持
def action_hold_the_call(phone):
    result = phone.hold()
    return result


# 使用按键恢复通话，前置条件必须为保持状态
def action_resume_the_hold(phone):
    check_status = phone.check_status('hold')
    if check_status is True:
        result = phone.hold()
    else:
        log.error('Can not resume the call.')
        result = 500
    return result


# 用于设置时间间隔
def action_wait(seconds: int):
    time.sleep(seconds)
    return True


def action_set_idle(phone_list: list):

    idle_success = 0
    for i in phone_list:
        phone_i = phone_list.pop(i)
        result = phone_i.set_idle_status()
        if result is not 200:
            log.error("Set %s to Idle failed!" % phone_i)
        else:
            log.info("Set All phones to Idle success!")
            idle_success += 1
    if idle_success == len(phone_list):
        return True
    else:
        return False


def action_transfer(executor, target, mod):
    result = executor.transfer(target, mod)
    return result


# 静音键
def action_press_mute(phone):
    result = phone.press_key('MUTE')
    return result


# 开启DND
def action_dnd_on(phone):
    result = phone.press_key('DNDOn')
    return result


# 关闭DND
def action_dnd_off(phone):
    result = phone.press_key('DNDOff')
    return result


# 重启话机
def action_reboot_the_phone(phone):
    result = phone.press_key('Reboot')
    return result


def action_drd_flx_in(phone, number, pwd):
    result = phone.flexible_seating(method='in', solution='drd', number=number, pwd=pwd)
    return result


def action_drd_flx_out(phone):
    result = phone.flexible_seating(method='out', solution='drd')
    return result


def action_drd_acd_log_in(phone):
    result = phone.acd(method='in', solution='drd')
    return result


def action_drd_acd_log_out(phone):
    result = phone.acd(method='out', solution='drd')
    return result


