import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
import kagglehub

def preprocess(csv_path):
    df = pd.read_csv(csv_path , sep=',' ,encoding="ISO-8859-1") # load dataset.
    df = df[df['Season']=='Summer'] # use only summer olympics data.
    # Identify only the columns that are strings (objects)
    
    strip_cols = df.select_dtypes(include=['object']).columns

# Apply strip only to those columns
    df[strip_cols] = df[strip_cols].map(lambda x: " ".join(x.split()) if isinstance(x, str) else x)

        
# fill missing values
    df['Medal'] = df['Medal'].fillna('No Medal') # fill missing medals as no medal won
    cols = ['Age' , 'Weight' , 'Height']    
    # group by sport and then fill median.
    for col in cols:
        df[col] = df[col].fillna(df.groupby('Sport')[col].transform('median'))
        df[col] = df[col].fillna(df.groupby('Sex')[col].transform('median'))
     
     # one hot encode medal colums
    encoded = pd.get_dummies(df['Medal'], dtype=int)
    
    df = pd.concat([df , encoded] , axis=1) # get final df
    df.drop(columns=['ID'] , inplace=True) # drop un-needed columns
    
    # drop duplicate values
    duplicate_val_cols = ['Team' , 'Event' , 'Medal' , 'Year' , 'City' ,'Sport' , 'Games'] 
    df.drop_duplicates(subset=duplicate_val_cols , inplace=True)
    return df






    
    