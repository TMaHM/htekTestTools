# coding:utf-8

import socket
import sys
from multiprocessing import Process
from phoneFunction.syn_phonelib.htek_phone_conf import *


def handle_str(msg):
    import re
    import json

    f = open(SIGNAL_FILE, 'w', encoding='utf-8')
    print('Open file time is: %s' % time.time())
    __pat_str = r'(?<=GET)(.*)(?=HTTP)'
    msg = re.findall(__pat_str, msg)
    if msg:
        print(msg[0])
        msg = msg[0].strip()
    else:
        print('no msg')
        return None

    __pat_ip = r'[1,2]?[0-9]{1,2}\.[1,2]?[0-9]{1,2}\.[1,2]?[0-9]{1,2}\.[1,2]?[0-9]{1,2}'
    _self_ip = re.findall(__pat_ip, msg)[0]
    _action = msg.split('/')[-2]
    _signal_time = msg.split('/')[-1]
    print('received time: %s' % _signal_time)

    _msg_box = {_signal_time: {'ip': _self_ip, 'action': _action}}
    json.dump(_msg_box, f)
    f.close()
    print('Close file time is: %s\n' % time.time())
    return _action, _signal_time


def handle_client(cl_socket):
    """
    处理客户端请求
    """
    request_data = cl_socket.recv(1024)
    print('Received real time is: %s' % time.time())
    received_msg = handle_str('%s' % request_data)

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect(('10.3.3.205', 8010))
    send_msg = "%s" % (received_msg,)
    send_socket.send(send_msg.encode(encoding='utf-8'))

    # print("request data:", request_data)
    # print(type(request_data))
    # # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = "<h1>Message Confirmed</h1>"
    response = response_start_line + response_headers + "\r\n" + response_body
    #
    # # 向客户端返回响应数据
    cl_socket.send(bytes(response, "utf-8"))

    # 关闭客户端连接
    cl_socket.close()
    return True


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(128)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            # print("[%s, %s]用户连接上了" % (client_address, client_socket))
            # print('%s' % client_socket)
            # send_socket = ('127.0.0.1', 8010)
            handle_client_process = Process(target=handle_client, args=(client_socket,))

            handle_client_process.start()

            client_socket.close()
        except KeyboardInterrupt:
            server_socket.shutdown(2)
            server_socket.close()
            sys.exit(0)
