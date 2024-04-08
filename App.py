import os
import logging
import streamlit as st
from dotenv import load_dotenv

from frontend.src.components.Header import AppHeader
from frontend.src.components.ModelDetails import Model_Details
from frontend.src.components.Card import Card
from src.ETLPipe import ETLPipeline

load_dotenv(".env")
  
def App(): 
    try:
        AppHeader(os.getenv("TITLE"))
        
        data = Model_Details()
        
        if data == 'NO MODEL & BUDGET' or data is None:
            st.write('Enter Model and Budget')
        elif data == 'NO MODEL':
            st.write('Enter Model')
        elif data == 'NO BUDGET':
            st.write('Enter Valid Budget')
        else:              
            smartphone_model = str(data['Smartphone Model']) + ' Smart Phones'
            budget = str(data['Budget'])
            
            AppHeader("ETL Pipeline")
            df = ETLPipeline().run(smartphone_model, budget)
            
            AppHeader('Results')
            for index, row in df.iterrows():
                Card(row.to_dict())
           
    except Exception as e:
        logging.error('An Error Occured: ', exc_info=e)
        raise e
        

if __name__ == "__main__":
    App()