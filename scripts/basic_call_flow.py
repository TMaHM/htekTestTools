from htekTestTools.phones import Phone

from htekTestTools.settings import *

dut_1 = phone_list[0]
dut_2 = phone_list[1]

def basic_call(dut_list:list):
    num = len(dut_list)
    if num == 1:
        print('Need at least 2 phones!')
    elif num > 1 and num % 2 == 0:
        try:
            pass
        except:
            pass



    dut_1.dial(dut_2.ext)
    dut_2.answer('speaker')
    dut_1.keep_call(2)
    dut_2.end_call('speaker')


