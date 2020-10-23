import cgi, cgitb
from db_manipulate import Student

# [MANIPULATION, UID, NAME, AGE, SEX, CLASS, TEACHER, SCORE, VALID, RESERVED]
def get_message():
    try:
        form = cgi.FieldStorage()
        uid = form.getvalue('uid')
        stu = Student(UID = uid, NAME = None, AGE = None, SEX = None, CLASS = None, TEACHER = None, SCORE = None, VALID = 'UID', RESERVED = None)
        return 'SELECT', stu
    except:
        raise Exception('处理消息发生出错')