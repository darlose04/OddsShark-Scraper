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

    game_info = []
    
    
    for table in game_tables:
      
      for caption in table.select('caption'):
        away_team = caption.select('.table__name-short')[0].text
        home_team = caption.select('.table__name-short')[1].text
        # print("{0} at {1}".format(away_team, home_team))
      
      for item in table.select('tbody > tr > td'):
        print(item.text)
        
        
        if table.select('tbody > tr > td').index(item) == 1:
          predictedScore = item.text.split()
          # print(predictedScore)
          away_team_score = float(predictedScore[0])
          home_team_score = float(predictedScore[2])
          total_score = away_team_score + home_team_score
          # print("Total Score: {0}".format(total_score))
          # print("Away Score: {0}".format(away_team_score))
          # print("Home Score: {0}".format(home_team_score))

        if table.select('tbody > tr > td').index(item) == 4:
          computer_spread_pick = item.text
          # print("Computer Spread Pick: {0}".format(computer_spread_pick))
        
        if table.select('tbody > tr > td').index(item) == 5:
          computer_OU_pick = item.text
          # print("Computer Over Under Pick: {0}".format(computer_OU_pick))

        if item.text == "Public Consensus":

          for row in item.next_siblings:
            # print(row.text.split()[1])
            if row.text.split()[0] == away_team or row.text.split()[0] == home_team:
              public_spread_pick = row.text
              print("Public Spread Pick: {0}".format(public_spread_pick))
             
            
          
          
            
        
        
        # if table.select('tbody > tr > td').index(item) == 7:
        #   public_spread_pick = item.text
        #   # print("Public Spread: {0}".format(public_spread_pick))

        # if table.select('tbody > tr > td').index(item) == 8:
        #   public_OU_pick = item.text
        #   # print("Public O/U Pick: {0}".format(public_OU_pick))


      print("=================")
      


get_tables()