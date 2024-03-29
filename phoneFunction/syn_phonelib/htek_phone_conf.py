import logging
import os
import time

# 最大检查次数
MAX_CHECK_TIMES = 10
# 路径
CUR_DIR_PATH = '{}'.format(os.getcwd())
# PROJECT_ROOT_PATH = os.path.dirname(CUR_DIR_PATH)
PROJECT_ROOT_PATH = '{}htekTestTools/'.format(CUR_DIR_PATH.split('htekTestTools')[0])
# LOG 文件路径
LOG_DIR = '/tmp/htekPhoneLog/'
# 截屏临时路径
IMG_TEMP_PATH = '{cur_dir}/{img_dir}'.format(cur_dir=PROJECT_ROOT_PATH, img_dir='image/temp')
if not os.path.exists(IMG_TEMP_PATH):
    os.makedirs(IMG_TEMP_PATH)
# 标准截屏路径
IMG_STANDARD_PATH = '{cur_dir}/{img_dir}'.format(cur_dir=PROJECT_ROOT_PATH, img_dir='image/standard')
if not os.path.exists(IMG_STANDARD_PATH):
    os.makedirs(IMG_STANDARD_PATH)

# 当天的月，日
now_month = time.ctime().split(' ')[1]
now_date = time.ctime().split(' ')[2]
now_time = time.ctime().split(' ')[3].replace(':', '')

# signal文件
SIGNAL_DIR = '/tmp/htekPhoneLog/signal'
SIGNAL_FILE = '/tmp/htekPhoneLog/signal/signal.txt'
SIGNAL_HISTORY = '/tmp/htekPhoneLog/signal/signal_history.txt'
SIGNAL_BACK = '/tmp/htekPhoneLog/signal/signal-{month}-{date}{time}.txt'.format(month=now_month, date=now_date, time=now_time)
if not os.path.exists(SIGNAL_DIR):
    os.makedirs(SIGNAL_DIR)
if not os.path.exists(SIGNAL_FILE):
    open(SIGNAL_FILE, 'w').close()
if not os.path.exists(SIGNAL_HISTORY):
    open(SIGNAL_HISTORY, 'w').close()
elif os.path.getsize(SIGNAL_HISTORY) / 1024 ** 2 > 5:
    os.rename(SIGNAL_HISTORY, SIGNAL_BACK)
    open(SIGNAL_HISTORY, 'w').close()

# 定义话机状态字典，用于check_status()方法，但idle态不用此字典检查，而用GUI状态接口
p_status_dir = \
    {
        '0': 'idle', '[idle]': ['FXSState=0x80', 'CallCtlState=0x60', 'LCMState=-1 '],
        '1': 'speaker', '[Speaker]': ['FXSState=0x81', 'CallCtlState=0x61', 'LCMState=4 '],
        '2': 'outgoing', '[Outgoing]': ['FXSState=0x82', 'CallCtlState=0x62', 'LCMState=5 '],
        '3': 'talking', '[Talking]': ['FXSState=0x82', 'CallCtlState=0x64', 'LCMState=6 '],
        '4': 'ringing', '[Ringing]': ['FXSState=0x82', 'CallCtlState=0x63', 'LCMState=3 '],
        '5': 'hold', '[Hold]': ['FXSState=0x82', 'CallCtlState=0x87', 'LCMState=7 '],
        '6': 'new_initiate', '[New_Init]': ['FXSState=0x82', 'CallCtlState=0x81', 'LCMState=11 '],
        '7': 'new_talking', '[New_Talking]': ['FXSState=0x82', 'CallCtlState=0x82', 'LCMState=6 '],
        '8': 'conference', '[Conference]': ['FXSState=0x82', 'CallCtlState=0x88', 'LCMState=9 '],
        '9': 'conf_hold', '[Conf_Hold]': ['FXSState=0x82', 'CallCtlState=0x8d', 'LCMState=9 '],
    }
# 扩展板的Key对应的消息
exp_key_dir = \
    {
        'L1':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:0',
        'L2':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:1',
        'L3':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:2',
        'L4':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:3',
        'L5':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:4',
        'L6':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:5',
        'L7':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:6',
        'L8':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:7',
        'L9':  'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:8',
        'L10': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:9',
        'L11': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:10',
        'L12': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:11',
        'L13': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:12',
        'L14': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:13',
        'L15': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:14',
        'L16': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:15',
        'L17': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:16',
        'L18': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:17',
        'L19': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:18',
        'L20': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:19',
    }
# DSSKey字典
# dsskey_dir = {'l1': {'type':'linekey1_type', 'value':'linekey1_value',...}
dsskey_dir = {}
for i in range(1, 37):
    dsskey_dir['l' + str(i)] = {'type':    'linekey' + str(i) + '_type', 'value': 'linekey' + str(i) + '_value',
                                'account': 'linekey' + str(i) + '_account', 'label': 'linekey' + str(i) + '_label', }

