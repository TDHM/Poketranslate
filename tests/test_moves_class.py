import pytest

from poketranslate.moves import Moves

import pandas as pd

@pytest.fixture
def moves():
    pkm_ex_fr = ["Métamorph", "Monaflèmit", "Embrylex"]
    pkm_ex_en = ["Ditto", "Slaking", "Larvitar"]
    df_pkm = pd.DataFrame({"Source": pkm_ex_fr, "Translation": pkm_ex_en})
    pkms = pokemons.Pokemons(df_pkm, "./tbl/pkm_crystal.tbl", uppercase=True)
    
    return pkms

def test_generate_hex_translation(pkms):
    assert pkms.df_pokemons["Source"] == ["METAMORPH", "MONAFLEMIT", "EMBRYLEX"]
    assert pkms.df_pokemons["Translation"] == ["DITTO", "SLAKING", "LARVITAR"]

    pkms.df_pokemons["Source_hex"] ==
    pkms.df_pokemons["Translation_hex"] == 
    pkms.df_pokemons["padded_Source_hex"] == 
    pkms.df_pokemons["padded_Translation_hex"] ==