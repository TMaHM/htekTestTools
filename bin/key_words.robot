*** Setting ***
Library             ../config/usr_data.py
Library             ../phoneFunction/action.py
*** Keywords ***
${phone_1} CALL ${phone_2}
    ${result} =     make_call      ${phone_1}   ${phone_2}
    Should be equal As Integers   ${result}   200

${phone} ANSWER
    ${result} =     answer_call     ${phone}
    Should be equal As Integers    ${result}   200

${phone} Hang Up
    ${result} =     on_hook_call    ${phone}
    Should be equal As Integers     ${result}   200

SLEEP ${time}
    ${result} =     wait    ${time}
    Should be True      ${result}

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
    ${result} =     set_phones_idle         @{phone_list}
    Should be True  ${result}

${phone} Press Mute Key
    ${result} = press_the_mute_key          ${phone}
    Should be equal As Integers             ${result}   200

${phone} Enable DND
    ${result} = enable_the_dnd              ${phone}
    Should be equal As Interger             ${result}   200

${phone} Disable DND
    ${result} = disable_the_dnd             ${phone}
    Should be equal As Interger             ${result}   200

