import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel 


def get_data():
    #Get the books
    df = pd.read_csv('books.csv')
    return df


def similar_books(title):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')

    books = get_data()

    matrix = tf.fit_transform(books["description"])

    cosine_similarities = linear_kernel(matrix,matrix)

    indices = pd.Series(books.index, index=books['title'])

    if title not in books["title"].unique():
        return "No such movie in dataset"

    else:
        idx = indices[title]

        sim_scores = list(enumerate(cosine_similarities[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:31]

        movie_indices = [i[0] for i in sim_scores]

        return books["title"].iloc[movie_indices]