from tortoise import fields
from tortoise.models import Model
from ..library.models import Track

class Track_params(Model):
    id = fields.IntField(pk=True, 
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    track_id: fields.ForeignKeyRelation['Track'] = fields.ForeignKeyField('models.Track', related_name='Track_id')
    valence = fields.FloatField()
    acousticness = fields.FloatField()
    danceability = fields.FloatField()
    energy = fields.FloatField()
    explicit = fields.BooleanField()
    instrumentalness = fields.FloatField()
    liveness = fields.FloatField()
    loudness = fields.FloatField()
    speechiness = fields.FloatField()
    tempo = fields.FloatField()

    class PydanticMeta:
        allow_cycles=False

    class Meta:
        table='Track_params'
