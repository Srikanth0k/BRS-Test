import uvicorn
import numpy as np
import json
import pandas as pd
from fastapi import FastAPI
import pickle
app=FastAPI()

sim_score= pd.read_pickle(open('similarity_scores.pkl', 'rb'))
books = pd.read_pickle(open('books.pkl', 'rb'))
book_pivot = pd.read_pickle(open('pt.pkl','rb'))

@app.get('/')
def index():
    return {'message': 'APP DEV TEST'}

@app.get("/recommendBook")
def recommend(book_name):
    # index fetch
    index = np.where(book_pivot.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(sim_score[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == book_pivot.index[i[0]]]

        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        
        data.append(item)
    
    df=pd.DataFrame(data, columns=["title", "author"])
    val = df.to_json(orient="records")
    val = json.loads(val)
    
    return val

if __name__ == '__main__':
     uvicorn.run(app, port=80, host='127.0.0.1:8000')
