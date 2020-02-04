import socket


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    localIpAddr = s.getsockname()[0]
    if localIpAddr[:10] == '192.168.4.':
        connectToIpAddr = '192.168.4.1:8081'
    else:
        connectToIpAddr = '10.233.102.94:8888'
    return connectToIpAddr
