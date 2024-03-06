import re
import logging

class Standardizer:
    
    def __init__(self) -> None:
        pass
    
    def ModelName(self, title):
        try:            
            return title[:title.index('(')].strip()
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def ColorName(self, title):
        try:
            try:
                return title[title.index('(') + 1 : title.index(',')].strip()
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def Rating(self, rate):
        try:
            try:
                return float(rate)
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def Price(self, price):
        try:
            try:
                return int(re.sub(r'[₹|,]', '', price))
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def RAM(self, ram):
        try:
            try:
                return ram.split('|')[0]
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def ROM(self, rom):
        try:
            try:
                return rom.split('|')[1]
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def Dimension(self, display):
        try:
            try:
                return float(display.split()[0])
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def BattPower(self, battery):
        try:
            try:
                return int(battery.split()[0])
            except:
                return ''
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
        
    def run(self, raw_data):
        try:
            df = raw_data

            df['model'] = df['title'].apply(lambda x: self.ModelName(x))
            df['color'] = df['title'].apply(lambda x: self.ColorName(x))
            df['rating'] = df['rating'].apply(lambda x: self.Rating(x))
            df['amount'] = df['price'].apply(lambda x: self.Price(x))
            df['RAM'] = df['RAM/ROM'].apply(lambda x: self.RAM(x))
            df['ROM'] = df['RAM/ROM'].apply(lambda x: self.ROM(x))
            df['dimension'] = df['display'].apply(lambda x: self.Dimension(x))
            df['battery_power'] = df['battery'].apply(lambda x: self.BattPower(x))
            
            df = df.dropna()
            df = df[['url', 'title', 'rating', 'display', 'camera', 'battery', 'model', 'color', 'RAM/ROM', 'price'] + [col for col in df.columns if col not in ['url', 'title', 'rating', 'price', 'display', 'camera', 'battery', 'model', 'color', 'RAM/ROM']]]
            
            return df
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e