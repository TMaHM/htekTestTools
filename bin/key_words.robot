*** Setting ***
Library             ../config/usr_data.py
Library             ../phoneFunction/action.py
*** Keywords ***
${phone_1} CALL ${phone_2}
    ${result} =  make_call      ${phone_1}   ${phone_2}
    Should be equal As Integers   ${result}   200

${phone} ANSWER
    ${result} = answer_call     ${phone}
    Should be equal As Integers    ${result}   200

${phone} Hang Up
    ${result} = end_call        ${phone}
    Should be equal As Integers     ${result}   200

SLEEP ${time}
    wait    ${time}
    Should be True

${phone_1} Blind Transfer to ${phone_3}
    ${result} =     blind_transfer_call     ${phone_1}   ${phone_2}
    Should be True  ${result}

${phone_1} AT Transfer to ${phone_3}
    ${result} =     AT_transfer_call       ${phone_1}   ${phone_2}
    Should be True  ${result}

${phone_1} SAT Transfer to ${phone_3}
    ${result} =     SAT_transfer_call      ${phone_1}   ${phone_2}
    Should be True  ${result}

Set @{phone_list} to Idle
