import tensorflow as tf
import numpy as np
import pandas as pd
import json
from data_processing import prepare_features

class MovieRecommender:
    def __init__(self, model_path, movie_info_path):
        self.model = self.load_model(model_path)
        self.movie_info = pd.read_csv(movie_info_path)  # Carregando informações dos filmes

    def load_model(self, model_path):
        try:
            model = tf.keras.models.load_model(model_path)
            print("Modelo carregado com sucesso de:", model_path)
            return model
        except Exception as e:
            print("Erro ao carregar o modelo:", e)

    def predict(self, user_id):
        try:
            # Criar pares de usuário-filme para todos os filmes
            all_movie_ids = self.movie_info['movieId'].values
            user_movie_pairs = np.transpose([np.repeat(user_id, len(all_movie_ids)), all_movie_ids])
            
            # Fazendo previsões para todos os filmes
            predictions = self.model.predict([user_movie_pairs[:, 0], user_movie_pairs[:, 1]])
            
            # Selecionar os top-10 filmes
            top_k_indices = np.argsort(predictions[:, 0])[::-1][:10]
            top_k_movie_ids = all_movie_ids[top_k_indices]
            top_k_movies = self.movie_info.loc[self.movie_info['movieId'].isin(top_k_movie_ids)]
            
            return top_k_movies
        except Exception as e:
            print("Erro ao fazer previsão:", e)

if __name__ == "__main__":
    model_path = '../data/cinematch.keras'
    movie_info_path = '../data/movies.csv'
    recommender = MovieRecommender(model_path, movie_info_path)
    
    user_id = 123  # ID de um usuário exemplo para quem as recomendações serão geradas

    # Carregar dados do usuário específico e preparar features
    data = pd.read_csv('../data/new_user_data.csv')
    
    # Carregar vocabulários
    with open('../data/genre_vocab.json', 'r') as f:
        genre_vocab = json.load(f)
    with open('../data/tag_vocab.json', 'r') as f:
        tag_vocab = json.load(f)

    features = prepare_features(data, genre_vocab, tag_vocab)

    # Fazer previsão usando features preparadas
    recommended_movies = recommender.predict(features)
    print("Filmes recomendados:")
    print(recommended_movies)
