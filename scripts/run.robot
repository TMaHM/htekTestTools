*** Settings ***
Library     ../phoneFunction/action.py
Resource    ./htek_keywords.robot
Variables   ../config/usr_data.py

*** Test Cases ***
Case Test 1
    [Setup]   sleep call  ${dut_1}
    ${dut_1} Call ${dut_2}
    ${dut_2} answer the call
    ${dut_2} Hung Up
    set idle  ${dut_1}
    [Teardown]   sleep call    ${dut_2}

