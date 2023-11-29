import mysql.connector
from Pageable import PageRequest
class ConnectDB:
    def __init__(self, host='localhost', user='root', password='', database='pbl4_updated'):
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

    def close(self):
        self.myCursor.close()
        self.mydb.close()

class UserDAO:
    def __init__(self):
        self.connect = ConnectDB()

    def findById(self, id):
        sql = f"SELECT * FROM USER WHERE id = {id}"
        self.connect.myCursor.execute(sql)
        result = self.connect.myCursor.fetchall()
        return result

    def findAll(self):
        sql = """SELECT user.id, name, class_name, faculty_name FROM user
                INNER JOIN class ON user.class_id = class.id
                INNER JOIN faculty ON user.faculty_id = faculty.id"""
        self.connect.myCursor.execute(sql)
        result = self.connect.myCursor.fetchall()
        return result

    def findPageable(self, pageable):
        try:
            sql = "SELECT user.id, name, class_name, faculty_name FROM user INNER JOIN class ON user.class_id = class.id INNER JOIN faculty ON user.faculty_id = faculty.id"

            if pageable.searcher.search != None:
                sql += f" WHERE user.{pageable.searcher.searchName} LIKE \"%{pageable.searcher.search}%\""
            sql += f" ORDER BY id LIMIT {pageable.maxPageItem} OFFSET {pageable.getOffset()}"
            print(sql)
            self.connect.myCursor.execute(sql)
            result = self.connect.myCursor.fetchall()
            result.append(self.totalItem())
            self.connect.close()
            print(result)
            return result
        except:
            print("sql error")
            return []

    def totalItem(self):
        try:
            sql = "SELECT COUNT(*) FROM user"
            self.connect.myCursor.execute(sql)
            result = self.connect.myCursor.fetchall()
            return result[0][0]
        except:
            return 0

class HistoryDAO:
    def __init__(self):
        self.connect = ConnectDB()

    def insert(self, user_id, session_id):
        sql = "INSERT INTO history (user_id, session_id) VALUES (%s, %s)"
        val = (user_id, session_id)
        self.connect.myCursor.execute(sql, val)
        self.connect.mydb.commit()


    def findPageable(self, pageable):
        try:
            sql = "SELECT history.id, user.name, history.time_checkin, history.time_checkout FROM history INNER JOIN user ON user.id = history.user_id"

            # if pageable.searcher.search != None:
            #     sql += f" WHERE user.{pageable.searcher.searchName} LIKE \"%{pageable.searcher.search}%\""
            sql += f" ORDER BY id LIMIT {pageable.maxPageItem} OFFSET {pageable.getOffset()}"
            self.connect.myCursor.execute(sql)
            result = self.connect.myCursor.fetchall()
            result.append(self.totalItem())
            self.connect.close()
            result = self.convertStr(result)
            return result
        except:
            print("sql error")
            return []

    def convertStr(self, tuple):
        tmp = []
        for i in tuple[:-1]:
            tmp.append(list(i))

        tmp.append(tuple[-1])
        for row in tmp[:-1]:
            row[0] = str(row[0])
            row[2] = str(row[2])
            row[3] = str(row[3])

        return tmp

    def totalItem(self):
        try:
            sql = "SELECT COUNT(*) FROM history"
            self.connect.myCursor.execute(sql)
            result = self.connect.myCursor.fetchall()
            return result[0][0]
        except:
            return 0

if __name__ == "__main__":

    # dao = UserDAO()
    # dao2 = HistoryDAO()
    #
    # pageable = PageRequest(page=1, maxPageItem=10)
    #
    # print(dao2.findPageable(pageable)[:-1])
    dao = UserDAO()
    print(dao.findById(2))

