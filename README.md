# Movie rating / box office / Awards by genre

#### The main purpose of this data analysis is to find out if there's a correlation between the rating of the movie and its box-office earnings. Movies high rated are always the ones that make more money?

#### Note that in order to make a fair analyis in terms of box-office earnings we are filtering movies just from the 2000's and movies with earnings dollar currency only.

### HYPOTHESIS

#### Other hypothesis we want to resolve:
####  1) Movies high rated are always the ones that make more money?
####  2) Movie genre vs rating 
####  2) Movie genre vs awards - Why is hard for comedy movies to get to the Oscars? Note we could only get 380 registers from IMDb api because of the request limit

## see analysis [here](https://nbviewer.jupyter.org/github/maria-luisa-gomez/movie-rating-genre-vs-box-office/blob/main/Movies_Analysis.ipynb))

### DATA SOURCE

#### For this proyect we are going to work with two different data sources: Kaggle and IMDb API (rapidapi)
#### KAGGLE: Originally this data was downloades from IMDb API but the we need more information from the API that is missing. From this data we are going to use mainly imdb_title_id, original_title, year, country, language, budget and worlwide_gross_income.
#### IMDb API (rapidapi): we are using imdb_title_id to make the request to the api and get the info about awards.
#### NOTES ABOUT IMDb API (rapidapi): 

#### You can only make a query by movie title througth IMBb API.  For example "Titanic".
#### Movie title is mandatory if you want any type of query througth IMBb API.  For example "Titanic" --> https://imdb-api.com/API/Search/{APIKey}/Titanic.
#### You'll get Titanic movie info and also information about movies that matches close variants of that one, like "Titan". That can be an issue and a complicated situation in which we will have to extract from all the matches the one we want. If you make 500 requests from 500 different movies, thousand of other movies information will be there.
#### For this matter we can make a title query by title ID (unique for each movie) and will make sure we get only the information of the movies we want.  We will use a IMDb csv dataset already available in Kaggle which includes these ids and its correspodent movie title.

### LIBRARIES

numpy

pandas

seaborn

datetime

matplotlib.pyplot

regex

plotly
