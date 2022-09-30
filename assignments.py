from datetime import datetime
from pytz import timezone  
import requests

def get_assignments(cookie):
  headers = {'cookie': cookie}
  # get date
  today = datetime.today().astimezone(timezone('US/Pacific')).strftime("%Y-%m-%d")
  request = requests.get(f'https://mvla.instructure.com/api/v1/planner/items?start_date={today}T07%3A00%3A00.000', headers=headers)

  assignments = []
  for i, assignment in enumerate(request.json()):
    print(assignment)
    assignments.append({
      'title': assignment['plannable']['title'],
      'link': assignment['html_url']
    })
    try:
      assignments[i]['due'] = assignment['plannable']['due_at'].split('T')[0]
    except KeyError: assignments[i]['due'] = None
    except AttributeError: assignments[i]['due'] = None

  return assignments
