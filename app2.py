
from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

data = pd.read_csv('FDCA320neo.csv')

X = data[['Distance', 'Altitude', 'WeightTO', 'ZFW']]
y = data['Total Fuel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_fuel', methods=['POST'])
def calculate_fuel():
    distance = int(request.form['distance'])
    altitude = int (request.form['altitude'])
    ZFW = int(request.form['ZFW'])
    
    fuel_req = rf_model.predict([[distance,altitude, ZFW]])[0]
    
    return render_template('result.html', fuel_req=fuel_req)

if __name__ == '__main__':
    app.run(debug=True)