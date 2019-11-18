from PhoneLib.htek_phones import Phone
# from phoneFunction.syn_phonelib.htek_phones import Phone

Zoy_UC501 = Phone('10.3.2.132', '626', line=1, usr='admin', pwd='admin')
Zoy_S505 = Phone('10.3.2.231', '627', line=1, usr='admin', pwd='admin')
Zoy_UC926E = Phone('10.3.2.74', '628', line=2, usr='admin', pwd='admin')


UC926E = Phone('10.3.3.192', '2054', line=3, model='uc926e', usr='admin', pwd='admin')
UC912_1 = Phone('10.3.2.123', '2055', line=1, model='uc912', usr='admin', pwd='admin')
UC926 = Phone('10.3.3.123', '0002', model='uc926')
UC505 = Phone('10.3.3.140', '2056', model='uc505')
UC912_2 = Phone('10.3.3.191', '2057', model='uc912M')

dspg1 = Phone('10.2.4.115', '633', line=1, model='uc926e', usr='admin', pwd='admin')
dspg2 = Phone('10.2.3.252', '632', line=2, model='uc912', usr='admin', pwd='admin')
dspg3 = Phone('10.2.4.112', '412', model='uc926')
dspg4 = Phone('10.2.4.114', '634', model='uc505')
dspg5 = Phone('10.2.2.27', '408', model='uc912M')


daily_uc923_1 = Phone('10.13.0.48', '4005', line=1, model='uc923', usr='admin', pwd='admin')
daily_uc923_2 = Phone('10.13.0.46', '4012', line=3, model='uc923', usr='admin', pwd='admin')
daily_uc912e_1 = Phone('10.13.0.88', '4007', line=3, model='uc912e', usr='admin', pwd='admin')
daily_uc926e_1 = Phone('10.13.0.33', '4016', line=1, model='uc926e', usr='admin', pwd='admin')
daily_uc912g_1 = Phone('10.13.0.87', '4006', line=1, model='uc912g', usr='admin', pwd='admin')

# 暂时不用
# daily_uc912e_2 = Phone('10.13.0.36', 'xxxx', line=2, model='uc912e', usr='admin', pwd='admin')
# daily_uc924e_1 = Phone('10.13.0.67', 'xxxx', line=2, model='uc924e', usr='admin', pwd='admin')
# daily_uc924_1 = Phone('10.13.0.27', 'xxxx', line=2, model='uc924', usr='admin', pwd='admin')


# stephen_dut_set = (stephen_UC926E, stephen_UC912_1, stephen_UC926, stephen_UC505, stephen_UC912_2)
# stephen_conf_list = (stephen_UC912_1, stephen_UC926, stephen_UC505, stephen_UC912_2)

drd_UC926 = Phone('192.168.22.56', '0000', line=1, usr='admin', pwd='metro')
drd_UC924E = Phone('10.3.3.68', '0017', line=1, model='uc924E', usr='admin', pwd='metro')


RING_GROUP = ''
