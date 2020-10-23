#!/usr/bin/python
# -*- coding: UTF-8 -*-

# CGI处理模块
import os,sys

string = sys.argv[1:]

h1_msg = ''
h2_msg = ''

# 获取数据
num1 = string[0].split('=')[1]
sign = string[1].split('=')[1]
num2 = string[2].split('=')[1]

if((num1 == '') or (num2 == '')):
    h1_msg = 'Input Invalid'
    h2_msg = 'Please input at least 2 numbers.'

if(sign == 'add'):
    res = int(num1) + int(num2)
    h1_msg = 'Calculation Rusult'
    h2_msg = 'The result is ' + str(res) + '.'
if(sign == 'sub'):
    res = int(num1) - int(num2)
    h1_msg = 'Calculation Rusult'
    h2_msg = 'The result is ' + str(res) + '.'
if(sign == 'mul'):
    res = int(num1) * int(num2)
    h1_msg = 'Calculation Rusult'
    h2_msg = 'The result is ' + str(res) + '.'
if(sign == 'div'):
    if(num2 == '0'):
        h1_msg = 'Input Invalid'
        h2_msg = 'Divisor cannot be 0.'
    else:
        res = int(num1) / int(num2)
        h1_msg = 'Calculation Rusult'
        h2_msg = 'The result is ' + str(res) + '.'

print("<html>")
print("<head>")
print("<title>Online Calculator Result</title>")
print("<style>")
print(".class1{")
print("text-align:center")
print("}")
print("</style>")
print("</head>")
print("<body>")
print('<div class="class1">')
print("<h1>")
print("%s"%h1_msg)
print("</h1>")
print("<h2>")
print("%s"%h2_msg)
print("</h2>")
print("</div>")
print("</body>")
print("</html>")



