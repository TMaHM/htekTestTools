from PhoneLib.htek_phones import Phone

Zoy_UC501 = Phone('10.3.2.132', '626', line=1, usr='admin', pwd='admin')
Zoy_S505 = Phone('10.3.2.231', '627', line=1, usr='admin', pwd='admin')
Zoy_UC926E = Phone('10.3.2.74', '628', line=2, usr='admin', pwd='admin')


dut_1 = Phone('10.3.3.18', '2054', line=3, model='uc926e', usr='admin', pwd='admin')
dut_2 = Phone('10.3.2.123', '2055', line=2, model='uc912', usr='admin', pwd='admin')

stephen_dut = Phone('10.3.2.217', '0000', line=1, usr='admin', pwd='admin')

drd_UC926 = Phone('192.168.22.56', '0000', line=1, usr='admin', pwd='metro')

phone_list = [stephen_dut, dut_2]

RING_GROUP = ''
