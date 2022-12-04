from tortoise import fields
from tortoise.models import Model

class Track(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    actors_ids: fields.ManyToManyRelation["Executor"] = fields.ManyToManyField(
        'models.Executor', related_name='Track_executor_id', through='Track_executors_id'
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

    class Meta:
        table = 'Track'

    def __str__(self):
        return self.name


class Executor(Model):
    id = fields.IntField(pk=True, uniqie=True, auto_increment=True, not_null=True)
    name = fields.CharField(max_length=255, not_null=True)
    followers_ids: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        'models.User', related_name='Executor_user_id', through='Executor_followers'
    )
    avatar_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Executor_picture_id'
    )
    registration_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table='Executor'

    def __str__(self):
        return self.name


class Album(Model):
    id = fields.IntField(pk=True, unique=True, auto_increment=True, not_null=True)
    name = fields.CharField(max_length=255, not_null=True)
    tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name='Album_track_id', through='Album_tracks'
    )
    executors_ids: fields.ManyToManyRelation["Executor"] = fields.ManyToManyField(
        'models.Executor', related_name='Album_executor_id', through='Album_executors'
    )
    preview_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Album_picture_id'
    )
    release_date = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = 'Album'
    
    def __str__(self):
        return self.name


class User(Model):
    id = fields.IntField(pk=True, auto_increment=True, not_null=True, unique=True)
    name = fields.CharField(max_length=255, not_null=True)
    registration_date = fields.DatetimeField(auto_now_add=True)
    email = fields.CharField(max_length=255, not_null=True)
    password = fields.CharField(max_length=255, not_null=True)
    login = fields.CharField(max_length=255, not_null=True)
    liked_tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name='User_track_id', through='User_liked_tracks'
    )
    following_executors_ids: fields.ManyToManyRelation["Executor"] = fields.ManyToManyField(
        'models.Executor', related_name='User_executor_id', through='User_following_executors'
    )
    avatar_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='User_picture_id'
    )
    playlists_ids: fields.ManyToManyRelation["Playlist"] = fields.ManyToManyField(
        'models.Playlist', related_name='Playlist_id', through='User_playlists'
    )
    favorite_genres_ids: fields.ManyToManyRelation["Genre"] = fields.ManyToManyField(
        'models.Genre', related_name='User_genre_id', through='User_genres'
    )
    albums_ids: fields.ManyToManyRelation["Album"] = fields.ManyToManyField(
        'models.Album', related_name='User_album_id', through='User_albums'
    )

    class Meta:
        table = 'User'

    def __str__(self):
        return self.name


class Playlist(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name='Playlist_track_id', through='Playlist_tracks'
    )
    release_date = fields.DateField(auto_now_add=True)
    creator_id: fields.ForeignKeyField(
        'models.User', related_name='Playlist_user_id'
    )

    class Meta:
        table = 'Playlist'

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


class Genre(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    alt_name = fields.CharField(max_length=255)

    class Meta:
        table = 'Genre'
    
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