import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=474a7f15ed8defb46291a4ce150b2a44&language=en-US'.format(movie_id))
    data=response.json()
    return 'https://image.tmdb.org/t/p/original/'+data['poster_path']
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:13]
    recommendations=[]
    recommendations_poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommendations.append(movies.iloc[i[0]].title)
        # fetch poster
        recommendations_poster.append(fetch_poster(movie_id))
    return recommendations,recommendations_poster

st.title('Movie Recommendation System')

movie_selected=st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommend(movie_selected)
    #n_rows = 1 + len(cat_images) // int(n_cols)
    rows = [st.container() for _ in range(4)]
    cols_per_row = [r.columns(3) for r in rows]
    cols = [column for row in cols_per_row for column in row]
    for image_index, poster in enumerate(posters):
        cols[image_index].image(poster,caption=names[image_index])

    # col1,col2,col3,col4,col5,col6=st.columns(6)
    # with col1:
    #
    #     st.image(posters[0],caption=names[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1],caption=names[1])
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])
    # with col6:
    #     st.text(names[5])
    #     st.image(posters[5])