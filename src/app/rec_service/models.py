from tortoise import fields
from tortoise.models import Model
from ..library.models import Track

class Track_params(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    track_id: fields.ForeignKeyRelation['Track'] = fields.ForeignKeyField('models.Track', related_name='Track_id')
    valence = fields.FloatField(not_null=False)
    acousticness = fields.FloatField(not_null=False)
    danceability = fields.FloatField(not_null=False)
    energy = fields.FloatField(not_null=False)
    explicit = fields.BooleanField(not_null=False)
    instrumentalness = fields.FloatField(not_null=False)
    liveness = fields.FloatField(not_null=False)
    loudness = fields.FloatField(not_null=False)
    speechiness = fields.FloatField(not_null=False)
    tempo = fields.FloatField(not_null=False)

    class PydanticMeta:
        allow_cycles=False

    class Meta:
        table='Track_params'
