import logging

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

class Processor:
    
    def __init__(self) -> None:
        pass
    
    def FilterRAM(self, df):
        try:
            df['RAM'] = df['RAM'].apply(lambda x: int(x.split()[0]))
            df = df[df['RAM'] == df['RAM'].max()]

            return df
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
        
    def FilterROM(self, df):
        try:
            df['ROM'] = df['ROM'].apply(lambda x: int(x.split()[0]))
            df = df[df['ROM'] == df['ROM'].max()]

            return df
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e
    
    def run(self, transformed_data, price):
        try:
            df, price = transformed_data, int(price)
            
            df = df[df['amount'] <= price]
            df = df[df['amount'].isin(df.nlargest(15, 'amount')['amount'])]
            
            df = df[df['rating'] == df['rating'].value_counts().idxmax()]
            df = df[df['dimension'] == df['dimension'].value_counts().idxmax()]
            
            df = self.FilterRAM(df)
            df = self.FilterROM(df)
            
            df = df[df['battery_power'] == df['battery_power'].max()]
            
            df = df[['url', 'title', 'model', 'color', 'rating', 'original_price', 'discount', 'price', 'RAM/ROM', 'display', 'camera', 'battery']] 
            return df
        except Exception as e:
            logging.error('An Error Occured: ', exc_info=e)
            raise e