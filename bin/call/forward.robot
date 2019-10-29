*** Settings ***
Documentation       基础通话业务测试
Library             ../../phoneFunction/action.py
Variables           ../../config/usr_data.py
Resource            ../key_words.robot


*** Test Cases ***
来电Forward
    ${UC926E} Call ${UC912_1}

    ${UC912_1} Answer
