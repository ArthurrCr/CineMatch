# __init__.py em src/
# Isso torna mais fácil importar as classes e funções dos módulos internos

from .model import MovieRecommender
from .data_processing import prepare_features, split_genres, encode_tags
