from PhoneLib.htek_phones import Phone

Zoy_UC501 = Phone('10.3.2.132', '626', line=1, usr='admin', pwd='admin')
Zoy_S505 = Phone('10.3.2.231', '627', line=1, usr='admin', pwd='admin')
Zoy_UC926E = Phone('10.3.2.74', '628', line=2, usr='admin', pwd='admin')


stephen_UC926E = Phone('10.3.3.18', '2054', line=3, model='uc926e', usr='admin', pwd='admin')
stephen_UC912_1 = Phone('10.3.2.123', '2055', line=2, model='uc912', usr='admin', pwd='admin')
stephen_UC926 = Phone('10.3.3.123', '0002', model='uc926')
stephen_UC505 = Phone('10.3.3.140', '2056', model='uc505')
stephen_UC912_2 = Phone('10.3.3.146', '2057', model='uc912M')

stephen_dut_set = (stephen_UC926E, stephen_UC912_1, stephen_UC926, stephen_UC505, stephen_UC912_2)
stephen_conf_list = (stephen_UC912_1, stephen_UC926, stephen_UC505, stephen_UC912_2)

drd_UC926 = Phone('192.168.22.56', '0000', line=1, usr='admin', pwd='metro')
drd_UC924E = Phone('10.3.3.68', '0017', line=1, model='uc924E', usr='admin', pwd='metro')


RING_GROUP = ''
