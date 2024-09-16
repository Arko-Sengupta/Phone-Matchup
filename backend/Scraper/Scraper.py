import re
import ast
import time
import logging
import requests
import pandas as pd

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Scraper:
    def __init__(self, limit: int = None, scraper_parameters: dict = None) -> None:
        """
        Initializes the Scraper Class with the provided parameters.

        Parameters:
        limit (int): Maximum number of products to scrape.
        scraper_parameters (dict): Configuration details like Selenium XPaths,
                                   Product Class Details, Chrome Driver Path & Headers
        """
        self.limit = limit
        self.selenium_dict = scraper_parameters['Selenium_dict']
        self.product_class_dict = scraper_parameters['Product_Class_dict']
        self.chrome_driver_path = scraper_parameters['Chrome_Driver_Path']
        self.headers = scraper_parameters['Headers']
        self.session = requests.Session()

        # Initialize Chrome Options
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

    def page_product_urls(self, query: str) -> list:
        """
        Scrapes Product URLs from search results using Selenium Automation.

        Parameters:
        query (str): The search term to be entered in the search bar of the website.

        Returns:
        list: A list of product URLs extracted from the search results.
        """
        try:
            driver = webdriver.Chrome(
                executable_path=self.chrome_driver_path, options=self.chrome_options
            )
            driver.get(str(self.selenium_dict['URL']))

            # Search Input XPATH is Required
            search_input = driver.find_element(By.XPATH, str(self.selenium_dict['INPUT_XPATH']))
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)

            # Next Button XPATH is Required
            # <a> tags class Selector is Required
            a_tags = []
            while True:
                page_a_tags = driver.find_elements(By.CSS_SELECTOR, str(self.selenium_dict['a_class']))
                a_tags.extend([a.get_attribute('href') for a in page_a_tags])

                # Navigate to the Next Page until there are no more pages
                try:
                    try:
                        next_button = driver.find_element(By.XPATH, str(self.selenium_dict['PAGE_1_NEXT_XPATH']))
                        next_button.click()
                    except Exception:
                        next_button = driver.find_element(By.XPATH, str(self.selenium_dict['PAGE_X_NEXT_XPATH']))
                        next_button.click()
                except Exception:
                    logging.info("Reached the last page or no Next Page Button found.")
                    break

                time.sleep(2)
            driver.quit()

            return list(set(a_tags))
        except Exception as e:
            logging.error('An Error Occurred while Extracting URLs: ', exc_info=e)
            raise e

    def product_details(self, url: str) -> dict:
        """
        Fetches and Parses Product Details from the provided product URL.

        Parameters:
        url (str): The URL of the product page to scrape.

        Returns:
        dict: A dictionary containing the product details.
        """
        try:
            response = self.session.get(url, headers=self.headers)

            if response.status_code == 200:
                product_details = {}
                soup = BeautifulSoup(response.text, 'lxml')

                # Extracting URL
                product_details['url'] = url

                # Extracting Title
                try:
                    title = ast.literal_eval(self.product_class_dict['title'])
                    product_details['title'] = re.sub(
                        r'[^\x00-\x7F]+', ' ', soup.find(title[0], class_=title[1]).get_text()
                    )
                except Exception:
                    product_details['title'] = 'NOT AVAILABLE'

                # Extracting Rating
                try:
                    rating = ast.literal_eval(self.product_class_dict['rating'])
                    product_details['rating'] = soup.find(rating[0], class_=rating[1]).get_text()
                except Exception:
                    product_details['rating'] = 'NOT AVAILABLE'

                # Extracting Original Price
                try:
                    original_price = ast.literal_eval(self.product_class_dict['original_price'])
                    product_details['original_price'] = soup.find(original_price[0], class_=original_price[1]).get_text()
                except Exception:
                    product_details['original_price'] = 'NOT AVAILABLE'

                # Extracting Discount
                try:
                    discount = ast.literal_eval(self.product_class_dict['discount'])
                    product_details['discount'] = soup.find(discount[0], class_=discount[1]).get_text().split()[0]
                except Exception:
                    product_details['discount'] = 'NOT AVAILABLE'

                # Extracting Price
                try:
                    price = ast.literal_eval(self.product_class_dict['price'])
                    product_details['price'] = soup.find(price[0], class_=price[1]).get_text()
                except Exception:
                    product_details['price'] = 'NOT AVAILABLE'

                # Extracting Features (RAM/ROM, Display, Camera, Battery)
                features = ast.literal_eval(self.product_class_dict['features'])
                try:
                    product_details['RAM/ROM'] = soup.find_all(features[0], class_=features[1])[0].get_text()
                except Exception:
                    product_details['RAM/ROM'] = 'NOT AVAILABLE'

                try:
                    product_details['display'] = soup.find_all(features[0], class_=features[1])[1].get_text()
                except Exception:
                    product_details['display'] = 'NOT AVAILABLE'

                try:
                    product_details['camera'] = soup.find_all(features[0], class_=features[1])[2].get_text()
                except Exception:
                    product_details['camera'] = 'NOT AVAILABLE'

                try:
                    product_details['battery'] = soup.find_all(features[0], class_=features[1])[3].get_text()
                except Exception:
                    product_details['battery'] = 'NOT AVAILABLE'

                return product_details
            else:
                logging.warning(f"Failed to fetch the URL {url}. Status code: {response.status_code}")
                return {}
        except Exception as e:
            logging.error(f"An Error Occurred while Scraping Product Details from {url}: ", exc_info=e)
            return {}

    def products(self, query: str) -> pd.DataFrame:
        """
        Gathers Product URLs based on the Search Query and Scrapes their details concurrently.

        Parameters:
        query (str): The search term used to find products.

        Returns:
        pd.DataFrame: A DataFrame containing the product details for all scraped products.
        """
        try:
            # Extract URLs from the Search Query
            products = self.page_product_urls(query)

            # Scrape Product Details in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=4) as executor:
                if self.limit is None:
                    product_details = list(executor.map(self.product_details, list(set(products))))
                else:
                    product_details = list(executor.map(self.product_details, list(set(products[: int(self.limit)]))))

            df = pd.DataFrame(product_details)
            return df
        except Exception as e:
            logging.error('An Error Occurred while fetching products: ', exc_info=e)
            raise e

    def run(self, query: str) -> pd.DataFrame:
        """
        Executes the full Scraping Process: From Querying the Product to Obtaining a DataFrame of results.

        Parameters:
        query (str): The search term used to find products.

        Returns:
        pd.DataFrame: A DataFrame containing the product details.
        """
        try:
            # Scrape the Products and clean the DataFrame
            df = self.products(query)
            df = df.dropna(how='all')  # Drop rows where all columns are NaN

            return df
        except Exception as e:
            logging.error('An Error Occurred during Execution: ', exc_info=e)
            raise e