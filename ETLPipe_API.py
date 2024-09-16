import json
import os
import logging
import pandas as pd
from dotenv import load_dotenv
from flask import Blueprint, Flask, jsonify, request

from backend.Scraper.Scraper import Scraper
from backend.Processor.Processor import Processor
from backend.Standardizer.Standardizer import Standardizer

# Configure Logging
logging.basicConfig(level=logging.INFO)

# Load Environment Variables
load_dotenv(".env")

class ETLPipeline:
    def __init__(self) -> None:
        """
        Initializes the ETLPipeline with Configurations for Scraping Parameters and Setting Up
        the Scraper, Standardizer, and Processor Instances.
        """
        # Load limit from Environment Variables
        self.limit = os.getenv("TEST")

        # Load Scraper Parameters from a JSON file
        with open('scraper_parameters.json') as f:
            self.data = json.load(f)

        # Instantiate Classes for Scraping, Transformation, and Filtering
        self.raw_data = Scraper(self.limit, self.data)
        self.transformed_data = Standardizer()
        self.filtered_data = Processor()

    def extract_data(self, query: str) -> pd.DataFrame:
        """
        Extract raw data using the Scraper instance based on the Brand Query.

        Args:
            query (str): The brand name to search for.

        Returns:
            DataFrame: Raw data extracted from the web.
        """
        try:
            return self.raw_data.run(query)
        except Exception as e:
            logging.error('An Error Occurred while Extracting Data: ', exc_info=e)
            raise e

    def transform_data(self, raw_data) -> pd.DataFrame:
        """
        Transform raw data using the Standardizer instance to Standardize Product Details.

        Args:
            raw_data: The raw data to be transformed.

        Returns:
            DataFrame: Transformed data with standardized product fields.
        """
        try:
            return self.transformed_data.run(raw_data)
        except Exception as e:
            logging.error('An Error Occurred while Transforming Data: ', exc_info=e)
            raise e

    def filter_data(self, transformed_data, price: str) -> pd.DataFrame:
        """
        Filter transformed data based on the price limit using the Processor Instance.

        Args:
            transformed_data: The data to be filtered.
            price (str): The maximum price for filtering products.

        Returns:
            DataFrame: Filtered data with products meeting the price criteria.
        """
        try:
            return self.filtered_data.run(transformed_data, price)
        except Exception as e:
            logging.error('An Error Occurred while Filtering Data: ', exc_info=e)
            raise e

    def run(self, brand: str, price: str) -> pd.DataFrame:
        """
        Execute the entire ETL Pipeline (Extract, Transform, and Filter) and return the Filtered data.

        Args:
            brand (str): The brand name for scraping.
            price (str): The maximum price for filtering products.

        Returns:
            DataFrame: Final filtered product data.
        """
        try:
            # Step 1: Extract raw data based on the brand
            raw_data = self.extract_data(brand)

            # Step 2: Transform raw data into standardized format
            transformed_data = self.transform_data(raw_data)

            # Step 3: Filter the data based on the price
            filtered_data = self.filter_data(transformed_data, price)

            return filtered_data
        except Exception as e:
            logging.error('An Error Occurred during the ETL Pipeline Execution: ', exc_info=e)
            raise e


class ETLPipe_API:
    """
    ETLPipe_API class sets up the Flask web API for the ETL Pipeline, allowing interaction
    with the pipeline through HTTP requests.
    """

    def __init__(self) -> None:
        """
        Initializes the Flask API, sets up the ETL Pipeline, and defines the API Routes.
        """
        # Create Flask App and Blueprint for ETL API
        self.app = Flask(__name__)
        self.ETLPile_blueprint = Blueprint('etl_pipeline', __name__)

        # Define Routes for the API
        self.ETLPile_blueprint.add_url_rule('/', 'SERVER_STARTED', self.SERVER_STARTED, methods=['GET'])
        self.ETLPile_blueprint.add_url_rule('/ETLPipe', 'ETLPipe', self.ETLPipe, methods=['POST'])

        # Instantiate ETLPipeline class
        self.ETLPile = ETLPipeline()

    def SERVER_STARTED(self) -> jsonify:
        """
        API Route to check if the server is running.

        Returns:
            JSON: A response indicating that the server is started.
        """
        try:
            return jsonify({'response': 200, 'SERVER STARTED': True}), 200
        except Exception as e:
            logging.error('An Error Occurred while Starting the Server: ', exc_info=e)
            raise e

    def ETLPipe(self) -> jsonify:
        """
        API Route to run the ETL Pipeline based on the brand and price provided in the POST request.

        Returns:
            JSON: Filtered product data or an error response.
        """
        try:
            # Parse JSON request to Extract Brand and Price
            data = request.get_json()
            brand, price = data['brand'], data['price']

            # Run the ETL Pipeline with the provided Brand and Price
            response = self.ETLPile.run(brand, price)

            # Return the Response as JSON
            return jsonify({'response': response.to_dict()}), 200
        except Exception as e:
            logging.error('An Error Occurred during the ETL Process: ', exc_info=e)
            return jsonify({'Error': str(e)}), 400

    def run(self) -> None:
        """
        Start the Flask Application and register the API Routes.

        Returns:
            None
        """
        try:
            # Register the ETL API blueprint and run the Flask App
            self.app.register_blueprint(self.ETLPile_blueprint)
            self.app.run(debug=True)
        except Exception as e:
            logging.error('An Error Occurred while Running the Server: ', exc_info=e)
            raise e


if __name__ == '__main__':
    
    # Start the ETL API
    server = ETLPipe_API()
    server.run()