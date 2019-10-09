*** Settings ***
Library     ../data/usr_data.py
Library     ../htekTestTools/test_cases.py

*** Keywords ***
A Call B
    ${phone 1}      ${phone 2}      ${phone 3} =        Dut List
    ${result} =     make_call      ${phone 1}      ${phone 2}
    Should Be Equal      ${result}      200

${phone 1} Call ${phone 2}
    ${result} =     make_call      ${phone 1}      ${phone 2}
    Should Be Equal      ${result}      200

Answer Call
    ${phone 1}      ${phone 2}      ${phone 3} =        Dut List
    ${result} =     test_cases.answer call     ${phone 2}
    Should Be Equal     ${result}       200

*** Test Cases ***
Case 1 [A Call B]
    ${phone 1}      ${phone 2}      ${phone 3} =        Dut List
    ${phone 1} Call ${phone 2}

Case 2 [B Answer]
    Answer Call

#Case 1 [Basic Call]
#    ${phone 1}      ${phone 2}      ${phone 3} =        Dut List
#    ${result} =     basic_call      ${phone 1}      ${phone 2}
#    Should Be True      ${result}

