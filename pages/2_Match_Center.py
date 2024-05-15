import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

import openpyxl, yattag
from openpyxl import load_workbook
from yattag import Doc, indent

from fungsiplot import vizone
from fungsiplot import tendang
from fungsiplot import ttendang
from fungsiplot import fulxg

st.set_page_config(page_title='Match Center', layout='wide')
st.markdown('# Match Center')

from menu import menu
menu()

df = pd.DataFrame()
for i in range(1,12):
  temp = pd.read_json('./data/'+str(i)+'.json')
  df = pd.concat([df, temp], ignore_index=True)

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)
dfxg = load_data(st.secrets["xgdata"])

col1, col2, col3 = st.columns(3)
with col1:
  komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='1')
with col2:
  gw = st.selectbox('Select GW', pd.unique(df['GW']), key='2')
  all_gws = st.checkbox('Select All GWs', key='5')
if all_gws:
  with col3:
    team = st.selectbox('Select Team', pd.unique(df['Team']), key='3')
  col1, col2 = st.columns(2)
  with col1:
    viz = st.selectbox('Select Visualization', ['Heatmap','Shots','Passes Attempted','Average Position',
                                                'Passes Received','Dribbles','Tackles','Intercepts',
                                                'Recoveries','Fouls','Possessions Lost'], key='11')
  with col2:
    temp = df[df['Team']==team]
    xgtemp = dfxg[dfxg['Team']==team].reset_index(drop=True)
    if (viz=='Passes Received'):
      pla = st.selectbox('Select Player', pd.unique(temp['Pas Name']), key='12')
      templa = temp[temp['Pas Name']==pla].reset_index(drop=True)
      all_pla = st.checkbox('Select All Players', key='13')
      if all_pla:
        vis = vizone(viz,temp)
      else:
        vis = vizone(viz,templa)
    elif (viz=='Shots'):
      pla = st.selectbox('Select Player', pd.unique(xgtemp['Player']), key='12')
      xgtemps = xgtemp[xgtemp['Player']==pla].reset_index(drop=True)
      all_pla = st.checkbox('Select All Players', key='13')
      if all_pla:
        vxg = ttendang(xgtemp)
      else:
        vxg = tendang(xgtemps)
    else:
      pla = st.selectbox('Select Player', pd.unique(temp['Act Name']), key='12')
      templa = temp[temp['Act Name']==pla].reset_index(drop=True)
      all_pla = st.checkbox('Select All Players', key='13')
      if all_pla:
        vis = vizone(viz,temp)
      else:
        vis = vizone(viz,templa)
  if (viz=='Shots'):
    st.pyplot(vxg)
  else:
    st.pyplot(vis)
else:
  with col3:
    temp = df[df['GW']==gw].reset_index(drop=True)
    xgtemp = dfxg[dfxg['GW']==gw].reset_index(drop=True)
    mat = st.selectbox('Select Match', pd.unique(temp['Match']), key='3')
  col1, col2 = st.columns(2)
  temp = temp[temp['Match']==mat].reset_index(drop=True)
  home = (temp['Match'].str.split(' -').str[0])[0]
  away = (temp['Match'].str.split('- ').str[1])[0]

  xgtemp2 = xgtemp[(xgtemp['Team']==home) | (xgtemp['Team']==away)].reset_index(drop=True)
  fuls = fulxg(xgtemp2,home,away)
  st.pyplot(fuls)
  
  with col1:
    ht = temp[temp['Team']==home].reset_index(drop=True)
    xgh = xgtemp[xgtemp['Team']==home].reset_index(drop=True)
    vizh = st.selectbox('Select Visualization', ['Heatmap','Shots','Passes Attempted','Average Position',
                                                 'Passes Received','Dribbles','Tackles','Intercepts',
                                                 'Recoveries','Fouls','Possessions Lost'], key='4')
    if (vizh=='Passes Received'):
      plah = st.selectbox('Select Player', pd.unique(ht['Pas Name']), key='6')
      htp = temp[temp['Pas Name']==plah].reset_index(drop=True)
      all_plah = st.checkbox('Select All Players', key='9')
      if all_plah:
        vish = vizone(vizh,ht)
      else:
        vish = vizone(vizh,htp)
      st.pyplot(vish)
    elif (vizh=='Shots'):
      plah = st.selectbox('Select Player', pd.unique(xgh['Player']), key='6')
      xghp = xgh[xgh['Player']==plah].reset_index(drop=True)
      all_plah = st.checkbox('Select All Players', key='9')
      if all_plah:
        vxgh = ttendang(xgh)
      else:
        vxgh = tendang(xghp)
      st.pyplot(vxgh)
    else:
      plah = st.selectbox('Select Player', pd.unique(ht['Act Name']), key='6')
      htp = temp[temp['Act Name']==plah].reset_index(drop=True)
      all_plah = st.checkbox('Select All Players', key='9')
      if all_plah:
        vish = vizone(vizh,ht)
      else:
        vish = vizone(vizh,htp)
      st.pyplot(vish)    
  with col2:
    at = temp[temp['Team']==away].reset_index(drop=True)
    xga = xgtemp[xgtemp['Team']==away].reset_index(drop=True)
    viza = st.selectbox('Select Visualization', ['Heatmap','Shots','Passes Attempted','Average Position',
                                                 'Passes Received','Dribbles','Tackles','Intercepts',
                                                 'Recoveries','Fouls','Possessions Lost'], key='7')
    if (viza=='Passes Received'):
      plaa = st.selectbox('Select Player', pd.unique(at['Pas Name']), key='8')
      atp = temp[temp['Pas Name']==plaa].reset_index(drop=True)
      all_plaa = st.checkbox('Select All Players', key='10')
      if all_plaa:
        visa = vizone(viza,at)
      else:
        visa = vizone(viza,atp)
      st.pyplot(visa)
    elif (viza=='Shots'):
      plaa = st.selectbox('Select Player', pd.unique(xga['Player']), key='8')
      xgap = xga[xga['Player']==plaa].reset_index(drop=True)
      all_plaa = st.checkbox('Select All Players', key='10')
      if all_plaa:
        vxga = ttendang(xga)
      else:
        vxga = tendang(xgap)
      st.pyplot(vxga)
    else:
      plaa = st.selectbox('Select Player', pd.unique(at['Act Name']), key='8')
      atp = temp[temp['Act Name']==plaa].reset_index(drop=True)
      all_plaa = st.checkbox('Select All Players', key='10')
      if all_plaa:
        visa = vizone(viza,at)
      else:
        visa = vizone(viza,atp)
      st.pyplot(visa)
    #st.write(temp[temp['Act Name']==pla].reset_index(drop=True))
    #st.image("./data/poster3.jpg")
