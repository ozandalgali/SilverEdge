from flask import Flask, Response
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_csv('output.csv')
        return Response(df.to_json(orient='values'), mimetype='application/json')
    except Exception as e:
        return str(e), 500

@app.route('/outliers', methods=['GET'])
def get_outliers():
    try:
        df = pd.read_csv('outliers.csv')
        return Response(df.to_json(orient='values'), mimetype='application/json')
    except Exception as e:
        return str(e), 5003

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)