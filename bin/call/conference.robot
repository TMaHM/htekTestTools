*** Settings ***
Documentation       基础通话业务测试
Library             ../../phoneFunction/action.py
Variables           ../../config/usr_data.py
Resource            ../key_words.robot


*** Test Cases ***
单主席五方会议
    FOR     ${loop}    IN RANGE     10000
        action log  info    >>> 5-ways conference start...
        ${dspg1} Call ${dspg2}
        ${dspg2} Answer
        ${dspg1} Initiate Conference with ${dspg3}
        wait 1
        ${dspg1} Add Conf Part ${dspg4}
        wait 1
        ${dspg1} Add Conf Part ${dspg5}
        wait 3
        ${dspg1} Hang Up
        action log  info    >>> 5-ways conference end...
    END
