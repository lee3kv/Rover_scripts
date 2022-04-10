import sched, time, board
from pymongo import MongoClient
from adafruit_bme280 import basic 

# setup for database
client = MongoClient("mongodb+srv://Senior:Senior2022@cluster0.o1ezz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["Data"]
collection = db["BME"]

# setup for scheduler
s = sched.scheduler(time.time, time.sleep)

# setup for bme280
i2c = board.I2C()
bme280 = basic.Adafruit_BME280_I2C(i2c)
# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

def data_format():
    # grab latest time every callback
    hour = time.strftime("%I_%M_%S", time.localtime())
    date = time.strftime("%m_%d", time.localtime())

    if (date[0] == '0'):
        date = date[1:]

    # bme data schema
    bme280data = {
        "date": date,
        "hour": hour,
        "temp": "{:.2f}".format(bme280.temperature), 
        "humidity": "{:.2f}".format(bme280.relative_humidity), 
        "pressure": "{:.2f}".format(bme280.pressure),
        "altitude": "{:.2f}".format(bme280.altitude),
    }

    # updates data with the latest values
    update = {'$push': bme280data}
    return update

def data_upload(sc): 
    collection.update_one({}, data_format(), upsert=True) #create if dne
    
    # setup for time
    seconds = time.time()
    local_time = time.ctime(seconds)

    # console log to show updates
    print("\nBME DATA UPDATED AT: {0}".format(local_time))
    print("Temperature: {0} C".format(bme280.temperature))
    print("Humidity: {0} %%".format(bme280.relative_humidity))
    print("Pressure: {0} hPa".format(bme280.pressure))
    print("Altitude: {0} meters".format(bme280.altitude))
    # repeat every 10 seconds
    s.enter(5, 2, data_upload, (s,))

# initiates data being sent to database
def run_data_upload():
    # start loop for intervaled data insertion
    s.enter(0, 1, data_upload, (s,))
    s.run()

run_data_upload()