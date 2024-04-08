import time
import logging
import streamlit as st

from src.scraper.Scraper import Scraper
from src.standardizer.Standardizer import Standardizer
from src.process.Processor import ProcessModel

logging.basicConfig(level=logging.INFO)

class ETLPipeline:
    
    def __init__(self):
        self.step_1 = None
        self.step_2 = None
        self.step_3 = None
        self.alert_1 = None
        self.alert_2 = None
        self.alert_3 = None

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
            self.step_1_header = st.header(f'1. Scraping {query} Data...')
            logging.info(f'Scraping {query} Data...')
            
            with st.spinner('Processing...'):
                raw_data = self.extract_data(query)
            self.alert_1 = st.success('Data Scraping Done!')
            time.sleep(5)
            
            self.step_2_header = st.header(f'2. Standardization {query} Data...')
            logging.info(f'Standardizing {query} Data...')
            
            with st.spinner('Processing...'):
                transformed_data = self.transform_data(raw_data)
            self.alert_2 = st.success('Data Standardize Done!')
            time.sleep(5)
            
            self.step_3_header = st.header(f'3. Filtering {query} Data...')
            logging.info(f'Filtering {query} Data...')
            
            with st.spinner('Processing...'):
                filtered_data = self.filter_data(transformed_data, price)
            self.alert_3 = st.success('Data Filter Done!')
            time.sleep(5)
            
            self.step_1_header.empty()
            self.alert_1.empty()
            self.step_2_header.empty()
            self.alert_2.empty()
            self.step_3_header.empty()
            self.alert_3.empty()
            
            return filtered_data
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e