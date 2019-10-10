from PhoneLib.htek_phones import Phone


dut_1 = Phone('10.3.2.217', '2054', line=3, usr='admin', pwd='admin')
dut_2 = Phone('10.3.2.123', '2055', line=2, usr='admin', pwd='admin')

stephen_dut = Phone('192.168.1.3', '0000', line=1, usr='admin', pwd='admin')


phone_list = [stephen_dut]

RING_GROUP = ''
