# -*- coding: utf-8 -*-
import os
import streamlit as st
from datetime import datetime
import pandas as pd
import math
import numpy as np
import random
import re
import plotly.express as px
import plotly.graph_objects as go
import math
import base64
from gtts import gTTS
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import scipy.stats as ss
from scipy.stats import chi2_contingency
import statsmodels.api as sm
from sklearn.neighbors import LocalOutlierFactor

from helper_func1 import find_common_strings
from simulations import simulate_two_months
from access_datetime import access_datetime

import warnings
warnings.filterwarnings('ignore')




###################### setting page title #####################################################################
st.set_page_config(page_title='Ask Your Data!',
                   page_icon='https://i.ibb.co/NLTT1H6/growth.png', 
                   layout="centered",
                   menu_items={'About':'Hello'})



hide_streamlit_style2= '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.viewerBadge_container__1QSob{visibility:hidden;}
.viewerBadge_link__1S137{visibility:hidden;}
.css-1rs6os {visibility: hidden;}
.css-17ziqus {visibility: hidden;}
.css-1aumxhk {
background-color:#fefae0 ;
background-image: none;
color: #ffffff
}
</style>
'''
st.markdown(hide_streamlit_style2, unsafe_allow_html=True) 
#https://i.ibb.co/V2CJ4xH/Untitled-presentation-22.jpg

#https://uploads-ssl.webflow.com/5fc49b7951c3f86d8a7a8d75/61d44b7534c2105cee96be8d_Tool%20background.gif
#https://i.postimg.cc/wMBNx3NM/27054.jpg
page_bg_img = '''
<style>
.stApp {
background-color: #fefae0;
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


title_html=f'<h1 style="font-family:Calibri; color:#DEF294; font-size: 80px;">Ask Your Data!</h1>'
st.markdown(title_html, unsafe_allow_html=True)



############################################################################## sidebar ##################################################################################################################
caption_html=f'<h1 style="font-family:Calibri; color:#babea9; font-size: 20px;">Efortlessly generate insights and improve your decision making capabilities.</h1>'
st.markdown(caption_html, unsafe_allow_html=True)
title_html=f'<h1 style="font-family:Calibri; color:#606D32; font-size: 25px;">Choose your dataset here >></h1>'
st.sidebar.markdown(title_html, unsafe_allow_html=True)


location_of_data = st.sidebar.file_uploader('')

options=['Select an option from here','Enter queries in Speech','View Dashboard','Generate Insights','Detect Anomalies/Outliers in your Dataset','Observe Statistical Inferences on your Data','Run Simulations to estimate Probabilities on historical Data',]
st.sidebar.write('')


title_html=f'<h1 style="font-family:Calibri; color:#606D32; font-size: 15px;">What do you want from your dataset?</h1>'
st.sidebar.markdown(title_html, unsafe_allow_html=True)
selected_option=st.sidebar.selectbox('',options)

options_dict={'Enter queries in Speech':'SP','View Dashboard':'DA','Generate Insights':'IN',\
'Detect Anomalies/Outliers in your Dataset':'OA','Observe Statistical Inferences on your Data':'ST',\
'Run Simulations to estimate Probabilities on historical Data':'MC'}

st.sidebar.write('')




title_html=f'<h1 style="font-family:Calibri; color:#606D32; font-size: 15px;">What is the currency of your dataset?</h1>'
st.sidebar.markdown(title_html, unsafe_allow_html=True)

rupee=st.sidebar.checkbox('Rupees')
dollar=st.sidebar.checkbox('Dollars')
euro=st.sidebar.checkbox('Euros')
other=st.sidebar.checkbox('Other Currency')

if rupee:
    selected_curr='Rupees'
elif dollar:
    selected_curr='Dollars'
elif euro:
    selected_curr='Euros'
elif other:
    selected_curr='Currencies'
else:
    pass

#######################################################################################################################################################################################################

stt_button = Button(label="Click on this button to Engage Speech Input", width=100)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

############################### function to autoplay audio ##########################################################################################

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
        
######################################################################################################################################################

if location_of_data:
    try: 
        data2=pd.read_csv(location_of_data)
        
        data2.drop(data2.columns[0],axis=1,inplace=True)
        
    except: 
        data2=pd.read_excel(location_of_data)
else:
    st.stop()
##################################################### accessing numerical columns #################################################
num_cols=data2.corr(numeric_only=True).columns
num_cols=list(num_cols)
try:
    num_cols.remove('Year')
except:
    pass

cat_cols=[cols for cols in data2.columns if not cols in data2.corr(numeric_only=True).columns]

try:
    cat_cols.remove('Month')
except:
    pass

data2.fillna('cols_inside',inplace=True)
#st.write(data2)

final_clean_df=pd.DataFrame()



from access_datetime import access_datetime

#st.write(access_datetime(data2))




##################################################### accessing categorical columns ###################################################

categories={}
for cols in cat_cols:
    col_cats_array=list(data2[cols].value_counts().keys())
    categories[cols]=col_cats_array

#st.write(categories)

######################################### dataset cleaning & preparation ##################################################################

data2.replace('Decemeber','December',inplace=True)
data=data2.copy()

total_months_stored=[]
total_years_stored=[]
month_dict=['January','February','March','April','May','June','July','August','September','October','November','December']


#lp=0
#for rp in range(len(data['Month'].values)):
    #if data['Month'][rp]=='cols_inside':
        
        #lp=rp
        #while data['Month'][lp] not in month_dict:
            #lp=lp-1
            #if data['Month'][lp] in month_dict:
                #total_months_stored.append(data['Month'][lp])
              
#years_fr=[]
#for year in data['Year'].values:
    #try:
        #try_int=int(year)

        #years_fr.append(year)
    #except:
        #pass
    


#lp=0
#for rp in range(len(data['Year'].values)):
    #if data['Year'][rp]=='cols_inside':
        
       # lp=rp
        #while data['Year'][lp] not in years_fr:
            #lp=lp-1
            #if data['Year'][lp] in years_fr:
                #total_years_stored.append(data['Year'][lp])

try:
    final_clean_df['Year']=total_years_stored
    final_clean_df['Month']=total_months_stored
except:
    pass

final_clean_df=data


############################################# automatically detecting categorical columns ####################################################################              

        









#####################################################################################################################################################################################

######################################################################################################################################################################

def text_queries(inp):
    
    ques_html=f'<h1 style="font-family:Calibri; color:#BAC9AA; font-size: 15px;">User asked: {inp}?</h1>'
    st.markdown(ques_html,unsafe_allow_html=True)
    inp=inp.lower()
    inp=inp.replace(' ','')
    #print(inp)
    
    match_columns=[]
    for i in data2.columns:
            i=i.lower()
            i=re.sub('[^a-zA-Z0-9]','',i)
            match_columns.append(i)
        
    data2.columns=match_columns
    
    match_aggrt='high|highest|most|low|lowest|least|average|avg|total|count'
    month_match={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,
                     'september':9,'october':10,'november':11,'december':12}
    
    store_columns=[]
    store_month_match=[]
    matchedaggr=[]
    ans=re.findall(match_aggrt,inp)
    
    for i in ans:
            matchedaggr.append(i)
    
        
    for i in match_columns:
            if i in inp.lower() or i[:-1] in inp.lower():
                store_columns.append(i)
    
    

    for i in month_match:
            if i in inp:
                store_month_match.append(i)


    

    year_mentioned=[]
    int_str=''
    
    for i in inp:
        if i.isdigit():
           int_str+=i
    if int_str:
        int_str=int(int_str)
        year_mentioned.append(int_str)
    else:
        pass

    stored_month_if_month_mentioned=[]
    
    ##################### categorical mapping #########################################################################################
    categories_found=[]

    for key in categories:
        for search in categories[key]:
            if search.lower() in inp:
                categories_found.append(search)
    
    #st.write(categories_found)
    

    remap_inp_cols={}

    for col in cat_cols:
        
        for j in categories_found:
            
            if j in list(data2[col.lower()].values):
                
                remap_inp_cols[col]=j

    #st.write(remap_inp_cols)
    
    ########################################################################################################################################    
    if 'lastmonth' in inp or 'previousmonth' in inp:
            store_query='last month'
            curr_month=datetime.now().month
            last_month=curr_month-1
            last_month_key=[i for i in month_match if month_match[i]==last_month]
            if 'month' in matchedaggr:
                matchedaggr.remove('month')
            store_month_match.append(last_month_key[0])
    elif 'lastmonth' in inp or 'previousmonth' not in inp and len(store_month_match)>0 and len(year_mentioned)>0:
        stored_month_if_month_mentioned.append(store_month_match[0])
    elif 'thismonth' in inp:
        store_query='this month'
        curr_month=datetime.now().month
        curr_month_key=[i for i in month_match if month_match[i]==curr_month]
        if 'month' in matchedaggr:
                matchedaggr.remove('month')
        store_month_match.append(curr_month_key[0])
        
    #st.write(store_month_match)    
        #print(last_key)
    
   
    ################################################# for queries based on totals and averages ###############################################################################################################
   
    ############# changed with automatic categorical column recognition ##############################################################################
    
   #####################################################################restored queries#####################################################################################################################################
  
    if 'total' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==0:
        flag=16
    elif 'average' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==0:
        flag=161
    elif 'total' in matchedaggr and len(store_month_match)!=0 and len(stored_month_if_month_mentioned)!=0 and len(year_mentioned)>0 and len(remap_inp_cols)==0:
        flag=17
    elif 'average' in matchedaggr and len(store_month_match)!=0 and len(stored_month_if_month_mentioned)!=0 and len(year_mentioned)>0 and len(remap_inp_cols)==0:
        flag=171
    elif 'total' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==1:
        flag=18
    elif 'average' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==1:
        flag=181
    elif 'total' in matchedaggr and len(store_month_match)>0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==1:
        flag=19
    elif 'average' in matchedaggr and len(store_month_match)>0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==1:
        flag=191
    elif 'total' in matchedaggr and len(store_month_match)>0 and len(stored_month_if_month_mentioned)>0 and len(year_mentioned)>0 and len(remap_inp_cols)==1:
        flag=20
    elif 'average' in matchedaggr and len(store_month_match)>0 and len(stored_month_if_month_mentioned)>0 and len(year_mentioned)>0 and len(remap_inp_cols)==1:
        flag=201
    elif 'total' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)==0 and len(remap_inp_cols)==2:
        flag=21
    elif 'average' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)==0 and len(remap_inp_cols)==2:
        flag=211
    elif 'total' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==2:
        flag=22
    elif 'average' in matchedaggr and len(store_month_match)==0 and len(stored_month_if_month_mentioned)==0 and len(year_mentioned)>0 and len(remap_inp_cols)==2:
        flag=221
    elif 'total' in matchedaggr and len(store_month_match)>0 and len(stored_month_if_month_mentioned)>0 and len(year_mentioned)>0 and len(remap_inp_cols)==2:
        flag=23
    elif 'average' in matchedaggr and len(store_month_match)>0 and len(stored_month_if_month_mentioned)>0 and len(year_mentioned)>0 and len(remap_inp_cols)==2:
        flag=231
 
  ##################################################################### for individual queries #####################################################################
    
    indvaggrts='high|highest|most|low|lowest|least|best|worst'
    hash_map_aggrts={'high':False,'highest':False,'most':False,'low':True,'lowest':True,'least':True,'best':False,'worst':True}
    ans=re.findall(indvaggrts,inp)
    matchedindvaggr=[]
    for i in ans:
            matchedindvaggr.append(i)
            try:
                mapped_aggrt=hash_map_aggrts[matchedindvaggr[0]]
            except:
                pass
    #st.write(mapped_aggrt)

    num_cols_stored=[cols for cols in num_cols if cols.lower() in store_columns]
    cat_cols_stored=[cols for cols in cat_cols if cols.lower() in store_columns]
    
    #st.write(query)
    query_broken=query.split(' ')
    #st.write(query_broken)

    cats_in_hash=[]

    
    for cols in cat_cols:
        for pieces in query_broken:
            if pieces.capitalize() in final_clean_df[cols].values:
                found_cols=cols
                found_vals=pieces
                cats_in_hash.append(found_cols)
                #st.write(pieces)

    if 'month' in store_columns:
        cat_cols_stored.append('Month')

    total_aggrt_on=num_cols_stored+cat_cols_stored
    #st.write(total_aggrt_on)
    #st.write(year_mentioned)
    #st.write(len(found_cols))
    #st.write(found_cols)

    if len(matchedindvaggr)>0 and len(store_columns)>0 and len(year_mentioned)==0:
        flag=1
    elif len(matchedindvaggr)>0 and len(store_columns)>0 and len(year_mentioned)>0 and len(cats_in_hash)==0:
        flag=2
    elif len(matchedindvaggr)>0 and len(store_columns)>0 and len(year_mentioned)>0 and len(found_cols)>0:
        flag=3
    #st.write(flag)
    #st.write(num_cols_stored)
    #st.write(cat_cols_stored)
    #st.write(year_mentioned)
    #st.write(store_regions)
    #st.write(found_cols)
    #st.write(found_vals)
    if flag==1:
        df=final_clean_df
        df_=df[total_aggrt_on]
    
        df_.sort_values(ascending=mapped_aggrt,by=num_cols_stored,inplace=True)
        ans=df_[cat_cols_stored[0]].values[0]
        return_ans=f'The {cat_cols_stored[0]} with {matchedindvaggr[0]}est {num_cols_stored[0]} was {ans}'
    elif flag==2:
        df=final_clean_df
        df_=df[total_aggrt_on]
        df_['Year']=final_clean_df['Year']
        df_['Year']=df['Year'].astype('int')
        df_.sort_values(ascending=mapped_aggrt,by=num_cols_stored,inplace=True)
        df_=df_[df_['Year']==year_mentioned[0]]
        ans=df_[cat_cols_stored[0]].values[0]
        return_ans=f'The {cat_cols_stored[0]} with {matchedindvaggr[0]}est {num_cols_stored[0]} in {year_mentioned[0]} was {ans}'
    elif flag==3:
        df=final_clean_df
        total_aggrt_on.append(found_cols)
        
        df_=df[total_aggrt_on]
        
        df_['Year']=final_clean_df['Year']
        df_['Year']=df['Year'].astype('int')
        df_.sort_values(ascending=mapped_aggrt,by=num_cols_stored,inplace=True)
        df_n=df_[(df_['Year']==year_mentioned[0])]
        df_n=df_n[df_n[found_cols]==found_vals]
        
        ans=df_[cat_cols_stored[0]].values[0]
        return_ans=f'The {cat_cols_stored[0]} with {matchedindvaggr[0]}est {num_cols_stored[0]} in {found_vals} on {year_mentioned[0]} was {ans}'

  
    ##########################################################################################################################################    
    match_finally_columns=[]

    for i in data2.columns:
            i=i.lower()
            i=re.sub('[^a-zA-Z0-9]','',i)
            if i in store_columns:
                match_finally_columns.append(i)
    ############################################################################################################################################
    
   
    

    if flag==17:
        df=final_clean_df
        df_=df[(df['Month']==store_month_match[0].capitalize()) & (df['Year']==year_mentioned[0])]

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} on {store_month_match[0]} {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==171:
        df=final_clean_df
        df_=df[(df['Month']==store_month_match[0].capitalize()) & (df['Year']==year_mentioned[0])]

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} on {store_month_match[0]} {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==16:
        df=final_clean_df
        df_=df[df['Year']==year_mentioned[0]]
        #st.write(df)

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} on {year_mentioned[0]} was {ans} {selected_curr}'
    if flag==161:
        df=final_clean_df
        df_=df[df['Year']==year_mentioned[0]]

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==18:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df['Year']==year_mentioned[0]]

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==181:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_['Year']==year_mentioned[0]]
        

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==19:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[(df_['Year']==year_mentioned[0]) & (df_['Month']==store_month_match[0].capitalize())]

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} on {store_month_match[0]} {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==191:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[(df_['Year']==year_mentioned[0]) & (df_['Month']==store_month_match[0].capitalize())]
        

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} on {store_month_match[0]} {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==20:
        df=final_clean_df

        df_=df[(df['Year']==year_mentioned[0]) & (df['Region']==store_regions[0].capitalize())]

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} in {store_regions[0]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==201:
        df=final_clean_df
        df_=df[(df['Year']==year_mentioned[0]) & (df['Region']==store_regions[0].capitalize())]

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} in {store_regions[0]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==21:
        df=final_clean_df
        #st.write(df)
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_[list(remap_inp_cols.keys())[1]]==remap_inp_cols[list(remap_inp_cols.keys())[1]]]
        

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} in {remap_inp_cols[list(remap_inp_cols.keys())[1]]} was {ans} {selected_curr}'
    elif flag==211:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_[list(remap_inp_cols.keys())[1]]==remap_inp_cols[list(remap_inp_cols.keys())[1]]]
        

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} in {remap_inp_cols[list(remap_inp_cols.keys())[1]]} was {ans} {selected_curr}'
        
    elif flag==22:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_[list(remap_inp_cols.keys())[1]]==remap_inp_cols[list(remap_inp_cols.keys())[1]]]
        df_=df_[df_['Year']==year_mentioned[0]]
        st.write(df_)
        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
    
        return_ans=f'The total {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} in {remap_inp_cols[list(remap_inp_cols.keys())[1]]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==221:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_[list(remap_inp_cols.keys())[1]]==remap_inp_cols[list(remap_inp_cols.keys())[1]]]
        df_=df_[df_['Year']==year_mentioned[0]]
       

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} in {remap_inp_cols[list(remap_inp_cols.keys())[1]]} on {year_mentioned[0]} was {ans} {selected_curr}'
        
    
    elif flag==23:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_[list(remap_inp_cols.keys())[1]]==remap_inp_cols[list(remap_inp_cols.keys())[1]]]
        df_=df_[df_['Year']==year_mentioned[0]]
        
        df_=df_[df_['Month']==store_month_match[0].capitalize()]
        
        

        ans=round(sum(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The total {match_finally_columns[0]} of {remap_inp_cols[list(remap_inp_cols.keys())[0]]} in {remap_inp_cols[list(remap_inp_cols.keys())[1]]} on {store_month_match[0]} {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==231:
        df=final_clean_df
        df_=df[df[list(remap_inp_cols.keys())[0]]==remap_inp_cols[list(remap_inp_cols.keys())[0]]]
        df_=df_[df_[list(remap_inp_cols.keys())[1]]==remap_inp_cols[list(remap_inp_cols.keys())[1]]]
        df_=df_[df_['Year']==year_mentioned[0]]
        df_=df_[df_['Month']==store_month_match[0]]
        

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} of {store_products[0]} in {store_regions[0]} on {year_mentioned[0]} was {ans} {selected_curr}'
    elif flag==241:
        df=final_clean_df
        df_=df[(df['Region']==store_regions[0].capitalize()) & (df['Product']==store_products[0].capitalize()) & (df['Month']==store_month_match[0]) &(df['Year']==year_mentioned[0])]

        ans=round(np.average(df_[match_finally_columns[0].capitalize()].values),2)
        return_ans=f'The average {match_finally_columns[0]} of {store_products[0]} in {store_regions[0]} on {store_month_match[0]} {year_mentioned[0]} was {ans} {selected_curr}'
    return return_ans


############################################################################ function for running Monte Carlo Simulations #################################################################


def run_mcs(column_chosen, num_sims):
    data2=final_clean_df
    #st.write(categories)

    st.caption('Please wait while the machine completes running Monte Carlo simulations on the historical Data.')

    for cat_col in categories:
        for unit in categories[cat_col]:
            perc,inc=simulate_two_months(data2,num_sims,column_chosen,cat_col,unit)

            st.title(f'Based on {num_sims} simulations on historical data, the estimated probability that {column_chosen} for {unit} next month will increase is {round((perc),2)} \
            with a mean expected return of {round(np.mean(inc),2)}%')
            








############################################################################ function for calculating insights #############################################################################3 
def generate_insights(data2,inputs_insights):

    data2=final_clean_df
    #month_match,year_match,date_match=access_datetime(data2)
    groupby_catcol=[col for col in data2.columns if not col in data2.corr(numeric_only=True).columns]
    groupby_catcol.remove('Month')
    grouped=data2.groupby(groupby_catcol)


    years_sorted=sorted(list(set(data2['Year'].values)))
    max_year_in_df=years_sorted[-1]
    second_max_year_in_df=years_sorted[-2]

    current_year = max_year_in_df
    prev_year=second_max_year_in_df

    def concat_datemonth(x,y):
        return pd.to_datetime(f'{math.ceil(y)}-{x}',format='%Y-%B')
    data2['dtcol']=np.vectorize(concat_datemonth)(data2['Month'],data2['Year'])

    months_lst=data2['Month'].values

    month_and_insight={}
    month_and_means={}
    insight_vals=[]

    month_and_cv={}
    high_corr_keys_and_val={}

    for i in inputs_insights:
        
        
        #st.write(high_corr_keys_and_val)


        #st.write(corr_table)

        for month in months_lst:

            
            needed_df=data2[data2['Month']==month]

            needed_df_median=np.median(needed_df[i].values)
            needed_df_std=np.std(needed_df[i].values)

            needed_df_cv=needed_df_std/needed_df_median

            final_characs=needed_df_median/needed_df_cv

            month_and_insight[month]=final_characs
            month_and_means[month]=needed_df_median
            

            insight_vals.append(final_characs)

       
        insight_vals=sorted(insight_vals)
        highest_val=insight_vals[-1]
        lowest_val=insight_vals[0]
    
        highest_key=''
        lowest_key=''
        

        for key in month_and_insight:
            if month_and_insight[key]==highest_val:
                highest_key=key
            elif month_and_insight[key]==lowest_val:
                lowest_key=key

        #################################################### year on year calculation ############################################################
        curr_year_df=sum(data2[data2['Year']==current_year][i].values)
        prev_year_df=sum(data2[data2['Year']==prev_year][i].values)
           
        diff=curr_year_df-prev_year_df
        perc=(diff/prev_year_df)*100


        res=''
        curr_year_df_median=np.median(data2[data2['Year']==current_year][i].values)
        prev_year_df_median=np.median(data2[data2['Year']==prev_year][i].values)

        diff_median=prev_year_df_median-curr_year_df_median
        if diff_median<0:
            res='decrease'
        elif diff_median>0:
            res='increase'

        perc=(diff/prev_year_df)*100

        ################################################################# print outs ################################################################# 
        st.write('----------------------------------------------------------------------------------------------------------------')  
        
        title_html=f'<h1 style="font-family:Calibri; color:#DEF294; font-size: 50px;">Did You Know?</h1>'
        st.markdown(title_html, unsafe_allow_html=True)
        
        st.write('----------------------------------------------------------------------------------------------------------------')  

        col1, col2, col3 = st.columns(3)
        col1.metric(highest_key,round(month_and_means[highest_key],2),"Highest Median")
        col2.metric(lowest_key,round(month_and_means[lowest_key],2),"Lowest Median",delta_color="inverse")
        col3.metric("",f"{round(perc,2)}%",f"Total {i} since last year",delta_color="off")

        st.write('----------------------------------------------------------------------------------------------------------------')  

        from conti_increase_finder import find_consecutive_three_increase
        

        for group_name, group_df in grouped:
            st.title(f"For {' in '.join(group_name)},")

            vals=group_df[i].values.tolist()
            arra_yr=group_df['Year'].values.tolist()
            arra_mnth=group_df['Month'].values.tolist()
    
            find_consecutive_three_increase(vals,arra_yr,arra_mnth)



        
        st.title(f'{i} is usually the highest during {highest_key} with a median value of {round(month_and_means[highest_key],2)} {selected_curr}.')
        st.title(f'{i} is usually the lowest during {lowest_key} with a median value of {round(month_and_means[lowest_key],2)} {selected_curr}')
        
       
        


        curr_year_df=sum(data2[data2['Year']==current_year][i].values)
        prev_year_df=sum(data2[data2['Year']==prev_year][i].values)
           
        diff=curr_year_df-prev_year_df
        perc=(diff/prev_year_df)*100


        res=''
        curr_year_df_median=np.median(data2[data2['Year']==current_year][i].values)
        prev_year_df_median=np.median(data2[data2['Year']==prev_year][i].values)

        diff_median=prev_year_df_median-curr_year_df_median
        if diff_median<0:
            res='decrease'
        elif diff_median>0:
            res='increase'
        
    

        perc=(diff/prev_year_df)*100
       
        if diff<0 and diff_median<0:
            st.title(f'There has been an {res} in median {i} across all products and regions by {round(diff_median,2)} {selected_curr}\
                     with an overall decrease by {round(perc,2)}% since last year.')
        elif diff>0 and diff_median>0:
            st.title(f'There has been an {res} in median {i} across all products and regions by {round(diff_median,2)} {selected_curr}\
                     with an overall {res} by {round(perc,2)}% since last year.')
        elif diff>0 and diff_median<0:
            st.title(f'There has been an {res} in median {i} across all products and regions by {round(diff_median,2)} {selected_curr}\
                     with an overall increase by {round(perc,2)}% since last year.')
        elif diff<0 and diff_median>0:
            st.title(f'There has been an {res} in median {i} across all products and regions by {round(diff_median,2)} {selected_curr}\
                     with an overall increase by {round(perc,2)}% since last year.')

        

            
        st.write('----------------------------------------------------------------------------------------------------------------')   




    
    str_categories=[]
    for key in categories:
        str_categories.append(key)
    #st.write(str_categories)

    stores1=[]
    stores2=[]

    for i in inputs_insights:
        for cat in str_categories:
            st.write('----------------------------------------------------------------------------------------------------------------')

            title_html=f'<h1 style="font-family:Calibri; color:#DEF294; font-size: 30px;">{cat}</h1>'
            st.markdown(title_html, unsafe_allow_html=True)

            

            st.write('----------------------------------------------------------------------------------------------------------------')

            df=data2[[i,cat,'Year']].groupby([cat,'Year']).mean()
            df1=data2[[i,cat,'Year']].groupby([cat,'Year']).sum()

            head_df_1=f'Mean {i}'
            head_df_2=f'Total {i}'

            

            df[head_df_1]=df[i]
            df[head_df_2]=df1[i]
            df.drop(i,axis=1,inplace=True)

            st.table(df)

            df2=data2[[i,cat]].groupby([cat]).sum()

            for year in data2['Year'].unique():
                
                df2=data2[data2['Year']==year]
                #st.write(df2)
                df2=df2[[i,cat]].groupby([cat]).sum()

                sum_cat_vals=sum(list(df2[i].values))
                df2[i]=df2[i].apply(lambda x: (x/sum_cat_vals)*100)

                head_df2=f'Total %age contribution to {i} in {year}'
                df2[head_df2]=df2[i]
                df2.drop(i,axis=1,inplace=True)
                st.table(df2)

            st.write('----------------------------------------------------------------------------------------------------------------')
  
    st.write('----------------------------------------------------------------------------------------------------------------') 
  
    considered_previously=[]
    for i in inputs_insights:


        
        for cat1 in str_categories:
            
            
            for cat2 in str_categories:
                
                
                if cat1!=cat2 and (cat1,cat2) not in considered_previously and (cat2,cat1) not in considered_previously:

                    try:
                        #st.write(cat1)
                        #st.write(cat2)

                        considered_previously.append((cat1,cat2))
                    
                        cat1_uniques=set(data2[cat1].values)
                        cat2_uniques=set(data2[cat2].values)
                    
                        for uniq1 in cat1_uniques:
                            for uniq2 in cat2_uniques:
                                df=data2[(data2[cat1]==uniq1) & (data2[cat2]==uniq2)]
                                #st.write(df)

                                df['year']=pd.DatetimeIndex(df['dtcol'].values).year
                                df=df[df['year']>=prev_year]
                
        
                                #fig=px.bar(df,x='dtcol',y=df[i],color=df[i],title=f'{i} of {cat1} in {cat2}')
                                #fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(217,224,223,0)")
                                #fig.update_yaxes(visible=False)
                                #st.plotly_chart(fig, use_container_width=True)

                                st.bar_chart(data=df, x='dtcol', y=i,use_container_width=True)

                                curr_year_df=sum(df[df['Year']==current_year][i].values)
                                prev_year_df=sum(df[df['Year']==prev_year][i].values)
                                diff=curr_year_df-prev_year_df
                                #st.write(diff)
        
                                perc=(diff/prev_year_df)*100
                                if diff<0:
                                    st.title(f'The net {i} for {uniq1} in {uniq2} decreased by {round(perc,2)}% since last year.')
                                else:
                                    st.title(f'The net {i} for {uniq1} in {uniq2} increased by {round(perc,2)}% since last year.')
                    except:
                        pass


######################################## function for calculating Statistical Inferences ###########################################################



def inf(data):

    """
    Calculating Statistical Inferences on Dataset 

    """

    counts_corr=0
    total_prints=0

    st.write('')
    st.write('')
    st.write('')
    st.write('')
    
    title_html=f'<h1 style="font-family:Calibri; color:#E8D5A4; font-size: 40px;">CORRELATIONS</h1>'
    st.markdown(title_html, unsafe_allow_html=True)
    st.caption('Measure of associations between numerical features in the Dataset')
    
    st.write('----------------------------------------------------------------------')

    if len(num_cols)<2:
        st.write('Insufficient number of features to observe Correlations')
    else:
        
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):

                try:
                    pear_corr=ss.pearsonr(data2[num_cols[i]],data2[num_cols[j]])
                    #st.write(pear_corr.statistic)

                    if pear_corr.statistic>=0.60:
                        st.write(f"There's an observed high positive correlation between {num_cols[i]} and {num_cols[j]} with a correlation \
                        statistic of {pear_corr.statistic} which suggests a positive increase in {num_cols[i]} is more often than not \
                        is linearly proportional to a positive increase in {num_cols[j]}")

                        counts_corr+=1
                    elif pear_corr.statistic<=-0.60:

                        st.write(f"There's an observed high negative correlation between {num_cols[i]} and {num_cols[j]} with a correlation \
                        statistic of {pear_corr.statistic} which suggests a decrease in {num_cols[i]} is more often than not \
                        is linearly proportional to a decrease in {num_cols[j]}")

                        counts_corr+=1
                    
                except:
                    pass
                    
        if counts_corr==0:
            st.write('Unfortunately, no significant Correlations have been found in the Dataset')
        else:
            pass
        st.write('----------------------------------------------------------------------')
    
    
    st.write('')
    st.write('')
    title_html=f'<h1 style="font-family:Calibri; color:#E8D5A4; font-size: 40px;">Analysis of Variance (ANOVA)</h1>'
    st.markdown(title_html, unsafe_allow_html=True)
    st.caption('ANOVA can be used to test whether there is a significant difference between the means \
             of Profit/Revenue etc of two or more products or services. This can help businesses to identify which products or services\
             are performing better with respect to the other and allocate resources accordingly.')

    st.caption('ANOVA works by decomposing the total variation in the dependent variable into two components:\
     variation due to differences between groups and variation due to differences within groups. The ratio of \
     these two components is used to calculate an F-statistic, which is used to test the null hypothesis that \
     all group means are equal.')
    st.write('----------------------------------------------------------------------')

    if len(cat_cols)==0 or len(num_cols)==0:
        st.write('Insufficent number of Categorical/Numerical Columns to observe ANOVA.')
    else:
        for num_col in num_cols:
            
            for col in categories:

                try:
                    model = sm.formula.ols(f'{num_col} ~ {col}', data=data2).fit()
                    table = sm.stats.anova_lm(model, typ=2)

                    
                    if table['PR(>F)'][0]<=0.05:

                        title_html=f'<h1 style="font-family:Calibri; color:#E8D5A4; font-size: 20px;">Analysis of Variance between the means of the various categories present in {col} with respect to {num_col}</h1>'
                        st.markdown(title_html, unsafe_allow_html=True)

                        st.write(f'Based on the p-value, it can be concluded that there is a SIGNIFICANT difference in the \
                        means of the items inside {col} being compared with respect to {num_col} which suggests that certain items\
                        might be underperforming or overperforming which need attention.')

                        st.caption(f'The table below displays the means of {num_col} of various items present in {col} which might\
                        help in the decision-making process.')

                        group_means = data2.groupby(col)[num_col].mean()
                        group_mean_index=group_means.index
                        group_mean_vals=group_means.values

                        group_means=pd.DataFrame(list(zip(group_mean_index,group_mean_vals)),columns=[col,f'Mean {num_col}'])
                        st.table(group_means)

                        total_prints+=1         
                except:
                    pass

        if total_prints==0:
            title_html=f'<h1 style="font-family:Calibri; color:#E8D5A4; font-size: 20px;">Unfortunately, no significant difference in means between the Categories has been\
            found for any of the Groups </h1>'
            st.markdown(title_html, unsafe_allow_html=True)
            

                


            st.write('-------------------------------------------------------------------------------------------')
           
                

##################################################################################################################################################################################################

def detect_anomaly(data,inputs_insights):

    """
    function to detect anomalies in the dataset.

    """

    title_html=f'<h1 style="font-family:Calibri; color:#DEF294; font-size: 40px;">Global Anomalies/Outliers</h1>'
    st.markdown(title_html, unsafe_allow_html=True)

    st.caption('By this procedure, first the Inter-quartile range is calculated. The Inter-quartile range is is a \
                  measure of the spread of the data, calculated as the difference between the third quartile (75th percentile) \
                  and the first quartile (25th percentile) of the data. The IQR is used to define an acceptable range of values, \
                  and data points that fall outside of this range are considered global outliers.')

    total_prints=0

    anom_months_counts={}

    cats=[]
    total_anom_points_list=[]

    

    for cols in categories:
        anom_points_list=[]

        for category in categories[cols]:

            cats.append(category)

            df_temp=data2[data2[cols]==category]
            find_anomaly_on=df_temp[inputs_insights]
            #st.write(df_temp)

            ################ Global Outliers ##############################

            title_html=f'<h1 style="font-family:Calibri; color:#E8D5A4; font-size: 20px;">Global Anomalies/Outliers using IQR for {category} on {inputs_insights}</h1>'
            st.markdown(title_html, unsafe_allow_html=True)

            fig=go.Figure()
            fig.add_trace(go.Box(y=find_anomaly_on, name="Data Point",boxpoints='suspectedoutliers', marker=dict(color='rgba(219, 64, 82, 0.6)',outliercolor='rgba(219, 64, 82, 0.6)',line=dict(outliercolor='rgba(219, 64, 82, 0.6)',outlierwidth=2)),line_color='rgb(8,81,156)'))
            fig.update_layout(title_text="Suspected Outliers on the Boxplot in Red, hover on the figure to reveal.")
            st.plotly_chart(fig, use_container_width=True)

            q1_pc1, q3_pc1 = df_temp[inputs_insights].quantile([0.25, 0.75])

            iqr_pc1 = q3_pc1 - q1_pc1

            lower_pc1 = q1_pc1 - (1.5*iqr_pc1)
            upper_pc1 = q3_pc1 + (1.5*iqr_pc1)

            st.write(f'IQR FOUND: {round(iqr_pc1,3)}')

            df_temp['anomaly_ii'] = ((df_temp[inputs_insights]>upper_pc1) | (df_temp[inputs_insights]<lower_pc1)).astype('int')

            df_anomalies=df_temp[df_temp['anomaly_ii']==1]



            #st.write(df_temp[df_temp['anomaly_ii']==1])

            try:
                found_months=df_anomalies['Month'].values
                found_years=df_anomalies['Year'].values
                found_values=df_anomalies[inputs_insights].values
            

            
            


                i=0
                while i<len(found_months):
                    title_html=f'<h1 style="font-family:Calibri; color:#F1EBDA; font-size: 15px;">An anomaly was found on {found_months[i]}, {found_years[i]} since \
                       the {inputs_insights} value {found_values[i]} showed significant deviation from the IQR</h1>'
                    st.markdown(title_html, unsafe_allow_html=True)

                    if found_months[i] in anom_months_counts:
                        anom_months_counts[found_months[i]]+=1
                    else:
                        anom_months_counts[found_months[i]]=1

                    anom_point=f'{found_months[i]},{found_years[i]}'
                    anom_points_list.append(anom_point)


                    i+=1
            
                total_anom_points_list.append(list(set(anom_points_list)))
            except:
                pass
            ################################### monthly outliers###########################################################
            try:
                std_month_df=df_temp[[inputs_insights,'Month']].groupby('Month').std()
                #st.write(std_month_df)

                st.write('_____________________________________________________________________________________________________________________________________')

                st.line_chart(std_month_df, use_container_width=True)
                st.caption(f'Standard Deviation of {category} {inputs_insights} by Month')

                title_html=f'<h1 style="font-family:Calibri; color:#F1EBDA; font-size: 15px;">Sharp peaks at any month on this plot indicates unusual behaviours\
                in {inputs_insights} within the lifecycle of that month through all the years that are present in the dataset.</h1>'
                st.markdown(title_html, unsafe_allow_html=True)

                st.write('_____________________________________________________________________________________________________________________________________')

            except:
                pass
            


    
    common_strings =find_common_strings(total_anom_points_list)
    #st.write(common_strings)
    #st.write(total_anom_points_list)

    st.write('')
    st.write('')

    st.image("https://cdn-icons-png.flaticon.com/512/5526/5526196.png",width=100)
    title_html=f'<h1 style="font-family:Calibri; color:#DEF294; font-size: 30px;">Did You Know?</h1>'
    st.markdown(title_html, unsafe_allow_html=True)

    if common_strings:

        all_content1=''
        for i in common_strings:
            all_content1+=i+' '

        all_content2=''
        for i in cats:
            all_content2+=i+','+' '

        title_html=f'<h1 style="font-family:Calibri; color:#F1EBDA; font-size: 15px;">Anomalies were found \
        in {all_content1} for each of {all_content2}. Certainly, this is not due to random chance.'

        st.markdown(title_html, unsafe_allow_html=True)
    
    sorted_dict = dict(sorted(anom_months_counts.items(), key=lambda item: item[1]))

    title_html=f'<h1 style="font-family:Calibri; color:#F1EBDA; font-size: 15px;">{list(sorted_dict.keys())[-1]} and {list(sorted_dict.keys())[-2]} were the \
    months which showed the highest number of Anomalies across all Categories. Do plan accordingly!</h1>'

    st.markdown(title_html, unsafe_allow_html=True)




    #st.write(anom_months_counts)

    st.write('------------------------------------------------------------------------------------------------------------------------------')
    st.write('------------------------------------------------------------------------------------------------------------------------------')

    

        

            




    

    




                    


            
                








################################################################### driver code ########################################################################################################

if location_of_data:
    
    
   

    try:
        sp=options_dict[selected_option]
    except:
        sp=''

    
    if sp=='SP': 
        result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)
        #query=st.text_input('Enter query:')
        #if len(query)>1:
           # answer=text_queries(query) 
            #st.title(answer)
            #tts_button = Button(label="Speak", width=100)

           # tts_button.js_on_event("button_click", CustomJS(code=f"""
           # var u = new SpeechSynthesisUtterance();
           # u.text = "{answer}";
           # u.lang = 'en-US';
           # speechSynthesis.speak(u);
           # """))

            #st.bokeh_chart(tts_button)
        #else:
            #st.stop()
        try:
            os.makedir("temp")
        except:
            pass
        
        if result:
           if "GET_TEXT" in result:

               try:
                    query=result.get("GET_TEXT")

                    
                    if 'ok' in query.lower() or 'great' in query.lower() or 'perfect' in query.lower() and len(query)<2:
                    
                        answer_html=f'<h1 style="font-family:Calibri; color:#D6EF7A; font-size: 30px;">Thank You! Please ask your next question!</h1>'
                        st.markdown(answer_html, unsafe_allow_html=True)
                        
                    
                    elif 'bye' in query.lower() or 'goodbye' in query.lower() and len(query)<2:
                        answer_html=f'<h1 style="font-family:Calibri; color:#D6EF7A; font-size: 30px;">Bye! We had a great interaction!</h1>'
                        st.markdown(answer_html, unsafe_allow_html=True)
                    elif 'hello' in query.lower() or 'hi' in query.lower() and len(query)<2:
                        answer_html=f'<h1 style="font-family:Calibri; color:#D6EF7A; font-size: 30px;">Hey there! How may I help you?</h1>'
                        st.markdown(answer_html, unsafe_allow_html=True)
                    else:
                        answer=text_queries(query)
                        answer_html=f'<h1 style="font-family:Calibri; color:#D6EF7A; font-size: 30px;">{answer}</h1>'
                        st.markdown(answer_html, unsafe_allow_html=True)
                
                        tts = gTTS(answer, lang='en',slow=False)
                        
                        tts.save("audio.mp3")
                        autoplay_audio("audio.mp3")
               
               except:
                    pass
                #speak = gTTS(text=answer,lang='en-in', slow=False)
                #speak.save('captured_voice.mp3')
                #speak.save('../Desktop/streamlitproj/captures_voice.mp3')
                #playsound('captured_voice.mp3')
                #os.remove('captured_voice.mp3')
                
        #else:
            #st.stop()
    elif sp=='DA':
            st.markdown('<iframe title="EDA_powerbi" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=632f5ce1-683f-4e40-ae7c-b396474a4807&autoAuth=true&ctid=5c979e27-0063-4697-891c-ba85b3eddf83" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)
    elif sp=='BO':
            result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

            if result:
                if "GET_TEXT" in result:
                    try:
                        query=result.get("GET_TEXT")
                        answer=text_queries(query)
        
                        st.subheader(answer)
                
                        tts_button = Button(label="Speak", width=100)

                        tts_button.js_on_event("button_click", CustomJS(code=f"""
                         var u = new SpeechSynthesisUtterance();
                         u.text = "{answer}";
                         u.lang = 'en-US';
                         speechSynthesis.speak(u);
                         """))
                    
                        st.bokeh_chart(tts_button)
                        st.markdown('<iframe title="EDA_powerbi" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=632f5ce1-683f-4e40-ae7c-b396474a4807&autoAuth=true&ctid=5c979e27-0063-4697-891c-ba85b3eddf83" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)
                    except:
                        pass
            else:
                st.stop()
    elif sp=='IN':
        inputs_insights=st.text_input("Do your year-on-year analysis on Data! (Ex:Sales/Profit/Revenue etc)")
        
        if len(inputs_insights)<1:
            st.stop()
        else:
             inputs_insights=inputs_insights.split(',')
             generate_insights(data2,inputs_insights)
    elif sp=='OA':
        inputs_insights=st.text_input("Find Anomalies/Outliers in your data! (Ex:Sales/Profit/Revenue etc)")

        if inputs_insights:
            
            try:
                detect_anomaly(data2,inputs_insights)
            except:
                st.write('Selected Column is not a Numerical Column or is not present in the Dataset')
        else:
            st.stop()
    elif sp=='ST':
        inf(data2)
    elif sp=='MC':
        column_chosen=st.text_input('Select a numerical column to run a Monte Carlo Simulation on:') 
        num_sims=st.slider('Number of Simulations to Run',min_value=1000,max_value=100000)

        if column_chosen and num_sims:
            run_mcs(column_chosen, num_sims)
        else:
            st.stop()
        
else:
    st.stop()

