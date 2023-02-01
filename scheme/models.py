from tortoise import fields
from tortoise.models import Model


class Track(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    actors_ids: fields.ManyToManyRelation["Artist"] = fields.ManyToManyField(
        'models.Artist', related_name='Track_artist_id', through='Track_artists_id'
    )
    duration = fields.TimeField()
    likes_ids: fields.ManyToManyRelation['User'] = fields.ManyToManyField(
        'models.User', related_name='User_playlists_ids', through='Track_likes_id'
    )
    comments_ids: fields.ManyToManyRelation['Track_comment'] = fields.ManyToManyField(
        'models.Track_comment', related_name='Track_comment_id', through='Track_comments_id'
    )
    preview_pic_id = fields.ForeignKeyField(
        'models.Picture', related_name='Track_picture_id'
    )
    genres_ids: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField(
        'models.Genre', related_name='Track_genre_id', through='Track_genres_id'
    )
    track_file_id = fields.ForeignKeyField(
        'models.Track_file', related_name='Track_file_id'
    )
    playlists: fields.ManyToManyRelation = fields.ManyToManyField(
        'models.Playlist', related_name='Playlist_track_id', through='Playlist_tracks'
    )
    user_tracks_ids: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        'models.Track', related_name='User_track_id', through='User_tracks_ids'
    )

    class Meta:
        table = 'Track'

    def __str__(self):
        return self.name


class Playlist(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    tracks_ids: fields.ManyToManyRelation[Track]
    release_date = fields.DateField(auto_now_add=True)
    creator_id: fields.ForeignKeyField(
        'models.User', related_name='Playlist_creator_id'
    )
    track_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Playlist', related_name='Playlist_id', through='User_playlists'
    )
    user_ids: fields.ManyToManyRelation['User'] = fields.ManyToManyField(
        'models.User', related_name='Playlist_users_ids', through='Playlist_users'
    )
    

    class Meta:
        table = 'Playlist'

    def __str__(self):
        return self.name


class Artist(Model):
    id = fields.IntField(pk=True, uniqie=True, auto_increment=True, not_null=True)
    name = fields.CharField(max_length=255, not_null=True)
    followers_ids: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        'models.User', related_name='Artist_user_id', through='Artist_followers'
    )
    avatar_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Artist_picture_id'
    )
    following_users_ids: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        'models.Artist', related_name='User_artist_id', through='User_following_artists'
    )
    registration_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table='Artist'

    def __str__(self):
        return self.name


class Album(Model):
    id = fields.IntField(pk=True, unique=True, auto_increment=True, not_null=True)
    name = fields.CharField(max_length=255, not_null=True)
    tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name='Album_track_id', through='Album_tracks'
    )
    artists_ids: fields.ManyToManyRelation["Artist"] = fields.ManyToManyField(
        'models.Artist', related_name='Album_artist_id', through='Album_artists'
    )
    user_ids: fields.ManyToManyRelation["Album"] = fields.ManyToManyField(
        'models.User', related_name='Album_user_ids', through='Album_users'
    )
    preview_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Album_picture_id'
    )
    release_date = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = 'Album'
    
    def __str__(self):
        return self.name


class Genre(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    alt_name = fields.CharField(max_length=255)
    favorite_genres_ids: fields.ManyToManyRelation["Genre"] = fields.ManyToManyField(
        'models.User', related_name='Genre_users_ids', through='User_genres'
    )

    class Meta:
        table = 'Genre'
    
    def __str__(self):
        return self.name


class User(Model):
    id = fields.IntField(pk=True, auto_increment=True, not_null=True, unique=True)
    name = fields.CharField(max_length=255, not_null=True)
    registration_date = fields.DatetimeField(auto_now_add=True)
    email = fields.CharField(max_length=255, not_null=True)
    password = fields.CharField(max_length=255, not_null=True)
    login = fields.CharField(max_length=255, not_null=True)
    user_track_ids: fields.ManyToManyRelation[Track]
    following_users_ids: fields.ManyToManyRelation[Artist]
    avatar_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='User_picture_id'
    )
    user_ids: fields.ManyToManyRelation[Playlist]
    favorite_genres_ids: fields.ManyToManyRelation[Genre]
    album_ids: fields.ManyToManyRelation[Album]

    class Meta:
        table = 'User'

    def __str__(self):
        return self.name


class Track_file(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    file_name = fields.CharField(max_length=255, unique=True)
    file_type = fields.CharField(max_length=15)


    class Meta:
        table = 'Track_file'

    def __str__(self):
        return self.name


class Track_comment(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    user_id = fields.ForeignKeyField(
        'models.User', related_name='Track_comment_user_id'
    )
    text = fields.TextField()

    class Meta:
        table = 'Track_comment'

    def __str__(self):
        return self.name


class Picture(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    file_name = fields.CharField(max_length=255, unique=True)
    file_type = fields.CharField(max_length=15)

    class Meta:
        table = 'Picture'

    def __str__(self):
        return self.name