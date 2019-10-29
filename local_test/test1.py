import os
import time


log_dir = '../log'
info_path = '../log/info.log'
debug_path = '../log/debug.log'
now_time = time.ctime().split(' ')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    open(info_path, 'w').close()
    open(debug_path, 'w').close()
else:
    if not os.path.exists(info_path):
        open(info_path, 'w').close()
        open(debug_path, 'w').close()
    else:
        info_size = os.path.getsize(info_path)
        debug_size = os.path.getsize(debug_path)
        if info_size / 1024 ** 2 > 0.5:
            os.rename(info_path, '../log/info_bak_%s-%s' % (now_time[4], now_time[2]))
            print(now_time, now_time[4], now_time[2])
            open(info_path, 'w').close()
        else:
            pass
        if debug_size / 1024 ** 2 > 0.5:
            os.rename(debug_path, '../log/debug_bak_%s-%s' % (now_time[4], now_time[2]))
            print(now_time, now_time[4], now_time[2])
            open(debug_path, 'w').close()
        else:
            print('not here')
