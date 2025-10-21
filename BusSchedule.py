#BusSchedule.py
#Name: Grant Schaeffer
#Date: 10/21/25
#Assignment: Bus Stop

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#the sample page was used, per the email
stopNumber = 2269
routeNumber = 11
direction = "EAST"
bus_times = ["5:20AM", "5:50AM", "6:20AM", "6:50AM",
    "7:20AM", "7:50AM", "8:20AM", "8:50AM",
    "9:20AM", "9:50AM", "10:20AM", "10:50AM",
    "11:20AM", "11:50AM", "12:20PM", "12:50PM",
    "1:20PM", "1:50PM", "2:20PM", "2:50PM",
    "3:20PM", "3:50PM", "4:20PM", "4:50PM",
    "5:20PM", "5:50PM", "6:20PM", "6:50PM",
    "7:50PM", "8:50PM", "9:50PM"]

def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def to24Hour(time12):
  hours, minutes_half = time12.split(":")
  minutes = minutes_half[:2]
  half = minutes_half[2:].upper()
  hours = int(hours)
  if half == "AM":
    if hours == 12:
      hours = 0
  elif half == "PM":
    if hours != 12:
      hours += 12
  return f"{hours:02d}:{minutes}"

def theHour(time):
  #return the hour
  time24 = to24Hour(time)
  return int(time24.split(":")[0])

def theMinute(time):
  #return the minute
  return int(time.split(":")[1][:2])

def isLater(time1, time2):
  #compares two times
  h1, m1 = map(int, time1.split(":"))
  h2, m2 = map(int, time2.split(":"))
  return (h1, m1) > (h2, m2)

def convert(gmttime):
  #convert to central time
  hour = gmttime.hour - 6
  if hour < 0:
    hour += 24  # wrap around midnight
  return gmttime.replace(hour=hour)

def main():
  url = "https://myride.ometro.com/Schedule?stopCode=2269&routeNumber=11&directionName=EAST"
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page
  #print(c1)
  current_gmt = datetime.utcnow()
  current_central = convert(current_gmt)
  current_time = current_central.strftime("%H:%M")
  print("Current Time:", current_time)

  bus_times_24 = [to24Hour(t) for t in bus_times]

  next_bus = None
  for t in bus_times_24:
    if isLater(t, current_time):
      next_bus = t
      break
  print("Next Bus Arrival: ", next_bus)

if __name__ == "__main__":
  main()
