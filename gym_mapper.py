#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import os
import sys
import glob
import yaml
from datetime import datetime
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import re


#os.chdir("sessions")
os.chdir(f"{os.path.dirname(os.path.realpath(sys.argv[0]))}/sessions")
pattern = ["*.txt"]
plot_name='progress.png'
pb_name='PB.txt'

def plot_progress(event):
  if os.path.exists(plot_name):
    timedelta = datetime.now() - datetime.fromtimestamp(os.stat(plot_name).st_mtime)
    if timedelta.seconds < 3:
      return

  exercises = {}
  plt.clf() # Clear plot
  for filename in [f for f in glob.glob(pattern[0]) if re.search("[a-zA-Z]{3} [0-9]{2}-[0-9]{2}-[0-9]{2}.txt", f)]:
      with open(os.path.join(os.getcwd(), filename), 'r') as f:
        try:
          exercises[datetime.strptime(filename.split(".")[0], '%a %d-%m-%y')] = yaml.safe_load(f.read())
        except:
            pass

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

  with open(pb_name, 'w') as f: 
      for k, v in e.items():
        f.write(f"{k}: {max(v['values']) if k != 'waist' else min(v['values'])}\n")
        plt.plot_date(v['dates'], v['values'], ls='solid', label=k)

  plt.style.use('fivethirtyeight')
  date_fmt = dates.DateFormatter('%d-%m-%y')
  plt.gca().xaxis.set_major_formatter(date_fmt)
  plt.gcf().set_size_inches(12, 8)
  #plt.tick_params(axis='x', which='major', labelsize = 7)
  
  plt.ylabel('Weight (KG)')
  plt.xlabel('Date')
  
  plt.title('Gym Progress')
  plt.legend()
  plt.savefig(plot_name) 
  print("Change detected, recreated png")
  #plt.show()
  


event_handler = PatternMatchingEventHandler(pattern, None, True, True)
event_handler.on_any_event = plot_progress

observer = Observer()
observer.schedule(event_handler, '.')
observer.start()
print("Starting..")
observer.join()
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  observer.stop()

  
  





    
  
    
