import pytest

import pandas as pd
import poketranslate.pokemons as pokemons

@pytest.fixture
def pkm_list():
    pkm_ex_fr = ["Métamorph", "Monaflèmit", "Embrylex"]
    pkm_ex_en = ["Ditto", "Slaking", "Larvitar"]
    df_pkm = pd.DataFrame({"Source": pkm_ex_fr, "Translation": pkm_ex_en})
    return df_pkm

@pytest.fixture
def tbl_data():
    with open("./tbl/pkm_crystal.tbl", 'r') as f:
        tbl_data = f.read()
    return tbl_data