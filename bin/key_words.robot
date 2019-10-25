*** Setting ***
Library             ../config/usr_data.py
Library             ../phoneFunction/action.py
*** Keywords ***
${phone_1} CALL ${phone_2}
    ${result} =     action_make_call      ${phone_1}   ${phone_2}
    Should be equal As Integers   ${result}   200

${phone} ANSWER
    ${result} =     action_answer_call     ${phone}
    Should be equal As Integers    ${result}   200

${phone} Hang Up
    ${result} =     action_on_hook_call    ${phone}
    Should be equal As Integers     ${result}   200

WAIT ${time}
    ${result} =     action_wait    ${time}
    Should be True      ${result}

${phone_1} Blind Transfer to ${phone_3}
    ${result} =     action_transfer     ${phone_1}    ${phone_3}    BT
    Should be True  ${result}

${phone_1} AT Transfer to ${phone_3}
    ${result} =     action transfer   ${phone_1}    ${phone_3}      AT
    Should be True  ${result}

${phone_1} SAT Transfer to ${phone_3}
    ${result} =     action transfer  ${phone_1}   ${phone_3}        SAT
    Should be True  ${result}

Set @{phone_list} to Idle
    ${result} =     action set idle    @{phone_list}
    Should be True  ${result}

${phone} Press Mute Key
    ${result} =     action press mute       ${phone}
    Should be equal As Integers             ${result}   200

${phone} Enable DND
    ${result} =     action dnd on           ${phone}
    Should be equal As Integers             ${result}   200

${phone} Disable DND
    ${result} =     action dnd off          ${phone}
    Should be equal As Integers             ${result}   200

