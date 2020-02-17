import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
###### helper functions. Use them when needed #######
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]
##################################################

##Step 1: Read CSV File
df = pd.read_csv("movie_dataset.csv")
#print df.columns
##Step 2: Select Features

features = ['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	except:
		print("Error:", row)	


df["combined_features"] = df.apply(combine_features,axis=1)

#print "Combined Features:", df["combined_features"].head()

##Step 4: Create count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix) 

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def update():
    try:
        movies=[]
        movie_user_likes=request.form.get("movielike")
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies =  list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
        i=0
        for element in sorted_similar_movies:
            movies.append(get_title_from_index(element[0]))
            i=i+1
            if i>50:
                print(movies,flush='True')
                return render_template("result.html", movies=movies)
    except Exception as e:
        print(e)
        return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)