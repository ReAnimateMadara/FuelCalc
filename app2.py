import numpy.array as array
from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

data = pd.read_csv('FDCA320neo.csv')

X = data[['Distance', 'Altitude', 'ZFW']]               #ZFW is the Zero-Fuel Weight, as in the weight of the aircraft without any fuel on board
y = data['Total Fuel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_fuel', methods=['POST'])
def calculate_fuel():
    
    #A320neo uses Jet A-1 type fuel, the density is approx 0.8037 kg/L
    
    fuel_density = 0.8037
    
    distance = int(request.form['distance'])            #Distance is in nm -> Nautical Miles
    altitude = int (request.form['altitude'])           #Altitude is in ft -> Feet
    ZFW = int(request.form['ZFW'])                      #ZFW is in kg -> kilogram
    
    fuel_req = rf_model.predict([[distance,altitude, ZFW]])[0]
    fuel_volume = fuel_req / fuel_density
    
    #Current fuel price given in rupees per kilo litre, taken from https://iocl.com/aviation-fuel gives price for 4 main airline hubs of india: mumbai, delhi, chennai, kolkata
    fuel_mumbai = 110592.31
    fuel_delhi = 118199.17
    fuel_kolkata = 126697.08
    fuel_chennai = 122423.92
    
    fuel_prices = {
    'Mumbai': fuel_mumbai,
    'Delhi': fuel_delhi,
    'Kolkata': fuel_kolkata,
    'Chennai': fuel_chennai
    }
    
    fuel_cost = fuel_volume * array(list(fuel_prices.values()))

    # Format the fuel cost for each location
    formatted_fuel_costs = {place: f'{cost:.2f} Rupees' for place, cost in zip(fuel_prices.keys(), fuel_cost)}

    return render_template('result.html', fuel_req=fuel_req, fuel_volume=fuel_volume, fuel_cost=formatted_fuel_costs)

if __name__ == '__main__':
    app.run(debug=True)