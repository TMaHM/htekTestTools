# Htek Auto Test Scripts Change Logs

## 2019-10-29

> Written by Stephen

* log

1. 调整了log存放路径的获取方式，现在最外层项目名必须是确定的`htekTestTools`

2. 增加了对log文件是否存在的判断，以及log文件大于5M则备份后清空的判断

3. 优化log打印，去除多余的打印

4. 在action中增加了action_log()函数，用以在RF脚本文件中记录日志

* bin

调整了目录结构，在bin下新增一层目录作为Test Suite

* RF脚本 -- conference

重写了五方会议脚本

执行时间缩短了15s(36s->21s)，具体实现在RF文件中通过keywords，而非直接在action.py中实现

## 2019-10-24

> Written by Stephen

1. 改变了当检查idle态时check_status()方法的实现，现在它将调用GUI接口，而不是原来的Call状态检查接口

2. 新增interfaces.md文档，记录了目前所能够使用的自动化测试接口原型

3. 修改了TestUrl类中的变量命名，统一使用url前缀，以避免不必要的误解

4. 为answer和end_call新增了默认值，现在在默认条件下，这两个方法将使用SPEAKER按键实现

5. 修改了Phone类中的transfer方法

## 2019-10-11

> Written by Stephen

1. 新增upgrade脚本，定义auto_upgrade及check_fw两个函数

2. 在PhoneLib.htek_phones中新增reboot方法

## 2019-10-10

> Written by Zoy

调整了整体目录结构

## 2019-09-28

> Written by Stephen

* /htekTestTools/phones.py

修改了Phone中的set_line_key方法

原方法在每一次调用时读取cfg.xml文件，并通过事先准备的正则匹配出对应的字段，从而动态找到line key各字段对应的P值

事实上，这种做法并不必要，因为每个字段的P值都是基本固定的

新的做法是准备好line key序号及其对应的各个字段的P值字典，并在需要时通过_get_p_value_of_lk方法查找

此后校验入参后，通过set_p_value方法设置相应P值为入参

##2019-10-10

>Writen by Zoy

修改框架目录结构，部分文件名称；

引入RobotFrameWork；

##2019-10-16

>Writen by Zoy

action.py、key_words.robot新增话机部分基础操作：

呼叫、应答、挂机、等待、Transfer、DND、状态设置等


