import time
import os
import logging
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from frontend.src.Components.Header import AppHeader
from frontend.src.Components.ModelForm import Model_Form
from frontend.src.Components.Card import Card
from frontend.src.Utils import bootstrap_utils

# Loading Environment Variables
load_dotenv(".env")

# Loading Styling
bootstrap_utils()

class ETLPipe:
    def __init__(self) -> None:
        """
        Initializes the ETLPipe object with necessary attributes from environment variables
        and imports custom UI components.
        """
        self.title = os.getenv("TITLE")
        self.SERVER_URL = os.getenv("ETL_PIPE_API")
        self.AppHeader = AppHeader
        self.Model_Form = Model_Form
        self.Card = Card

    def ETL_UI(self) -> None:
        """
        ETL_UI Method:
        - Manages the UI flow of the ETL process.
        - Displays a header, collects input data (model and budget), and calls an API to get results.
        - If valid data is received, displays it using cards.
        """
        try:
            # Display the Main Header of the App
            self.AppHeader(self.title)
            
            # Extract the User Input for Smartphone Model and Budget
            data = self.Model_Form()

            # Handling Invalid or Missing Data Cases
            if data == 'NO MODEL & BUDGET' or data is None: 
                st.write('Enter Model and Budget')
            elif data == 'NO MODEL': 
                st.write('Enter Model')
            elif data == 'NO BUDGET': 
                st.write('Enter Valid Budget')
            else:
                # Extract Valid Smartphone Model and Budget from the User Input
                smartphone_model, budget = data['Smartphone Model'], data['Budget']
                
                try:
                    # Display Spinner while the App fetches Data from the API
                    with st.spinner('Getting your results ready...'):
                        # Send a POST request to the Server API with the Model and Budget
                        df = requests.post(self.SERVER_URL, json={"brand": smartphone_model, "price": budget}).json()
                        df = pd.DataFrame(df['response'])
                        
                        # Display Header for Results Section
                        self.AppHeader('Results')

                        # Display each result as a Card by Iterating through the Data
                        for index, row in df.iterrows():
                            self.Card(row.to_dict())
                
                # Handle Exceptions during the API Call or Data Processing
                except Exception:
                    # Display a Warning in the UI for the User and Log the Error
                    Error = st.warning("An Error Occured!")
                    time.sleep(5)
                    Error.empty()
                    
        # Handle any Unexpected Exceptions in the Main UI flow
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e

if __name__ == "__main__":
    
    # Instantiate the ETLPipe object and run the ETL_UI Method
    App = ETLPipe()
    App.ETL_UI()