*** Settings ***
Documentation       基础通话业务测试
Library             ../../phoneFunction/action.py
Variables           ../../config/usr_data.py
Resource            ../key_words.robot


*** Test Cases ***
单主席五方会议
    action log  info    >>> 5-ways conference start...
    ${UC926E} Call ${UC912_1}
    ${UC912_1} Answer
    ${UC926E} Initiate Conference with ${UC926}
    wait 1
    ${UC926E} Add Conf Part ${UC505}
    wait 1
    ${UC926E} Add Conf Part ${UC912_2}
    wait 3
    ${UC926E} Hang Up
    action log  info    >>> 5-ways conference end...
