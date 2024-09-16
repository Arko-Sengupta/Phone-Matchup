import re
import logging
import pandas as pd

# Configure Logging
logging.basicConfig(level=logging.INFO)

class Standardizer:
    def __init__(self) -> None:
        """
        Initializes the Standardizer Class.
        This Class does not have any Class Variables.
        """
        pass

    def ModelName(self, title: str) -> str:
        """
        Extracts and returns the Model Name from a given title string.
        Assumes the model name appears before the first '(' character.

        Args:
            title (str): The product title.

        Returns:
            str: Extracted model name or an empty string in case of failure.
        """
        try:            
            return title[:title.index('(')].strip()
        except Exception as e:
            logging.error('An Error Occurred while extracting Model Name: ', exc_info=e)
            return ''

    def ColorName(self, title: str) -> str:
        """
        Extracts and returns the Color Name from the product title string.
        Assumes the color name appears between the first '(' and the first ','.

        Args:
            title (str): The product title.

        Returns:
            str: Extracted color name or an empty string in case of failure.
        """
        try:
            return title[title.index('(') + 1 : title.index(',')].strip()
        except Exception as e:
            logging.error('An Error Occurred while Extracting Color Name: ', exc_info=e)
            return ''

    def Rating(self, rate: str) -> float:
        """
        Converts and returns the Rating Value as a float.

        Args:
            rate (str): The rating value as a string.

        Returns:
            float: The rating as a float or 0.0 in case of failure.
        """
        try:
            return float(rate)
        except ValueError:
            logging.warning('Invalid Rating value, returning default: 0.0')
            return 0.0
        except Exception as e:
            logging.error('An Error Occurred while converting Rating: ', exc_info=e)
            return 0.0

    def Price(self, price: str) -> int:
        """
        Converts and returns the Price as an integer by removing currency symbols and commas.

        Args:
            price (str): The price value as a string (e.g., '₹1,299').

        Returns:
            int: The price as an integer or 0 in case of failure.
        """
        try:
            return int(re.sub(r'[₹|,]', '', price))
        except ValueError:
            logging.warning('Invalid price value, returning default: 0')
            return 0
        except Exception as e:
            logging.error('An Error Occurred while converting Price: ', exc_info=e)
            return 0

    def RAM(self, ram: str) -> str:
        """
        Extracts and returns the RAM Value from a string of the form 'RAM|ROM'.

        Args:
            ram (str): The RAM/ROM string.

        Returns:
            str: Extracted RAM value or an empty string in case of failure.
        """
        try:
            return ram.split('|')[0]
        except IndexError:
            logging.warning('RAM value not found, returning empty string.')
            return ''
        except Exception as e:
            logging.error('An Error Occurred while Extracting RAM: ', exc_info=e)
            return ''

    def ROM(self, rom: str) -> str:
        """
        Extracts and returns the ROM Value from a string of the form 'RAM|ROM'.

        Args:
            rom (str): The RAM/ROM string.

        Returns:
            str: Extracted ROM value or an empty string in case of failure.
        """
        try:
            return rom.split('|')[1]
        except IndexError:
            logging.warning('ROM value not found, returning empty string.')
            return ''
        except Exception as e:
            logging.error('An Error Occurred while Extracting ROM: ', exc_info=e)
            return ''

    def Dimension(self, display: str) -> float:
        """
        Extracts and converts the Display Dimension (assumed to be the first value) as a float.

        Args:
            display (str): The display dimension string.

        Returns:
            float: Extracted display dimension as a float or 0.0 in case of failure.
        """
        try:
            return float(display.split()[0])
        except (ValueError, IndexError):
            logging.warning('Invalid display dimension, returning default: 0.0')
            return 0.0
        except Exception as e:
            logging.error('An Error Occurred while extracting Dimension: ', exc_info=e)
            return 0.0

    def BattPower(self, battery: str) -> int:
        """
        Extracts and converts the Battery Power value as an integer.

        Args:
            battery (str): The battery power string.

        Returns:
            int: Extracted battery power or 0 in case of failure.
        """
        try:
            return int(battery.split()[0])
        except (ValueError, IndexError):
            logging.warning('Invalid battery power, returning default: 0')
            return 0
        except Exception as e:
            logging.error('An Error Occurred while extracting Battery Power: ', exc_info=e)
            return 0

    def run(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the raw data DataFrame by standardizing model, color, rating, price, RAM, ROM,
        display dimension, and battery power, and returns the cleaned DataFrame.

        Args:
            raw_data (pd.DataFrame): The raw data DataFrame to process.

        Returns:
            pd.DataFrame: The processed DataFrame with new columns added and null rows removed.
        """
        try:
            df = raw_data.copy()

            # Apply Each Transformation to the Respective Columns
            df['model'] = df['title'].apply(self.ModelName)
            df['color'] = df['title'].apply(self.ColorName)
            df['rating'] = df['rating'].apply(self.Rating)
            df['amount'] = df['price'].apply(self.Price)
            df['RAM'] = df['RAM/ROM'].apply(self.RAM)
            df['ROM'] = df['RAM/ROM'].apply(self.ROM)
            df['dimension'] = df['display'].apply(self.Dimension)
            df['battery_power'] = df['battery'].apply(self.BattPower)

            # Drop rows with Missing Values
            df = df.dropna()

            logging.info('Data Processing Complete.')
            return df
        except Exception as e:
            logging.error('An Error Occurred while processing the Data: ', exc_info=e)
            raise e