*** Settings ***
Documentation       基础通话业务测试
Library             ../phoneFunction/action.py
Variables           ../config/usr_data.py
Resource            ./key_words.robot

*** Test Cases ***
#基本呼叫
#    [Tags]    CALL
#    [Documentation]     主叫挂机

#    ${stephen_dut_1} CALL ${stephen_dut_2}
#    ${stephen_dut_2} ANSWER
#    ${stephen_dut_1} Hang Up


#Transfer
#    ${stephen_dut_1} Call ${stephen_dut_2}
#    ${stephen_dut_2} Answer
#    ${stephen_dut_2} Blind Transfer to ${stephen_dut_3}
#    WAIT 3
#    ${stephen_dut_3} Answer
#    Wait 3
#    ${stephen_dut_3} Hang up

*** Test Cases ***
单主席五方会议
    action log  info    >>> 5-ways conference start...
    ${stephen_UC926E} Call ${stephen_UC912_1}
    ${stephen_UC912_1} Answer
    ${stephen_UC926E} Initiate Conference with ${stephen_UC926}
    wait 1
    ${stephen_UC926E} Add Conf Part ${stephen_UC505}
    wait 1
    ${stephen_UC926E} Add Conf Part ${stephen_UC912_2}
    wait 3
    ${stephen_UC926E} Hang Up
    action log  info    >>> 5-ways conference end...