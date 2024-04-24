import sys
import io
import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
import urllib

from listfungsi import get_detail
from listfungsi import get_pct
from listfungsi import get_playerlist

st.set_page_config(page_title='Player Search', layout='wide')
st.markdown('# Search')

from menu import menu
menu()

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)

df1 = load_data(st.secrets["datateam"])
df2 = load_data(st.secrets["datapemain"])

with st.expander('Open'):
    col1, col2 = st.columns(2)
    with col1:
        komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='3')
    with col2:
        mins = st.number_input('Input minimum mins. played', min_value=90, step=90, key='4')
    rank_pct = get_pct(df1, df2, mins, komp)[2]

db_temp = get_detail(df2)
db_temp2 = db_temp[['Name','Age Group','Nat. Status']]
temple = pd.merge(rank_pct, db_temp2, on='Name', how='left')
templist = rank_pct.drop(['Name','Position','Team','MoP','Kompetisi'], axis=1)
metlist = list(templist)

col1, col2= st.columns(2)
with col1:
  pos = st.selectbox('Select Position', pd.unique(temple['Position']), key='87')
  nats = st.multiselect('Select Nat. Status', ['Foreign', 'Local'], key='86')
with col2:
  ages = st.multiselect('Select Age Groups', ['Senior', 'U23'], key='88')
  arr_met = st.multiselect('Select Metrics', metlist, key='84')

playlist = get_playerlist(temple, komp, pos, mins, nats, ages, arr_met)

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    playlist.to_excel(writer, sheet_name='Sheet1', index=False)
download = st.download_button(
    label="Download data as Excel",
    data=buffer.getvalue(),
    file_name='player-list.xlsx',
    mime='application/vnd.ms-excel', key = 0)

st.dataframe(playlist.head(10))
