from Model.DAO.UserDAO import UserDAO

users = UserDAO().getAll()

print(users)