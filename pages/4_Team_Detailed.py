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

from fungsiplot import plot_skuad
from fungsiplot import plot_skuadbar
from fungsiplot import plot_form

from listfungsi import data_team
from listfungsi import data_player
from listfungsi import get_list
from listfungsi import get_detail
from listfungsi import get_pssw
from listfungsi import get_wdl
from listfungsi import get_skuad
from listfungsi import get_formasi
from menu import menu

st.set_page_config(page_title='Team Detailed', layout='wide')
st.markdown('# Team Detailed')

menu()

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

col1, col2, col3 = st.columns(3)
with col1:
  komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='50')
with col2:
  smt = fulldata[fulldata['Kompetisi']==komp]
  team = st.selectbox('Select Team', pd.unique(smt['Team']), key='51')
with col3:
  smt = smt[smt['Team']==team]
  gw = st.multiselect('Select GWs', pd.unique(smt['Gameweek']), key='52')
  all_gws = st.checkbox('Select All GWs', key='307')
  if all_gws:
    gw = pd.unique(smt['Gameweek'])
ds = get_pssw(fulldata, th, team, gw)
ds = ds.replace('', pd.NA)
ps = ['PS1','PS2','PS3','PS4','PS5']
s = ['S1','S2','S3','S4','S5','S6','S7']
w = ['W1','W2','W3','W4','W5','W6','W7']

col1, col2 = st.columns(2)
with col1:
  st.subheader(team+'\'s Results')
  rslt = get_wdl(fulldata, team, gw)
  st.dataframe(rslt, hide_index=True)
with col2:
  st.subheader(team+'\'s Squad List')
  skd = get_skuad(df1, df2, team, gw)
  st.dataframe(skd)

st.subheader(team+'\'s Squad - % of Minutes Played')
col1, col2 = st.columns(2)
with col1:
  skbr = plot_skuadbar(df1, df2, team, gw)
  st.pyplot(skbr)
with col2:
  sksc = plot_skuad(df1, df2, team, gw)
  st.pyplot(sksc)

st.subheader(team+'\'s Characteristics')
col1, col2, col3 = st.columns(3)
with col1:
  st.markdown('**Play Style**')
  for col in ds[ps]:
    if (ds[col].isnull().values.any() == False):
      st.markdown(':large_yellow_square:'+' '+list(ds[col])[0])
with col2:
  st.markdown('**Strengths**')
  for col in ds[s]:
    if (ds[col].isnull().values.any() == False):
      st.markdown(':large_green_square:'+' '+list(ds[col])[0])
with col3:
  st.markdown('**Weaknesses**')
  for col in ds[w]:
    if (ds[col].isnull().values.any() == False):
      st.markdown(':large_red_square:'+' '+list(ds[col])[0])

st.subheader(team+'\'s Starting Formation')
gw2 = st.selectbox('Select GW', pd.unique(smt['Gameweek']), key='53')
full_form = get_formasi(df1, cd)
sf = plot_form(full_form, cf, team, gw2)

st.pyplot(sf)
