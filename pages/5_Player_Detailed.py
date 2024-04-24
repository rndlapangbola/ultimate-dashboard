import sys
import io
import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
import urllib

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.patches as patches
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch

from fungsiplot import beli_pizza
from fungsiplot import plot_compare

from listfungsi import data_team
from listfungsi import data_player
from listfungsi import get_list
from listfungsi import get_detail
from listfungsi import get_radar
from listfungsi import get_simi
from listfungsi import get_pct
from menu import menu

menu()

st.set_page_config(page_title='Player Detailed', layout='wide')
st.markdown('# Player Detailed')

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)

df1 = load_data(st.secrets["datateam"])
df2 = load_data(st.secrets["datapemain"])
th = load_data(st.secrets["th"])
cf = load_data(st.secrets["cf"])
cd = load_data(st.secrets["cd"])

from datetime import date
df1['Date'] = pd.to_datetime(df1.Date)
df1['Month'] = df1['Date'].dt.strftime('%B')
df22 = get_detail(df2)
df = pd.merge(df1, df2.drop(['Name'], axis=1), on='Player ID', how='left')
fulldata = get_detail(df)
mlist = get_list(fulldata)

col1, col2 = st.columns(2)
with col1:
    mins = st.number_input('Input minimum mins. played', min_value=90, max_value=3060, step=90, key=96)
with col2:
    komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='101')
rank_p90 = get_pct(df1, df2, mins, komp)[0]
rank_tot = get_pct(df1, df2, mins, komp)[1]
rank_pct = get_pct(df1, df2, mins, komp)[2]
col2, col3, col4 = st.columns(3)
with col2:
    tempp = rank_p90[rank_p90['Kompetisi']==komp]
    klub = st.selectbox('Select Team', pd.unique(tempp['Team']), key='102')
with col3:
    tempp = tempp[tempp['Team']==klub]
    pos = st.selectbox('Select Position', pd.unique(tempp['Position']), key='103')
with col4:
    tempp = tempp[tempp['Position']==pos]
    ply = st.selectbox('Select Player', pd.unique(tempp['Name']), key='104')

col5, col6 = st.columns(2)
with col5:
    rdr = get_radar(rank_pct,rank_p90,rank_tot,pos,ply)
    rdr['Percentile'] = rdr['Percentile']/100
    st.subheader(ply+' Scouting Report')
    st.caption('vs '+pos+' in '+komp+' | Min. '+str(mins)+' mins played')
    st.data_editor(rdr, column_config={'Percentile':st.column_config.ProgressColumn('Percentile',width='medium',min_value=0,max_value=1)},hide_index=True)
        
with col6:
    smr = get_simi(rank_p90,df2,ply,pos)
    st.subheader('Similar Players to '+ply)
    st.dataframe(smr.head(7), hide_index=True)
col7, col8 = st.columns(2)
with col7:
    piz = beli_pizza(komp, pos, klub, ply, rank_pct, mins)
    with open('pizza.jpg', 'rb') as img:
        fn = 'Perf.Radar_'+ply+'.jpg'
        btn = st.download_button(label="Download Report as a Radar!", data=img,
                                 file_name=fn, mime="image/jpg")
with col8:
    #mirip = smr.head(7)
    ply2 = st.selectbox('Select Similar Player', pd.unique(smr.head(7)['Name']), key='105')
    #ply2 = st.text_input('Select Similar Player', placeholder='Select Similar Player')
    cpre = plot_compare(ply, ply2, pos, rank_p90)
    st.pyplot(cpre)
