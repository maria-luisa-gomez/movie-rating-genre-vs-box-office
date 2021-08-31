#!/usr/bin/env python
# coding: utf-8

# # Download and clean Dataset


# ## Movie industry analysis ##
# 
# #### The main purpose of this data analysis is to find out if there's a correlation between the rating of the movie and its box-office earnings. Movies high rated are always the ones that make more money? 
# 
# 
# ### HYPOTHESIS
# #### Other hypothesis we want to resolve:
# ####  1) Movie genre vs rating 
# ####  2) Movie genre vs awards - Why is hard for comedy movies to get to the Oscars?
 
# ### DATA SOURCE
# #### For this proyect we are going to work with two different data sources: Kaggle and IMDb API
# #### KAGGLE: Originally this data was downloades from IMDb API but the we need more information from the API that is missing. From this data we are going to use mainly imdb_title_id, original_title, year, country, language, budget and worlwide_gross_income.
# #### IMDb API: we are using imdb_title_id to make the request to the api and get the info about awards.



#Import libraries 

import numpy as np
import pandas as pd

import re

import warnings

warnings.filterwarnings('ignore')

# https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset -> Kaggle URL Dataset


#Download Kaggle dataset

!kaggle datasets download -d stefanoleone992/imdb-extensive-dataset


# Find downloaded zip file from Kaggle

!ls


#Decompress zip file

!tar -xzvf imdb-extensive-dataset.zip


#Delete downloaded zip file

!rm -rf imdb-extensive-dataset.zip


!rm -rf IMDb names.csv
# !rm -rf IMDb ratings.csv **
!rm -rf title_principals.csv                


# Read and convert the csv source data into a pandas dataframe.

pd.set_option('display.max_columns', None)
kaggle_movie_ratings = pd.read_csv("IMDb ratings.csv",encoding = "ISO-8859-1")


# print(kaggle_movie_ratings.head())


# Read and convert the csv source data into a pandas dataframe.

pd.set_option('display.max_columns', None)
kaggle_movie_dataset = pd.read_csv("IMDb movies.csv",encoding = "ISO-8859-1")



# Shows first 3 rows of the dataset.

# print(kaggle_movie_dataset.head(2))

# print(kaggle_movie_dataset.info())

# Generate various summary statistics, excluding NaN values.

# print(kaggle_movie_dataset.describe().T)


# It seems the mayority of the variables in this dataset are discrete/categorical type. We might be able to use "count" methods for these ones after applying some data cleaning and data consolidation. We will get clearer information later on. For this analytis we are not going to use the continous variables


# Calculates the percentage of null registers for each variable

percent_missing = round(kaggle_movie_dataset.isnull().sum() * 100 / len(kaggle_movie_dataset), 2)
percent_missing


# We definatelly need the "worlwide_gross_income" column and the "worlwide_gross_income" for this analysis even though they have one the highest missing data percentage. It shouldn't be a big inconvenience since we can only make 500 requests to the IMDb API (we need one per movie)


# Remove rows where the following columns values are missing


import movies_functions as mf
kaggle_movie_dataset2 = mf.notNulls(get_notnulls_columns, kaggle_movie_dataset)


# print(kaggle_movie_dataset2.info())



# Calculates the percentage of null registers for each variable

percent_missing2 = round(kaggle_movie_dataset2.isnull().sum() * 100 / len(kaggle_movie_dataset), 2)
percent_missing2


# #### Let's check if there are null values within the columns we want to use after deleting null values from "budget"


# Gets number of registers and variables of this dataset

# prin(kaggle_movie_dataset.shape)


# print(kaggle_movie_dataset2.shape)


# #### We need "worlwide_gross_income" to be and integer and we are going to selecto only $ currency


get_dollars = kaggle_movie_dataset2["worlwide_gross_income"].str.startswith('$', na=False)

kaggle_movie_dataset2[get_dollars]

# print(kaggle_movie_dataset2.head())


