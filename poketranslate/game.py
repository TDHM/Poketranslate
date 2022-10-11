import pandas as pd
import re

class Game:
    def __init__(self, romfile: str, pkm_dataframe: pd.DataFrame, moves_dataframe: pd.DataFrame) -> None:
        """Use TBL dataframes, TM/HM (moves) dataframe and Pokemon list dataframe (Source / Translation) to translate given ROM

        Args:
            romfile (str): path to romfile
            moves_dataframe (pd.DataFrame): dataframe with TM/HM in both languages
            full_tbl (pd.DataFrame): full TBL table for the game
            small_tbl (pd.DataFrame): shortened TBL file
        """
        self.romfile = romfile
        
        self.moves_dataframe = moves_dataframe
        self.pkm_dataframe = pkm_dataframe
        
        with open(romfile, 'rb') as f:
            self.hex_romdata = f.read().hex()
        
    def replace_moves(self):
        """Use Python's replace in strings to translate the game from the hexdata
        """
        #self.moves_dataframe["count"] = 0
        
        for i in range(self.moves_dataframe.shape[0]):
            i_Source_hex = self.moves_dataframe.loc[i]["Source_hex"]
            i_Translation_hex = self.moves_dataframe.loc[i]["resized_Translation_hex"]
            #self.moves_dataframe.at[i, "count"] = self.hex_romdata.count(i_Source_hex.lower())
            self.hex_romdata = self.hex_romdata.replace(i_Source_hex.lower(), i_Translation_hex.lower())
            
        #self.moves_dataframe.to_excel("count_moves.xlsx")

    def replace_pkm_names(self):
        """Find and replace HEX Pokemon names to translate them
        """
        #self.pkm_dataframe["count"] = 0
        
        for i in range(self.pkm_dataframe.shape[0]):
            i_Source_hex = self.pkm_dataframe.loc[i]["padded_Source_hex"]
            i_Translation_hex = self.pkm_dataframe.loc[i]["padded_Translation_hex"]
            #self.pkm_dataframe.at[i, "count"] = self.hex_romdata.count(i_Source_hex.lower())
            self.hex_romdata = re.sub(i_Source_hex.lower(), i_Translation_hex.lower(), self.hex_romdata)

        #self.pkm_dataframe.to_excel("count_pkm.xlsx")
            
    def save_translated_rom(self):
        """Save translated game with postfix _translated. Filename must contain only one point "."
        """
        new_name = self.romfile.replace(".", "_translated.")
        with open(new_name, 'wb') as f:
            f.write(bytes.fromhex(self.hex_romdata))