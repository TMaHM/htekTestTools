*** Settings ***
Library     OperatingSystem

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

*** Test Cases ***
Example 1
	Log			${NAMEs1}
	Log Many	@{NAMEs1}