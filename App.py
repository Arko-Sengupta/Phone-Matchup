import time
import logging
import streamlit as st

from frontend.src.components.Header import AppHeader
from frontend.src.components.ModelDetails import Model_Details

from src.ETLPipe import ETLPipeline
  
def main(): 
    try:
        AppHeader()
        
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
            
            with st.spinner('Getting your result ready...'):
                 df = ETLPipeline().run(smartphone_model, budget)
                 st.dataframe(df, use_container_width=True)
                 
            alert = st.success("Here's your result...!")
            time.sleep(5)
            alert.empty()
           
    except Exception as e:
        logging.error('An Error Occured: ', exc_info=e)
        raise e
        

if __name__ == "__main__":
    main()