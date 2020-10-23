import os
from datetime import datetime

OK = '200'  # 成功相应码
FAIL = '404'  # 错误相应码
HTML_HEAD = 'Content-Type: text/html'  # 响应头部
ROOT = './webroot'
NOT_FOUND_HTML = "/404.html"
DEFAUT_HTML = "/index.html"


class HttpRequestHandle(object):
    def __init__(self):
        self.method = ''
        self.request_context = []  # 请求报文
        self.url = ''
        self.protocol = "HTTP/1.1"
        self.host = ''
        self.request_body = ''
        self.request_data = ''
        self.error_code = OK  # 错误码
        self.response_head = HTML_HEAD
        self.response_body = ''

        self.time = ''

    def HandleRequest(self, request):  # socket传入request
        if request != b'':
            request_lines = request.splitlines()

            for line in request_lines:
                self.request_context.append(line.decode("utf-8"))  # 解析报文

            head_line = self.request_context[0].split(" ")  # 头文件格式：method url protocol

            self.method = head_line[0]
            self.url = head_line[1]
            self.protocol = head_line[2]

            self.host = self.request_context[1].split(" ")[1]

            self.time = str(datetime.now())

            # 处理post请求
            if self.method == 'POST':
                # 加入post请求加入body部分
                body_index = self.request_context.index("")
                for line in self.request_context[body_index + 1:]:
                    self.request_body = line + '\n'

                # 长度为1，设为默认页面
                if len(self.url) == 1:
                    self.url = DEFAUT_HTML

                file_name = self.url
                file_path = "." + file_name
                self.HandleFile(file_path)

            # 处理GET请求
            if self.method == 'GET':

                if len(self.url) == 1:
                    self.url = DEFAUT_HTML

                file_name = self.url.split('?', 1)[0]
                file_path = "." + file_name
                self.HandleFile(file_path)

    # 处理文件，构造返回体
    def HandleFile(self, file_path):

        # 文件不存在，打印404
        if not os.path.isfile(file_path):
            self.error_code = FAIL
            f = open("." + NOT_FOUND_HTML, 'r')
            self.response_body = f.read()
            f.close()

        # 文件存在
        else:
            self.error_code = OK

            # 打印html
            if file_path.endswith('.html'):
                f = open(file_path, 'r')
                self.response_body = f.read()
                f.close()

            # 运行cgi
            if file_path.endswith('.py'):

                if(self.request_body!=None):
                    command = self.request_body.split("&")
                    command_line = " ".join(command)
                    m = os.popen("python " + file_path + " " + command_line, 'r', 1)
                else:
                    m = os.popen("python " + file_path, 'r', 1)
                res = m.buffer.read().decode(encoding='utf-8')
                self.response_body = ''.join(res[res.index('<html>'):])

    def GetResponse(self):

        response_start = self.protocol + " " + self.error_code
        response = response_start + "\r\n" + self.response_head + "\r\n\r\n" + self.response_body

        return response
