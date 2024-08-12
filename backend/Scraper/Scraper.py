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
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    
    def __init__(self, limit=None, Scraper_Parametres=None):
        self.limit = limit
        self.Selenium_dict = Scraper_Parametres['Selenium_dict']
        self.Product_Class_dict = Scraper_Parametres['Product_Class_dict']
        self.session = requests.Session()
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_driver_path = ChromeDriverManager().install()
        
    def PageProductURLs(self, query):
        try:
            self.chrome_options.add_argument('--headless')
            
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(str(self.Selenium_dict['URL']))
            
            # Search Input EPATH is Required
            search_input = driver.find_element(By.XPATH, str(self.Selenium_dict['INPUT_XPATH']))
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)
            
            # Next Button XPATH is Required
            # <a> tags class Selector is Required
            a_tags = []
            while True:
                page_a_tags = driver.find_elements(By.CSS_SELECTOR, str(self.Selenium_dict['a_class']))
                a_tags.extend([a.get_attribute('href') for a in page_a_tags])
                
                try:
                    try:
                        next_button = driver.find_element(By.XPATH, str(self.Selenium_dict['PAGE_1_NEXT_XPATH']))
                        next_button.click()
                    except:
                        next_button = driver.find_element(By.XPATH, str(self.Selenium_dict['PAGE_X_NEXT_XPATH']))
                        next_button.click()
                except:
                    break
                
                time.sleep(2)                
            driver.quit()
                
            return list(set(a_tags))
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
        
    def ProductDetails(self, url):
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                product_details = {}
                
                soup = BeautifulSoup(response.text, 'lxml')
                
                try:
                    product_details['url'] = url
                except:
                    product_details['url'] = '#'
                    
                try:
                    title = ast.literal_eval(self.Product_Class_dict['title'])
                    product_details['title'] = re.sub(r'[^\x00-\x7F]+', ' ', soup.find(title[0], class_=title[1]).get_text())
                except:
                    product_details['title'] = 'NOT AVAILABLE'
                    
                try:
                    rating = ast.literal_eval(self.Product_Class_dict['rating'])
                    product_details['rating'] = soup.find(rating[0], class_=rating[1]).get_text()
                except:
                    product_details['rating'] = 'NOT AVAILABLE'
                
                try:
                    original_price = ast.literal_eval(self.Product_Class_dict['original_price'])
                    product_details['original_price'] = soup.find(original_price[0], class_=original_price[1]).get_text()
                except:
                    product_details['original_price'] = 'NOT AVAILABLE'
                
                try:
                    discount = ast.literal_eval(self.Product_Class_dict['discount'])
                    product_details['discount'] = soup.find(discount[0], class_=discount[1]).get_text().split()[0]
                except:
                    product_details['discount'] = 'NOT AVAILABLE'
                    
                try:
                    price = ast.literal_eval(self.Product_Class_dict['price'])
                    product_details['price'] = soup.find(price[0], class_=price[1]).get_text()
                except:
                    product_details['price'] = 'NOT AVAILABLE'
                 
                features = ast.literal_eval(self.Product_Class_dict['features'])   
                try:
                    product_details['RAM/ROM'] = soup.find_all(features[0], class_=features[1])[0].get_text()
                except:
                    product_details['RAM/ROM'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['display'] = soup.find_all(features[0], class_=features[1])[1].get_text()
                except:
                    product_details['display'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['camera'] = soup.find_all(features[0], class_=features[1])[2].get_text()
                except:
                    product_details['camera'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['battery'] = soup.find_all(features[0], class_=features[1])[3].get_text()
                except:
                    product_details['battery'] = 'NOT AVAILABLE'

                return product_details
            else:
                return {}
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
        
    def Products(self, query):
        try:
            products = self.PageProductURLs(query)
                
            with ThreadPoolExecutor(max_workers=4) as executor:
                if self.limit == None:
                    product_details = list(executor.map(self.ProductDetails, list(set(products))))
                else:
                    product_details = list(executor.map(self.ProductDetails, list(set(products[:int(self.limit)]))))
                
            df = pd.DataFrame(product_details)
                
            return df
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
        
    def run(self, query):
        try:
            df = self.Products(query)
            df = df.dropna()
            
            return df
        except Exception as e:
            logging.error('An Error Occcured: ', exc_info=e)
            raise e