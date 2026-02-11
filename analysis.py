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

