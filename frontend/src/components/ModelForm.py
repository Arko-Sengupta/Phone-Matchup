import logging
import streamlit as st
from typing import Union, Dict

def Model_Form() -> Union[str, Dict[str, str], None]:
    """
    Renders a form in Streamlit to input Smartphone Model and Budget Details.
    """
    # Define Custom CSS Style
    custom_css = """
    <style>
        .stForm {
            min-width: 250px;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    try:
        with st.form("model_details", clear_on_submit=True):
            # Input fields
            smartphone_model = st.text_input("Smartphone Brand:", value='', help="Enter the Smartphone Brand")
            budget = st.number_input("Budget:", min_value=0, step=2000, format='%d', help="Enter your Budget (min 2000)")

            # Form Submit Button
            submitted = st.form_submit_button("Submit")

            # Form Validation and Response
            if submitted:
                if not smartphone_model and budget < 2000:
                    return 'NO MODEL & BUDGET'
                elif not smartphone_model:
                    return 'NO MODEL'
                elif budget < 2000:
                    return 'NO BUDGET'
                else:
                    return {"Smartphone Model": f"{smartphone_model} Smartphones", "Budget": str(budget)}
        return None
    
    except Exception as e:
        logging.error('An Error Occurred while Processing the Form.', exc_info=True)
        raise e