line_key_dir = {
    'linekey1':  {'type': 'P41200', 'mode': 'P20600', 'value': 'P41300', 'label': 'P41400', 'acc': 'P41500',
                  'ext':  'P41600', },
    'linekey2':  {'type': 'P41201', 'mode': 'P20601', 'value': 'P41301', 'label': 'P41401', 'acc': 'P41500',
                  'ext':  'P41600', },
    'linekey3':  {'type': 'P41202', 'mode': 'P20602', 'value': 'P41302', 'label': 'P41402', 'acc': 'P41500',
                  'ext':  'P41600', },
    'linekey4':  {'type': 'P41203', 'mode': 'P20603', 'value': 'P41303', 'label': 'P41403', 'acc': 'P41500',
                  'ext':  'P41600', },
    'linekey5':  {'type': 'P20200', 'mode': 'P20604', 'value': 'P20201', 'label': 'P20202', 'acc': 'P20203',
                  'ext':  'P20204', },
    'linekey6':  {'type': 'P20205', 'mode': 'P20605', 'value': 'P20206', 'label': 'P20207', 'acc': 'P20208',
                  'ext':  'P20209', },
    'linekey7':  {'type': 'P20210', 'mode': 'P20606', 'value': 'P20211', 'label': 'P20212', 'acc': 'P20213',
                  'ext':  'P20214', },
    'linekey8':  {'type': 'P20215', 'mode': 'P20607', 'value': 'P20216', 'label': 'P20217', 'acc': 'P20218',
                  'ext':  'P20219', },
    'linekey9':  {'type': 'P20220', 'mode': 'P20608', 'value': 'P20221', 'label': 'P20222', 'acc': 'P20223',
                  'ext':  'P20224', },
    'linekey10': {'type': 'P20225', 'mode': 'P20609', 'value': 'P20226', 'label': 'P20227', 'acc': 'P20228',
                  'ext':  'P20229', },
    'linekey11': {'type': 'P20230', 'mode': 'P20610', 'value': 'P20231', 'label': 'P20232', 'acc': 'P20233',
                  'ext':  'P20234', },
    'linekey12': {'type': 'P20235', 'mode': 'P20611', 'value': 'P20236', 'label': 'P20237', 'acc': 'P20238',
                  'ext':  'P20239', },
    'linekey13': {'type': 'P20240', 'mode': 'P20612', 'value': 'P20241', 'label': 'P20242', 'acc': 'P20243',
                  'ext':  'P20244', },
    'linekey14': {'type': 'P20245', 'mode': 'P20613', 'value': 'P20246', 'label': 'P20247', 'acc': 'P20248',
                  'ext':  'P20249', },
    'linekey15': {'type': 'P20250', 'mode': 'P20614', 'value': 'P20251', 'label': 'P20252', 'acc': 'P20253',
                  'ext':  'P20254', },
    'linekey16': {'type': 'P20255', 'mode': 'P20615', 'value': 'P20256', 'label': 'P20257', 'acc': 'P20258',
                  'ext':  'P20259', },
    'linekey17': {'type': 'P20260', 'mode': 'P20616', 'value': 'P20261', 'label': 'P20262', 'acc': 'P20263',
                  'ext':  'P20264', },
    'linekey18': {'type': 'P20265', 'mode': 'P20617', 'value': 'P20266', 'label': 'P20267', 'acc': 'P20268',
                  'ext':  'P20269', },
    'linekey19': {'type': 'P20270', 'mode': 'P20618', 'value': 'P20271', 'label': 'P20272', 'acc': 'P20273',
                  'ext':  'P20274', },
    'linekey20': {'type': 'P20275', 'mode': 'P20619', 'value': 'P20276', 'label': 'P20277', 'acc': 'P20278',
                  'ext':  'P20279', },
    'linekey21': {'type': 'P20280', 'mode': 'P20620', 'value': 'P20281', 'label': 'P20282', 'acc': 'P20283',
                  'ext':  'P20284', },
    'linekey22': {'type': 'P20285', 'mode': 'P20621', 'value': 'P20286', 'label': 'P20287', 'acc': 'P20288',
                  'ext':  'P20289', },
    'linekey23': {'type': 'P20290', 'mode': 'P20622', 'value': 'P20291', 'label': 'P20292', 'acc': 'P20293',
                  'ext':  'P20294', },
    'linekey24': {'type': 'P20295', 'mode': 'P20623', 'value': 'P20296', 'label': 'P20297', 'acc': 'P20298',
                  'ext':  'P20299', },
    'linekey25': {'type': 'P20300', 'mode': 'P20624', 'value': 'P20301', 'label': 'P20302', 'acc': 'P20303',
                  'ext':  'P20304', },
    'linekey26': {'type': 'P20305', 'mode': 'P20625', 'value': 'P20306', 'label': 'P20307', 'acc': 'P20308',
                  'ext':  'P20309', },
    'linekey27': {'type': 'P20310', 'mode': 'P20626', 'value': 'P20311', 'label': 'P20312', 'acc': 'P20313',
                  'ext':  'P20314', },
    'linekey28': {'type': 'P20315', 'mode': 'P20627', 'value': 'P20316', 'label': 'P20317', 'acc': 'P20318',
                  'ext':  'P20319', },
    'linekey29': {'type': 'P20320', 'mode': 'P20628', 'value': 'P20321', 'label': 'P20322', 'acc': 'P20323',
                  'ext':  'P20324', },
    'linekey30': {'type': 'P20325', 'mode': 'P20629', 'value': 'P20326', 'label': 'P20327', 'acc': 'P20328',
                  'ext':  'P20329', },
    'linekey31': {'type': 'P20330', 'mode': 'P20630', 'value': 'P20331', 'label': 'P20332', 'acc': 'P20333',
                  'ext':  'P20334', },
    'linekey32': {'type': 'P20335', 'mode': 'P20631', 'value': 'P20336', 'label': 'P20337', 'acc': 'P20338',
                  'ext':  'P20339', },
    'linekey33': {'type': 'P20340', 'mode': 'P20632', 'value': 'P20341', 'label': 'P20342', 'acc': 'P20343',
                  'ext':  'P20344', },
    'linekey34': {'type': 'P20345', 'mode': 'P20633', 'value': 'P20346', 'label': 'P20347', 'acc': 'P20348',
                  'ext':  'P20349', },
    'linekey35': {'type': 'P20350', 'mode': 'P20634', 'value': 'P20351', 'label': 'P20352', 'acc': 'P20353',
                  'ext':  'P20354', },
    'linekey36': {'type': 'P20355', 'mode': 'P20635', 'value': 'P20356', 'label': 'P20357', 'acc': 'P20358',
                  'ext':  'P20359', },
}

