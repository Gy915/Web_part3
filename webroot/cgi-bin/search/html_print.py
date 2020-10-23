from db_manipulate import Student, DB

def htmlf(function):
    def func(*args, **kwargs):
        print('<html>')
        print('<head>')
        print('<meta charset="utf-8">')
        print('<title>Student Search System</title>')
        print('<style>')
        print('.class1{')
        print('text-align:center')
        print('}')
        print('</style>')
        print('</head>')
        print('<body>')
        print('<div class = "class1">')
        print('<h1>Student Search System</h1>')
        print('<h2>Searching Result:</h2>')
        print('<table border = "1px" align="center">')
        print('<tr>')
        print('<th>学号</th>')
        print('<th>姓名</th>')
        print('<th>年龄</th>')
        print('<th>性别</th>')
        print('<th>班号</th>')
        print('<th>任课老师</th>')
        print('<th>分数</th>')
        print('</tr>')
        print('<tr>')
        function(*args, **kwargs)
        print('</tr>')
        print('</table>')
        print('</div>')
        print('</body>')
        print('</html>')
    return func

@htmlf
def execute(mpl, stu):
    def select(stu):
        db = DB()
        data = db.db_select(stu)
        for row in data:
            #print(row)
            for line in row:
                print("<td>")
                print(line)
                print("</td>")
    def insert(stu):
        db = DB()
        db.db_insert(stu)
        print('插入数据成功')
    def update(stu):
        db = DB()
        db.db_update(stu)
        print('更新数据成功')
    def delete(stu):
        db = DB()
        db.db_delete(stu)
        print('删除数据成功')
    MANIPULATE = {'SELECT':select, 'INSERT':insert, 'UPDATE':update, 'DELETE':delete}
    MANIPULATE.get(mpl)(stu)
