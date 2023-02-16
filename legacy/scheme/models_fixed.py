from tortoise import fields
from tortoise.models import Model

class Track(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            not_null=True)
    duration = fields.TimeField(not_null=True)
    track_file_path = fields.CharField(max_length=255,
                                    not_null=True)
    track_file_type = fields.CharField(max_length=15, 
                                    not_null=True)
    artists_ids: fields.ManyToManyRelation['Artist'] = fields.ManyToManyField('models.Artist', 
                                                                            related_name='track_ids', 
                                                                            through='Tracks_artists')
    users_likes_ids: fields.ManyToManyRelation['User'] = fields.ManyToManyField('models.User',
                                                                            related_name='liked_tracks',
                                                                            through='Tracks_users')
    comments_ids: fields.ManyToManyRelation['Comment'] = fields.ManyToManyField('models.Comment',
                                                                            related_name='track_id',
                                                                            through='Tracks_comments')
    album_ids: fields.ManyToManyRelation['Album'] = fields.ManyToManyField('models.Album',
                                                                            related_name='tracks_ids',
                                                                            through='Track_album')
    playlists_ids: fields.ManyToManyRelation['Playlist']
    picture_id = fields.ForeignKeyField('models.File', related_name='Track_id')
    genre_id = fields.ForeignKeyField('models.Genre', related_name='Genre_id') 
    
    class Meta: table = 'Track'
    def __str__(self): return self.name


class Album(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            not_null=True)
    release_date = fields.DatetimeField(auto_now_add=True)
    tracks_ids: fields.ManyToManyRelation['Track']
    users_ids: fields.ManyToManyRelation['User']
    artists_ids: fields.ManyToManyRelation['Artist'] = fields.ManyToManyField('models.Artist', 
                                                                            related_name='albums_ids',
                                                                            through='Album_artists')
    genres_ids: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre', 
                                                                            related_name='genres_ids',
                                                                            through='Albums_genres')
    picture_id = fields.ForeignKeyField('models.File', 
                                        related_name='Album_id')
    
    class Meta: table = 'Album'
    def __str__(self): return self.name

class Artist(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            unique=True, 
                            not_null=True)
    registration_date = fields.DatetimeField(auto_now_add=True)
    picture_id = fields.ForeignKeyField('models.File', related_name='Artist_id')
    users_ids: fields.ManyToManyRelation['User'] = fields.ManyToManyField('models.User',
                                                                        related_name='following_artists', 
                                                                        through='Artist_users')
    genres_ids: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre',
                                                                            related_name='artists_ids',
                                                                            through='Artists_genres')
    albums_ids: fields.ManyToManyRelation['Album']    
    track_ids: fields.ManyToManyRelation['Track']

    class Meta: table = 'Artist'
    def __str__(self): return self.name


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
    genre_users: fields.ManyToManyRelation['User']
    playlists_ids: fields.ManyToManyRelation['Playlist']
    artists_ids: fields.ManyToManyRelation['Artist']
    album_ids: fields.ManyToManyRelation['Album']

    class Meta: table = 'Genre'
    def __str__(self): return self.name


class User(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True,
                        auto_increment=True) 
    registration_date = fields.DatetimeField(auto_now_add=True)
    email = fields.CharField(max_length=127,
                            unique=True,
                            not_null=True)
    password = fields.CharField(max_length=127,
                                not_null=True)
    login = fields.CharField(max_length=63,
                            unique=True,
                            not_null=True)
    liked_tracks: fields.ManyToManyRelation['Track']
    comments: fields.ManyToManyRelation['Comment'] = fields.ManyToManyField('models.Comment',
                                                                        related_name='user_id',
                                                                        through='Users_comments')
    following_artists: fields.ManyToManyRelation['Artist']
    liked_playlists: fields.ManyToManyRelation['Playlist'] = fields.ManyToManyField('models.Playlist',
                                                                                    related_name='users_ids',
                                                                                    through='Users_playlists')
    liked_albums: fields.ManyToManyRelation['Album'] = fields.ManyToManyField('models.Album',
                                                                            related_name='users_ids',
                                                                            through='User_albums')
    liked_genres: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField('models.Genre',
                                                                                related_name='genre_users',
                                                                                through='Users_genres')
    picture_id = fields.ForeignKeyField('models.File', related_name='User_id')
    
    class Meta: table = 'User'
    def __str__(self): return self.name


class Playlist(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True,
                        auto_increment=True)
    name = fields.CharField(max_length=63,
                            not_null=True)
    description = fields.TextField()
    release_date = fields.DatetimeField(auto_now_add=True)
    tracks_ids: fields.ManyToManyRelation[Track] = fields.ManyToManyField('models.Track',
                                                                            related_name='placlists_ids',
                                                                            through='Playlists_tracks')
    creator_id: fields.OneToOneRelation[User] = fields.OneToOneField('models.User', 
                                                                    related_name='User_id')
    users_ids: fields.ManyToManyRelation[User]
    genres_ids: fields.ManyToManyRelation[Genre] = fields.ManyToManyField('models.Genre',
                                                                        related_name='playlists_ids',
                                                                        through='Playlist_genres')
    
    picture_id = fields.ForeignKeyField('models.File', related_name='Playlist_id')

    class Meta: table = 'Playlist'
    def __str__(self): return self.name


class Comment(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True,
                        auto_increment=True)
    text = fields.TextField()
    publishing_date: fields.DatetimeField(auto_now_add=True)
    user_id: fields.ManyToManyRelation[User]
    track_id: fields.ManyToManyRelation[Track]

    class Meta: table = 'Comment'
    def __str__(self): return self.name


class File(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True,
                        auto_increment=True)
    file_name = fields.CharField(max_length=63, unique=True)
    file_type = fields.CharField(max_length=15)
    data_type = fields.CharField(max_length=63)

    class Meta: table = 'File'
    def __str__(self): return self.name