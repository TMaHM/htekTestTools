# Htek Auto Test Tools

Htek 自动化测试脚本

## 框架说明
```
data/
├── conf.py
├── __init__.py
└── usr_data.py
docs/
└── __init__.py
htekTestTools/
├── htekTestTools.py
├── __init__.py
├── phones.py
└── tests/
        └──unit_test.py
scripts/
└── main.py
README.md
TODO.md
```

**1. data**

存放配置文件

conf.py -> 全局配置

usr_data.py -> 用户自定义配置 -> 后期可能会改为使用excel

**2. docs**

计划用于存放文档，例如脚本如何编写，如何运行

**3. htekTestTools**

脚本文件目录

phones.py -> 定义了Phone类 -> 接受一系列参数对话机实例化

```python
phone = Phone('10.3.2.123', '8724', line=1, usr='admin', pwd='admin')
```

htekTestTools.py -> 定义了最终使用的函数

```python
basic_call(phone_a, phone_b)
```

**4. scripts**

最终实际执行的脚本文件目录

main.py 是包含所有测试用例的脚本

定制化的测试用例脚本可以由实际使用者添加
