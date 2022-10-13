import pandas as pd

from utils import make_dict_str_to_hex, get_encoding

class Pokemons:
    def __init__(self, df_pokemons: pd.DataFrame, tbl_path: str, uppercase: bool) -> None:
        """Generates HEX translated Pokemon names dataframes

        Args:
            df_pokemons (pd.DataFrame): Pandas DataFrame of Pokémon list
            small_tbl (str): path short TBL file for the corresponding game
            uppercase (bool): wether Pokemon names are upper-cased or not (default False in argparge in main.py)
        """
        self.df_pokemons = df_pokemons
        self.tbl_path = tbl_path
        self.uppercase = uppercase
        
        self.df_pokemons.columns = ["Source", "Translation"]
        
        with open(tbl_path, 'r') as f:
                    self.tbl_data = f.read()

        self.dict_table = make_dict_str_to_hex(self.tbl_data)
        
    def generate_hex_translation(self):
        """Add columns to df_pokemons dataframe with translated HEX values
        """
        if self.uppercase:
            self.df_pokemons["Source"] = self.df_pokemons["Source"].str.upper()
            self.df_pokemons["Translation"] = self.df_pokemons["Translation"].str.upper()
            
        self.df_pokemons["Source_hex"] = self.df_pokemons["Source"].apply(lambda x: get_encoding(x, self.dict_table))
        self.df_pokemons["Translation_hex"] = self.df_pokemons["Translation"].apply(lambda x: get_encoding(x, self.dict_table))
        self.df_pokemons["padded_Source_hex"] = self.df_pokemons["Source_hex"].apply(self.pad_hex)
        self.df_pokemons["padded_Translation_hex"] = self.df_pokemons["Translation_hex"].apply(self.pad_hex)
        
    def get_pkm_dataframe(self) -> pd.DataFrame:
        """Retrieve translated pokemon list dataframe

        Returns:
            pd.DataFrame: dataframe used to translate pokemon names in class Game
        """
        self.generate_hex_translation()
        
        # Sort values by length in order to avoid conflicts between names during find and replace in Hex
        self.df_pokemons = self.df_pokemons.sort_values(by="Source", key=lambda x: x.str.len(), ascending=False)
        
        return self.df_pokemons
        
    @staticmethod
    def pad_hex(hex_value):
        nb_bytes = len(hex_value)//2
        nb_pads_needed = 10-nb_bytes
        padded_hex_value = hex_value
        for i in range(nb_pads_needed):
            padded_hex_value += "50"
            
        return padded_hex_value