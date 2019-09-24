import logging
import os

# 最大检查次数
MAX_CHECK_TIMES = 10

# 定义话机状态字典，用于status.py，设置idle态及check状态
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

exp_blf_dir = \
    {
        'L1': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:0',
        'L2': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:1',
        'L3': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:2',
        'L4': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:3',
        'L5': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:4',
        'L6': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:5',
        'L7': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:6',
        'L8': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:7',
        'L9': 'EXPANSION:EXP_NO:0EXP_PAGE:0EXP_KEYNO:8',
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

dsskey_dir = {}

for i in range(1, 37):
    dsskey_dir['l' + str(i)] = {'type': 'linekey' + str(i) + '_type', 'value': 'linekey' + str(i) + '_value',
                                'account': 'linekey' + str(i) + '_account', 'label': 'linekey' + str(i) + '_label', }

key_type_code_dir = {
    'N/A': '0',
    'LINE': '1',
    'SPEEDDIAL': '2',
    'BLF': '3',
    'BLF LIST': '4',
    'VOICEMAIL': '5',
    'DIRECT PICKUP': '6',
    'GROUP PICKUP': '7',
    'CALL PARK': '8',
    'INTERCOM': '9',
    'DTMF': '10',
    'PREFIX': '11',
    'LOCAL GROUP': '12',
    'XML GROUP': '13',
    'XML BROWSER': '14',
    'LDAP': '15',
    'NETWORK DIRECTORIES': '16',
    'CONFERENCE': '17',
    'FORWARD': '18',
    'TRANSFER': '19',
    'HOLD': '20',
    'DND': '21',
    'REDIAL': '22',
    'CALL RETURN': '23',
    'SMS': '24',
    'RECORD': '25',
    'URL RECORD': '26',
    'PAGING': '27',
    'GROUP LISTENING': '28',
    'PUBLIC HOLD': '29',
    'PRIVATE HOLD': '30',
    'HOT DESKING': '32',
    'ACD': '33',
    'ZERO TOUCH': '34',
    'URL': '35',
    'NETWORK GROUP': '44',
    'MULTICAST PAGING': '47',
    'GROUP CALL PARK': '51',
    'CALLPARK RETRIEVE': '52',
    'PULL CALL': '53'}

key_account_code_dir = {
    'ACCOUNT1': '0',
    'ACCOUNT2': '1',
    'ACCOUNT3': '2',
    'ACCOUNT4': '3',
    'ACCOUNT5': '4',
    'ACCOUNT6': '5',
}


class Logger:

    def __init__(self, echo: bool = False, clevel=logging.DEBUG, Flevel=logging.DEBUG):

        # 当前所在目录的路径
        # root_path = os.path.dirname(os.getcwd())
        root_path = os.getcwd()
        print(root_path)
        # log及截屏文件存放目录
        # log_dir_path = root_path + '\\log\\' + cur_exec_file_nosuffix + '\\'
        log_dir = root_path + r'/log/'
        self.screen_dir = log_dir + r'screenShot/'
        # log文件绝对路径
        info_path = log_dir + r'info.log'
        debug_path = log_dir + r'debug.log'
        screen_file = self.screen_dir

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

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


# log = Logger(echo=False)

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

        self.prefix = 'http://%s' % self.ip

        self.screenshot = self.prefix + '/download_screen'
        self.keyboard = self.prefix + '/AutoTest&keyboard='
        self.url_status = self.prefix + '/AutoTest&autoverify=STATE='
        self.url_get_memory = self.prefix + '/AutoTest&autoverify=MEMORYFREE'
        self.setting = self.prefix + '/AutoTest&setting='


def phone_status(status):
    """
    通过传入的话机状态的参数，匹配p_status_dir字典
    :param status: 要check的话机状态，如idle，提供给check_status调用，匹配状态字典中的值
    :return: 根据传入的参数，返回话机当前状态码或状态名
    Usage::
        status = 'idle'
        code = p_status(status) -> 返回状态对应的url末尾的检查码
        status = ['FXSState=0x82', 'CallCtlState=0x8d', 'LCMState=9 ']
        -> 返回对应的状态名
    """
    if status in p_status_dir.values():
        for key, value in p_status_dir.items():
            if status == value:
                return key
    else:
        return None
