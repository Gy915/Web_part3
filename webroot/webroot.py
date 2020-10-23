import socket
import os
import threading
from Httpserver import HttpRequestHandle
import sys
import queue

class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    #每次从任务队列里获取一个任务并处理
    def run(self):
        while True:

            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()

class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        print("create a threadpool, the num is %d" % thread_number)
        for i in range(self.thread_number):     # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


def show_log(http_req):
    log_list=http_req.request_context

    code = http_req.error_code              #状态码
    time = '[' + http_req.time + ']'        #访问时间
    if(len(http_req.request_context)!=0):
        """
        for line in log_list:
            print(line)
        """
        if(http_req.method == 'GET'):
            for line in log_list:
                if('GET' in line):
                    method = line
                if('Host' in line):
                    ip_address = line.split(':')[1]
                if('User-Agent' in line):
                    User_Agent = line.split(':')[1]

            log = ip_address + " - " + time + ' ' + method + " -" + code + User_Agent + '\n'


        if (http_req.method == 'POST'):
            for line in log_list:
                if ('POST' in line):
                    method = line
                if ('Host' in line):
                    ip_address = line.split(':')[1]
                if ('Referer' in line):
                    Referer = line
                if ('User-Agent' in line):
                    User_Agent = line.split(':')[1]

            log = ip_address + " - " + time + ' ' + method + ' ' + Referer +" -" + code + User_Agent + '\n'
        print()
        print(log)
        f = open("log/msg.log", "a")
        f.write(log)
        f.close()


def tcp_link(sock, addr):
    request = sock.recv(1024)
    print()
    print("*" * 20)
    print('Accept new connection from %s:%s...' % addr)
    print('thread %s is handling the task' % threading.current_thread().name)
    http_req = HttpRequestHandle()
    http_req.HandleRequest(request)
    # 发送数据
    show_log(http_req)
    sock.send(bytes(http_req.GetResponse(), "utf-8"))
    # print(http_req.GetResponse())
    sock.close()
    print('thread %s has finished the task!' % threading.current_thread().name)

    print("*" * 20)
    print()
def start_server(thread_num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 可以重复地址
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 监听端口:
    s.bind(("", 8888))
    # 监听队列大小设成5(最多连接128个用户)
    s.listen(5)
    thread_pool = ThreadPoolManger(thread_num)
    print('Waiting for connection...')
    print("*" * 20)
    print()

    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 加入任务池并处理
        thread_pool.add_work(tcp_link, *(sock, addr))

if __name__ == '__main__':
    # 每次打开项目后首先清理上一次的log文件
    filename = r'log/msg.log'
    if os.path.exists(filename):
        f = open(filename, "a+")
        f.seek(0)
        f.truncate()
    thread_num = int(sys.argv[1])
    start_server(thread_num)
