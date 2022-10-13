import sys
import argparse
import time

import pandas as pd

from game import Game
from pokemons import Pokemons
from moves import Moves

import pandas as pd

if __name__ == '__main__':
    start = time.time()
    
    parser = argparse.ArgumentParser(description="Translate Pokemon ROM using given translation tables.")
    parser.add_argument("-r", "--rom", type=str,
                    help="path to pokemon rom")
    parser.add_argument("-p", "--pokemons", type=str,
                        help="path to pokemon list")
    parser.add_argument("-m", "--moves", type=str,
                    help="path to moves list")
    parser.add_argument("-t", "--tbl", type=str,
                help="path to TBL file")
    parser.add_argument('--uppercase', action='store_true')
    args = parser.parse_args()

    df_pokemons = pd.read_excel(args.pokemons)
    pokemons = Pokemons(df_pokemons, args.tbl, args.uppercase)
    df_translated_pkm = pokemons.get_pkm_dataframe()
    romfile = args.rom
    df_moves = pd.read_excel(args.moves)
    moves = Moves(df_moves, args.tbl, args.uppercase)
    df_translated_moves = moves.get_moves_dataframe()
    game = Game(romfile=romfile, pkm_dataframe=df_translated_pkm, moves_dataframe=df_translated_moves)
    game.replace_moves()
    game.replace_pkm_names()
    end = time.time()
    print("Time elapsed: ", end - start)
    game.save_translated_rom()