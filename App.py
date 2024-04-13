import os
import time
import logging
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from frontend.src.Components.Header import AppHeader
from frontend.src.Components.ModelForm import Model_Form
from frontend.src.Components.Card import Card

load_dotenv(".env")

class ETLPipe:
    
    def __init__(self):
        self.title = os.getenv("TITLE")
        self.ERROR_MESSAGE = os.getenv("ERROR_MESSAGE")
        self.SERVER_URL = os.getenv("ETL_PIPE_API")
        self.AppHeader = AppHeader
        self.Model_Form = Model_Form
        self.Card = Card
        
    def ETL_UI(self):
        try:
            self.AppHeader(self.title)
            
            data = self.Model_Form()
            if data == 'NO MODEL & BUDGET' or data is None: st.write('Enter Model and Budget')
            elif data == 'NO MODEL': st.write('Enter Model')
            elif data == 'NO BUDGET': st.write('Enter Valid Budget')
            else:
                smartphone_model, budget = data['Smartphone Model'], data['Budget']
                
                try:
                    with st.spinner('Getting your results ready...'):
                         df = requests.post(self.SERVER_URL, json={"brand": smartphone_model, "price": budget}).json()
                         df = pd.DataFrame(df['response'])
                 
                         self.AppHeader('Results')
                         for index, row in df.iterrows():
                             Card(row.to_dict())
                except:
                    Error = st.warning(self.ERROR_MESSAGE); time.sleep(5); Error.empty()
                    
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

if __name__ == "__main__":
    
    App = ETLPipe()
    App.ETL_UI()