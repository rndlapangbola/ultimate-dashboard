import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

import openpyxl, yattag
from openpyxl import load_workbook
from yattag import Doc, indent

st.set_page_config(page_title='Match Center', layout='wide')
st.markdown('# Match Center')

df = pd.DataFrame()
for i in range(1,11):
  temp = pd.read_json('./data/'+str(i)+'.json')
  df = pd.concat([df, temp], ignore_index=True)

col1, col2, col3 = st.columns(3)
with col1:
  komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='1')
with col2:
  gw = st.selectbox('Select GW', pd.unique(df['GW']), key='2')
  all_gws = st.checkbox('Select All GWs', key='5')
if all_gws:
  with col3:
    team = st.selectbox('Select Team', pd.unique(df['Team']), key='3')
else:
  with col3:
    temp = df[df['GW']==gw].reset_index(drop=True)
    mat = st.selectbox('Select Match', pd.unique(temp['Match']), key='3')
col1, col2, col3 = st.columns(3)
with col1:
  temp = temp[temp['Match']==mat]
  temp = temp[temp['Team']=='Bali United FC'].reset_index(drop=True)
  viz = st.selectbox('Select Visualization', ['Heatmap','Shots','Passes','Dribbles',
                                              'Tackles','Intercepts','Recoveries','Fouls',
                                              'Possessions Lost','Aerials'], key='4')
  pla = st.selectbox('Select Player', pd.unique(temp['Act Name']), key='6')
  st.write(temp[temp['Act Name']==pla].reset_index(drop=True))
#st.image("./data/poster3.jpg")
