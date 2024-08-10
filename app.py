import requests
import sqlite3
import warnings
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from st_aggrid import AgGrid, GridOptionsBuilder
warnings.filterwarnings("ignore")

def fetch_data_from_db(database_path, table_name):
    ""
    with sqlite3.connect(database_path) as conn:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
    return df

def biz_napirendi_df(DATABASE_PATH,onk,folder_uuid):
	with sqlite3.connect(DATABASE_PATH) as conn:
		query = f"SELECT * FROM {onk.db_biz_napirendi} WHERE folder_uuid='{folder_uuid}'"
		df = pd.read_sql_query(query, conn)
		df.sort_values(by="napirend",inplace=True)
		df.reset_index(drop=True, inplace=True)
		df.index += 1
		return df
		
def test_napirendi_df(DATABASE_PATH,onk,folder_uuid):
	with sqlite3.connect(DATABASE_PATH) as conn:
		query = f"SELECT * FROM {onk.db_test_napirendi} WHERE folder_uuid='{folder_uuid}'"
		df = pd.read_sql_query(query, conn)
		df.sort_values(by="napirend",inplace=True)
		df.reset_index(drop=True, inplace=True)
		df.index += 1
		return df 
		
def filter_df(df: pd.DataFrame, year:str, bizottsag=None):
	if year:
		dff = df[df['Dátum'].str.contains(f'^{year}', na=False)]

	if bizottsag != "Mindegyik":
		dff = dff[dff["Bizottság"] == bizottsag]
	dff.reset_index(drop=True, inplace=True)	
	dff.index += 1
	return dff

def	aggrid_settings(df,hidden_cols=None,wrap_cols=None):
	gb = GridOptionsBuilder.from_dataframe(df)
	gb.configure_selection('single')
	
	if wrap_cols:
		for col in wrap_cols:
			gb.configure_column(col, wrapText=True, autoHeight=True)
			
	if hidden_cols:
		for col in hidden_cols:
			gb.configure_column(col, hide=True)
	grid_options = gb.build()
	
	return grid_options

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

onk_dict = {"Újbuda":ujbuda,
"Második kerület":IIker,
"Székesfehérvár":fehervar}

with col1:
    onkorm = st.selectbox("Önkormányzat",(ujbuda.name, 
    IIker.name, 
    fehervar.name)
    )
    onk = onk_dict[onkorm]
    year_url = f"{onk.base_url}/inv/years"
    inv_year_r = requests.get(year_url, verify=False)
    years = inv_year_r.json()['content']

with col2:
    year = st.selectbox("Év",years,index=0)
    
with col3:
	detail_df = fetch_data_from_db(DATABASE_PATH, onk.db_detail)
	bizottsagok = list(detail_df["nev"].unique())
	bizottsagok.insert(0, "Mindegyik")
	bizottsag = st.selectbox("Bizottság",bizottsagok,index=0)
	
if year and bizottsag:
	folder_df = fetch_data_from_db(DATABASE_PATH, onk.db_folder)
	detail_df = fetch_data_from_db(DATABASE_PATH, onk.db_detail)
	merged = folder_df.merge(detail_df,on="uuid",how="left")
	narrow_df = merged[["datum_x","idopont_x","kategoria_x","nev","uuid"]]
	narrow_df.columns = ["Dátum","Időpont","Kategória","Bizottság","uuid"]
	narrow_df = filter_df(narrow_df,year,bizottsag)
	grid_options = aggrid_settings(narrow_df,['uuid'])
	grid_response = AgGrid(narrow_df, gridOptions=grid_options, update_mode='SELECTION_CHANGED')


try:
	selected_row = grid_response['selected_rows']
	st.subheader(f"{selected_row['Dátum'].iloc[0]} {selected_row['Bizottság'].iloc[0]}")
	folder_uuid = selected_row['uuid'].iloc[0]
	
	if "testület" in selected_row['Bizottság'].iloc[0]:
		test_napi_df = test_napirendi_df(DATABASE_PATH,onk,folder_uuid)
		test_napi_df = test_napi_df[["targy","eloterjeszto"]]
		if len(test_napi_df) == 0:
			st.warning("Nincs megjeleníthető adat")
		else:
			napirendi_list = list(test_napi_df["targy"])
			napirendi_list.insert(0, "Napirendi pontok:")
			selected = st.selectbox("",napirendi_list)
			if selected:
				st.dataframe(test_napi_df[test_napi_df["targy"]==selected])
				st.write("Előterjesztés")
				st.write("...")
				st.write("Döntési javaslatok")
				st.write("...")
				st.write("Mellékletek")
				
			
	else:
		biz_napi_df = biz_napirendi_df(DATABASE_PATH,onk,folder_uuid)
		biz_napi_df = biz_napi_df[["targy","eloterjeszto"]]
		if len(biz_napi_df) == 0:
			st.warning("Nincs megjeleníthető adat")
		else:
			napirendi_list = list(biz_napi_df["targy"])
			napirendi_list.insert(0, "Napirendi pontok:")
			selected = st.selectbox("",napirendi_list)
			if selected:
				selected_df = biz_napi_df[biz_napi_df["targy"]==selected]
				if len(selected_df) > 0:
					st.write("Előterjesztés")
					st.write("* elo.pdf")
					st.write("Döntési javaslatok")
					st.write("* jav.pdf")
					st.write("Mellékletek")
					st.write("* melleklet.pdf")

except Exception as e:
	pass
	
with st.expander("Jegyzőkönyv"):
	st.write("TODO")
	
with st.expander("Határozatok"):
	st.write("TODO")	
		


