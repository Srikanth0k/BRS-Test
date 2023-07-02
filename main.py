import uvicorn
import numpy as np
import pandas as pd 
from fastapi import FastAPI
import pickle
app=FastAPI()

similarity_scores= pickle.load(open('similarity_scores.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
books_pivot = pickle.load(open('pt.pkl','rb'))

@app.get('/')
def index():
    return {'message': 'APP DEV TEST'}

@app.get("/recommendBook")
def recommend(book_name):
    # index fetch
    index = np.where(books_pivot.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == books_pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        
        data.append(item)
    
    return data

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
