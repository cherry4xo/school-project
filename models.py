from tortoise import fields
from tortoise.models import Model

class Track(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    actors_ids: fields.ManyToManyRelation["Executor"] = fields.ManyToManyField(
        'models.Executor', related_name='Executor_id', through='track_executors'
    )
    album_id = fields.ForeignKeyField(
        'models.Album', related_name='Album_id'
    )
    duration = fields.TimeField()
    likes_ids: fields.ManyToManyRelation['User'] = fields.ManyToManyField(
        'models.User', related_name='User_playlists_ids', through='track_likes'
    )
    comments_ids: fields.ManyToManyRelation['Track_comment'] = fields.ManyToManyField(
        'models.Track_comment', related_name='Track_comment_id', through='track_comments'
    )
    preview_pic_id = fields.ForeignKeyField(
        'models.Picture', related_name='Picture_id'
    )
    genres_ids: fields.ManyToManyRelation['Genre'] = fields.ManyToManyField(
        'models.Genre', related_name='Genre_id', through='track_genres'
    )
    track_file_id = fields.ForeignKeyField(
        'models.Track_file', related_name='Track_file_id'
    )
    release_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'Track'

    def __str__(self):
        return self.name


class Executor(Model):
    id = fields.IntField(pk=True, uniqie=True, auto_increment=True, not_null=True)
    name = fields.CharField(max_length=255, not_null=True)
    albums_ids: fields.ManyToManyRelation["Album"] = fields.ManyToManyField(
        'models.Album', related_name="Album_id", through='Executor_albums'
    )
    tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name="Track_id", through='Executor_tracks'
    )
    followers_ids: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        'models.User', related_name='User_id', through='Executor_followers'
    )
    avatar_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Picture_id'
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
        'models.Track', related_name='Track_id', through='Album_tracks'
    )
    likes_ids: fields.fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        'models.User', related_name='User_id', through='Album_likes'
    )
    executors_ids: fields.ManyToManyRelation["Executor"] = fields.ManyToManyField(
        'models.Executor', related_name='Executor_id', through='Album_executors'
    )
    preview_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Picture_id'
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
    liked_tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name='Track_id', through='User_liked_tracks'
    )
    following_executors_ids: fields.ManyToManyRelation["Executor"] = fields.ManyToManyField(
        'models.Executor', related_name='Executor_id', through='User_following_executors'
    )
    avatar_file_id = fields.ForeignKeyField(
        'models.Picture', related_name='Picture_id'
    )
    playlists_ids: fields.ManyToManyRelation["Playlist"] = fields.ManyToManyField(
        'models.Playlist', related_name='Playlist_id', through='User_playlists'
    )
    favorite_genres_ids: fields.ManyToManyRelation["Genre"] = fields.ManyToManyField(
        'models.Genre', related_name='Genre_id', through='User_genres'
    )
    albums_ids: fields.ManyToManyRelation["Album"] = fields.ManyToManyField(
        'models.Album', related_name='Album_id', through='User_albums'
    )

    class Meta:
        table = 'User'

    def __str__(self):
        return self.name


class Playlist(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)
    tracks_ids: fields.ManyToManyRelation["Track"] = fields.ManyToManyField(
        'models.Track', related_name='Track_id', through='Playlist_tracks'
    )
    release_date = fields.DateField(auto_now_add=True)
    users_likes_ids: fields.ManytoManyRelation["User"] = fields.ManyToManyField(
        'models.User', related_name='User_id', through='Playlist_user_likes'
    )

    class Meta:
        table = 'Playlist'

    def __str__(self):
        return self.name


class Track_file(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    file_name = fields.charField(max_length=255, unique=True)
    file_type = fields.charField(max_length=15)


    class Meta:
        table = 'Track_file'

    def __str__(self):
        return self.name


class Track_comment(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    user_id = fields.ForeignKeyField(
        'models.User', related_name='User_id'
    )
    text = fields.TextField()

    class Meta:
        table = 'Track_comment'

    def __str__(self):
        return self.name


class Genre(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    name = fields.CharField(max_length=255, not_null=True)

    class Meta:
        table = 'Genre'
    
    def __str__(self):
        return self.name


class Picture(Model):
    id = fields.IntField(pk=True, unique=True, not_null=True, auto_increment=True)
    file_name = fields.charField(max_length=255, unique=True)
    file_type = fields.charField(max_length=15)

    class Meta:
        table = 'Picture'

    def __str__(self):
        return self.name