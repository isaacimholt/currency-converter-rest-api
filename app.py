import xml.etree.ElementTree as etree

import requests
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, inputs

app = Flask(__name__)
api = Api(app)


def get_exchange_rates(xml_url: str = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml') -> dict:
    rates = {}
    response = requests.get(xml_url)
    root = etree.fromstring(response.content)

    for child in root.find('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
        date = child.attrib['time']
        rates[date] = {}

        for item in child:
            curr = item.attrib['currency'].lower()
            rate = item.attrib['rate']
            rates[date][curr] = float(rate)

        # simplify conversion logic
        rates[date]['eur'] = 1.0

    return rates


# todo: use cache http://flask.pocoo.org/docs/1.0/patterns/caching/
exchange_rates = get_exchange_rates()

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('amount', type=float, required=True, case_sensitive=False,
                    help='The amount to convert (e.g. 12.35). Error: {error_msg}')
parser.add_argument('src_currency', type=str, required=True, case_sensitive=False,
                    help='ISO currency code for the source currency to convert (e.g. EUR, USD, GBP). Error: {error_msg}')
parser.add_argument('dest_currency', type=str, required=True, case_sensitive=False,
                    help='ISO currency code for the destination currency to convert (e.g. EUR, USD, GBP). Error: {error_msg}')
parser.add_argument('reference_date', type=inputs.date, required=True, case_sensitive=False,
                    help='Reference date for the exchange rate, in YYYY-MM-DD format. Error: {error_msg}')


@app.route('/')
def all_exchange_rates():
    return jsonify(exchange_rates)


class ExchangeRate(Resource):
    def get(self):

        args = parser.parse_args()
        reference_date = args['reference_date']
        reference_date = reference_date.strftime('%Y-%m-%d')
        src_currency = args['src_currency']
        dest_currency = args['dest_currency']
        amount = args['amount']

        currencies = exchange_rates.get(reference_date)
        if currencies is None:
            return {'message': {'reference_date': f'No exchange rates found for reference date {reference_date}'}}, 404

        src_rate = currencies.get(src_currency)
        if src_rate is None:
            return {'message': {'src_currency': f'No currency found for code {src_currency}'}}, 404

        dest_rate = currencies.get(dest_currency)
        if dest_rate is None:
            return {'message': {'dest_currency': f'No currency found for code {dest_rate}'}}, 404

        return {
            'amount':   amount / src_rate * dest_rate,
            'currency': dest_currency,
        }


# todo: fix route
api.add_resource(ExchangeRate, '/convert')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
