import logging
import streamlit as st
from typing import Dict, Any

def Card(specs: Dict[str, Any]) -> None:
    """
    Renders a Card UI Component in Streamlit based on the provided specification dictionary.
    
    Input:
    - specs: A dictionary containing the following required keys:
        - 'title' (str): The title of the product.
        - 'url' (str): The URL for reference.
        - 'model' (str): The model of the product.
        - 'color' (str): The color of the product.
        - 'rating' (float): The rating of the product.
        - 'original_price' (float): The original price of the product.
        - 'discount' (float): The discount percentage.
        - 'price' (float): The final price after discount.
        - 'RAM/ROM' (str): The RAM/ROM specification.
        - 'display' (str): The display specification.
        - 'camera' (str): The camera specification.
        - 'battery' (str): The battery specification.
    """
    try:
        # Validate that all fields
        required_keys = [
            'title', 'url', 'model', 'color', 'rating', 'original_price', 
            'discount', 'price', 'RAM/ROM', 'display', 'camera', 'battery'
        ]
        
        # Check for Missing Keys in Specifications
        for key in required_keys:
            if key not in specs:
                raise ValueError(f"Missing required key in specs: '{key}'")
        
        # Render the Card with data
        st.markdown(
            f"""
            <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin-bottom: 15px'>
                <h3 style='text-align: center;'>{specs['title']}</h3>
                <hr>
                <p><strong>Refer to: </strong> <a href="{specs['url']}" target="_blank">{specs['title']}</a></p>
                <p><strong>Title: </strong> {specs['title']}</p>
                <p><strong>Model:</strong> {specs['model']}</p>
                <p><strong>Color:</strong> {specs['color']}</p>
                <p><strong>Rating:</strong> {specs['rating']}</p>
                <p><strong>Original Price:</strong> {specs['original_price']}</p>
                <p><strong>Discount: </strong> {specs['discount']}%</p>
                <p><strong>Price: </strong> {specs['price']}</p>
                <p><strong>RAM/ROM: </strong> {specs['RAM/ROM']}</p>
                <p><strong>Display: </strong> {specs['display']}</p>
                <p><strong>Camera: </strong> {specs['camera']}</p>
                <p><strong>Battery: </strong> {specs['battery']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except ValueError as ve:
        logging.error(f"Input Validation Error: {ve}")
    except Exception as e:
        logging.error('An Error Occurred while rendering the Card.', exc_info=True)
        raise e