# models.py
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.calendars = []

    def manageEvents(self):
        pass

class Event:
    def __init__(self, id, title, description, startDate):
        self.id = id
        self.title = title
        self.description = description
        self.startDate = startDate

class CalendarModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.listOfEvents = []

    def addEvent(self, event):
        self.listOfEvents.append(event)

    def getEventsByDate(self, date):
        return [ev for ev in self.listOfEvents if ev.startDate == date]
