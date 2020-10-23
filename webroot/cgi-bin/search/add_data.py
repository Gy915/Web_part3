from db_manipulate import Student, DB

# UID = None, NAME = None, AGE = None, SEX = None, CLASS = None, TEACHER = None, SCORE = None, VALID = None, RESERVED = None
stu1 = Student(UID = 1120170001, NAME = 'ZhangSan', AGE = 19, SEX = 'Male', CLASS = '07111703', TEACHER = 'Mr Wang', SCORE = 98, VALID = None, RESERVED = None)
stu2 = Student(UID = 1120170002, NAME = 'LiSi', AGE = 19, SEX = 'Male', CLASS = '07111703', TEACHER = 'Mr Wang', SCORE = 97, VALID = None, RESERVED = None)
stu3 = Student(UID = 1120170003, NAME = '张三', AGE = 19, SEX = 'Male', CLASS = '07111703', TEACHER = '王老师', SCORE = 97, VALID = None, RESERVED = None)
db = DB()
db.db_insert(stu1)
db.db_insert(stu2)
db.db_insert(stu3)