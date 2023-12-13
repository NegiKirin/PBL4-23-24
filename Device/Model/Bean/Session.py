

class Session:
    def __init__(self, id, idRoom, status, day, startTime, endTime):
        self.id = id
        self.idRoom = idRoom
        self.status = status
        self.day = day
        self.startTime = startTime
        self.endTime = endTime
        self.listStudent = []
        self.room = None
