try:
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from flask import Flask, render_template, request
    import subprocess
    import sys
    import easygui
    
    required_libraries = ['pandas', 'scikit-learn', 'flask', 'easygui']

    missing_libraries = [lib for lib in required_libraries if lib not in sys.modules]

    if missing_libraries:
        for library in missing_libraries:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])


    class AircraftModel:
           
        def __init__(self, csv_filename, zfw_min, zfw_max, distance_min, distance_max, altitude_max, fuel_density):
            self.model = self.load_aircraft_data(csv_filename)
            self.zfw_min = zfw_min
            self.zfw_max = zfw_max
            self.distance_min = distance_min
            self.distance_max = distance_max
            self.altitude_max = altitude_max
            self.fuel_density = fuel_density

        def load_aircraft_data(self, csv_filename):
            data = pd.read_csv(csv_filename)
            X = data[['Distance', 'Altitude', 'ZFW']]
            Y = data['Total Fuel']
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.5, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            return model

        def calculate_fuel(self, distance, altitude, zfw):
            if (
                self.zfw_min <= zfw <= self.zfw_max
                and altitude <= self.altitude_max
                and self.distance_min <= distance <= self.distance_max
            ):
                fuel_req = self.model.predict([[distance, altitude, zfw]])[0]
                fuel_volume = int(fuel_req / self.fuel_density)
                return fuel_req, fuel_volume, None
            else:
                error_message = f'''
                ZFW cannot be below {self.zfw_min} kg or above {self.zfw_max} kg,
                Altitude should be below {self.altitude_max} ft,
                Distance should be between {self.distance_min} nm and {self.distance_max} nm
                '''
                return None, None, error_message

        def calculate_fuel_cost(self, fuel_volume, fuel_prices):
            return {place: f'{cost * fuel_volume / 1000:,.0f} Rupees' for place, cost in fuel_prices.items()}

    def create_app():
        app = Flask(__name__)
        
        fuel_prices = {                #This data is taken from https://iocl.com/aviation-fuel
        'Mumbai': 110.59231,
        'Delhi': 118.19917,
        'Kolkata': 126.69708,
        'Chennai': 122.42392
        }
     

        # Define aircraft models
        a320neo_model = AircraftModel('FDCA320neo.csv', 44220, 64300, 100, 1700, 39100, 0.8037)
        b738_model = AircraftModel('FDCB738.csv', 43111, 62731, 100, 2000, 41100, 0.8)
        a321neo_model = AircraftModel('FDCA321neo.csv', 49580, 75600, 99, 2001, 39100, 0.81)

        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/calculate_fuelA20N', methods=['POST'])
        def calculate_fuelA20N():
            distance = int(request.form['distance'])
            altitude = int(request.form['altitude'])
            zfw = int(request.form['ZFW'])
            fuel_req, fuel_volume, error_message = a320neo_model.calculate_fuel(distance, altitude, zfw)
            if error_message:
                return render_template('error.html', error_message=error_message)
            formatted_fuel_costs = {place: f'{cost * fuel_volume:.0f} Rupees' for place, cost in fuel_prices.items()}

            return render_template('result.html', fuel_req=fuel_req, fuel_volume=fuel_volume, fuel_cost=formatted_fuel_costs)

        @app.route('/calculate_fuelB738', methods=['POST'])
        def calculate_fuelB738():
            distance = int(request.form['distance'])
            altitude = int(request.form['altitude'])
            zfw = int(request.form['ZFW'])
            fuel_req, fuel_volume, error_message = b738_model.calculate_fuel(distance, altitude, zfw)
            if error_message:
                return render_template('error.html', error_message=error_message)
            formatted_fuel_costs = {place: f'{cost * fuel_volume:.0f} Rupees' for place, cost in fuel_prices.items()}

            return render_template('result.html', fuel_req=fuel_req, fuel_volume=fuel_volume, fuel_cost=formatted_fuel_costs)

        @app.route('/calculate_fuelA21N', methods=['POST'])
        def calculate_fuelA21N():
            distance = int(request.form['distance'])
            altitude = int(request.form['altitude'])
            zfw = int(request.form['ZFW'])
            fuel_req, fuel_volume, error_message = a321neo_model.calculate_fuel(distance, altitude, zfw)
            if error_message:
                return render_template('error.html', error_message=error_message)
            
            formatted_fuel_costs = {place: f'{cost * fuel_volume:.0f} Rupees' for place, cost in fuel_prices.items()}

            return render_template('result.html', fuel_req=fuel_req, fuel_volume=fuel_volume, fuel_cost=formatted_fuel_costs)

        return app

    if __name__ == '__main__':
        app = create_app()
        app.run(debug=True)
                
            
except ImportError as e:
    easygui.msgbox(f"Required libraries are missing: {str(e)}", "Library Check", "OK")
    exit(1)
