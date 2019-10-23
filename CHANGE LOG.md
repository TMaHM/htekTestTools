# Htek Auto Test Scripts Change Logs

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


