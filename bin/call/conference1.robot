*** Settings ***
Documentation       基础通话业务测试
Library             ../../phoneFunction/action.py
Variables           ../../config/usr_data.py
Resource            ../key_words.robot


*** Test Cases ***
单主席五方会议
    FOR     ${loop}    IN RANGE     1200
        action log  info    >>> 5-ways conference start...
        ${daily_uc923_1} Call ${daily_uc923_2}
        ${daily_uc923_2} Answer
        ${daily_uc923_1} Initiate Conference with ${daily_uc912e_1}
        wait 1
        ${daily_uc923_1} Add Conf Part ${daily_uc926e_1}
        wait 1
        ${daily_uc923_1} Add Conf Part ${daily_uc912g_1}
        wait 3
        ${daily_uc923_1} Hang Up
        action log  info    >>> 5-ways conference end...
    END