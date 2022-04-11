import sched, time
from pymongo import MongoClient
import gpsd

# setup for database
client = MongoClient("mongodb+srv://Senior:Senior2022@cluster0.o1ezz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["Data"]
collection = db["GPS"]

# setup for scheduler
s = sched.scheduler(time.time, time.sleep)

# setup for GPS
gpsd.connect()

def get_location():
  # Get gps position
  packet = gpsd.get_current()
  
  try:
    lat, lon = packet.position()
    return lat, lon
  except gpsd.NoFixError:
    return -999.99, -999.99

def data_format():
    # grab latest time every callback
    hour = time.strftime("%I_%M_%S", time.localtime())
    date = time.strftime("%m_%d", time.localtime())

    if (date[0] == '0'):
        date = date[1:]

     a,b = get_location()
        
    # gps data schema
    gpsdata= {
        "date": date,
        "hour": hour,
        "lat": a,
        "lon": b
    }

    # updates data with the latest values
    update = {'$push': gpsdata}
    return update

def data_upload(sc): 
    collection.update_one({}, data_format(), upsert=True) #create if dne
    
    # setup for time
    seconds = time.time()
    local_time = time.ctime(seconds)
    a,b = get_location()

    # console log to show updates
    print("\nGPS DATA UPDATED AT: {0}".format(local_time))
    print("Latitude: {0} C".format(a))
    print("Longitude: {0} %%".format(b))
    # repeat every 5 seconds
    s.enter(5, 2, data_upload, (s,))

# initiates data being sent to database
def run_data_upload():
    # start loop for intervaled data insertion
    s.enter(0, 1, data_upload, (s,))
    s.run()

run_data_upload()
