import numpy as np
from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

fuel_mumbai = 110592.31 / 1000
fuel_delhi = 118199.17 / 1000
fuel_kolkata = 126697.08 / 1000
fuel_chennai = 122423.92 / 1000

fuel_prices = {
'Mumbai': fuel_mumbai,
'Delhi': fuel_delhi,
'Kolkata': fuel_kolkata,
'Chennai': fuel_chennai
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_fuelA20N', methods=['POST'])
def calculate_fuelA20N():
    
    data = pd.read_csv('FDCA320neo.csv')

    X = data[['Distance', 'Altitude', 'ZFW']]               #ZFW is the Zero-Fuel Weight, as in the weight of the aircraft without any fuel on board
    y = data['Total Fuel']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    distance = int(request.form['distance'])            #Distance is in nm -> Nautical Miles
    altitude = int (request.form['altitude'])           #Altitude is in ft -> Feet
    ZFW = int(request.form['ZFW'])                      #ZFW is in kg -> kilogram
    
    try:
        if ((ZFW >= 44220 or ZFW <= 64300) or altitude <= 39100):
            if (distance >= 100 or distance <= 1700):
                
                #A320neo uses Jet A-1 type fuel, the density is approx 0.8037 kg/L
                
                fuel_density = 0.8037
                
                fuel_req = rf_model.predict([[distance,altitude, ZFW]])[0]
                fuel_req_formatted = '{:.0f}'.format(fuel_req)
                
                fuel_volume = fuel_req / fuel_density
                fuel_volume_formatted = '{:.0f}'.format(fuel_volume)
                
                #Current fuel price given in rupees per kilo litre, taken from https://iocl.com/aviation-fuel 
                #gives price for 4 main airline hubs of india: mumbai, delhi, chennai, kolkata
                
                fuel_cost = fuel_volume * np.array(list(fuel_prices.values()))

                # Format the fuel cost for each location
                formatted_fuel_costs = {place: f'{cost:,.0f} Rupees' for place, cost in zip(fuel_prices.keys(), fuel_cost)}

                return render_template('result.html', fuel_req=fuel_req_formatted, fuel_volume=fuel_volume_formatted, fuel_cost=formatted_fuel_costs)
            
        else:
                raise ValueError('''
                                 ZFW cannot be below 44220kg or above 64300, 
                                 Altitude should be below 39000ft, 
                                 Distance should be in between 100nm to 1700nm
                                 ''')
    
    except ValueError as e:                 #Common type of exception which can occur
        return render_template('error.html', error_message=str(e))
    except Exception as e:                  #Other types of exception which can occur
        return render_template('error.html', error_message=str(e))

@app.route('/calculate_fuelB738', methods=['POST'])
def calculate_fuelB738():
    
    data = pd.read_csv('FDCB738.csv')

    X = data[['Distance', 'Altitude', 'ZFW']]               #ZFW is the Zero-Fuel Weight, as in the weight of the aircraft without any fuel on board
    y = data['Total Fuel']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    distance = int(request.form['distance'])            #Distance is in nm -> Nautical Miles
    altitude = int (request.form['altitude'])           #Altitude is in ft -> Feet
    ZFW = int(request.form['ZFW'])                      #ZFW is in kg -> kilogram
    
    try:
        if ((ZFW < 43111 or ZFW > 62731) or altitude < 41100):
            if (distance >= 100 or distance <= 2000):
                
                fuel_density = 0.8
                
                fuel_req = rf_model.predict([[distance,altitude, ZFW]])[0]
                fuel_req_formatted = '{:.0f}'.format(fuel_req)
                
                fuel_volume = fuel_req / fuel_density
                fuel_volume_formatted = '{:.0f}'.format(fuel_volume)
                
                fuel_cost = fuel_volume * np.array(list(fuel_prices.values()))
                formatted_fuel_costs = {place: f'{cost:,.0f} Rupees' for place, cost in zip(fuel_prices.keys(), fuel_cost)}

                return render_template('result.html', fuel_req=fuel_req_formatted, fuel_volume=fuel_volume_formatted, fuel_cost=formatted_fuel_costs)
        
        else:
            raise ValueError('''
                             ZFW cannot be below 43111kg or greater than 62731kg, 
                             Cruising Altitude should be below 41100 feet, 
                             Distance should be in between 100 and 2000 nm only.
                             ''')
    except ValueError as e:
        return render_template('error.html', error_message=str(e))
    except Exception as e:
        return render_template('error.html', error_message=str(e))
    
@app.route("/calculate_fuelA21N", methods=['POST'])
def calculate_fuelA21N():
    data = pd.read_csv('FDCA321neo.csv')

    X = data[['Distance', 'Altitude', 'ZFW']]               #ZFW is the Zero-Fuel Weight, as in the weight of the aircraft without any fuel on board
    y = data['Total Fuel']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    distance = int(request.form['distance'])            #Distance is in nm -> Nautical Miles
    altitude = int (request.form['altitude'])           #Altitude is in ft -> Feet
    ZFW = int(request.form['ZFW'])                      #ZFW is in kg -> kilogram
    
    try:
        if((ZFW > 49580 or ZFW < 75600) or altitude < 39100):
            if (distance >= 99 or distance <= 2001):
                
                fuel_density = 0.81
                
                fuel_req = rf_model.predict([[distance,altitude, ZFW]])[0]
                fuel_req_formatted = '{:.0f}'.format(fuel_req)
                
                fuel_volume = fuel_req / fuel_density
                fuel_volume_formatted = '{:.0f}'.format(fuel_volume)
                
                fuel_cost = fuel_volume * np.array(list(fuel_prices.values()))
                formatted_fuel_costs = {place: f'{cost:,.0f} Rupees' for place, cost in zip(fuel_prices.keys(), fuel_cost)}

                return render_template('result.html', fuel_req=fuel_req_formatted, fuel_volume=fuel_volume_formatted, fuel_cost=formatted_fuel_costs)
        
        else:
            raise ValueError('''
                             ZFW cannot be below 49580 or greater than 62731kg, 
                             Cruising Altitude should be below 39100 feet, 
                             Distance should be in between 100 and 2000 nm only.
                             ''')
    except ValueError as e:
        return render_template('error.html', error_message=str(e))
    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)