"""
端口池 用于维护代理可用端口范围
"""
import os
import signal
import socket

from apicopilot.proxy.store import MongoEngine


class PortStatus:
    IDLE = "IDLE"
    BUSY = "BUSY"


PORT_POLL = range(37000, 38000)


def get_port_state(port: int) -> str:
    """
    获取端口状态
    :param port:
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        return PortStatus.BUSY
    else:
        return PortStatus.IDLE


def kill_port_pid(port: int) -> None:
    """
    根据端口号找到对于pid并kill掉
    :param port: 要查询的端口
    :return: None
    """
    pid_info = \
        os.popen("netstat -nlp | grep :%s | awk '{print $7}' | awk -F"'/'" '{ print $1 }'" % (port)).read().split(
            '/')[0]
    print(f"端口号为{port}的进程为:{pid_info}")
    if pid_info:
        for pid in set(pid_info.strip().split('\n')):
            os.kill(int(pid), signal.SIGKILL)


def get_a_idle_port():
    """
    获取一个空闲的port
    :return:
    """
    for port in PORT_POLL[:900]:
        if get_port_state(port=port) == PortStatus.IDLE:
            return port
        continue
    else:
        raise Exception("无可用代理端口可用")


def assign_port_for_user(username: str = ""):
    """
    分配一个端口给用户
    :return:
    """
    if not username:
        # 未登录用户从倒数100个端口里面选择空闲port
        for port in PORT_POLL[:-100:-1]:
            if get_port_state(port=port) == PortStatus.IDLE:
                return port
            continue
        else:
            raise Exception("无可用代理端口可用")

    else:
        # 有身份用户 先查mongo有无此用户的历史port， 有则直接返回，没有则找一个空闲port并分配给此用户
        mongoengine = MongoEngine()
        mapping_collection = mongoengine.db_handle['mapping']
        results = mapping_collection.find({"username": username})
        if results:
            for result in results:
                if get_port_state(result['port']) == PortStatus.IDLE:
                    return result['port']

        for port in PORT_POLL[:900]:
            if get_port_state(port=port) == PortStatus.IDLE and not mapping_collection.find_one({"port": port}):
                mapping_collection.insert_one({
                    "username": username,
                    "port": port
                })
                return port
            continue
        else:
            raise Exception("无可用代理端口可用")
