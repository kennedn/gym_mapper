#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import os
import glob
import yaml
from datetime import datetime
import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler
import re

plt.style.use('fivethirtyeight')

os.chdir("sessions")
pattern = ["*.txt"]
plot_name='progress.png'

def plot_progress(event):
  if os.path.exists(plot_name):
    timedelta = datetime.now() - datetime.fromtimestamp(os.stat(plot_name).st_mtime)
    if timedelta.microseconds < 200000:  # 200ms
      return

  exercises = {}
  plt.clf() # Clear plot
  for filename in [f for f in glob.glob(pattern[0]) if re.search("[a-zA-Z]{3} [0-9]{2}-[0-9]{2}-[0-9]{2}.txt", f)]:
      with open(os.path.join(os.getcwd(), filename), 'r') as f:
              exercises[datetime.strptime(filename.split(".")[0], '%a %d-%m-%y')] = yaml.safe_load(f.read())

  e = {}
  for y, v in sorted(exercises.items()):
    for k, x in exercises[y].items():
      if not e.get(k):
        e[k] = {}
      if not e[k].get('dates'):
        e[k]['dates'] = [y]
      else:
        e[k]['dates'].append(y)

      if not e[k].get('values'):
        e[k]['values'] = [x]
      else:
        e[k]['values'].append(x)

  
  for k, v in e.items():
    plt.plot_date(v['dates'], v['values'], ls='solid', label=k)

  date_fmt = dates.DateFormatter('%d-%m-%y')
  plt.gca().xaxis.set_major_formatter(date_fmt)
  plt.gcf().set_size_inches(12, 8)
  #plt.tick_params(axis='x', which='major', labelsize = 7)
   
  plt.ylabel('Weight')
  plt.xlabel('Date')
  plt.legend()
   
  plt.title('Gym Progress')
  plt.savefig(plot_name) 
  print("Change detected, recreated png")
  #plt.show()
  


event_handler = PatternMatchingEventHandler(pattern, None, True, True)
event_handler.on_any_event = plot_progress

observer = PollingObserver()
observer.schedule(event_handler, '.')
observer.start()
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  observer.stop()
observer.join()

  
  





    
  
    
