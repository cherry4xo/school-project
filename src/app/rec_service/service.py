import os
import json

from typing import Optional, List
from collections import defaultdict

from fastapi import HTTPException, Form, Depends, File, UploadFile
from fastapi.responses import FileResponse

import pandas as pd
import numpy as np
from sklearn.compose import make_column_selector
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
        self.dataset = pd.read_csv('src/app/rec_service/data/release_data.csv', 
                                    delimiter=',', 
                                    skiprows=1, 
                                    names=['id', 'name', 'artists', 'year', 'explicit', 'valence', 'acousticness', 'danceability', 
                                           'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo'],
                                    encoding='utf-8')
        self.data = pd.DataFrame(self.dataset)
        self.track_cluster_pipeline = Pipeline([('scaler', StandardScaler()),
                                                ('kmeans', KMeans(n_clusters=10, verbose=False))], 
                                                verbose=False)
        self.X = self.data.select_dtypes(np.number)
        self.X = self.X.fillna(0)
        self.X = self.X.drop(columns=['year'])
        self.cols = list(self.X.columns)
        self.track_cluster_pipeline.fit(self.X)
        self.track_cluster_labels = self.track_cluster_pipeline.predict(self.X)
        self.data['cluster_label'] = self.track_cluster_labels
        self.number_cols = ['explicit', 'valence', 'acousticness', 'danceability', 
                            'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo']
        self.str_cols = ['id', 'name', 'artists', 'year']

    async def get_track_artists_names(self, **kwargs) -> Optional[List]:
        _track = await models.Track.get(**kwargs)
        return await models.Artist.filter(tracks=_track.id).values('name')

    async def get_track_data_by_id(self, **kwargs) -> schemas.Track_page_get:
        _track = await models.Track.get_or_none(**kwargs)
        _artists_track = await models.Artist.filter(tracks=_track.id).values('id')
        _artists_track_response = []
        for j in _artists_track:
            _artist_track = await models.Artist.get(id=j['id'])
            _artists_track_response.append({'id': _artist_track.id, 
                                            'name': _artist_track.name})
        return {'track_data': await schemas.Track_get_schema.from_tortoise_orm(_track),
                'artists': _artists_track_response}

    async def get_id_by_track_name(self, **kwargs):
        obj = await models.Track.get(**kwargs)
        return obj.id

    async def get_track_params(self, id: dict) -> Optional[pd.DataFrame]:
        track_data = defaultdict()
        _track = await models.Track.get(id=id['id'])
        _params = (await self.get_schema.from_tortoise_orm(
                    await model_params.Track_params.get(track_id=_track.id)))
        _track_params_json = _params.json()
        _track_params_dict = json.loads(_track_params_json)

        track_data['name'] = [_track.name]
        track_data['artists'] = [await self.get_track_artists_names(id=_track.id)]
        track_data['duration_s'] = [_track.duration_s]
        for key, value in _track_params_dict.items():
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

    def flatten_dict_list(self, dict_list) -> defaultdict:
        flattened_dict = defaultdict()
        for key in dict_list[0].keys():
            flattened_dict[key] = []
        
        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)

        return flattened_dict
    
    async def recommend_tracks(self, track_list, n_tracks=20) -> List[schemas.Track_page_get]:
        
        metadata_cols = ['id']
        track_dict = self.flatten_dict_list(track_list)

        track_center = await self.get_mean_vector(track_list)
        scaler = self.track_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(self.data[self.number_cols])
        scaled_track_center = scaler.transform(track_center.reshape(1, -1))
        distances = cdist(scaled_track_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_tracks][0])

        rec_tracks = self.data.iloc[index]

        rec_tracks = rec_tracks[~rec_tracks['name'].isin(track_dict['name'])]
        rec_tracks_dict = rec_tracks[metadata_cols].to_dict(orient='records')

        rec_tracks_list = [value for _, value in self.flatten_dict_list(rec_tracks_dict).items()][0]

        return [await self.get_track_data_by_id(id=i) for i in rec_tracks_list]

    async def get_recommends_by_library_tracks(self, **kwargs):

        obj = await models.User.get(**kwargs)
        _library = await models.Library.get(user=obj)
        _tracks = await models.Track.filter(libraries=_library.id).values('id', 'name')
        return await self.recommend_tracks(_tracks)

rec_service = Recs_service()

