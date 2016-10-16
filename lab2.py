#!/usr/bin/python
import logging
from spyne import Application, srpc, ServiceBase, Iterable, UnsignedInteger, String, Unicode
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
logging.basicConfig()
logger = logging.getLogger(__name__)


import requests
#from datetime import datetime
import json
import datetime
import urllib
import re
from collections import Counter

class CrimeAPIService(ServiceBase):
    @srpc(float, float, float, float, _returns=Iterable(Unicode))
    def checkcrime(lat, lon, radius, key):
       
       time1 = datetime.datetime.strptime('12:01 AM', '%H:%M %p')
       time2 = datetime.datetime.strptime('03:00 AM', '%H:%M %p')
       time3 = datetime.datetime.strptime('03:01 AM', '%H:%M %p')
       time4 = datetime.datetime.strptime('06:00 AM', '%H:%M %p')
       time5 = datetime.datetime.strptime('06:01 AM', '%H:%M %p')
       time6 = datetime.datetime.strptime('09:00 AM', '%H:%M %p')
       time7 = datetime.datetime.strptime('09:01 AM', '%H:%M %p')
       time8 = datetime.datetime.strptime('12:00 PM', '%H:%M %p')
       time9 = datetime.datetime.strptime('12:01 PM', '%H:%M %p')
       time10 = datetime.datetime.strptime('03:00 PM', '%H:%M %p')
       time11 = datetime.datetime.strptime('03:01 PM', '%H:%M %p')
       time12 = datetime.datetime.strptime('06:00 PM', '%H:%M %p')
       time13 = datetime.datetime.strptime('06:01 PM', '%H:%M %p')
       time14 = datetime.datetime.strptime('09:00 PM', '%H:%M %p')
       time15 = datetime.datetime.strptime('09:01 PM', '%H:%M %p')
       time16= datetime.datetime.strptime('12:00 AM', '%H:%M %p')
       
       payload={'lat':lat,'lon':lon, 'radius':radius, 'key':'.'}
       r=requests.get('https://api.spotcrime.com/crimes.json',params=payload) 
       api_data=r.json()        #change api_data to crime_data
       total_crimes = len(api_data["crimes"]) 
       
       crime_type={}            #change crime type to crime_data
       for n in range (len(api_data["crimes"])):
            if (api_data["crimes"][n]["type"]) not in crime_type:
                crime_type[(api_data["crimes"][n]["type"])] = 1
            else:
                crime_type[(api_data["crimes"][n]["type"])] += 1
                
       event_time={}
       counter1 = 0
       counter2 = 0
       counter3 = 0
       counter4 = 0
       counter5 = 0
       counter6 = 0
       counter7 = 0
       counter8 = 0
       for n in range (len(api_data["crimes"])):
            
            date = datetime.datetime.strptime(api_data["crimes"][n]['date'], '%m/%d/%y %H:%M %p')
            timeStr = date.strftime("%H:%M %p")
            time = datetime.datetime.strptime(timeStr, '%H:%M %p')
            #print json.dumps(timeStr)
            if(time>=time1 and time<=time2):
                counter1 +=1
                event_time["12:01 AM to 03:00 AM"] = counter1
            elif(time>=time3 and time<=time4):
                counter2 +=1
                event_time["03:01 AM to 06:00 AM"] = counter2
            elif(time>=time5 and time<=time6):
                counter3 +=1
                event_time["06:01 AM to 09:00 AM"] = counter3
            elif(time>=time7 and time<=time8):
                counter4 +=1
                event_time["09:01 AM to 12:00 PM"] = counter4
            elif(time>=time9 and time<=time10):
                counter5 +=1
                event_time["12:01 PM to 03:00 PM"] = counter5
            elif(time>=time11 and time<=time12):
                counter6 +=1
                event_time["03:01 PM to 06:00 PM"] = counter6
            elif(time>=time13 and time<=time14):
                counter7 +=1
                event_time["06:01 PM to 09:00 PM"] = counter7
            elif(time>=time15 or time == time16):
                counter8 +=1
                event_time["09:01 PM to 12:00 AM"] = counter8
      # yield total_crimes
      # yield ctype
       
       dangerous_st = []
       and_list = []
       new = []
       for n in range (len(api_data["crimes"])):
           address = api_data["crimes"][n]["address"];
           street = re.sub(r'\d* *block *o?f? *',"",address,flags=re.IGNORECASE)
           dangerous_st.append(street)
       for i in dangerous_st:
           if '&' in i:
            and_list.append(i)
       for j in and_list:
           splitted = re.split(" & ",j)
           new = new + splitted
       dangerous_st = dangerous_st + new                          
       top = Counter(dangerous_st).most_common(3)
       top_three = []
       for sublist in top:
           top_three.append(sublist[0])
                
       
       final = json.dumps({'total_crime':total_crimes,'crime_type_count':crime_type,'event_time_count':event_time,'the_most_dangerous_streets':top_three})
       yield final
       
application = Application([CrimeAPIService],
    tns='spyne.examples.hello',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=JsonDocument() 
)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production. 
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()