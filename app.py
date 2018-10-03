import collections
import xml.etree.ElementTree as etree

import requests
from flask import Flask, request
from flask import jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

xml_url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
response = requests.get(xml_url)
root = etree.fromstring(response.content)

exchange_rates = collections.defaultdict(dict)

for child in root.find('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
    for item in child:
        date = child.attrib['time']
        curr = item.attrib['currency']
        rate = item.attrib['rate']
        exchange_rates[date][curr] = float(rate)


@app.route('/')
def hello_world():
    return jsonify(exchange_rates)


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
