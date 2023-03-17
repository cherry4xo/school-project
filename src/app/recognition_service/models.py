from tortoise import fields
from tortoise.models import Model
from ..library.models import Track

class Track_spectorgram(Model):
    peaks_file_path = fields.CharField(max_length=1000, not_null=False, default='')
    track_id: fields.ForeignKeyRelation['Track'] = fields.ForeignKeyField('models.Track', 
                                                                        related_name='track_peaks')

    class PydanticMeta:
        allow_cycles=False

    class Meta:
        table='Track_spectrogram'