key_type_code_dir = {
    'N/A':                 '0',
    'LINE':                '1',
    'SPEEDDIAL':           '2',
    'BLF':                 '3',
    'BLF LIST':            '4',
    'VOICEMAIL':           '5',
    'DIRECT PICKUP':       '6',
    'GROUP PICKUP':        '7',
    'CALL PARK':           '8',
    'INTERCOM':            '9',
    'DTMF':                '10',
    'PREFIX':              '11',
    'LOCAL GROUP':         '12',
    'XML GROUP':           '13',
    'XML BROWSER':         '14',
    'LDAP':                '15',
    'NETWORK DIRECTORIES': '16',
    'CONFERENCE':          '17',
    'FORWARD':             '18',
    'TRANSFER':            '19',
    'HOLD':                '20',
    'DND':                 '21',
    'REDIAL':              '22',
    'CALL RETURN':         '23',
    'SMS':                 '24',
    'RECORD':              '25',
    'URL RECORD':          '26',
    'PAGING':              '27',
    'GROUP LISTENING':     '28',
    'PUBLIC HOLD':         '29',
    'PRIVATE HOLD':        '30',
    'HOT DESKING':         '32',
    'ACD':                 '33',
    'ZERO TOUCH':          '34',
    'URL':                 '35',
    'NETWORK GROUP':       '44',
    'MULTICAST PAGING':    '47',
    'GROUP CALL PARK':     '51',
    'CALLPARK RETRIEVE':   '52',
    'PULL CALL':           '53'}

key_mode_code_dir = {
    'default': '0',
    'lock':    '1',
    'float':   '2',
}

key_acc_code_dir = {
    'ACCOUNT1': '0',
    'ACCOUNT2': '1',
    'ACCOUNT3': '2',
    'ACCOUNT4': '3',
    'ACCOUNT5': '4',
    'ACCOUNT6': '5',
}

