import gpsd

# Connect to the local gpsd
gpsd.connect()

def get_location():
  # Get gps position
  packet = gpsd.get_current()
  
  try:
    lat, lon = packet.position()
    return lat, lon
  except gpsd.NoFixError:
    return -999.99, -999.99
  
# See the inline docs for GpsResponse for the available data
a,b = get_location
print(a)
print(b)
