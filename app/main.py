from flask import Flask, render_template, request, Response
import json
from .valApi import ValorantAPI

app = Flask(__name__)

match_movement_hash = {
  'INCREASE': 'Increase',
  'MINOR_INCREASE': 'Increase',
  'MAJOR_INCREASE': 'Increase',
  'DECREASE': 'Decrease',
  'MAJOR_DECREASE': 'Decrease',
  'MINOR_DECREASE': 'Decrease',
  'PROMOTED': 'Promoted',
  'DEMOTED': 'Demoted'
}

@app.route('/')
def home():
  return render_template('login.html')
  # return '<h1>Hello World<h1>'

#   return Response(json_res, mimetype="application/json")

@app.route('/match_history', methods=['POST'])
def display_match_history():
  try:
    username = request.form['username']
    password = request.form['password']

    valorant = ValorantAPI(username, password)
    print('hello world')

    json_res = valorant.get_match_history()

    posts = []
    for match in json_res['Matches']:
      # print(match)
      if match['CompetitiveMovement'] == 'MOVEMENT_UNKNOWN':
        continue
      game_outcome = 'Victory' if 'INCREASE' in match['CompetitiveMovement'] or 'PROMOTED' in match['CompetitiveMovement'] else 'Defeat'
      lp_change = ''
      
      before = match['TierProgressBeforeUpdate']
      after = match['TierProgressAfterUpdate']

      if match['CompetitiveMovement'] == 'PROMOTED':
        lp_change = '+' + str(after + 100 - before)
        match_data = {
          'lp_change': lp_change,
          'current_lp': after,
          'game_outcome': game_outcome,
          'movement': match_movement_hash[match['CompetitiveMovement']],
          'status': 'win'
        }
      elif match['CompetitiveMovement'] == 'DEMOTED':
        lp_change = '-' + str(before + 100 - after)
        match_data = {
          'lp_change': lp_change,
          'current_lp': after,
          'game_outcome': game_outcome,
          'movement': match_movement_hash[match['CompetitiveMovement']],
          'status': 'loss'
        }
      else:
        if before < after:
          # won
          lp_change = '+' + str(after - before)
          status = 'win'
        else:
          # lost
          lp_change = str(after - before)
          status = 'loss'

        match_data = {
          'lp_change': lp_change,
          'current_lp': after,
          'game_outcome': game_outcome,
          'movement': match_movement_hash[match['CompetitiveMovement']],
          'status': status        
        }
      posts.append(match_data)
    # print(posts)
    return render_template('match_history.html', posts=posts)
  except:
    return render_template('error.html')