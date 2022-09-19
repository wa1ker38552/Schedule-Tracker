from bs4 import BeautifulSoup
import requests


def schedule(id, cookie):
  headers = {'cookie': cookie}
  request = requests.get(f'https://mvla.aeries.net/student/Scheduling/GetClassScheduleView/{id}/20/MST/?_=1663262822420', headers=headers)
  soup = BeautifulSoup(request.text, 'html.parser')

  # manual scrape to find schedule
  classes = []
  tables = [item.get_text().replace('\n', '') for item in soup.find_all('tr')][4:]
  for i, item in enumerate(tables): 
    for j, char in enumerate(item.replace('\r', '').replace('\t', '').split('-')[1]):
      if char == str(i):
        classes.append(item.replace('\r', '').replace('\t', '').split('-')[1][:j].strip())
        break

  return classes[1:]
