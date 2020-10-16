import re
import socket
 
from multiprocessing import Process
 
# 设置静态文件根目录
HTML_ROOT_DIR = "./html"


def handle_client(client_socket):
    """处理客户端请求"""
 
    # 接收客户端请求数据(报文)
    request_data = client_socket.recv(1024)
    if request_data != b'':
        print("request_data:", request_data)
    
        # splitlines返回的是一个列表形式
        request_lines = request_data.splitlines()
        print("==" * 20)
        print(request_lines)
        print("==" * 20)
        for line in request_lines:
            print(line)
    
        # 'GET / HTTP/1.1'
        request_start_line = request_lines[0]
        print("*" * 20)
        # 用户要请求的文件名(request_start_line由byte转化成str类型)
        print(request_start_line.decode("utf-8"))
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
        print(file_name)
        if "/" == file_name:
            file_name = "index.html"
        else :
            file_name = file_name[1:]
    
        # 打开文件，读取内容
        try:
            file = open(file_name, "rb")
        except IOError:
            response_start_line = "HTTP/1.1 404 Not Found\r\n"
            response_headers = "Server:My server\r\n"
            response_body = "The file is not found"
        else:
            file_data = file.read()
            file.close()
    
            # 构造相应数据
            # 构建：响应行
            # 响应的起始行
            response_start_line = "HTTP/1.1 200 OK\r\n"
            # 自己伪造的服务器的响应头
            response_headers = "Server:My server\r\n"
            # 响应体
            # response_body = "hello world"
            response_body = file_data.decode("utf-8")
    
        response = response_start_line + response_headers + "\r\n" + response_body
        print("#" * 20)
        print("response data:", response)
        print("#" * 20)
 
        # 向客户端返回响应数据
        # 字符串转化成字节
        client_socket.send(bytes(response, "utf-8"))
    
        # 关闭客户端连接
        client_socket.close()
 
 
if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 可以重复地址
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 接收任何IP地址,端口号8000
    server_socket.bind(("", 8080))
    # 监听队列大小设成128(最多连接128个用户)
    server_socket.listen(128)
 
    # 采用多进程的用户监听
    while True:
        # 等待连接
        # 接收到的是客户端的socket，和客户端的地址
        client_socket, client_address = server_socket.accept()
        # 打印：第一个参数是：IP地址，第二个参数是：端口号（存在于client_address里，它本身是个元组）
        # print("[%s,%s]用户连接上" % (client_address[0], client_address[1]))
        print("[%s,%s]用户连接上" % client_address)
        # Process参数target应该接收的是函数名，args接收的应该是个元组
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        # 开启进程
        handle_client_process.start()
        # 客户端的socket已经没有用了，关闭
        client_socket.close()