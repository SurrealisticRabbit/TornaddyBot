from nwsapy import nwsapy
from data import Database

events = ['Tornado Watch','Tornado Warning']
BufferDB = Database('AlertBuffer')

class AlertObject():
    def __init__(self, inputAlert):
        self.inputAlert = inputAlert
        self.title = inputAlert.headline
        self.severity = inputAlert.severity
        self.areas = inputAlert.area_desc
        self.status = inputAlert.status
        self.description = inputAlert.description
        self.instruction = inputAlert.instruction
        self.messageType = inputAlert.message_type
        self.sender = inputAlert.sender_name
    
    def consolePrint(self):
        print('\n'+self.title)
        print('Severity: '+self.severity)
        print('Areas:')
        for i in self.areas:
            print('   -' + i)
        print('Status: '+self.status)
        print('Full Desc: \n' + self.description + '\n')

def checkDB(headline):
    db = BufferDB.get_database()
    for i in db:
        if headline in i:
            return True

def addToDB(headline, weatherEvent):
    BufferDB.saveToDatabase(headline, weatherEvent, 0)

def getActiveAlerts():
    activeBuffer = []
    nwsapy.set_user_agent('DiscordBot', 'developer@discord.com')
    for weather_event in events:
        activeAlerts = nwsapy.get_active_alerts(event=weather_event)
        if len(activeAlerts) > 0:
            for alert in activeAlerts:
                if checkDB(alert.headline):
                    pass
                else:
                    addToDB(alert.headline, weather_event)
                    activeBuffer.append(alert)
    return activeBuffer