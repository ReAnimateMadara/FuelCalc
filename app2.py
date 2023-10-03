# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 09:20:05 2023

@author: Hrishit
"""

from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

data = pd.read_csv('FDCA320neo.csv')

X = data[['Distance', 'Altitude', 'WeightTO']]
y = data['Total Fuel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

default_alt = 35000
default_TOWeight = 69968

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_fuel', methods=['POST'])
def calculate_fuel():
    distance = float(request.form['distance'])
    
    fuel_req = rf_model.predict([[distance,default_alt,default_TOWeight]])[0]
    
    return render_template('result.html', fuel_req=fuel_req)

if __name__ == '__main__':
    app.run(debug=True)