import pandas as pd
import numpy as np
import json

def split_genres(data, genre_vocab):
    """
    Cria uma representação de one-hot encoding para cada gênero com base no vocabulário fornecido.
    """
    for genre in genre_vocab:
        data['genre_' + genre] = data['genres'].apply(lambda x: 1 if genre in x else 0)
    return data

def encode_tags(data, tag_vocab):
    """
    Cria uma representação de one-hot encoding para tags com base no vocabulário fornecido.
    """
    for tag in tag_vocab:
        data['tag_' + tag] = data['tag'].apply(lambda x: 1 if x == tag else 0)
    return data

def prepare_features(data, genre_vocab, tag_vocab):
    """
    Função que processa os dados usando vocabulários específicos para gêneros e tags.
    """
    data = split_genres(data, genre_vocab)
    data = encode_tags(data, tag_vocab)

    # Preparar features para modelo
    features = {
        'user_id': np.array(data['userId']),
        'movie_id': np.array(data['movieId']),
        'genres': np.array(data[['genre_' + g for g in genre_vocab]]),
        'tags': np.array(data[['tag_' + t for t in tag_vocab]])
    }
    return features

if __name__ == "__main__":
    # Carregar vocabulários
    with open('../data/genre_vocab.json', 'r') as f:
        genre_vocab = json.load(f)
    with open('../data/tag_vocab.json', 'r') as f:
        tag_vocab = json.load(f)

    # Carregar dados
    data = pd.read_csv('../data/novos_dados.csv')
    features = prepare_features(data, genre_vocab, tag_vocab)
    print("Features prepared for model input:", features)
