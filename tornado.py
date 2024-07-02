from nwsapy import nwsapy
from data import Database
import datetime
import json

events = ['Tornado Watch', 'Tornado Warning', 'Child Abduction Emergency']
BufferDB = Database('AlertBuffer')

class AlertObject:
    def __init__(self, input_alert):
        self.inputAlert = input_alert
        self.title = input_alert.headline
        self.severity = input_alert.severity
        self.areas = input_alert.area_desc
        self.status = input_alert.status
        self.description = input_alert.description
        self.instruction = input_alert.instruction
        self.messageType = input_alert.message_type
        self.sender = input_alert.sender_name
        self.event = input_alert.event

    def console_print(self):
        print('\n' + self.title)
        print('Severity: ' + self.severity)
        print('Areas:')
        for i in self.areas:
            print('   -' + i)
        print('Status: ' + self.status)
        print('Full Desc: \n' + self.description + '\n')


def check_db(headline):
    db = BufferDB.get_database()
    for i in db:
        if headline in i:
            return True


def add_to_db(headline, weather_event):
    BufferDB.save_to_database(headline, weather_event, 0)

def json_date_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return str(obj)

def get_current_alerts():
    active_buffer = []
    nwsapy.set_user_agent('DiscordBot', 'developer@discord.com')
    for weather_event in events:
        active_alerts = nwsapy.get_active_alerts(event=weather_event)
        if len(active_alerts) > 0:
            for alert in active_alerts:
                if check_db(alert.headline):
                    with open('dump.json', 'w+') as f:
                        d = alert.to_dict()
                        f.write(json.dumps(d, default=json_date_encoder))
                    pass
                else:
                    print(f'[!] New active alert: {alert.headline}')
                    add_to_db(alert.headline, weather_event)
                    active_buffer.append(alert)
            print(f'[*] Added ' + str(len(active_alerts)) + ' entries to Database')
    return active_buffer
