import logging
import streamlit as st
from typing import Union
from ..Utils import bootstrap_utils

def AppHeader(title: Union[str, None]) -> None:
    """
    Renders a Application Header with title.

    Input:
    - title (str): The title to be displayed in the header. If no title is provided, 
      a default message is shown.
    """    
    try:
        # Ensure the Title is a string or None
        if not isinstance(title, (str, type(None))):
            raise ValueError("Title must be a string or None.")
        
        # Load Bootstrap and Utilities
        bootstrap_utils()

        # Define CSS for the Header
        st.markdown(
            """
            <style>
                .fs {
                    min-width: 250px;
                    font-size: 50px;
                    font-weight: bold;
                    margin: 0;
                }

                @media screen and (max-width: 650px) {
                    .fs {
                        font-size: 30px;
                    }
                }

                @media screen and (max-width: 400px) {
                    .fs {
                        font-size: 15px;
                    }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Display the Title
        st.markdown(
            f'''<p class="container fs text-center">{title if title else "Default App Title"}</p>''',
            unsafe_allow_html=True
        )
        
    except ValueError as ve:
        logging.error(f"Input Validation Error: {ve}")
    except Exception as e:
        logging.error("An Error Occurred while rendering the App Header.", exc_info=True)
        raise e
