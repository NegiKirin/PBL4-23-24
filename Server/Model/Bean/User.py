
class User:
    def __init__(self, id, fullname, dateOfBirth, email, gender, idRole, cccd):
        self.id = id
        self.fullname = fullname
        self.dateOfBirth = dateOfBirth
        self.email = email
        self.gender = gender
        self.idRole = idRole
        self.cccd = cccd
        self.listSession = []
        self.role = None
        self.status = None