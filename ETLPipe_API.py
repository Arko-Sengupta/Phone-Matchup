import  os
import json
import logging
from dotenv import load_dotenv
from flask import Blueprint, Flask, jsonify, request

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

from backend.Scraper.Scraper import Scraper
from backend.Processor.Processor import Processor
from backend.Standardizer.Standardizer import Standardizer

load_dotenv(".env")

class ETLPipeline:
    
    def __init__(self):
        self.limit = os.getenv("TEST")
        with open('Scraper_Parameters.json') as f:
            self.data = json.load(f)
        self.raw_data = Scraper(self.limit, self.data)
        self.transformed_data = Standardizer()
        self.filtered_data = Processor()

    def extract_data(self, query):
        try:
            return self.raw_data.run(query)
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def transform_data(self, raw_data):
        try:
            return self.transformed_data.run(raw_data)
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def filter_data(self, transformed_data, price):
        try:
            return self.filtered_data.run(transformed_data, price)
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def run(self, brand, price):
        try:
            raw_data = self.extract_data(brand)
            transformed_data = self.transform_data(raw_data)
            filtered_data = self.filter_data(transformed_data, price)
            
            return filtered_data
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e

class ETLPipe_API:

    def __init__(self):
        self.app = Flask(__name__)
        self.ETLPile_blueprint = Blueprint('etl_pipeline', __name__)
        self.ETLPile_blueprint.add_url_rule('/', 'SERVER_STARTED', self.SERVER_STARTED, methods=['GET'])
        self.ETLPile_blueprint.add_url_rule('/ETLPipe', 'ETLPipe', self.ETLPipe, methods=['POST'])
        self.ETLPile = ETLPipeline()
        
    def SERVER_STARTED(self):
        try:
            return jsonify({'response': 200, 'SERVER STARTED': True}), 200
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

    def ETLPipe(self):
        try:
            data = request.get_json()
            brand, price = data['brand'], data['price']
            
            response = self.ETLPile.run(brand, price)
            return jsonify({'response': response.to_dict()}), 200
        except Exception as e:
            logging.error('An Error Occurred: ', exc_info=e)
            return jsonify({'Error': str(e)}), 400
        
    def run(self):
        try:
            self.app.register_blueprint(self.ETLPile_blueprint)
            self.app.run(debug=True)
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

if __name__=='__main__':
      
    server = ETLPipe_API()
    server.run()