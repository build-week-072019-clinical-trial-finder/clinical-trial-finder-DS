from flask import Flask, request, render_template, Blueprint
from flask_json import FlaskJSON, JsonError, json_response
import os
import requests
from flask_cors import CORS
import json

#Local Imports
from data.dataFrameLoader import df
from dfParser import *
from indexHelper import *

application = app = Flask(__name__)
FlaskJSON(app)
cors = CORS(app)

@app.route('/')
def root():
    """
    Testing
    """
    return "Test Successful"

@app.route('/fetch_search', methods=['POST'])
def fetch_data():
  """
  API route that receives search query and returns clinical trials that match search
  """
  data = request.get_json(force=True)

  user_search = data['user_search']
  page = data['page']
  gender = data['gender']
  age = data['age']
  country = data['country']

  country_df = country_parse(df, country)
  sorted_df = score_docs(search_freq(tokenizer(user_search), country_df), country_df)
  gendered_df = gender_parse(sorted_df, gender)
  final_df = age_parse(gendered_df, age)

  total_results = len(final_df)

  start_ind, end_ind = paginate(page)

  page = final_df[start_ind:end_ind]  

  return json_response(total_results = total_results, results=page.to_json(orient='records'))

@app.route('/fetch_result', methods=['POST'])
def fetch_result():
  """
  Returns specified result based upon a studies ID
  """
  data = request.get_json(force=True)

  trial_id = data['trial_id']

  spec_trial = df.loc[df.index == trial_id]

  return spec_trial.to_json(orient='records')


if __name__ == '__main__':
    application.run()
