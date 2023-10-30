import mysql.connector

class ConnectDB:
    def __init__(self, host='localhost', user='root', password='', database='pbl4'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.myCursor = self.mydb.cursor()


class UserDAO:
    def __init__(self, connect=None):
        self.connect = connect

    def findAll(self):
        sql = 'SELECT * FROM user'
        self.connect.myCursor.execute(sql)
        result = self.connect.myCursor.fetchall()
        return result

    def findUser(self, pageable=None):
        sql = """SELECT user.id, name, class_name, faculty_name FROM user
                INNER JOIN class ON user.class_id = class.id
                INNER JOIN faculty ON user.faculty_id = faculty.id"""
        self.connect.myCursor.execute(sql)
        result = self.connect.myCursor.fetchall()
        return result


if __name__ == "__main__":
    conn = ConnectDB()
    dao = UserDAO(conn)
    for row in dao.findUser():
        print(row)