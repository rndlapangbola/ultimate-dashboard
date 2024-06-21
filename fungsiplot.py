import os
import pandas as pd
import glob
from datetime import date
import numpy as np
from sklearn import preprocessing

from mplsoccer import Pitch, VerticalPitch, PyPizza, Radar, grid
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.font_manager as fm
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as patches
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)

from PIL import Image
from tempfile import NamedTemporaryFile
import urllib
import os

posdict = {'gk':{'position':'Goalkeeper',
                 'metrics':['Name','Long Goal Kick Ratio','Pass Accuracy','Cross Claim',
                            'Keeper - Sweeper','Saves','Save Ratio','Penalty Save']},
           'cb':{'position':'Center Back',
                 'metrics':['Name','Shots','Goals','Assist','Pass Accuracy',
                            'Tackle','Intercept','Recovery','Blocks','Aerial Won Ratio']},
           'fb':{'position':'Fullback',
                 'metrics':['Name','Shots','Goals','Create Chance','Assist','Pass Accuracy','Dribble',
                            'Cross','Tackle','Intercept','Recovery','Blocks','Aerial Won Ratio']},
           'cm':{'position':'Midfielder',
                 'metrics':['Name','Shots','Goals','Create Chance','Shot on Target Ratio','Assist',
                            'Pass Accuracy','Dribble','Tackle','Intercept','Recovery','Blocks']},
           'cam/w':{'position':'Attacking 10/Winger',
                    'metrics':['Name','Shots','Goals','Create Chance','Shot on Target Ratio',
                               'Conversion Ratio','Assist','Pass Accuracy','Dribble','Cross',
                               'Tackle','Intercept','Recovery']},
           'fw':{'position':'Forward',
                 'metrics':['Name','Shots','Goals','Create Chance','Shot on Target Ratio',
                            'Conversion Ratio','Assist','Pass Accuracy','Dribble','Tackle',
                            'Intercept','Recovery','Aerial Won Ratio']}}

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Bold.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

bold = fm.FontProperties(fname=f.name)

github_url = 'https://github.com/google/fonts/blob/main/ofl/poppins/Poppins-Regular.ttf'
url = github_url + '?raw=true'

response = urllib.request.urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

reg = fm.FontProperties(fname=f.name)

path_eff = [path_effects.Stroke(linewidth=2, foreground='#ffffff'),
            path_effects.Normal()]

hcolors = ['#ffffff', '#d5dcdc', '#acb9b9', '#839696', '#597373', '#305050', '#062d2d']
hcmap = ListedColormap(hcolors, name="hcmap")
hcmapr = hcmap.reversed()

acolors = ['#052d2d', '#094329', '#0b5825', '#0e6e21', '#10841d', '#129919', '#15af15']
acmap = ListedColormap(acolors, name="acmap")
acmapr = acmap.reversed()

