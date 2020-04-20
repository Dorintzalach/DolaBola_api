import pymysql

class Database:
    def __init__(self):
        host = 'root.csrlcaaimlih.us-east-2.rds.amazonaws.com'
        user = 'root'
        password = 'Dola080990Bola220792'
        db = 'DolaBola_DB'
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def get_all_blog_items(self):
        self.cur.execute("SELECT * FROM blog_items")
        result = self.cur.fetchall()
        return result
