from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pprint
import csv

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
  url = "https://www.oddsshark.com/ncaab/computer-picks"
  response = get_url(url)

  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    
    tables = html.select('table')
    game_tables = tables[:-1]

    game_info = []
    
    
    for table in game_tables:
      game_dict = {}
      
      for caption in table.select('caption'):
        away_team = caption.select('.table__name-short')[0].text
        game_dict['Away Team'] = away_team
        home_team = caption.select('.table__name-short')[1].text
        game_dict['Home Team'] = home_team
      
      for item in table.select('tbody > tr > td'):
        # print(item.text)
        # print(table.select('tbody > tr > td').index(item))
        
        if table.select('tbody > tr > td').index(item) == 1:
          predictedScore = item.text.split()
          away_team_score = float(predictedScore[0])
          game_dict['Away Score'] = away_team_score
          home_team_score = float(predictedScore[2])
          game_dict['Home Score'] = home_team_score
          total_score = away_team_score + home_team_score
          game_dict['Total Score'] = total_score
          

        if table.select('tbody > tr > td').index(item) == 4:
          computer_spread_pick = item.text
          game_dict['Computer Spread Pick'] = computer_spread_pick
        
        if table.select('tbody > tr > td').index(item) == 5:
          computer_OU_pick = item.text
          game_dict['Computer O/U Pick'] = computer_OU_pick

        if item.text == "Public Consensus":

          for row in item.next_siblings:
            if len(row.text.split()) == 0:
              continue
            
            if row.text.split()[0] == away_team or row.text.split()[0] == home_team:
              print(row.text)
              public_spread_pick = row.text
              game_dict['Public Spread Pick'] = public_spread_pick

            if row.text.split()[0] == 'Over' or row.text.split()[0] == 'Under' or row.text.split()[0] == '':
              print(row.text)
              public_OU_pick = row.text
              game_dict['Public O/U Pick'] = public_OU_pick
        
        if table.select('tbody > tr > td').index(item) == 10:
          public_spread_percent = item.text
          game_dict['Consensus Spread %'] = public_spread_percent
          

        if table.select('tbody > tr > td').index(item) == 11:
          public_OU_percent = item.text
          game_dict['Consensus O/U %'] = public_OU_percent
          

      game_info.append(game_dict)
      print("=================")
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
    # pp.pprint(game_info)

  csv_columns = ['Away Team', 'Home Team', 'Away Score', 'Home Score', 'Total Score', 'Computer Spread Pick', 'Computer O/U Pick', 'Public Spread Pick', 'Public O/U Pick', 'Consensus Spread %', 'Consensus O/U %']

  csv_file = "NCAABets.csv"
  try:
    with open(csv_file, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
      writer.writeheader()
      for data in game_info:
        writer.writerow(data)
  except IOError:
    print("I/O error")
      
get_tables()