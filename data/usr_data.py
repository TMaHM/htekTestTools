from htekTestTools.phones import Phone

phone_1 = Phone('10.3.2.72', '3062', line=1, usr='admin', pwd='admin')
phone_2 = Phone('10.3.2.69', '0000', line=1, usr='admin', pwd='admin')
phone_3 = Phone('10.3.3.22', '8724', line=1, usr='admin', pwd='admin')
dut = Phone('192.168.1.2', '0000', line=1, usr='admin', pwd='admin')

phone_list = [phone_1, phone_2, phone_3]