*** Settings ***
Library     ../config/usr_data.py
Library     ../phoneFunction/action.py


*** Keywords ***
A Call B
    ${phone 1}      ${phone 2}      ${phone 3} =        Dut List
    ${result} =     make_call      ${phone 1}      ${phone 2}
    should be equal as integers      ${result}      200

${phone 1} Call ${phone 2}
    ${result} =     make_call      ${phone 1}      ${phone 2}
    should be equal as integers      ${result}      200

${dut} Answer the call
    ${result} =     answer_call     ${dut}
    should be equal as integers     ${result}       200

${dut} Hung Up
    ${result} =     on_hook_call    ${dut}
    should be equal as integers  ${result}      200
