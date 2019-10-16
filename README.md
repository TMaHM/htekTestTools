# Htek Auto Test Tools

Htek 自动化测试脚本

## 框架说明
```
config/
├── conf.py
├── __init__.py
└── usr_data.py
phoneFunction/
├── action.py
├── __init__.py
├── phones.py
bin/
├── key_words.py
├── run.robot
├── log/
    ├── info.log
    ├── debug.log
    ├── screenshot
├── log.html
├── report.html
├── output.xml
README.md
CHANGE LOG.md
```

**1. config**

存放配置文件

conf.py -> 全局配置

usr_data.py -> 用户自定义配置 -> 后期可能会改为使用excel

**2. phoneFunction**

定义话机类以及基本行为

action.py -> 定义了最终使用的函数

phones.py -> 定义了Phone类 -> 接受一系列参数对话机实例化

实际运用存放路径为
./venv/lib/python3.5/Site-package

```python
from PhoneLib.htek_phones import Phone

phone = Phone('10.3.2.123', '8724', line=1, usr='admin', pwd='admin')
```

***3.bin***
存放robot文件以及相关日志、报表
key_words.robot集中编写keywords，粒度较小
run.robot集中编写测试用例

## 已知 BUG

1. 当一个账号同时注册在两台话机 (A，B) 上，此时来电 A 接起后，可能判断其状态不为 [talking]，造成脚本报错 -> 此类报错不会导致脚本中断