def plot_skuad(data, data2, team, gws):
  df = data.copy()
  db = data2.copy()

  gw_list = gws

  import datetime as dt
  from datetime import date

  today = date.today()
  db['Age'] = db['DoB'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))

  df = df[df['Team']==team]
  df = df[df['Gameweek'].isin(gw_list)]
  fil = df[['Player ID','MoP']]
  fil = fil.groupby('Player ID', as_index=False).sum()
  fil = fil[fil['MoP']>0]
  fil['%Min'] = round(((fil['MoP']/(df['Gameweek'].max()*90))*100),2)

  fin = pd.merge(fil, db, on='Player ID', how='left')
  fin = fin[['Nickname','Age','%Min']]

  fig, ax = plt.subplots(figsize=(10,10), dpi=500)
  fig.patch.set_facecolor('#ffffff')
  ax.set_facecolor('#ffffff')
  ax.grid(ls='--', color='#000000', alpha=0.2)

  ax.scatter(fin['Age'], fin['%Min'], color='#7ed957', s=150, edgecolors='#ffffff', zorder=10)

  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['bottom'].set_color('#000000')
  ax.spines['left'].set_color('#000000')

  for t in ax.xaxis.get_ticklines(): t.set_color('#000000')
  ax.tick_params(axis='x', colors='#000000')

  for t in ax.yaxis.get_ticklines(): t.set_color('#000000')
  ax.tick_params(axis='y', colors='#000000')

  for tick in ax.get_xticklabels():
    tick.set_fontproperties(bold)

  for tick in ax.get_yticklabels():
    tick.set_fontproperties(bold)

  ax.axvline(x=23.5, color='#f2ff00', linestyle='--', alpha=0.7, zorder=2)
  ax.fill_between([15,23.5], 0, 100, color='#f2ff00', alpha=0.4)
  ax.text(19.25, 50,'U-23 PLAYER', ha='center', va='center', color='#000000',
          fontproperties=bold, size=16, rotation=90, alpha=0.7)

  ax.set_xticks([15, 20, 25, 30, 35, 40])
  ax.set_yticks([0, 20, 40, 60, 80, 100])
  ax.set_ylim(bottom=0)
  ax.set_ylim(top=100)
  ax.set_xlim(left=15)
  ax.set_xlim(right=40)

  ax.set_xlabel('Age', color='#000000', fontproperties=bold, size=11)
  ax.set_ylabel('% Mins Played', color='#000000', fontproperties=bold, size=11)

  for i in range(len(fin)):
    ax.annotate(fin['Nickname'][i], xy=(fin['Age'][i]+0.5, fin['%Min'][i]), c='#000000', va='center',
                zorder=11, ha='left', size=6, weight='bold', path_effects=path_eff)

  plt.savefig('skuadsca.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
  
  return fig
  

def plot_skuadbar(data, data2, team, gws):
  df = data.copy()
  db = data2.copy()

  gw_list = gws

  import datetime as dt
  from datetime import date

  today = date.today()
  db['Age'] = db['DoB'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))

  df = df[df['Team']==team]
  df = df[df['Gameweek'].isin(gw_list)]
  fil = df[['Player ID','MoP']]
  fil = fil.groupby('Player ID', as_index=False).sum()
  fil = fil[fil['MoP']>0]

  fin = pd.merge(fil, db, on='Player ID', how='left')
  fin = fin[['Nickname','Age','MoP']]
  fin['Range'] = '0'

  for i in range(len(fin)):
    if (fin['Age'][i]<24):
      fin['Range'][i] = '15-24'
    elif (fin['Age'][i]>=24) and (fin['Age'][i]<31):
      fin['Range'][i] = '24-30'
    elif (fin['Age'][i]>=31) and (fin['Age'][i]<36):
      fin['Range'][i] = '31-35'
    else:
      fin['Range'][i] = '35+'
    
  fin = fin[['Range','MoP']]
  fin = fin.groupby('Range', as_index=False).sum()
  fin['%Min'] = round(((fin['MoP']/fin['MoP'].sum())*100),0)

  fig, ax = plt.subplots(figsize=(10,10), dpi=500)
  fig.patch.set_facecolor('#ffffff')
  ax.set_facecolor('#ffffff')

  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['bottom'].set_color('#000000')
  ax.spines['left'].set_color('#000000')

  for t in ax.xaxis.get_ticklines(): t.set_color('#000000')
  ax.tick_params(axis='x', colors='#000000')

  for t in ax.yaxis.get_ticklines(): t.set_color('#000000')
  ax.tick_params(axis='y', colors='#000000')

  for tick in ax.get_xticklabels():
    tick.set_fontproperties(bold)

  for tick in ax.get_yticklabels():
    tick.set_fontproperties(bold)
  
  bar = ax.barh(fin['Range'], fin['%Min'], color='#7ed957')

  for bar in bar.patches:
    ax.annotate(str(format(bar.get_width(), '.0f'))+'%',
              (bar.get_width()/2,
               bar.get_y() + bar.get_height()/2), ha='center', va='center',
              size=14, xytext=(0, 8), fontproperties=bold,
              textcoords='offset points',color='#000000')

  ax.set_xticks([0, 20, 40, 60, 80, 100])
  ax.set_xlim(right=100)
  ax.set_ylabel('Age Range', color='#000000', fontproperties=bold, size=11)
  ax.set_xlabel('% Mins Played', color='#000000', fontproperties=bold, size=11)


  plt.savefig('skuadbar.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
  
  return fig

def plot_form(data, data2, team, gw):
  df = data.copy()
  cf = data2.copy()

  dft = df[df['Team']==team].reset_index(drop=True)
  temp = dft[dft['Gameweek']==gw].reset_index(drop=True)
  temp['Formation'] = temp['Formation'].astype(str)
  cf = cf[cf['Formation']==temp['Formation'][0]].reset_index(drop=True)

  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  pitch = VerticalPitch(half=True, pitch_type='wyscout', corner_arcs=True,
                        pitch_color='#ffffff', line_color='#000000',
                        stripe_color='#fcf8f7', goal_type='box', pad_bottom=5,
                        pad_right=0.5, pad_left=0.5, stripe=True, linewidth=3.5)
  pitch.draw(ax=ax)
  #ax.add_patch(FancyBboxPatch((0, 45), 200, 4.5, fc='#ffffff', ec='#ffffff', lw=2))

  cf['X'] = 100 - cf['X']
  ax.scatter(cf['Y'], cf['X'], color='#7ed957', s=2500, edgecolors='#f2ff00', lw=4)
  for i in range(len(cf)):
    pitch.annotate(cf['Position'][i], xy=(cf['X'][i], cf['Y'][i]), c='#000000', va='center', zorder=11,
                   ha='center', size=16, weight='bold', ax=ax, path_effects=path_eff)
  
  mst = dft.drop(['Gameweek','Team'], axis=1).groupby('Formation', as_index=False).count()
  mst = mst.sort_values(by='Match', ascending=False).reset_index(drop=True)
  fmt = mst['Formation'][0]
  jml = mst['Match'].max()

  ax.annotate(text='Most Used Starting Formation: '+fmt+' ('+str(jml)+')',
              size=14, xy=(1, 49), xytext=(0,-18),
              textcoords='offset points', color='black', ha='left',
              zorder=9, va='center', fontproperties=bold)
  ax.annotate(text='Match: '+temp['Match'][0], size=14, xy=(0, 102), xytext=(0,-18),
              textcoords='offset points', color='black', ha='left',
              zorder=9, va='center', fontproperties=bold)
  
  plt.savefig('stafor.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')

  return fig

def beli_pizza(komp, pos, klub, name, data, mins):
  df = data.copy()
  df = df[df['Position']==pos]

  #DATA 
  if (pos=='Forward'):
    temp = df[posdict['fw']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average FW')].reset_index(drop=True)
    slice_colors = ["#22af15"] * 5 + ["#adaf15"] * 1 + ["#a215af"] * 2 + ["#2115af"] * 4
    text_colors = ["#FAFAFA"] * 5 + ["#0E1117"] * 1 + ["#FAFAFA"] * 6

  elif (pos=='Winger') or (pos=='Attacking 10'):
    temp = df[posdict['cam/w']['metrics']].reset_index(drop=True)
    if (pos=='Winger'):
      temp = temp[(temp['Name']==name) | (temp['Name']=='Average W')].reset_index(drop=True)
    else:
      temp = temp[(temp['Name']==name) | (temp['Name']=='Average CAM')].reset_index(drop=True)
        
    slice_colors = ["#22af15"] * 5 + ["#adaf15"] * 1 + ["#a215af"] * 3 + ["#2115af"] * 3
    text_colors = ["#FAFAFA"] * 5 + ["#0E1117"] * 1 + ["#FAFAFA"] * 6

  elif (pos=='Midfielder'):
    temp = df[posdict['cm']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average CM')].reset_index(drop=True)
        
    slice_colors = ["#22af15"] * 4 + ["#adaf15"] * 1 + ["#a215af"] * 2 + ["#2115af"] * 4
    text_colors = ["#FAFAFA"] * 4 + ["#0E1117"] * 1 + ["#FAFAFA"] * 6

  elif (pos=='Fullback'):
    temp = df[posdict['fb']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average FB')].reset_index(drop=True)
        
    slice_colors = ["#22af15"] * 3 + ["#adaf15"] * 1 + ["#a215af"] * 3 + ["#2115af"] * 5
    text_colors = ["#FAFAFA"] * 3 + ["#0E1117"] * 1 + ["#FAFAFA"] * 8

  elif (pos=='Center Back'):
    temp = df[posdict['cb']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average CB')].reset_index(drop=True)
        
    slice_colors = ["#22af15"] * 2 + ["#adaf15"] * 1 + ["#a215af"] * 1 + ["#2115af"] * 5
    text_colors = ["#FAFAFA"] * 2 + ["#0E1117"] * 1 + ["#FAFAFA"] * 6

  elif (pos=='Goalkeeper'):
    temp = df[posdict['gk']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==name) | (temp['Name']=='Average GK')].reset_index(drop=True)
        
    slice_colors = ["#22af15"] * 2 + ["#a215af"] * 5
    text_colors = ["#FAFAFA"] * 7

  #temp = temp.drop(['Team'], axis=1)

  avg_player = temp[temp['Name'].str.contains('Average')]
  av_name = list(avg_player['Name'])[0]
  params = list(temp.columns)
  params = params[1:]

  a_values = []
  b_values = []
    
  for x in range(len(temp['Name'])):
    if temp['Name'][x] == name:
      a_values = temp.iloc[x].values.tolist()
    if temp['Name'][x] == av_name:
      b_values = temp.iloc[x].values.tolist()
        
  a_values = a_values[1:]
  b_values = b_values[1:]

  values = [a_values,b_values]

  #PLOT
  baker = PyPizza(params=params, background_color="#0E1117", straight_line_color="#0E1117",
                  straight_line_lw=2, last_circle_lw=0, other_circle_lw=0, inner_circle_size=5)
   
  fig, ax = baker.make_pizza(a_values, compare_values=b_values, figsize=(10, 10),
                             color_blank_space="same", slice_colors=slice_colors,
                             value_colors=text_colors, value_bck_colors=slice_colors,
                             blank_alpha=0.35,
                             
                             kwargs_slices=dict(edgecolor="none", zorder=0, linewidth=2),
                             kwargs_compare=dict(facecolor="none", edgecolor="#0E1117",
                                                 zorder=8, linewidth=2, ls='--'),
                             kwargs_params=dict(color="#FAFAFA", fontproperties=reg, fontsize=10, va="center"),
                             kwargs_values=dict(color="#0E1117", fontproperties=reg, fontsize=11, zorder=3,
                                                bbox=dict(edgecolor="#FAFAFA", boxstyle="round,pad=0.2", lw=1)),
                             kwargs_compare_values=dict(color="#252627", fontproperties=reg, fontsize=11, zorder=3, alpha=0,
                                                        bbox=dict(edgecolor="#252627", facecolor="#E1E2EF",
                                                                  boxstyle="round,pad=0.2", lw=1, alpha=0)))
  
  fig.text(0.515, 0.975, name + ' - ' + klub, fontproperties=bold, size=16,
           ha="center", color="#FAFAFA", weight='bold')
  fig.text(0.515, 0.953, "Percentile Rank vs League Average "+pos,
           fontproperties=bold, size=11, ha="center", color="#FAFAFA")

  CREDIT_1 = "Data: Lapangbola.com"
  CREDIT_2 = komp+" | Season 2022/23 | Min. "+str(mins)+" mins played"

  fig.text(0.515, 0.02, f"{CREDIT_1}\n{CREDIT_2}", fontproperties=bold,
           size=9, color="#FAFAFA", ha="center")
             
  if (pos != 'Goalkeeper'):
    fig.text(0.268, 0.935, "Goal Threat                 Creativity                In Possession                Out of Possession",
             fontproperties=reg, size=10, color="#FAFAFA", va='center')
    
    fig.patches.extend([
        plt.Rectangle((0.247, 0.9275), 0.015, 0.015, fill=True, color="#22af15",
                      transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.390, 0.9275), 0.015, 0.015, fill=True, color="#adaf15",
                      transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.515, 0.9275), 0.015, 0.015, fill=True, color="#a215af",
                      transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.668, 0.9275), 0.015, 0.015, fill=True, color="#2115af",
                      transform=fig.transFigure, figure=fig)
        ])
  else:
    fig.text(0.398, 0.935, "Distribution                         Goalkeeping",
             fontproperties=reg, size=10, color="#FAFAFA", va='center')
    
    fig.patches.extend([
        plt.Rectangle((0.375, 0.9275), 0.015, 0.015, fill=True, color="#22af15",
                      transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.550, 0.9275), 0.015, 0.015, fill=True, color="#a215af",
                      transform=fig.transFigure, figure=fig)
        ])
    
  plt.savefig('pizza.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
  
  return fig

def plot_compare(p1, p2, pos, data):
  df = data.copy()

  if (pos=='Forward'):
    temp = df[posdict['fw']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)
  elif (pos=='Winger') or (pos=='Attacking 10'):
    temp = df[posdict['cam/w']['metrics']].reset_index(drop=True)
    if (pos=='Winger'):
      temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)
    else:
      temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)
  elif (pos=='Midfielder'):
    temp = df[posdict['cm']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)
  elif (pos=='Fullback'):
    temp = df[posdict['fb']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)
  elif (pos=='Center Back'):
    temp = df[posdict['cb']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)
  elif (pos=='Goalkeeper'):
    temp = df[posdict['gk']['metrics']].reset_index(drop=True)
    temp = temp[(temp['Name']==p1) | (temp['Name']==p2)].reset_index(drop=True)

  params = list(temp.columns)
  params = params[1:]

  low = []
  high = []
  #ranges = []
  p1_values = []
  p2_values = []

  #Form minimum and maximum values for radar plot
  for x in params:
    a = min(df[params][x])
    a = a - (a*.1)
    
    b = max(df[params][x])
    b = b + (b*.1)
    
    low.append(a)
    high.append(b)
    #ranges.append((a,b))

  for x in range(len(temp['Name'])):
    if temp['Name'][x] == p1:
      p1_values = temp.iloc[x].values.tolist()
    if temp['Name'][x] == p2:
      p2_values = temp.iloc[x].values.tolist()

  p1_values = p1_values[1:]
  p2_values = p2_values[1:]

  radar = Radar(params, low, high, num_rings=4,
                ring_width=1, center_circle_radius=1)
  
  fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                  title_space=0, endnote_space=0, grid_key='radar', axis=False)
  radar.setup_axis(ax=axs['radar'])
  rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#e8e6e6', edgecolor='#000000')
  radar_output = radar.draw_radar_compare(p1_values, p2_values, ax=axs['radar'],
                                          kwargs_radar={'facecolor': '#7ed957', 'alpha': 0.5},
                                          kwargs_compare={'facecolor': '#f2ff00', 'alpha': 0.5})
  radar_poly, radar_poly2, vertices1, vertices2 = radar_output
  range_labels = radar.draw_range_labels(ax=axs['radar'], fontproperties=reg, fontsize=15)
  param_labels = radar.draw_param_labels(ax=axs['radar'], fontproperties=bold, fontsize=15)

  endnote_text = axs['endnote'].text(0.99, 0.5, 'All stats are per 90 stats', fontsize=15,
                                     fontproperties=reg, ha='right', va='center')
  title1_text = axs['title'].text(0.01, 0.65, p1, fontsize=20, color='#7ed957',
                                  fontproperties=bold, ha='left', va='center')
  title3_text = axs['title'].text(0.99, 0.65, p2, fontsize=20, color='#f2ff00',
                                  fontproperties=bold, ha='right', va='center')
  
  plt.savefig('radar.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')

  return fig

