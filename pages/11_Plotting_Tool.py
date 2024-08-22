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
from listfungsi import get_cs
from listfungsi import milestone

st.set_page_config(page_title='Full Season Statistics', layout='wide')
st.markdown('# Statistics')

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)

df1 = load_data(st.secrets["newfull"])
df2 = load_data(st.secrets["datapemain"])
histdata = load_data(st.secrets["hist"])

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
        mime='application/vnd.ms-excel', key = 0)
    st.write(show_tim_data)

with players:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='6')
        temp_pull = fulldata[fulldata['Kompetisi']==komp]
        team = st.multiselect('Select Teams', pd.unique(temp_pull['Team']), key='10')
        all_teams = st.checkbox('Select All Teams', key='303')
        if all_teams:
            team = pd.unique(temp_pull['Team'])
    with col2:
        temp_pull = temp_pull[temp_pull['Team'].isin(team)]
        pos = st.multiselect('Select Positions', pd.unique(temp_pull['Position']), key='7')
        all_poss = st.checkbox('Select All Positions', key='304')
        if all_poss:
             pos = pd.unique(temp_pull['Position'])
        temp_pull = temp_pull[temp_pull['Position'].isin(pos)]
        age = st.multiselect('Select Age Group', pd.unique(temp_pull['Age Group']), key='11')
    with col3:
        temp_pull = temp_pull[temp_pull['Age Group'].isin(age)]
        nat = st.multiselect('Select Nationality', pd.unique(temp_pull['Nat. Status']), key='8')
        temp_pull = temp_pull[temp_pull['Nat. Status'].isin(nat)]
        month = st.multiselect('Select Month', pd.unique(temp_pull['Month']), key='12')
        all_mos = st.checkbox('Select All Months', key='305')
        if all_mos:
            month = pd.unique(temp_pull['Month'])
    with col4:
        temp_pull = temp_pull[temp_pull['Month'].isin(month)]
        venue = st.multiselect('Select Venue', pd.unique(temp_pull['Home/Away']), key='9')
        temp_pull = temp_pull[temp_pull['Home/Away'].isin(venue)]
        gw = st.multiselect('Select Gameweek', pd.unique(temp_pull['Gameweek']), key='17')
        all_gws = st.checkbox('Select All GWs', key='306')
        if all_gws:
            gw = pd.unique(temp_pull['Gameweek'])
    with col5:
        mins = st.number_input('Input minimum mins. played', min_value=0,
                               max_value=3060, step=90, key=18)
        metrik = st.multiselect('Select Metrics', mlist, key='19')
    cat = st.selectbox('Select Category', ['Total', 'per 90'], key='16')
    show_player_data = data_player(fulldata, komp, team, pos, month, venue,
                                   gw, age, nat, metrik, mins, cat, df22)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        show_player_data.to_excel(writer, sheet_name='Sheet1', index=False)
    download = st.download_button(
        label="Download data as Excel",
        data=buffer.getvalue(),
        file_name='player-data_downloaded ('+date+').xlsx',
        mime='application/vnd.ms-excel', key = 1)
    st.write(show_player_data)

from menu import menu
menu()