kaggle_movie_dataset2['worlwide_gross_income'] = kaggle_movie_dataset2['worlwide_gross_income'].str.replace('$', "")
kaggle_movie_dataset2.head()


# #### For simplicity we want o aggregate some of the categories within the genre column, but first we want to check how many unique values these ones have 

# Checking how many register we have for genre category


# print(dict(kaggle_movie_dataset2.genre.value_counts()))



genre_list = ['Drama', 'Comedy', 'Action', 'Crime', 'Horror', 'Adventure', 'Biography', 'Thriller', 'Fantasy', 'Animation']


# This function aggregates categories within a column given a list of categories


ref_column = "genre"
new_column = "genre_main"

kaggle_movie_dataset2 = mf.categoryAggr(genre_list, kaggle_movie_dataset2, ref_column, new_column)


# Everything that is out of this new assortment is going to be named as "Other"
kaggle_movie_dataset2.loc[~kaggle_movie_dataset2["genre_main"].isin(genre_list), "genre_main"] = "Other"

# print(dict(kaggle_movie_dataset2.genre_main.value_counts()))

# print(kaggle_movie_dataset2.head(2))


# Let's change also genre_main data type to category
kaggle_movie_dataset2["genre_main"] = kaggle_movie_dataset2["genre_main"].astype("category")


# #### For simplicity, we are going to take out 'Other' category from genre_main


kaggle_movie_dataset2 = kaggle_movie_dataset2[(kaggle_movie_dataset2["genre_main"] != "Other")]


# #### Drop not needed columns

selected_columns = ['imdb_title_id', 'title', 'original_title', 'year', 'genre', 'genre_main', 'duration', 'country', 'language', 'director', 'writer', 'actors','budget', 'worlwide_gross_income']


kaggle_movie_dataset_final = kaggle_movie_dataset2[kaggle_movie_dataset2.columns.intersection(selected_columns)]


# Rearrage columns
kaggle_movie_dataset_final = kaggle_movie_dataset_final[['imdb_title_id', 'title', 'original_title', 'year', 'genre', 'genre_main', 'duration', 'country', 'language', 'director', 'writer', 'actors', 'budget','worlwide_gross_income']]


# #### In order to make a fair comparison between movies for the gross income, we are going to select movies just from 2000's so inflation doesn't affect much


# Turn year values into integers

kaggle_movie_dataset_final["year"] = kaggle_movie_dataset_final["year"].astype("int")
# print(kaggle_movie_dataset_final.info())



# Filter out movies before the 2000's
kaggle_movie_dataset_final = kaggle_movie_dataset_final[(kaggle_movie_dataset_final["year"]>= 2000)]
# print(kaggle_movie_dataset_final.info())

# print(kaggle_movie_dataset_final.shape)


# #### We need a subset equally weighted

movie_dataset_final_sample = kaggle_movie_dataset_final.sample(n = 500, weights = kaggle_movie_dataset_final.groupby("genre_main")["genre_main"].transform('count'))


# print(dict(movie_dataset_final_sample.genre_main.value_counts()))


# #### Attach rating column to kaggle_movie_dataset_final dataframe from kaggle_movie_ratings. Only for movies within first dataframe


# Drop columns not nedeed from kaggle_movie_ratings
selected_columns_ratings = ['imdb_title_id', 'weighted_average_vote']
kaggle_movie_ratings2 = kaggle_movie_ratings[kaggle_movie_ratings.columns.intersection(selected_columns_ratings)]
# print(kaggle_movie_ratings2.head())



# Pandas Excel Vlookup :)

kaggle_movie_dataset_final = kaggle_movie_dataset_final.merge(kaggle_movie_ratings2, on='imdb_title_id')
# print(kaggle_movie_dataset_final.shape)


# #### Export to CSV

# Complete dataset
kaggle_movie_dataset_final.to_csv('kaggle_movie_dataset_final.csv', sep =',',index = False)


# Sample of 500 (rapidApi limit)
movie_dataset_final_sample.to_csv('movie_dataset_final_sample.csv', sep =',',index = False)

