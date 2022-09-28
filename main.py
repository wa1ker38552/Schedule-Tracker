from assignments import get_assignments
from flask import render_template
from flask import make_response
from schedule import schedule
from flask import redirect
from flask import request
from pytz import timezone
from flask import Flask
from replit import db
import datetime
import pytz
import json


# fetch json data about schedule from schedule.json
schedule_data = json.load(open('schedule.json', 'r'))

def get_schedule(s):
  bell = {
    'monday': [s[0], 'Passing Period', s[1], 'Brunch', 'Passing Period', s[2], 'Passing Period', s[3], 'Lunch', 'Passing Period', s[4], 'Passing Period', s[5], 'Passing Period', s[6]],
    'tuesday': [s[0], 'Brunch', 'Passing Period', s[2], 'Lunch', 'Passing Period', s[4], 'Passing Period', s[6]],
    'wednesday': [s[1], 'ACT', 'Brunch', 'Passing Period', s[3], 'Lunch', 'Passing Period', s[5]],
    'thursday': [s[0], 'Brunch', 'Passing Period', s[2], 'Lunch', 'Passing Period', s[4], 'Passing Period', s[6]],
    'friday': [s[1], 'ACT', 'Brunch', 'Passing Period', s[3], 'Lunch', 'Passing Period', s[5]]
    }
  
  # get current day of the week
  day = datetime.datetime.today().astimezone(timezone('US/Pacific')).strftime('%A').lower()
  
  try:
    date = schedule_data[day]
  except KeyError:
    # saturday or sunday
    return ["School hasn't started yet!", '00', '00', '00']
  
  # format current time in 24 hour clock format
  now = datetime.datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).strftime('%H:%M:%S')
  # convert into datetime.time
  now = datetime.time(int(now.split(':')[0]), int(now.split(':')[1]), int(now.split(':')[2]))
  # force time for debug
  # now = datetime.time(9, 26, 30)

  for i, class_time in enumerate(date):
    for t in class_time: 
      # create datetime.time object
      period_start = datetime.time(int(t.split(':')[0]), int(t.split(':')[1]), 0)
      period_end   = datetime.time(int(class_time[t].split(':')[0]), int(class_time[t].split(':')[1]), 0)
  
      # check time range
    if period_start <= now <= period_end:
      # set a variable to catch NameError 
      current_period = i
      break
    
  # current class
  try:
    current_class = bell[day][current_period]
      
    # calculate time until next class
    time_now   = datetime.datetime.combine(datetime.date.today(), now)
    period_end = datetime.datetime.combine(datetime.date.today(), period_end)
    
    # get total time in seconds
    total_diff = (period_end-time_now).total_seconds()
    formatted_difference = str(datetime.timedelta(seconds=total_diff))
    
    data = formatted_difference.split(':')
    data.insert(0, current_class)

    if current_period == len(bell[day])-1:
      data.append('School ends')
    else:
      # don't show passingp period as next class
      if bell[day][current_period+1] == 'Passing Period':
        data.append(bell[day][current_period+2])
      else:
        data.append(bell[day][current_period+1])
    
    # format for 0's in front
    if len(data[1]) == 1: data[1] = f'0{data[1]}'
    if len(data[2]) == 1: data[2] = f'0{data[2]}'
    if len(data[3]) == 1: data[3] = f'0{data[3]}'

    return data
  except NameError:
    return ["There is no school right now!", '00', '00', '00', None]
  

# default schedule for no tokens
default = ['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7']

app = Flask(__name__)

@app.route('/')
def home():
  # homepage, rarely used except on-connection
  try:
    data = get_schedule(db['tokens'][str(request.cookies.get('token'))])
  except KeyError: 
    data = get_schedule(default)
  return render_template('index.html', data=data)

@app.route('/settings')
def settings():
  return render_template('settings.html')

@app.route('/metadata')
def metadata():
  try:
    data = get_schedule(db['tokens'][str(request.cookies.get('token'))])
  except KeyError: 
    data = get_schedule(default)

  time = ':'.join(data[1:4])
  for i in range(3): data.pop(1)
  data.insert(1, time)
  return data

@app.route('/setcookie', methods=['POST'])
def setcookie():
  # creates a token cookie with your aeries_token
  # aeries tokens expie after 1 hour so any information saved is obsolete
  # values for database is your schedule
  aeries_token = request.form['token']
  user_id = request.form['id']

  try:
    data = get_schedule(schedule(user_id, aeries_token))
    
    # save to database {'aeries token': [schedule]}
    # needs to save aeries_token to database to ensure that website cookies match
    db['tokens'][str(aeries_token)] = schedule(user_id, aeries_token)
  except:
    # invalid token passed, set to default
    db['tokens'][str(aeries_token)] = default

  # create cookies
  response = make_response(redirect('/', code=302))
  response.set_cookie('token', aeries_token)

  return response

@app.route('/getcookie', methods=['POST', 'GET'])
def getcookie():
  try:
    return list(db['tokens'][str(request.cookies.get('token'))])
  except KeyError: return 'Your cookie has not been saved to the database, login again to save it.'

@app.route('/set_theme', methods=['POST'])
def set_theme():
  response = make_response(redirect('/', code=302))
  response.set_cookie("theme", request.form['theme'])

  return response

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


# db['tokens'] = {}
app.run(host='0.0.0.0', port=8080)
