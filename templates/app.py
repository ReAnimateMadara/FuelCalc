from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

fuel_data = pd.read_csv('FDCA320neo.csv')

X = fuel_data[['Distance','Altitude', 'WeightTO']]
y = fuel_data['Total Fuel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form.get('user_input')

def randomforest_plot_gen(X_test, y_test):
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(X_test['Distance'], y_test, alpha=0.5, label='Actual Total Fuel')
    plt.scatter(X_test['Distance'], y_pred, alpha=0.5, label='Predicted Total Fuel')
    plt.xlabel('Distance')
    plt.ylabel('Total Fuel')
    plt.title('Actual vs. Predicted Total Fuel vs. Distance')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.scatter(X_test['Distance'], y_test, alpha=0.5, label='Actual Total Fuel')
    plt.xlabel('Distance')
    plt.ylabel('Total Fuel')
    plt.title('Actual Total Fuel vs. Distance')
    plt.legend()
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return plot_base64
