from html_print import execute
from db_manipulate import Student
from msg_processing import get_message

def main():
    mpl, stu = get_message()
    execute(mpl, stu)

if __name__ == "__main__":
    main()