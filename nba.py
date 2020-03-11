from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def get_url(url):
  """
  Gets the content at url by making a HTTP GET request
  """

  try:
    with closing(get(url, stream=True)) as resp:
      if is_good_response(resp):
        return resp.content
      else:
        return None

  except RequestException as e:
    log_error('Error during request to {0} : {1}'.format(url, str(e)))
    return None

def is_good_response(resp):
  """
  Returns True if the response seems to be HTML, False otherwise
  """
  content_type = resp.headers['Content-Type'].lower()
  return (resp.status_code == 200
    and content_type is not None
    and content_type.find('html') > -1)

def log_error(e):
  """
  prints the error if it exists
  """
  print(e)

def get_tables():
  """
  Downloads and parses through html tables containing scoring and betting info
  """
  url = "https://www.oddsshark.com/nba/computer-picks"
  response = get_url(url)

  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    
    tables = html.select('table')
    game_tables = tables[:-1]
    
    
    for table in game_tables:
      for caption in table.select('caption'):
        away_team = caption.select('.table__name-short')[0].text
        home_team = caption.select('.table__name-short')[1].text
        print("{0} at {1}".format(away_team, home_team))
      for item in table.select('tbody > tr > td'):
        print(item.text)
        if table.select('tbody > tr > td').index(item) == 1:
          predictedScore = item.text.split()
          # print(predictedScore)
          away_team_score = float(predictedScore[0])
          home_team_score = float(predictedScore[2])
          print("Away Score: {0}".format(away_team_score))
          print("Home Score: {0}".format(home_team_score))
        
        

      print("=================")
      


get_tables()