*** Settings ***
Library     ../phoneFunction/action.py


*** Keywords ***
${phone 1} Call ${phone 2}
    ${result} =     make_call      ${phone 1}      ${phone 2}
    should be equal as integers      ${result}      200

${dut} Answer the call
    ${result} =     answer_call     ${dut}
    should be equal as integers     ${result}       200

${dut} Hung Up
    ${result} =     on_hook_call    ${dut}
    should be equal as integers  ${result}      200

${phone 1} test ${phone 2}
    make_call      ${phone 1}      ${phone 2}
    answer_call     ${phone 2}
    on_hook_call    ${phone 2}

${phone} pressed ${key}
    press key   ${phone}    ${key}
