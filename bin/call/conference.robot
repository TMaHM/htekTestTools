*** Settings ***
Documentation       基础通话业务测试
Library             ../../phoneFunction/action.py
Variables           ../../config/usr_data.py
Resource            ../key_words.robot


*** Test Cases ***
Conference
    ${stephen_UC926E} Initiate Conference ${stephen_conf_list}