def plot_PN(data, min_pass, team, min_min, max_min, match, gw):
  pass_between = data.copy()
  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  fig.patch.set_facecolor('#ffffff')
  ax.set_facecolor('#ffffff')

  pitch = Pitch(pitch_type='wyscout', pitch_color='#ffffff', line_color='#000000', pad_bottom=13, pad_top=12,
                corner_arcs=True, stripe=True, stripe_color='#fcf8f7', goal_type='box', linewidth=3.5)
  pitch.draw(ax=ax)

  cmap = plt.cm.get_cmap(hcmap)
  for row in pass_between.itertuples():
    if row.Count > min_pass:
      if abs(row.Y_end - row.Y) > abs(row.X_end - row.X):
        if row.Passer > row.Recipient:
          x_shift, y_shift = 0, 2
        else:
          x_shift, y_shift = 0, -2
      else:
        if row.Passer > row.Recipient:
          x_shift, y_shift = 2, 0
        else:
          x_shift, y_shift = -2, 0

      ax.plot([row.X_end+x_shift, row.X+x_shift],[row.Y_end+y_shift, row.Y+y_shift],
              color=cmap(row.passes_scaled), lw=3, alpha=row.passes_scaled)

      ax.annotate('', xytext=(row.X_end+x_shift, row.Y_end+y_shift),
                  xy=(row.X_end+x_shift+((row.X-row.X_end)/2),
                      row.Y_end+y_shift+((row.Y-row.Y_end)/2)),
                  arrowprops=dict(arrowstyle='->', color=cmap(row.passes_scaled),
                                  lw=3, alpha=row.passes_scaled), size=25)
  avgpos = pass_between[['Passer', 'X', 'Y', 'size', 'No', 'Pos', 'Status', 'Nick']]
  avgpos = avgpos.groupby(['Passer', 'X', 'Y', 'size', 'No', 'Pos', 'Status', 'Nick'], as_index=False).nunique()
      
  for i in range(len(avgpos)):
    if (avgpos['Status'][i]=='Full'):
      pitch.scatter(avgpos['X'][i], avgpos['Y'][i], s = avgpos['size'][i], zorder=10,
                    color='#ffffff', edgecolors='#000000', linewidth=5, ax=ax)
    elif (avgpos['Status'][i]=='Sub In'):
      pitch.scatter(avgpos['X'][i], avgpos['Y'][i], s = avgpos['size'][i], zorder=10,
                    color='#ffffff', edgecolors='#000000', linewidth=5, ax=ax)
      pitch.scatter(avgpos['X'][i]-1.5, avgpos['Y'][i]-2, s = 300, zorder=10,
                    color='#7ed957', edgecolors='#000000', linewidth=2, ax=ax, marker='^')
    else:
      pitch.scatter(avgpos['X'][i], avgpos['Y'][i], s = avgpos['size'][i], zorder=10,
                    color='#ffffff', edgecolors='#000000', linewidth=5, ax=ax)
      pitch.scatter(avgpos['X'][i]+1.5, avgpos['Y'][i]+2, s = 300, zorder=10,
                    color='#e66009', edgecolors='#000000', linewidth=2, ax=ax, marker='v')
    pitch.annotate(avgpos['No'][i], xy=(avgpos['X'][i], avgpos['Y'][i]), c='#000000', va='center', zorder=11,
                   ha='center', size=16, weight='bold', ax=ax, path_effects=path_eff)
    pitch.annotate(avgpos['Nick'][i], xy=(avgpos['X'][i], avgpos['Y'][i]+5), c='#000000', va='center', zorder=11,
                   ha='center', size=14, weight='bold', ax=ax, path_effects=path_eff)
              
  if (min_min == 0):
    min_mins = min_min+1
  else:
    min_mins = min_min

  if (max_min == 91):
    max_mins = max_min-1
  else:
    max_mins = max_min

  anot_x = [75, 79, 84, 90]
  anot_y = [105.35, 105.25, 105.15, 105]
  anot_s = [500, 1000, 1500, 2000]
  for x, y, s in zip(anot_x, anot_y, anot_s):
    ax.scatter(x, y, s=s, c='#ffffff', lw=5,
               marker='o', edgecolors='#000000')
  pitch.arrows(74, 110, 92, 110, width=2, color='#000000',
               headwidth=7, ax=ax)
  ax.text(75, 112, '1 pass', ha='center', fontproperties=bold, color='#000000', size='16', va='center')
  ax.text(90, 112, '40+ passes', ha='center', fontproperties=bold, color='#000000', size='16', va='center')

  anot_x1 = [8, 12, 16, 20]
  anot_x2 = [11, 15, 19, 23]
  anot_a = [0.7, 0.8, 0.9, 1]
  anot_c = ['#839696','#597373','#305050','#062d2d']
  for x1, x2, a, c in zip(anot_x1, anot_x2, anot_a, anot_c):
    pitch.lines(x1, 109, x2, 102, color=c,
                zorder=1, lw=4, alpha=a, ax=ax)
  pitch.arrows(7, 110, 23, 110, width=2, color='#000000',
               headwidth=7, ax=ax)
  if (min_pass == 1):
    ax.text(8, 112, str(min_pass)+' pass', ha='center', fontproperties=bold, color='#000000', size='16', va='center')
  else:
    ax.text(8, 112, str(min_pass)+' passes', ha='center', fontproperties=bold, color='#000000', size='16', va='center')
  ax.text(23, 112, '10+ passes', ha='center', fontproperties=bold, color='#000000', size='16', va='center')

  pitch.scatter(40, 106, s = 800, zorder=10, color='#7ed957',
                edgecolors='#000000', linewidth=4, ax=ax, marker='^')
  ax.text(40, 112, 'Subbed In', ha='center', fontproperties=bold, color='#000000', size='16', va='center')
  pitch.scatter(60, 106, s = 800, zorder=10, color='#e66009',
                edgecolors='#000000', linewidth=4, ax=ax, marker='v')
  ax.text(60, 112, 'Subbed Out', ha='center', fontproperties=bold, color='#000000', size='16', va='center')

  ax.text(0, -8, 'PASSING NETWORK', ha='left', fontproperties=bold, color='#000000', size='22', va='center')
  ax.text(0, -4, team.upper()+' | MINUTES: '+str(min_mins)+'-'+str(max_mins), ha='left', fontproperties=reg, color='#000000', size='18', va='center')
  ax.text(100, -8, match.upper(), ha='right', fontproperties=reg, color='#000000', size='18', va='center')
  ax.text(100, -4, gw, ha='right', fontproperties=reg, color='#000000', size='18', va='center')
  
  plt.savefig('pnet.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
  
  return fig

def vizone(kind, data):
  df = data.copy()
  if (kind=='Passes Received'):
    df = df[df['Pas Zone'].notna()].reset_index(drop=True)
    dx = df[df['Action']=='passing'].reset_index(drop=True)
    dx = dx[['Pas Name', 'Action', 'Team', 'Pas Zone']].rename(columns={'Pas Name':'Act Name','Pas Zone':'Act Zone'})
    temp = dx['Act Zone'].apply(lambda x: pd.Series(list(x)))
    dx['X'] = temp[0]
    dx['Y'] = temp[1]
    dx['Y'] = dx['Y'].replace({'A':10,'B':30,'C':50,'D':70,'E':90})
    dx['X'] = dx['X'].replace({'1':8.34,'2':25.34,'3':42.34,
                               '4':59.34,'5':76.34,'6':93.34})
    dx = dx[['Act Name','Team','Action','X','Y']]
  else:
    df = df[df['Act Zone'].notna()].reset_index(drop=True)
    if (kind=='Passes Attempted'):
      dx = df[(df['Action']=='passing') | (df['Action']=='pass failed')].reset_index(drop=True)
    elif (kind=='Dribbles'):
      dx = df[(df['Action']=='dribble success') | (df['Action']=='dribble failed')].reset_index(drop=True)
    elif (kind=='Tackles'):
      dx = df[(df['Action']=='tackle') | (df['Action']=='tackle failed')].reset_index(drop=True)
    elif (kind=='Intercepts'):
      dx = df[(df['Action']=='intercept') | (df['Action']=='intercept failed')].reset_index(drop=True)
    elif (kind=='Recoveries'):
      dx = df[(df['Action']=='recovery ball')].reset_index(drop=True)
    elif (kind=='Clearances'):
      dx = df[(df['Action']=='clearance')].reset_index(drop=True)
    elif (kind=='Fouls'):
      dx = df[(df['Action']=='foul')].reset_index(drop=True)
    elif (kind=='Possessions Lost'):
      dx = df[(df['Action']=='loose ball')].reset_index(drop=True)
    elif (kind=='Defensive Actions'):
      dx = df[(df['Action']=='tackle') | (df['Action']=='intercept') | (df['Action']=='recovery ball') | (df['Action']=='clearance')].reset_index(drop=True)
    elif (kind=='Heatmap'):
      dx = df.copy()
    dx = dx[['Act Name', 'Action', 'Team', 'Act Zone']]
    temp = dx['Act Zone'].apply(lambda x: pd.Series(list(x)))
    dx['X'] = temp[0]
    dx['Y'] = temp[1]
    dx['Y'] = dx['Y'].replace({'A':10,'B':30,'C':50,'D':70,'E':90})
    dx['X'] = dx['X'].replace({'1':8.34,'2':25.34,'3':42.34,
                               '4':59.34,'5':76.34,'6':93.34})
    dx = dx[['Act Name','Team','Action','X','Y']]
  #dx = dx[dx['Act Name']==player].reset_index(drop=True)

  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  fig.patch.set_facecolor('#ffffff')
  ax.set_facecolor('#ffffff')
  pitch = Pitch(pitch_type='wyscout', pitch_color='#ffffff', line_color='#000000', line_zorder=2,
                corner_arcs=True, goal_type='box', linewidth=3.5)
  pitch.draw(ax=ax)

  bin_statistic = pitch.bin_statistic(dx.X, dx.Y, statistic='count', bins=(6, 5), normalize=True)
  pitch.heatmap(bin_statistic, ax=ax, cmap='Greens', edgecolor='#ffffff', lw=0)
  labels = pitch.label_heatmap(bin_statistic, color='#ffffff', fontsize=22, fontproperties=bold,
                               ax=ax, ha='center', va='center', str_format='{:.0%}')

  return fig

def tendang(data):
  df_player = data.copy()
  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)

  pitch = VerticalPitch(half=True, pitch_type='wyscout', corner_arcs=True,
                        pitch_color='#ffffff', line_color='#000000',
                        stripe_color='#fcf8f7', goal_type='box', pad_bottom=5,
                        pad_right=0.5, pad_left=0.5, stripe=True, linewidth=3.5)
  pitch.draw(ax=ax)

  goalp = df_player[df_player['Event']=='Goal']['Event'].count()
  shots = df_player[df_player['Event']!='Goal']['Event'].count() + goalp
  player = (df_player['Player'].tolist())[0] #NEW
  team = (df_player['Team'].tolist())[0] #NEW
  xgtotp = round((df_player['xG'].sum()),2)
  gps = round((goalp/shots)*100,1)
  xgps = round((xgtotp/shots),2)

  for i in range(len(df_player)):
    if (df_player['Event'][i] == 'Goal' or df_player['Event'][i] == 'Penalty Goal'):
      ax.scatter(df_player['Y'][i], df_player['X'][i], s=df_player['xG'][i]*10000,
                 c='#7ed957', marker='o', edgecolors='#000000', lw=3.5, zorder=10)
    elif (df_player['Event'][i] == 'Shot On'):
      ax.scatter(df_player['Y'][i], df_player['X'][i], s=df_player['xG'][i]*10000,
                 c='#f2ff00', marker='o', edgecolors='#000000', lw=3.5)
    elif (df_player['Event'][i] == 'Shot Off'):
      ax.scatter(df_player['Y'][i], df_player['X'][i], s=df_player['xG'][i]*10000,
                 c='#a6a6a6', marker='o', edgecolors='#000000', lw=3.5)
    else:
      ax.scatter(df_player['Y'][i], df_player['X'][i], s=df_player['xG'][i]*10000,
                 c='#e66009', marker='o', edgecolors='#000000', lw=3.5)

  annot_texts = ['Goals', 'xG', 'Shots', 'Conversion\nRatio (%)', 'xG/Shots']
  annot_x = [10.83 + x*17.83 for x in range(0,5)]
  annot_stats = [goalp, xgtotp, shots, gps, xgps]

  for x, s, h in zip(annot_x, annot_texts, annot_stats):
    ax.annotate(text=s, size=22, xy=(x+3.5, 56.5), xytext=(0,-18),
                textcoords='offset points', color='black', ha='center',
                zorder=9, va='center', fontproperties=bold, path_effects=path_eff)
    ax.annotate(text=h, size=78, xy=(x+3.5, 60), xytext=(0,-18),
                textcoords='offset points', color='black', ha='center',
                zorder=9, va='center', fontproperties=bold, path_effects=path_eff)

  ax.add_patch(FancyBboxPatch((0, 45), 200, 4.5, fc='#ffffff', ec='#ffffff', lw=2))

  annot_x = [4 + x*25 for x in range(0,4)]
  annot_texts = ['Goals', 'Shots On Target', 'Shots Off Target', 'Shots Blocked']

  ax.scatter(4, 48, s=800, c='#7ed957', lw=3.5,
             marker='o', edgecolors='#000000')
  ax.scatter(29, 48, s=800, c='#f2ff00', lw=3.5,
             marker='o', edgecolors='#000000')
  ax.scatter(54, 48, s=800, c='#a6a6a6', lw=3.5,
             marker='o', edgecolors='#000000')
  ax.scatter(79, 48, s=800, c='#e66009', lw=3.5,
             marker='o', edgecolors='#000000')

  for x, s in zip(annot_x, annot_texts):
    ax.annotate(text=s, size=24, xy=(x+2.5, 49), xytext=(0,-18),
                textcoords='offset points', color='black', ha='left',
                zorder=9, va='center', fontproperties=bold)
  ax.add_patch(FancyBboxPatch((0.65, 50.5), 65, 1.35, fc='#cbfd06', ec='#cbfd06', lw=2))
  ax.annotate(text=player+' - '+team, size=26, xy=(1, 52), xytext=(0,-18),
              textcoords='offset points', color='black', ha='left',
              zorder=9, va='center', fontproperties=bold)

  ax.annotate(text='-Nilai xG->', size=21, xy=(87, 54), xytext=(0,-18),
              textcoords='offset points', color='black', ha='left',
              zorder=9, va='center', fontproperties=bold, path_effects=path_eff)
  ax.scatter(87.5, 51.15, s=300, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  ax.scatter(90.5, 51.25, s=500, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  ax.scatter(93.5, 51.35, s=700, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  ax.scatter(97, 51.45, s=900, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')

  return fig

def ttendang(data):
  df_team = data.copy()

  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)

  pitch = VerticalPitch(half=True, pitch_type='wyscout', corner_arcs=True,
                        pitch_color='#ffffff', line_color='#000000',
                        stripe_color='#fcf8f7', goal_type='box', pad_bottom=5,
                        pad_right=0.5, pad_left=0.5, stripe=True, linewidth=3.5)
  pitch.draw(ax=ax)

  goal = df_team[df_team['Event']=='Goal']['Event'].count()
  team = (df_team['Team'].tolist())[0] #NEW
  son = df_team[df_team['Event']=='Shot On']['Event'].count()
  soff = df_team[df_team['Event']=='Shot Off']['Event'].count()
  sblocked = df_team[df_team['Event']=='Shot Blocked']['Event'].count()
  xgtot = round((df_team['xG'].sum()),2)

  for i in range(len(df_team)):
    if (df_team['Event'][i] == 'Goal' or df_team['Event'][i] == 'Penalty Goal'):
      ax.scatter(df_team['Y'][i], df_team['X'][i], s=df_team['xG'][i]*10000,
                 c='#7ed957', marker='o', edgecolors='#000000', lw=3.5)
    elif (df_team['Event'][i] == 'Shot On'):
      ax.scatter(df_team['Y'][i], df_team['X'][i], s=df_team['xG'][i]*10000,
                 c='#f2ff00', marker='o', edgecolors='#000000', lw=3.5)
    elif (df_team['Event'][i] == 'Shot Off'):
      ax.scatter(df_team['Y'][i], df_team['X'][i], s=df_team['xG'][i]*10000,
                 c='#a6a6a6', marker='o', edgecolors='#000000', lw=3.5)
    else:
      ax.scatter(df_team['Y'][i], df_team['X'][i], s=df_team['xG'][i]*10000,
                 c='#e66009', marker='o', edgecolors='#000000', lw=3.5)

  annot_texts = ['Goals\nConceded', 'Shots\nOn Target', 'Shots\nOff Target', 'Shots\nBlocked', 'xGA Total']
  annot_x = [10.83 + x*17.83 for x in range(0,5)]
  annot_stats = [goal, son, soff, sblocked, xgtot]

  for x, s, h in zip(annot_x, annot_texts, annot_stats):
    ax.annotate(text=s, size=22, xy=(x+3.5, 56.5), xytext=(0,-18),
                textcoords='offset points', color='black', ha='center',
                zorder=9, va='center', fontproperties=bold, path_effects=path_eff)
    ax.annotate(text=h, size=78, xy=(x+3.5, 60), xytext=(0,-18),
                textcoords='offset points', color='black', ha='center',
                zorder=9, va='center', fontproperties=bold, path_effects=path_eff)

  ax.add_patch(FancyBboxPatch((0, 45), 200, 4.5, fc='#ffffff', ec='#ffffff', lw=2))

  annot_x = [4 + x*25 for x in range(0,4)]
  annot_texts = ['Goals Conceded', 'Shots On Target', 'Shots Off Target', 'Shots Blocked']

  ax.scatter(4, 48, s=800, c='#7ed957', lw=3.5,
             marker='o', edgecolors='#000000')
  ax.scatter(29, 48, s=800, c='#f2ff00', lw=3.5,
             marker='o', edgecolors='#000000')
  ax.scatter(54, 48, s=800, c='#a6a6a6', lw=3.5,
             marker='o', edgecolors='#000000')
  ax.scatter(79, 48, s=800, c='#e66009', lw=3.5,
             marker='o', edgecolors='#000000')

  for x, s in zip(annot_x, annot_texts):
    ax.annotate(text=s, size=24, xy=(x+2.5, 49), xytext=(0,-18),
                textcoords='offset points', color='black', ha='left',
                zorder=9, va='center', fontproperties=bold)

  ax.add_patch(FancyBboxPatch((0.65, 50.5), 35, 1.35, fc='#cbfd06', ec='#cbfd06', lw=2))
  ax.annotate(text=team18, size=26, xy=(1, 52), xytext=(0,-18),
              textcoords='offset points', color='black', ha='left',
              zorder=9, va='center', fontproperties=bold) ##TEAM

  ax.annotate(text='-Nilai xGA->', size=21, xy=(87, 54), xytext=(0,-18),
              textcoords='offset points', color='black', ha='left',
              zorder=9, va='center', fontproperties=bold, path_effects=path_eff)
  ax.scatter(87.5, 51.15, s=300, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  ax.scatter(90.5, 51.25, s=500, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  ax.scatter(93.5, 51.35, s=700, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  ax.scatter(97, 51.45, s=900, c='#a6a6a6', lw=2,
             marker='o', edgecolors='#000000')
  
  return fig

def fulxg(data, home, away):
  fig, ax = plt.subplots(figsize=(20, 20), dpi=500)
  fig.patch.set_facecolor('#ffffff')
  ax.set_facecolor('#ffffff')

  pitch = Pitch(pitch_type='wyscout', pitch_color='#ffffff', line_color='#000000', pad_bottom=13, pad_top=12,
                corner_arcs=True, stripe=True, stripe_color='#fcf8f7', goal_type='box', linewidth=3.5)
  pitch.draw(ax=ax)

  hdata = data[data['Team']==home].reset_index(drop=True)
  hgoal = hdata[hdata['Event']=='Goal']['Event'].count()
  hxg = round((hdata['xG'].sum()),2)
  hshot = hdata[hdata['Event']!='Goal']['Event'].count() + hgoal
  hxgps = round((hxg/hshot),2)

  adata = data[data['Team']==away].reset_index(drop=True)
  agoal = adata[adata['Event']=='Goal']['Event'].count()
  axg = round((adata['xG'].sum()),2)
  ashot = adata[adata['Event']!='Goal']['Event'].count() + agoal
  axgps = round((axg/ashot),2)

  for i in range(len(data)):
    if (data['Team'][i] == home):
      data['X'][i] = 100-data['X'][i]
      data['Y'][i] = 100-data['Y'][i]
    else:
      data['X'][i] = data['X'][i]
      data['Y'][i] = data['Y'][i]
  for i in range(len(data)):
    if (data['Event'][i] == 'Goal'):
      ax.scatter(data['X'][i], data['Y'][i], s=data['xG'][i]*5000,
                 c='#7ed957', marker='o', edgecolors='#000000', lw=3, zorder=10)
    else:
      ax.scatter(data['X'][i], data['Y'][i], s=data['xG'][i]*5000,
                 c='#ffffff', marker='o', edgecolors='#000000', lw=3, zorder=10)
      
  annot_texts = ['Goals', 'Expected Goals (xG)', 'Shots', 'xG/Shot']
  annot_y = [35 + y*9 for y in range(0,4)]
  annot_stats_h = [hgoal, hxg, hshot, hxgps]
  annot_stats_a = [agoal, axg, ashot, axgps]

  for y, s, h, a in zip(annot_y, annot_texts, annot_stats_h, annot_stats_a):
    ax.add_patch(FancyBboxPatch((37.5, y), 25, 5, fc='#000000', ec='#ffffff',
                                alpha=0.15, boxstyle=patches.BoxStyle('Round', pad=1)))
    ax.add_patch(FancyBboxPatch((32, y), 3, 5, fc='#000000', ec='#ffffff',
                                alpha=0.15, boxstyle=patches.BoxStyle('Round', pad=1)))
    ax.add_patch(FancyBboxPatch((65, y), 3, 5, fc='#000000', ec='#ffffff',
                                alpha=0.15, boxstyle=patches.BoxStyle('Round', pad=1)))
    ax.annotate(text=s, size=22, xy=(50,y), xytext=(0,-18),
                textcoords='offset points', color='#000000', ha='center', fontproperties=bold,
                zorder=9, va='center', path_effects=path_eff)
    ax.annotate(text=h, size=22, xy=(33.5,y), xytext=(0,-18),
                textcoords='offset points', color='#000000', ha='center', fontproperties=bold,
                zorder=9, va='center', path_effects=path_eff)
    ax.annotate(text=a, size=22, xy=(66.5,y), xytext=(0,-18),
                textcoords='offset points', color='#000000', ha='center', fontproperties=bold,
                zorder=9, va='center', path_effects=path_eff)

  ax.scatter(32, 95, s=500, c='#ffffff', marker='o', ec='#000000', lw=3)
  ax.text(34, 95, 'Shots', ha='left', fontproperties=bold, color='#000000', size='18', va='center')
  ax.scatter(42, 95, s=500, c='#7ed957', marker='o', ec='#000000', lw=3)
  ax.text(44, 95, 'Goals', ha='left', fontproperties=bold, color='#000000', size='18', va='center')

  ax.text(52.5, 91, '-xG value->', ha='left', fontproperties=bold, color='#000000', size='18', va='center')
  ax.scatter(53, 95, s=500, c='#ffffff', marker='o', ec='#000000', lw=3)
  ax.scatter(57, 95, s=700, c='#ffffff', marker='o', ec='#000000', lw=3)
  ax.scatter(61, 95, s=900, c='#ffffff', marker='o', ec='#000000', lw=3)

  DC_to_FC = ax.transData.transform
  FC_to_NFC = fig.transFigure.inverted().transform
  DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

  ax_coords = DC_to_NFC([29.5, 28])
  logo_ax = fig.add_axes([ax_coords[0], ax_coords[1], 0.055, 0.055], anchor = "C")
  club_icon = Image.open('./data/logo/'+home+'.png')
  logo_ax.imshow(club_icon)
  logo_ax.axis("off")

  ax_coords = DC_to_NFC([62.5, 28])
  logo_ax = fig.add_axes([ax_coords[0], ax_coords[1], 0.055, 0.055], anchor = "C")
  club_icon = Image.open('./data/logo/'+away+'.png')
  logo_ax.imshow(club_icon)
  logo_ax.axis("off")

  ax.text(34, 25, home.upper(), ha='center', fontproperties=bold, color='#000000', size='22', va='center')
  ax.text(66, 25, away.upper(), ha='center', fontproperties=bold, color='#000000', size='22', va='center')

  return fig
