from tortoise import fields
from tortoise.models import Model
from ..user.models import User
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Library(Model):
    id = fields.IntField(pk=True,
                        unique=True,
                        not_null=True, 
                        auto_increment=True)
    
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField('models.User',
                                                                    related_name='User_id')

    tracks: fields.ManyToManyRelation['Track'] = fields.ManyToManyField('models.Track',
                                                                        related_name='libraries',
                                                                        through='Library_tracks')
    artists: fields.ManyToManyRelation['Artist'] = fields.ManyToManyField('models.Artist',
                                                                        related_name='libraries',
                                                                        through='Library_artists')
    albums: fields.ManyToManyRelation['Album'] = fields.ManyToManyField('models.Album',
                                                                        related_name='libraries',
                                                                        through='Library_albums')
    playlists: fields.ManyToManyRelation['Playlist'] = fields.ManyToManyField('models.Playlist',
                                                                            related_name='libraries',
                                                                            through='Library_playlists')
    genres: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre',
                                                                        related_name='libraries',
                                                                        through='Libraries_genres')

    class Meta:
        table = 'Library'


class Track(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=255, 
                            not_null=True)
    duration_s = fields.IntField(default=None)
    track_file_path = fields.CharField(max_length=1000,
                                        not_null=True,
                                        default='')

    picture_file_path = fields.CharField(max_length=1000,
                                        not_null=True, default='data/default_image.png')

    libraries: fields.ManyToManyRelation['Library']
    artists: fields.ManyToManyRelation['Artist'] = fields.ManyToManyField('models.Artist',
                                                                        related_name='tracks',
                                                                        through='Tracks_artists')
    playlists: fields.ManyToManyRelation['Playlist'] = fields.ManyToManyField('models.Playlist',
                                                                            related_name='tracks',
                                                                            through='Tracks_playlists')

    album: fields.ForeignKeyNullableRelation['Album'] = fields.ForeignKeyField('models.Album',
                                                                        related_name='Album_id',
                                                                        null=True)
    genre: fields.ForeignKeyRelation['Genre'] = fields.ForeignKeyField('models.Genre',
                                                                        related_name='Album_id')
                                                                
    class PydanticMeta:
        allow_cycles = False

    class Meta:
        table = 'Track'
        

class Playlist(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            not_null=True)
    description = fields.TextField()
    release_date = fields.CharField(max_length=30)

    picture_file_path = fields.CharField(max_length=1000,
                                        not_null=True)

    libraries: fields.ManyToManyRelation['Library']
    tracks: fields.ManyToManyRelation['Track']
    genres: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre',
                                                                        related_name='playlists',
                                                                        through='Playlists_genres')

    creator: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField('models.User',
                                                                        related_name='playlist_creator_id')

    class PydanticMeta:
        allow_cycles = False

    class Meta:
        table = 'Playlist'


class Genre(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            unique=True, 
                            not_null=True)
    alt_name = fields.CharField(max_length=63,
                                unique=True)
    description = fields.TextField()

    libraries: fields.ManyToManyRelation['Library']
    artists: fields.ManyToManyRelation['Artist']
    albums: fields.ManyToManyRelation['Album']
    playlists: fields.ManyToManyRelation['Playlist']

    class PydanticMeta:
        allow_cycles = False

    class Meta:
        table = 'Genre'


class Artist(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            unique=True, 
                            not_null=True)
    registration_date = fields.CharField(max_length=30)

    picture_file_path = fields.CharField(max_length=1000,
                                        not_null=True)

    libraries: fields.ManyToManyRelation['Library']
    tracks: fields.ManyToManyRelation['Track']
    genres: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre',
                                                                        related_name='artists',
                                                                        through='Artists_genres')
    albums: fields.ManyToManyRelation['Album'] = fields.ManyToManyField('models.Album',
                                                                        related_name='artists',
                                                                        through='Artists_albums')

    class PydanticMeta:
        allow_cycles = False

    class Meta:
        table = 'Artist'


class Album(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=255, 
                            not_null=True)
    description = fields.TextField()
    release_date = fields.CharField(max_length=127)

    picture_file_path = fields.CharField(max_length=1000,
                                        not_null=True)

    libraries: fields.ManyToManyRelation['Library']
    artists: fields.ManyToManyRelation['Artist']
    genres: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre',
                                                                        related_name='albums',
                                                                        through='Albums_genres')

    class PydanticMeta:
        allow_cycles = False

    class Meta:
        table = 'Album' 


class Comment(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    text = fields.TextField()
    publishing_date = fields.CharField(max_length=30)
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField('models.User',
                                                                    related_name='comments')
    track: fields.ForeignKeyRelation['Track'] = fields.ForeignKeyField('models.Track',
                                                                        related_name='comments')

    class PydanticMeta:
        allow_cycles = False

    class Meta:
        table = 'Comment'


Comment_pydantic = pydantic_model_creator(Comment, name='Comment')
Comment_in_pydantic = pydantic_model_creator(Comment, name='Comment_in', exclude_readonly=True)
Comment_pydantic_list = pydantic_queryset_creator(Comment)
