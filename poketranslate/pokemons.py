import pandas as pd

from utils import make_dict_str_to_hex, get_encoding

class Pokemons:
    def __init__(self, pkm_list_path: str, tbl_path: str, uppercase: bool) -> None:
        """Generates HEX translated Pokemon names dataframes

        Args:
            pkm_list_path (str): path to Excel Pokémon list
            small_tbl (str): path short TBL file for the corresponding game
            uppercase (bool): wether Pokemon names are upper-cased or not (default False in argparge in main.py)
        """
        self.pkm_list_path = pkm_list_path
        self.tbl_path = tbl_path
        self.uppercase = uppercase
        
        self.pkm_list = pd.read_excel(self.pkm_list_path)
        self.pkm_list.columns = ["Source", "Translation"]
        
        with open(tbl_path, 'r') as f:
                    self.tbl_data = f.read()

        self.dict_table = make_dict_str_to_hex(self.tbl_data)
        
    def generate_hex_translation(self):
        """Add columns to pkm_list dataframe with translated HEX values
        """
        if self.uppercase:
            self.pkm_list["Source"] = self.pkm_list["Source"].str.upper()
            self.pkm_list["Translation"] = self.pkm_list["Translation"].str.upper()
            
        self.pkm_list["Source_hex"] = self.pkm_list["Source"].apply(lambda x: get_encoding(x, self.dict_table))
        self.pkm_list["Translation_hex"] = self.pkm_list["Translation"].apply(lambda x: get_encoding(x, self.dict_table))
        self.pkm_list["padded_Source_hex"] = self.pkm_list["Source_hex"].apply(self.pad_hex)
        self.pkm_list["padded_Translation_hex"] = self.pkm_list["Translation_hex"].apply(self.pad_hex)
        
    def get_pkm_dataframe(self) -> pd.DataFrame:
        """Retrieve translated pokemon list dataframe

        Returns:
            pd.DataFrame: dataframe used to translate pokemon names in class Game
        """
        self.generate_hex_translation()
        
        # Sort values by length in order to avoid conflicts between names during find and replace in Hex
        self.pkm_list = self.pkm_list.sort_values(by="Source", key=lambda x: x.str.len(), ascending=False)
        
        return self.pkm_list
        
    @staticmethod
    def pad_hex(hex_value):
        nb_bytes = len(hex_value)//2
        nb_pads_needed = 10-nb_bytes
        padded_hex_value = hex_value
        for i in range(nb_pads_needed):
            padded_hex_value += "50"
            
        return padded_hex_value