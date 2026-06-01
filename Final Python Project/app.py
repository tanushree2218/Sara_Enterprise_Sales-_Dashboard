import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 

#load dataset

df = pd.read_excel(r"dataset/Financial_Sample (2).xlsx")

# Removing Missing Values
for col in df.columns:
    if df[col].isnull().sum()>0:
        if df[col].dtype == 'str':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].mean())


st.set_page_config(page_title="Sara Enterprises" , layout='wide')
st.title("Sales Analysis For Sara Enterprises...")

filtered_df = df.copy()
col1 ,  col2 , col3 , col4 , col5 =st.columns(5)
with col1:
    country = st.selectbox("Select Country",["All"]+list(df["Country"].unique()))
    if country!="All":
        filtered_df = filtered_df[filtered_df["Country"] == country]
with col2:
    segment = st.selectbox("Select Segment",["All"]+list(df["Segment"].unique()))
    if segment!="All":
        filtered_df = filtered_df[filtered_df["Segment"] == segment]

with col3:
    product = st.selectbox("Select Product",["All"]+list(df["Product"].unique()))
    if product!="All":
        filtered_df = filtered_df[filtered_df["Product"] == product]
with col4:
    db = st.selectbox("Select Discount Band",["All"]+list(df["Discount Band"].unique()))
    if db!="All":
        filtered_df = filtered_df[filtered_df["Discount Band"] == db]
with col5:
    year = st.selectbox("Select Year",["All"]+list(df["Year"].unique()))
    if year !="All":
        filtered_df = filtered_df[filtered_df["Year"] == year]

# KPI : KEY POINT INDICATOR

col1 , col2 , col3 , col4 , col5 = st.columns([1.1,1,1,1,1])
with col1:
    st.metric("Total Sales" , round(filtered_df[' Sales'].sum(),2)) 
with col2:
    st.metric("Total Profit" , round(filtered_df['Profit'].sum(),2)) 
with col3:
    st.metric("Total Sold Quantity" , round(filtered_df['Units Sold'].sum(),2)) 
with col4:
    st.metric("Total Discount" , round(filtered_df['Discounts'].sum(),2)) 
with col5:
    st.metric("Total Orders" , filtered_df.shape[0]) 

col1 , col2 = st.columns(2)
with col1:
    fig , ax = plt.subplots(figsize=(10,4))
    sns.barplot( x='Segment' , y='Profit' , data=filtered_df, ax=ax)
    st.pyplot(fig)
with col2:
    fig , ax =plt.subplots(figsize=(10,4))
    sns.histplot(x='Profit' , data=filtered_df , kde=True , ax=ax )
    st.pyplot(fig)
fig , ax =plt.subplots(figsize=(12,2))
sbm = filtered_df.groupby('Month Name')[' Sales'].sum().reindex(filtered_df.sort_values('Month Number')['Month Name'].unique()).reset_index()
sns.lineplot( x='Month Name' , y=' Sales' , data= sbm , ax=ax)
st.pyplot(fig)
     
st.dataframe(filtered_df , height=250)