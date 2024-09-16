import logging
import streamlit as st

def bootstrap_utils() -> None:
    """
    Integrates Bootstrap and related utilities into Streamlit using HTML Markup.
    """
    try:
        # Define Custom CSS Style
        custom_css = """
        <style>
            .stMarkdown {
                min-width: 250px;
            }
            
            .stSpinner {
                min-width: 250px;
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
                
        # Load Bootstrap CSS and JavaScript Along with jQuery and Popper
        st.markdown("""
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logging.error('An Error Occurred while loading Bootstrap Utilities.', exc_info=True)
        raise e