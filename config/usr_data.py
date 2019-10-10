from PhoneLib.htek_phones import Phone


# phone_1 = Phone('10.3.2.217', '2054', line=3, usr='admin', pwd='admin')
# phone_2 = Phone('10.3.2.123', '8724', line=1, usr='admin', pwd='admin')
# phone_3 = Phone('10.3.3.22', '8724', line=1, usr='admin', pwd='admin')
# dut = Phone('192.168.1.2', '0000', line=1, usr='admin', pwd='admin')
#
# phone_list = [phone_1, phone_2, phone_3]


def create_phone(ip, ext, line, usr, pwd):
    phone = Phone(ip, ext, line, usr=usr, pwd=pwd)
    return phone


def dut_list():
    phone_a = Phone('10.3.2.217', '2054', line=3, usr='admin', pwd='admin')
    phone_b = Phone('10.3.2.123', '2055', line=2, usr='admin', pwd='admin')
    phone_c = Phone('10.3.3.22', '8724', line=1, usr='admin', pwd='admin')

    phone_list = (phone_a, phone_b, phone_c)
    return phone_list


class MyPhone(Phone):
    def __init__(self, ip: str, extension: str, line=1, usr='admin', pwd='admin'):
        Phone.__init__(self, ip, extension, line, usr, pwd)
        self.ip = ip
        self.ext = extension
        self.line = line
        self.usr = usr
        self.pwd = pwd


dut_1 = Phone('10.3.2.217', '2054', line=3, usr='admin', pwd='admin')
dut_2 = Phone('10.3.2.123', '2055', line=2, usr='admin', pwd='admin')

dut_1.set_idle_status()

MYLIST = ['1', '2', '3']
