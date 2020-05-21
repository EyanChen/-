# coding : utf-8

"""
扫描自己网段内,哪些IP被占用,用于搜索局域网联机
"""
import os
import threading
import socket

first_ip = ''
useable = []


def ping_ip(target_ip):
    # 用os的popen方法,返回结果是个文件,直接读取,
    result = os.popen('ping -n 1 ' + target_ip).readlines()
    # 检测文件里有无TTL,有就是可用IP
    for line in list(result):
        if not line:
            continue
        if line.upper().find('TTL') > 0:
            print('IP: %s已占用! ' % (target_ip))
            useable.append(target_ip)
            break


if __name__ == '__main__':
    # 拿到自己的主机名(hostname)
    hostname = socket.gethostname()
    # 根据hostname 找IP段
    ip_addr = socket.gethostbyname(hostname)
    # print(ip_addr)
    index = ip_addr.rfind('.')
    first_ip = ip_addr[0:index + 1]
    # print(first_ip)

    thread_list = []
    for x in range(1, 256):  # 开线程提高效率
        target_ip = first_ip + str(x)
        thread = threading.Thread(target=ping_ip, args=(target_ip,))
        thread.start()
        thread_list.append(thread)
    for x in thread_list:
        x.join()

    print('当前局域网占用的IP有: ')
    print(useable)
