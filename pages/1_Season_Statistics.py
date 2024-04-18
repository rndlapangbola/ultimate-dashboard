import sys
import io
import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
import urllib

from listfungsi import data_team
from listfungsi import data_player
from listfungsi import get_list
from listfungsi import get_detail

st.set_page_config(page_title='Full Season Statistics', layout='wide')
st.markdown('# Statistics')

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)

df1 = load_data(st.secrets["datateam"])
df2 = load_data(st.secrets["datapemain"])

from datetime import date
df1['Date'] = pd.to_datetime(df1.Date)
df1['Month'] = df1['Date'].dt.strftime('%B')
df22 = get_detail(df2)
df = pd.merge(df1, df2.drop(['Name'], axis=1), on='Player ID', how='left')
fulldata = get_detail(df)
mlist = get_list(fulldata)

from datetime import date
date = date.today().strftime("%Y-%m-%d")

teams, players = st.tabs(['Team Stats', 'Player Stats'])

with teams:
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='3')
  with col2:
    temp_full = fulldata[fulldata['Kompetisi']==komp]
    month = st.multiselect('Select Month', pd.unique(temp_full['Month']), key='14')
    all_mos = st.checkbox('Select All Months', key='301')
    if all_mos:
      month = pd.unique(temp_full['Month'])
  with col3:
    temp_full = temp_full[temp_full['Month'].isin(month)]
    venue = st.multiselect('Select Venue', pd.unique(temp_full['Home/Away']), key='5')
  with col4:
    temp_full = temp_full[temp_full['Home/Away'].isin(venue)]
    gw = st.multiselect('Select Gameweek', pd.unique(temp_full['Gameweek']), key='4')
    all_gws = st.checkbox('Select All GWs', key='302')
    if all_gws:
      gw = pd.unique(temp_full['Gameweek'])
  with col5:
    cat = st.selectbox('Select Category', ['Goal Threat', 'in Possession', 'out of Possession', 'Misc'], key='13')
  show_tim_data = data_team(fulldata, komp, month, gw, venue, cat)

  buffer = io.BytesIO()
  with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    show_tim_data.to_excel(writer, sheet_name='Sheet1', index=False)
  download = st.download_button(
    label="Download data as Excel",
    data=buffer.getvalue(),
    file_name='team-data_downloaded ('+date+').xlsx',
    mime='application/vnd.ms-excel',
    key = 0)
  
  st.write(show_tim_data)

    
