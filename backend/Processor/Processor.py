import logging
import pandas as pd

# Configure Logging
logging.basicConfig(level=logging.INFO)

class Processor:
    def __init__(self) -> None:
        """
        Initializes the Processor Class.
        This Class does not have any Class Variables.
        """
        pass

    def FilterRAM(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame to retain rows with the Maximum RAM Values.

        Args:
            df (pd.DataFrame): The input DataFrame containing product data.

        Returns:
            pd.DataFrame: Filtered DataFrame with only the rows having the maximum RAM.
        """
        try:
            # Convert RAM values to integers and filter by Maximum RAM
            df['RAM'] = df['RAM'].apply(lambda x: int(x.split()[0]))
            df = df[df['RAM'] == df['RAM'].max()]
            logging.info('RAM filtering completed.')
            return df
        except Exception as e:
            logging.error('An Error Occurred while Filtering RAM: ', exc_info=e)
            raise e

    def FilterROM(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame to retain rows with the Maximum ROM Values.

        Args:
            df (pd.DataFrame): The input DataFrame containing product data.

        Returns:
            pd.DataFrame: Filtered DataFrame with only the rows having the maximum ROM.
        """
        try:
            # Convert ROM values to integers and filter by Maximum ROM
            df['ROM'] = df['ROM'].apply(lambda x: int(x.split()[0]))
            df = df[df['ROM'] == df['ROM'].max()]
            logging.info('ROM filtering completed.')
            return df
        except Exception as e:
            logging.error('An Error Occurred while Filtering ROM: ', exc_info=e)
            raise e

    def run(self, transformed_data: pd.DataFrame, price: str) -> pd.DataFrame:
        """
        Processes the transformed data by applying various filters like Price Limit, Top 15 Amount,
        Rating, Dimension, RAM, ROM, and Battery Power, and returns a Filtered DataFrame.

        Args:
            transformed_data (pd.DataFrame): The DataFrame containing transformed product data.
            price (str): The maximum price as a string (which will be converted to an integer).

        Returns:
            pd.DataFrame: The final filtered DataFrame with relevant product details.
        """
        try:
            # Convert Price to Integer and Filter DataFrame
            df = transformed_data
            price = int(price)
            logging.info(f'Filtering Products under the Price: {price}')

            # Filter Amount less than or equal to the Specified Price
            df = df[df['amount'] <= price]

            # Select Top 15 Product Amount
            df = df[df['amount'].isin(df.nlargest(15, 'amount')['amount'])]

            # Filter Most Common Rating and Dimension
            df = df[df['rating'] == df['rating'].value_counts().idxmax()]
            df = df[df['dimension'] == df['dimension'].value_counts().idxmax()]

            # Apply RAM and ROM filters
            df = self.FilterRAM(df)
            df = self.FilterROM(df)

            # Filter Maximum Battery Power
            df = df[df['battery_power'] == df['battery_power'].max()]

            # Select the Relevant Columns
            df = df[['url', 'title', 'model', 'color', 'rating', 'original_price', 'discount', 'price', 'RAM/ROM', 'display', 'camera', 'battery']]
            
            logging.info('Data Processing Completed Successfully.')
            return df
        except Exception as e:
            logging.error('An Error Occurred while running the Processor: ', exc_info=e)
            raise e