from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)

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
        
      
      for item in table.select('tbody > tr > td'):
        
        if table.select('tbody > tr > td').index(item) == 1:
          predictedScore = item.text.split()
          away_team_score = float(predictedScore[0])
          home_team_score = float(predictedScore[2])
          total_score = away_team_score + home_team_score
          

        if table.select('tbody > tr > td').index(item) == 4:
          computer_spread_pick = item.text
        
        if table.select('tbody > tr > td').index(item) == 5:
          computer_OU_pick = item.text

        if item.text == "Public Consensus":

          for row in item.next_siblings:
            
            if row.text.split()[0] == away_team or row.text.split()[0] == home_team:
              public_spread_pick = row.text

            if row.text.split()[0] == 'Over' or row.text.split()[0] == 'Under':
              public_OU_pick = row.text
        
        if table.select('tbody > tr > td').index(item) == 10:
          public_spread_percent = item.text
          

        if table.select('tbody > tr > td').index(item) == 11:
          public_OU_percent = item.text
          

      game_dict = {
        'away_team': away_team,
        'home_team': home_team,
        'predicted_away_score': away_team_score,
        'predicted_home_score': home_team_score,
        'total_score': total_score,
        'comp_spread_pick': computer_spread_pick,
        'comp_ou_pick': computer_OU_pick,
        'public_spread_pick': public_spread_pick,
        'public_ou_pick': public_OU_pick,
        'public_consensus_spread_%': public_spread_percent,
        'public_consensus_ou_%': public_OU_percent
      }

      game_info.append(game_dict)
      # print("=================")
      # print("{0} at {1}".format(away_team, home_team))
      # print("Predicted Away Score: {0}".format(away_team_score))
      # print("Predicted Home Score: {0}".format(home_team_score))
      # print("Predicted Total Score: {0}".format(total_score))
      # print("Computer Spread Pick: {0}".format(computer_spread_pick))
      # print("Computer Over Under Pick: {0}".format(computer_OU_pick))
      # print("Public Spread Pick: {0}".format(public_spread_pick))
      # print("Public O/U Pick: {0}".format(public_OU_pick))
      # print("Consensus Spread %: {0}".format(public_spread_percent))
      # print("Consensus O/U %: {0}".format(public_OU_percent))
  pp.pprint(game_info)
      
  

get_tables()