import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# we have inserted "Overall" record to do future overall analysis 
def get_country_years(df_copy):
    # get unique country
    country = df_copy['NOC'].unique().tolist()
    country.insert(0 , "Overall")
    # get unique years.
    years = df_copy['Year'].unique().tolist()
    years.sort()
    return years,country
# get medal tally
def get_medal_tally(df , year , country):
    '''
    there can be 4 cases in case of getting medal tally
    1) overall analysis by year of a country
    3) performance by country
    2) performance by year
    4) performance by country and year.
    '''
    medal_df = df[['Team' , 'NOC' , 'Games' ,'Year' , 'City' , 'Sport' , 'Event' , 'No Medal' , 'Gold' , 'Silver' , 'Bronze' , 'Medal']]

    flag = 0
    # case1
    if(year == 'Overall' and country =='Overall'):
        temp_df = medal_df
    # case 2
    if(year=='Overall' and country!='Overall'):
       flag = 1
       temp_df =  medal_df[medal_df['NOC']==country] 
    # case 3
    if(year!='Overall' and country =='Overall'):
        temp_df = medal_df[medal_df['Year']==int(year)]
    # case 4
    if( year!='Overall' and country!='Overall'):
       temp_df =  medal_df[(medal_df['NOC']==country) & (medal_df['Year']==year)]
       
    # get medals by each country and Year.
    if(flag==1):
        medal_tally = temp_df.groupby(['Year']).sum()[['Gold' , 'Silver' , 'Bronze']].sort_values(by='Year' , ascending=True).reset_index()
        
    else:
        
        medal_tally = temp_df.groupby(['NOC']).sum()[['Gold' , 'Silver' , 'Bronze']].sort_values(by='Gold' , ascending=False).reset_index()
        
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    # print(medal_tally)
    return medal_tally
# get info over the years . can be nations that participated each year or number of events each year.
def info_over_years(dataframe , col):
    # no. of nations participated in olympics each year.
    info_over_time = dataframe.drop_duplicates(['Year' , col])['Year'].value_counts().reset_index().sort_values(by='count')
    info_over_time.rename(columns={f'count':col , 'Year':'Edition'},inplace=True)
    return info_over_time
# get most successful players by sports.
def most_successful_by_sport(df ,sport):
    temp = df[df['Medal'].notna()]
    if sport!='Overall':
        temp = df[df['Sport']==sport]
    
    top_players = temp['Name'].value_counts().reset_index()
    top_players.columns = ['Name' , 'Medals']
    # left join original and top_players data frame on name.
    x = top_players.merge(df , on='Name' , how='left')[['Name' , 'Sport' , 'Medals' , 'NOC']].drop_duplicates('Name')
    return x.head(10)
# get most successful players of a country 
def most_successful_by_country_code(df ,country_code):
    temp = df[df['Medal'].notna()]
    temp = df[df['NOC']==country_code]
    top_players = temp['Name'].value_counts().reset_index()
    top_players.columns = ['Name' , 'Medals']
    # left join original and top_players data frame on name.
    x = top_players.merge(df , on='Name' , how='left')[['Name' , 'Sport' , 'Medals' , 'NOC']].drop_duplicates('Name')
    return x.head(10)
# get events_over_years in a pivot table
def events_over_years(df , country):
    df = df.drop_duplicates(['Year' , 'Sport' , 'Event'])
    x = df[df['NOC']==country]
    event_over_time = x.pivot_table(index = 'Sport' , values='Event'  , columns='Year', aggfunc='count' , fill_value=0)
    return event_over_time
