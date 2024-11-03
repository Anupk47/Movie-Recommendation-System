import streamlit as st
import pickle
import requests
import os


#since the github size limit is 100mb and similar.pkl size is more than 150mb it was a nuisance
#so added externally downloadble similar.pkl file when streamlit will first deploy it will download all 
#similar.pkl file

def download_pkl_from_dropbox(url,filename):
    response = requests.get(url, stream=True)
    with open(filename,"wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


dropbox_url =   'https://www.dropbox.com/scl/fi/hx4l86hqblw337vgl7zag/similar.pkl?rlkey=cft9cw5sihuybabvz5rmb050p&st=ji0rusob&dl=1'
filename = 'similar.pkl'

          
#checking if file already exists locally to avoid repeated downloads    
if not os.path.exists(filename):
    st.write("Downloading Recommendatoin data...")
    download_pkl_from_dropbox(dropbox_url, filename)


#loading the downloaded file 
with open(filename, 'rb') as file:
    recommend = pickle.load(file)
    
    
#load the movies.pkl file
mv = pickle.load(open('movies.pkl','rb'))
mv_title= mv['title'].values



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=89f970116f55c100c6adc1f21157ad34'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    
    
    

# recommend = pickle.load(open('similar.pkl','rb'))




def recommends(movie):
    movie_index = mv[mv['title'] == movie].index[0] #takes the index of current movie
    distances = recommend[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    
    recommend_movies_poster= []
    
    recommendations = [mv.iloc[i[0]].title for i in movie_list]  # List of recommended movie titles
    for i in movie_list:
        movie_id = mv.iloc[i[0]].id
        
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommendations,recommend_movies_poster
    

st.title('MOVIE RECOMMENDATION SYSTEM')


option = st.selectbox(
    "FIND SIMILAR MOVIES",
    (mv_title),
    index=None,
    placeholder="Select Movie To get Recommended...",
)


    
#st.write("You selected:", option)


if st.button("Get Recommendations"):
    recommended_movies, posters = recommends(option)
    
    # First row with columns of custom widths
    col1, spacer1, col2, spacer2, col3, spacer3, col4, spacer4, col5 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1,0.1, 1])

    with col1:
        st.text(recommended_movies[0])
        st.image(posters[0])

    with col2:
        st.text(recommended_movies[1])
        st.image(posters[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(posters[2])
        
    with col4:
        st.text(recommended_movies[3])
        st.image(posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(posters[4])        

    # Second row to display remaining items below
    col6, spacer5, col7, spacer6, col8, spacer7, col9, spacer8, col10 = st.columns([1, 0.1, 1, 0.1, 1,0.1, 1,0.1,1])

    with col6:
        st.text(recommended_movies[5])
        st.image(posters[5])     

    with col7:
        st.text(recommended_movies[6])
        st.image(posters[6])  

    with col8:
        st.text(recommended_movies[7])
        st.image(posters[7])  
    with col9:
        st.text(recommended_movies[8])
        st.image(posters[8]) 
    with col10:
        st.text(recommended_movies[9])
        st.image(posters[9]) 
 