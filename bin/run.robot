*** Settings ***
Documentation       基础通话业务测试
Variables             ../config/usr_data.py
Resource            ./key_words.robot

*** Test Cases ***
基本呼叫
    [Tags]    CALL
    [Documentation]     主叫挂机
    ${Zoy_UC501} CALL ${Zoy_S505}
    ${Zoy_S505} ANSWER

*** Keywords ***
Provided precondition
    Setup system under test