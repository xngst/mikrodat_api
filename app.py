import requests
import sqlite3
import warnings

from dataclasses import dataclass

import streamlit as st
import pandas as pd

#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode

warnings.filterwarnings("ignore")

def fetch_data_from_db(database_path, table_name):
    with sqlite3.connect(database_path) as conn:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
    return df

@dataclass
class Onkorm:
    name: str
    base_url: str
    db_folder: str
    db_detail: str
    db_biz: str
    db_test: str
    db_test_napirendi: str
    db_biz_napirendi: str    
    db_melleklet: str
    db_jegyzokv: str
    db_jegyz_dok: str
    db_hatarozat: str

DATABASE_PATH = 'onkorm.db'

ujbuda = Onkorm(name = "Újbuda",
                base_url="https://mikrodat.ujbuda.hu/app/cms/api/honlap", 
                db_folder="ujbuda_meghivo_mappa",
                db_detail="ujbuda_meghivo_reszlet",
                db_test = "ujbuda_test_meghivo",
                db_biz = "ujbuda_biz_meghivo",
                db_test_napirendi="ujbuda_test_napirendi",
                db_biz_napirendi="ujbuda_biz_napirendi",
                db_melleklet="ujbuda_melleklet",
                db_jegyzokv="ujbuda_jegyzokonyv",
                db_jegyz_dok="ujbuda_jegy_dok",
                db_hatarozat="ujbuda_hatarozatok",
               )

IIker = Onkorm(name = "Második kerület",
               base_url="https://testulet.masodikkerulet.hu/app/cms/api/honlap", 
               db_folder="IIker_inv_folders",
               db_detail="IIker_detail",
               db_biz = "IIker_biz_meghivo",
               db_test = "IIker_test_meghivo",
               db_test_napirendi="IIker_test_napirendi",
               db_biz_napirendi="IIker_biz_napirendi",
               db_melleklet="IIker_melleklet",
               db_jegyzokv="IIker_jegyzokonyv",
               db_jegyz_dok="IIker_jegy_dok",
               db_hatarozat="IIker_hatarozatok",
              )
 
fehervar = Onkorm(name="Székesfehérvár",
                  base_url="https://mikrodat.szekesfehervar.hu/app/cms/api/honlap", 
                  db_folder="fehervar_folders",
                  db_detail="fehervar_detail",
                  db_biz = "fehervar_biz_meghivo",
                  db_test = "fehervar_test_meghivo",
                  db_test_napirendi="fehervar_test_napirendi",
                  db_biz_napirendi="fehervar_biz_napirendi", 
                  db_melleklet="fehervar_melleklet",
                  db_jegyzokv="fehervar_jegyzokonyv",
                  db_jegyz_dok="fehervar_jegy_dok",
                  db_hatarozat="fehervar_hatarozatok",
                 )

onks = [ujbuda, IIker, fehervar]

st.title("Önkormányzat Frontend teszt")

col1, col2, col3 = st.columns(3)

onk_dict = {"Újbuda":ujbuda,"Második kerület":IIker,"Székesfehérvár":fehervar}

with col1:
    onkorm = st.selectbox("Önkormányzat",(ujbuda.name, IIker.name, fehervar.name))
    onk = onk_dict[onkorm]
    year_url = f"{onk.base_url}/inv/years"
    inv_year_r = requests.get(year_url, verify=False)
    years = inv_year_r.json()['content']

with col2:
    year = st.selectbox("Év",years)
    
with col3:
	detail_df = fetch_data_from_db(DATABASE_PATH, onk.db_detail)
	bizottsagok = list(detail_df["nev"].unique())
	#bizottsagok.append("Mindegyik")
	bizottsagok.insert(0, "Mindegyik")
	bizottsag = st.selectbox("Bizottság",bizottsagok,index=0)

if year:
	folder_df = fetch_data_from_db(DATABASE_PATH, onk.db_folder)
	folder_df = folder_df[folder_df['datum'].str.contains(f'^{year}')]
	folder_df.reset_index(drop=True, inplace=True)
	folder_df.index += 1
	
	detail_df = fetch_data_from_db(DATABASE_PATH, onk.db_detail)
	merged = folder_df.merge(detail_df,on="uuid",how="left")
	narrow_df = merged[["datum_x","idopont_x","kategoria_x","nev","uuid","name","dateLastModified"]]
	narrow_df.columns = ["Dátum","Időpont","Kategória","Bizottság","uuid","name","dateLastModified"]

if bizottsag: 
	if bizottsag == "Mindegyik":
		folder_df = fetch_data_from_db(DATABASE_PATH, onk.db_folder)
		folder_df.index += 1
		detail_df = fetch_data_from_db(DATABASE_PATH, onk.db_detail)
		merged = folder_df.merge(detail_df,on="uuid",how="left")
		narrow_df = merged[["datum_x","idopont_x","kategoria_x","nev","uuid","name","dateLastModified"]]
		narrow_df.columns = ["Dátum","Időpont","Kategória","Bizottság","uuid","name","dateLastModified"]
		st.dataframe(narrow_df)

	else:
		narrow_df = narrow_df[narrow_df["Bizottság"] == bizottsag]
		st.dataframe(narrow_df)
		

