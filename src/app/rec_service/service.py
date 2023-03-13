import os

from typing import Optional, List
from collections import defaultdict

from fastapi import HTTPException, Form, Depends, File, UploadFile
from fastapi.responses import FileResponse

import pandas as pd
import numpy as np
from sklearn.metrics import euclidean_distances
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import difflib

from ..base.service_base import Service_base
from .. library import models
from . import models as model_params
from . import schemas

class Recs_service(Service_base):
    model = model_params.Track_params
    get_schema = schemas.Params_get_schema

    def __init__(self):
        self.dataset = pd.read_csv('data/release_data.csv')
        self.data = pd.DataFrame(self.dataset)
        self.track_cluster_pipeline = Pipeline([('scaler', StandardScaler()),
                                                ('kmeans', KMeans(n_clusters=10, verbose=False))], 
                                                verbose=False)
        self.number_cols = ['name', 'artists', 'duration_s', 'year', 'explicit', 'valence', 'acousticness', 
                            'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo']

    async def get_track_artists_names(self, **kwargs) -> Optional[List]:
        _track = await models.Track.get(**kwargs)
        return await models.Artist.filter(tracks=_track.id).values('name')

    async def get_track_params(self, **kwargs) -> Optional[pd.DataFrame]:
        track_data = defaultdict()
        _track = await models.Track.get(**kwargs)
        _track_params_json = (await self.get_schema.from_tortoise_orm(
                                await model_params.Track_params.get(**kwargs))
                            .json(indent=4))

        track_data['name'] = [_track.name]
        track_data['artists'] = [self.get_track_artists_names(id=_track.id)]
        track_data['duration_s'] = [_track.duration_s]

        for key, value in _track_params_json.items():
            track_data[key] = value

        return pd.DataFrame(track_data)

    async def get_mean_vector(self, song_list_id):
        track_vectors = []

        for i in song_list_id:
            track_data = await self.get_track_params(id=i)
            track_vector = track_data[self.number_cols].values
            track_vectors.append(track_vector)

        track_matrix = np.array(list(track_vectors))
        return np.mean(track_matrix, axis=0)

    def flatten_dict_list(self, dict_list):
        flattened_dict = defaultdict()
        for key in dict_list[0].keys():
            flattened_dict[key] = []
        
        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)

        return flattened_dict
    
    def recommend_songs(self, track_list, n_tracks=10):
        
        metadata_cols = ['name', 'year', 'artists']
        track_dict = self.flatten_dict_list(track_list)

        track_center = self.get_mean_vector(track_list)
        scaler = self.track_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(self.data[self.number_cols])
        scaled_track_center = scaler.transform(track_center.reshape(1, -1))
        distances = cdist(scaled_track_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_tracks][0])

        rec_tracks = self.data.iloc[index]
        rec_tracks = rec_tracks[~rec_tracks['name'].isin(track_dict['name'])]
        return rec_tracks[metadata_cols].to_dict(orient='records')


rec_service = Recs_service()

