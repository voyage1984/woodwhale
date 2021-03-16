import inspect

l_history = ['h_date','h_title','h_article']
db_name  = 'PyQt5_db'
username = 'testuser'
password = 'password'

def func_name():
    funcname = ": "+inspect.stack()[1][3]
    return funcname

if __name__ == '__main__':
    import MyDatabase
    db = MyDatabase.DBModel()
    db.conn(username,password)