# 各功能分型号及Solution的LCD像素点坐标
acd_pixel_dir = {
    'acd_in':          {
        'uc926':  {'drd': (386, 4, 414, 34), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (379, 10, 402, 38), 'routit': (1, 1, 1, 1)},
    },
    'acd_out':         {
        'uc926':  {'drd': (386, 4, 414, 34), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (379, 10, 402, 38), 'routit': (1, 1, 1, 1), },
    },
    'acd_available':   {
        'uc926':  {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
    },
    'acd_wrap up':     {
        'uc926':  {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
    },
    'acd_unavailable': {
        'uc926':  {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
    },
    'acd_dispcode':    {
        'uc926':  {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
    }
}

flx_pixel_dir = {
    'flx_in':  {
        'uc926':  {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
    },
    'flx_out': {
        'uc926':  {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
        'uc924e': {'drd': (0, 0, 0, 0), 'routit': (1, 1, 1, 1), },
    },
}


class Logger:

    def __init__(self, echo: bool = False, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        # log及截屏文件存放目录
        log_dir = LOG_DIR + r'log/'
        log_backup = log_dir + r'backup/'
        self.screen_dir = log_dir + r'screenShot'
        # log文件绝对路径
        info_path = log_dir + r'info.log'
        debug_path = log_dir + r'debug.log'
        # screen_file = self.screen_dir  # 不知道为什么存在，先隐掉

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            os.makedirs(log_backup)
            open(info_path, 'w').close()
            open(debug_path, 'w').close()
        else:
            if not os.path.exists(info_path):
                open(info_path, 'w').close()
                open(debug_path, 'w').close()
            else:
                if not os.path.exists(log_backup):
                    os.makedirs(log_backup)
                else:
                    pass
                info_size = os.path.getsize(info_path)
                debug_size = os.path.getsize(debug_path)
                if info_size / 1024 ** 2 > 5:
                    print('---Backup info.log because large than 5M.----')
                    os.rename(info_path,
                              '{dir}info_bak_{month}{date}{time}.log'.format(dir=log_backup, month=now_month,
                                                                             date=now_date, time=now_time))
                    open(info_path, 'w').close()
                else:
                    pass
                if debug_size / 1024 ** 2 > 5:
                    print('---Backup debug.log because large than 5M---')
                    os.rename(debug_path,
                              '{dir}debug_bak_{month}{date}{time}.log'.format(dir=log_backup, month=now_month,
                                                                              date=now_date, time=now_time))
                    open(debug_path, 'w').close()
                else:
                    pass

        if not os.path.exists(self.screen_dir):
            os.makedirs(self.screen_dir)

        self.logger_debug = logging.getLogger(info_path)
        self.logger_info = logging.getLogger(debug_path)
        self.logger_debug.setLevel(logging.DEBUG)
        self.logger_info.setLevel(logging.INFO)
        fmt_info = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fmt_debug = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置终端日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt_info)
        sh.setFormatter(fmt_debug)
        sh.setLevel(clevel)
        # 设置文件日志
        fh_info = logging.FileHandler(info_path)
        fh_debug = logging.FileHandler(debug_path)
        fh_info.setFormatter(fmt_info)
        fh_debug.setFormatter(fmt_debug)
        fh_info.setLevel(Flevel)
        fh_debug.setLevel(Flevel)
        if echo:
            self.logger_info.addHandler(sh)
            self.logger_debug.addHandler(sh)
        self.logger_info.addHandler(fh_info)
        self.logger_debug.addHandler(fh_debug)

    def debug(self, message):
        self.logger_debug.debug(message)

    def info(self, message):
        self.logger_info.info(message)

    def war(self, message):
        self.logger_info.warning(message)

    def error(self, message):
        self.logger_info.error(message)


log = Logger(echo=False)


class TestUrl:
    """
    通用型URL的集合，提供给Phone类调用，部分需要附加参数
    ip: Phone的IP
    usr&pwd: 默认admin，需要改变时传入相应参数
    Usage::
        见phones 14行
    """

    def __init__(self, ip, usr='admin', pwd='admin'):
        self.ip = ip
        self.usr = usr
        self.pwd = pwd

        self.url_prefix = 'http://{usr}:{pwd}@{ip}'.format(usr=self.usr, pwd=self.pwd, ip=self.ip)
        self.url_screenshot = self.url_prefix + '/download_screen'
        self.url_keyboard = self.url_prefix + '/AutoTest&keyboard='
        self.url_status = self.url_prefix + '/AutoTest&autoverify=STATE='
        self.url_idle_status = '{prefix}/AutoTest&gui=LCD_Idle_Win:0'.format(prefix=self.url_prefix)
        self.url_get_memory = self.url_prefix + '/AutoTest&autoverify=MEMORYFREE'
        self.url_setting = self.url_prefix + '/AutoTest&setting='

        self.url_drd_prefix = self.url_prefix + '/AutoTest&drd='


def phone_status(status):
    """
    通过传入的话机状态的参数，匹配p_status_dir字典
    :param status: 要check的话机状态，如talking，提供给check_status调用，匹配状态字典中的值
    :return: 根据传入的参数，返回话机当前状态码或状态名
    Usage::
        status = 'talking'
        code = p_status(status) -> 返回状态对应的url末尾的检查码，如1
        status = ['FXSState=0x82', 'CallCtlState=0x8d', 'LCMState=9 ']
        -> 返回对应的状态名
    """
    if status in p_status_dir.values():
        for key, value in p_status_dir.items():
            if status == value:
                return key
    else:
        return None
