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
    dataframe = dataframe[dataframe['col'].notna()]
    info_over_time = dataframe.drop_duplicates(['Year' , col])['Year'].value_counts().reset_index().sort_values(by='count')
    info_over_time.rename(columns={f'count':col , 'Year':'Edition'},inplace=True)
    return info_over_time
# get most successful players by sports.
def most_successful_by_sport(df ,sport):
    temp = df[df['Medal'].notna()]
    temp = df[(df['Medal']!='No Medal')]

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
    temp = df[(df['Medal']!='No Medal') & (df['NOC']==country_code)]
    top_players = temp['Name'].value_counts().reset_index()
    top_players.columns = ['Name' , 'Medals']
    # left join original and top_players data frame on name.
    x = top_players.merge(df , on='Name' , how='left')[['Name' , 'Sport' , 'Medals' , 'NOC']].drop_duplicates('Name')
    return x.head(10)
# get events_over_years in a pivot table
def events_over_years(df , country):
        df = df.drop_duplicates(['Year' , 'Sport' , 'Event'])
        df = df[df['NOC'].notna()]
        x = df[df['NOC']==country]
        event_over_time = x.pivot_table(index = 'Sport' , values='Event'  , columns='Year', aggfunc='count' , fill_value=0).reset_index()
        return event_over_time
# medal_tally countrywise
def medal_tally_country_wise(df, country):
    temp = df.dropna(subset=['Medal'])
    temp = df[(df['NOC'] == country) & (df['Medal'] != 'No Medal')]
    temp = temp.drop_duplicates(subset=['NOC', 'Year', 'Sport', 'Event', 'Medal'])
    country_wise_medal_tally = temp.groupby('Year').count()['Medal'].reset_index()
    return country_wise_medal_tally
# medal_tally countrywise over the years.
def medal_over_the_years(df,country):
    df = df.dropna(subset=['Medal'])
    df = df.drop_duplicates(subset=['NOC', 'Year', 'Sport', 'Event', 'Medal'])
    new_df = df[(df['NOC']==country)&(df['Medal']!='No Medal')]
    x = new_df.pivot_table(index='Sport' , values='Medal' , columns='Year',  aggfunc='count' ,fill_value=0).reset_index()
    return x 

def age_distribution_by_sport(df):
    athlete_df = df.drop_duplicates(subset=['Name','NOC'])
    gold_won = athlete_df[athlete_df['Medal']=='Gold']
    unique_sports = gold_won['Sport'].value_counts().head(20).index.tolist()
    sport_names = []
    val = []
    for sport in unique_sports:
        ages = gold_won[gold_won['Sport']==sport]['Age']
        val.append(ages)
        sport_names.append(sport)
        
def weight_vs_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','NOC','Medal'])
    if sport !='Overall':
        temp_df = athlete_df[(athlete_df['Sport']==sport)]
        return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name','NOC'])
    men = athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women ,on='Year' ,how='left')
    final.rename(columns={'Name_x':'Men' , 'Name_y':'Women'},inplace=True)
    final = final.fillna(0)
    final = final.astype(int)
    return final 