import logging

from src.scraper.Scraper import Scraper
from src.standardizer.Standardizer import Standardizer
from src.process.Processor import ProcessModel

logging.basicConfig(level=logging.INFO)

class ETLPipeline:
    
    def __init__(self):
        pass

    def extract_data(self, query):
        try:
            raw_data = Scraper()
            raw_data = raw_data.run(query)
            
            return raw_data
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def transform_data(self, raw_data):
        try:
            transformed_data = Standardizer()
            transformed_data = transformed_data.run(raw_data)
            
            return transformed_data
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def filter_data(self, transformed_data, price):
        try:
            filtered_data = ProcessModel()
            filtered_data = filtered_data.run(transformed_data, price)
            
            return filtered_data
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def run(self, query, price):
        try:
            logging.info(f'Scraping {query} Data...')
            raw_data = self.extract_data(query)
            
            logging.info(f'Standardizing {query} Data...')
            transformed_data = self.transform_data(raw_data)
            
            logging.info(f'Filtering {query} Data...')
            filtered_data = self.filter_data(transformed_data, price)
            
            return filtered_data
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e