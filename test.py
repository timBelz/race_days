from flask import Flask, render_template, jsonify
from influxdb_client import InfluxDBClient
import yaml

app = Flask(__name__)

# Load credentials

with open("credentials.yaml", "r") as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

influxdb_client = InfluxDBClient(url=credentials["influxdb"]["url"],
                                 token=credentials["influxdb"]["token"],
                                 org=credentials["influxdb"]["org"]
                                 )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def date():
    query = 'from(bucket: "{}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "herzfrequenz")'.format(credentials['influxdb']['bucket'])
    result = influxdb_client.query_api().query(org=credentials['influxdb']['org'], query=query)
    points = []
    for table in result:
        for record in table.records:
            points.append({"time": record.get_time(), "value": record.get_value()})
            
if __name__ == '__main__':
    app.run(debug=True)