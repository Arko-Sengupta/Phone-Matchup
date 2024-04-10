import logging
import streamlit as st

def Model_Form():
    try:
             
        with st.form("model_details", clear_on_submit=True):
            
            smartphone_model = st.text_input("Smartphone Brand:", value='')
            budget = st.number_input("Budget:", min_value=0, step=2000, format='%d')
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                if not smartphone_model and budget < 2000:
                    return 'NO MODEL & BUDGET'
                elif not smartphone_model:
                    return 'NO MODEL'
                elif budget < 2000:
                    return 'NO BUDGET'
                else:
                    return {"Smartphone Model": str(smartphone_model + " Smartphones"), "Budget": str(budget)}
     
    except Exception as e:
        logging.error('An Error Occured: ', exc_info=e)
        raise e