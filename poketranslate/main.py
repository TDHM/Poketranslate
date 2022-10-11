import sys
import argparse

import time

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

    pokemons = Pokemons(args.pokemons, args.tbl, args.uppercase)
    pkm_dataframe = pokemons.get_pkm_dataframe()
    romfile = args.rom
    moves = Moves(args.moves, args.tbl, args.uppercase)
    moves_dataframe = moves.get_moves_dataframe()
    game = Game(romfile=romfile, pkm_dataframe=pkm_dataframe, moves_dataframe=moves_dataframe)
    game.replace_moves()
    game.replace_pkm_names()
    end = time.time()
    print("Time elapsed: ", end - start)
    game.save_translated_rom()