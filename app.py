import xml.etree.ElementTree as etree

import requests
from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# todo: use cache http://flask.pocoo.org/docs/1.0/patterns/caching/
exchange_rates = {}

# todo: put this into xml_url -> dict function
xml_url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
response = requests.get(xml_url)
root = etree.fromstring(response.content)

for child in root.find('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
    date = child.attrib['time']
    exchange_rates[date] = {}
    for item in child:
        curr = item.attrib['currency']
        rate = item.attrib['rate']
        exchange_rates[date][curr] = float(rate)
    exchange_rates[date]['EUR'] = 1.0  # simplify conversion logic


@app.route('/')
def all_exchange_rates():
    return jsonify(exchange_rates)


class ExchangeRate(Resource):
    def get(self, amount: float, src_currency: str, dest_currency: str, reference_date: str):

        currencies = exchange_rates.get(reference_date)
        if currencies is None:
            return {'error': f'No exchange rates found for reference date {reference_date}'}

        src_rate = currencies.get(src_currency)
        if src_rate is None:
            return {'error': f'No currency found for code {src_currency}'}

        dest_rate = currencies.get(dest_currency)
        if dest_rate is None:
            return {'error': f'No currency found for code {dest_rate}'}

        return {
            'amount':   amount / src_rate * dest_rate,
            'currency': dest_currency,
        }


# todo: fix route
api.add_resource(ExchangeRate, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
