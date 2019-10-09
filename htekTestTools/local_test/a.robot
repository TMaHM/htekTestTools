*** Settings ***
Library     OperatingSystem
#Library     ${CURDIR}${/}local_test.py
Library     ../test_cases.py
#Library     ./phones.py
Library     ./test_data.py


*** Variables ***
${GREET}    Hello
${NAME}     world
@{LIST}     robot   framework

*** Variables ***
&{USER 1}       name=Matti    address=xxx         phone=123
&{USER 2}       name=Teppo    address=yyy         phone=456
&{MANY}         first=1       second=${2}         ${3}=third
&{EVEN MORE}    &{MANY}       first=override      empty=
...             =empty        key\=here=value
${Phone 1}      phone_1
${Phone 2}      phone_2


*** Test Cases ***
Constants
    Log    Hello
    Log    Hello, world!!
    Log    ['robot, framework']

Variables
    Log    ${GREET}
    Log    ${GREET}, ${NAME}!!
    Log    ${LIST}
    Log Many    @{LIST}
    Log    &{USER 1}[name]
    Log    ${USER 1.name}

*** Test Cases ***
Example
    ${list} =           Create List     first   second      third
    Length Should Be    ${list}     3
    Log Many            @{list}

*** Variables ***
@{NAMEs1}		Matti		Teppo
@{NAMEs2}		@{NAMEs1}	Seppo
@{NOTHING}
@{MANY}			one		two		three	four
...				five	six		seven
@{phone_list}    dut_list


#*** Test Cases ***
#Local Test
#    MyTest      t

*** Test Cases ***
Case 1 [Basic Call]
    ${phone 1}      ${phone 2}      ${phone_3} =    phone_list
#    ${phone 1} =       Create Phone   10.3.2.217      2054    3   admin   admin
#    ${phone 2} =       Create Phone   10.3.2.123      8724    1   admin   admin
    Log     ${phone 1}
    ${result} =     basic_call      ${phone 1}      ${phone 2}
    Should Be True     ${result}

#Case 2 [Basic Call 2]
#    ${phone_1}      ${phone_2}      ${phone_3} =    phone_list
#    ${result} =     basic_call      ${phone_1}      ${phone_2}
#    Should Be True      ${result}