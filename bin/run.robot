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

Conference
    FOR     ${index}    IN RANGE    100
        ${stephen_UC926E} Initiate Conference ${stephen_conf_list}
        log  ${index}
    END