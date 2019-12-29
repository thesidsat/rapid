from flask import Flask, render_template, request
import pandas as pd
from flaskwebgui import FlaskUI
import matplotlib.pyplot as plt
app = Flask(__name__)

#ui = FlaskUI(app)
@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/summary', methods = ['GET', 'POST'])
def summary():
   if request.method == 'POST':
      file = request.files['data']
      raw_data, summary, infer_data = data_preprocessing(file)
      data_visualisation(infer_data)
      return render_template("summary.html", raw_data = raw_data, summary = summary)
"""
TODO: handling missing values
"""	
def data_preprocessing(file):
      raw_data = pd.read_csv(file)
      percent_missing = raw_data.isnull().sum() * 100 / len(raw_data)
      infer_data = raw_data.apply(lambda col: pd.to_datetime(col, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
      summary_df = pd.DataFrame({'Percent Missing': percent_missing, 'Type': infer_data.dtypes})
      data_visualisation(raw_data)
      return raw_data.head(5), summary_df, infer_data
#TODO: Set limit for number of unique values
def data_visualisation(data):
   categorical_df = data.select_dtypes(include = [object])
   for column in categorical_df:
      if categorical_df[column].nunique() < 20:
         fig = plt.figure()
         categorical_df[column].value_counts().plot(kind='bar')
         fig.savefig(column+'.jpg')

   numerical_df = data.select_dtypes(include = [int,float])
   numerical_df = numerical_df.fillna(numerical_df.mean())
   for column in numerical_df:
      fig = plt.figure()
      print (numerical_df[column])
      numerical_df.plot(kind='bar')
      fig.savefig(column+'.jpg')

   return 

   
   
if __name__ == '__main__':
   app.run()