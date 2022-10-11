import pandas as pd

from utils import make_dict_str_to_hex, get_encoding

class Moves:
    def __init__(self, moves_list_path: str, tbl_path: str, uppercase: bool) -> None:
        """Generates HEX translated TM/HM (moves) names dataframes

        Args:
            moves_list_path (str): path to Excel TM/HM list
            tbl_path (str): path to full TBL file for the corresponding game
            uppercase (bool): wether moves are upper-cased or not (default False in argparse in main.py)
        """
        self.moves_list_path = moves_list_path
        self.tbl_path = tbl_path
        self.uppercase = uppercase
        
        self.moves_list = pd.read_excel(self.moves_list_path)
        self.moves_list.columns = ["Source", "Translation"]
        
        with open(tbl_path, 'r') as f:
                    self.tbl_data = f.read()

        self.dict_table = make_dict_str_to_hex(self.tbl_data)
        
    def generate_hex_translation(self):
        """Add columns to pkm_list dataframe with translated HEX values
        """
        if self.uppercase:
            self.moves_list["Source"] = self.moves_list["Source"].str.upper()
            self.moves_list["Translation"] = self.moves_list["Translation"].str.upper()

        self.moves_list["Source_hex"] = self.moves_list["Source"].apply(lambda x: get_encoding(x, self.dict_table))
        self.moves_list["Translation_hex"] = self.moves_list["Translation"].apply(lambda x: get_encoding(x, self.dict_table))
        self.moves_list["resized_Translation_hex"] = self.moves_list.apply(lambda x: self.match_length_hex(x["Source_hex"], x["Translation_hex"]), axis=1)
        
    def get_moves_dataframe(self) -> pd.DataFrame:
        """Retrieve translated moves list dataframe

        Returns:
            pd.DataFrame: dataframe used to translate moves names in class Game
        """
        self.generate_hex_translation()
        
        # Sort values by length in order to avoid conflicts between names during find and replace in Hex
        self.moves_list = self.moves_list.sort_values(by="Source", key=lambda x: x.str.len(), ascending=False)
        
        return self.moves_list
    
    @staticmethod
    def match_length_hex(hex_value_source, hex_value_dest):
        nb_bytes_source = len(hex_value_source)//2
        nb_bytes_dest = len(hex_value_dest)//2
        nb_bytes_diff = nb_bytes_source - nb_bytes_dest
        if nb_bytes_diff > 0:
            for i in range(nb_bytes_diff):
                hex_value_dest += "7F"
        else:
            hex_value_dest = hex_value_dest[:len(hex_value_source)]
        return hex_value_dest