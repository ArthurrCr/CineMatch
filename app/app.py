from flask import Flask, request, jsonify
import pandas as pd
import json
from src import MovieRecommender, prepare_features

app = Flask(__name__)

# Carregar vocabulários uma única vez quando o servidor iniciar
with open('../data/genre_vocab.json', 'r') as f:
    genre_vocab = json.load(f)
with open('../data/tag_vocab.json', 'r') as f:
    tag_vocab = json.load(f)

recommender = MovieRecommender('../data/cinematch.keras', '../data/movies.csv')

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    if user_id:
        user_id = int(user_id)  # Converter o user_id para inteiro
        data = pd.read_csv('../data/new_user_data.csv')  # Ou qualquer outro meio de obter dados do usuário
        features = prepare_features(data, genre_vocab, tag_vocab)
        
        # Filtrar os features apenas para o user_id solicitado (ajuste conforme necessário)
        user_features = {k: v[data['userId'] == user_id] for k, v in features.items()}
        
        recommended_movies = recommender.predict(user_features)
        return jsonify(recommended_movies.to_dict()), 200
    else:
        return "User ID is required", 400

if __name__ == '__main__':
    app.run(debug=True)
