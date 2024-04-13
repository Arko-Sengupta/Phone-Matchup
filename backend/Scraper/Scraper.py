import re
import logging
import requests
import pandas as pd

from itertools import chain
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)


class Scraper:
    
    def __init__(self, limit=None):
        self.limit = limit
        self.session = requests.Session()
        
    def GeneratePageURL(self, page_num):
        try:
            return f'https://www.flipkart.com/search?q={self.product}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY&page={page_num}'
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def TotalPages(self):
        try:
            response = self.session.get(self.GeneratePageURL(1))
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                
                total_pages = soup.find('span', class_='_10Ermr')
                total_pages = total_pages.get_text().split()
                
                total_products, page_products = int(total_pages[5].replace(',', '')), int(total_pages[3])
                
                if total_products%page_products:
                    total_pages = total_products//page_products + 1
                else:
                    total_pages = total_products//page_products
                
                return total_pages
            else:
                return 0
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
        
    def TotalPageURLs(self):
        try:
            return [self.GeneratePageURL(page_num) for page_num in range(1, self.TotalPages() + 1)]
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
            raise e
    
    def PageProductURLs(self, url):
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                
                page_product_urls = soup.find_all('a', class_='_1fQZEK')
                
                if len(page_product_urls) == 0:
                    page_product_urls = soup.find_all('a', class_='_2UzuFa')

                page_product_urls = ['https://www.flipkart.com' + a['href'] for a in page_product_urls]
                
                return page_product_urls
            else:
                return []
        except Exception as e:
            logging.error('An Error Occured:', exc_info=e)
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
                    product_details['title'] = re.sub(r'[^\x00-\x7F]+', ' ', soup.find('span', class_='B_NuCI').get_text())
                except:
                    product_details['title'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['rating'] = soup.find('div', class_='_3LWZlK').get_text()
                except:
                    product_details['rating'] = 'NOT AVAILABLE'
                
                try:
                    product_details['original_price'] = soup.find('div', class_='_3I9_wc _2p6lqe').get_text()
                except:
                    product_details['original_price'] = 'NOT AVAILABLE'
                
                try:
                    product_details['discount'] = soup.find('div', class_='_3Ay6Sb _31Dcoz').get_text().split()[0]
                except:
                    product_details['discount'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['price'] = soup.find('div', class_='_30jeq3 _16Jk6d').get_text()
                except:
                    product_details['price'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['RAM/ROM'] = soup.find_all('li', class_='_21Ahn-')[0].get_text()
                except:
                    product_details['RAM/ROM'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['display'] = soup.find_all('li', class_='_21Ahn-')[1].get_text()
                except:
                    product_details['display'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['camera'] = soup.find_all('li', class_='_21Ahn-')[2].get_text()
                except:
                    product_details['camera'] = 'NOT AVAILABLE'
                    
                try:
                    product_details['battery'] = soup.find_all('li', class_='_21Ahn-')[3].get_text()
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
            self.product = '+'.join(query.lower().split())
            
            page_urls = self.TotalPageURLs()
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                products = list(chain.from_iterable(executor.map(self.PageProductURLs, page_urls)))
                
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