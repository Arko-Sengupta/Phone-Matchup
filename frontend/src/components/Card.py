import logging
import streamlit as st

def Card(specs):
    try:
        st.markdown(
            f"""
            <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin-bottom: 15px'>
                <h3 style='text-align: center;'>{specs['title']}</h3>
                <hr>
                <p><strong>Refer to: </strong> <a href={specs['url']}>{specs['title']}</a></p>
                <p><strong>Title: </strong> {specs['title']}</p>
                <p><strong>Model:</strong> {specs['model']}</p>
                <p><strong>Color:</strong> {specs['color']}</p>
                <p><strong>Rating:</strong> {specs['rating']}</p>
                <p><strong>Original Price:</strong> {specs['original_price']}</p>
                <p><strong>Discount: </strong> {specs['discount']}</p>
                <p><strong>Price: </strong> {specs['price']}</p>
                <p><strong>RAM/ROM: </strong> {specs['RAM/ROM']}</p>
                <p><strong>Display: </strong> {specs['display']}</p>
                <p><strong>Camera: </strong> {specs['camera']}</p>
                <p><strong>Battery: </strong> {specs['battery']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        logging.error('An Error Occured: ', exc_info=e)
        raise e