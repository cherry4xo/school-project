from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class User(Model):
    id = fields.IntField(pk=True,
                        unique=True, 
                        not_null=True, 
                        auto_increment=True)
    name = fields.CharField(max_length=63)
    login = fields.CharField(max_length=127,
                            unique=True)
    email = fields.CharField(max_length=255, 
                            unique=True)
    hashed_password = fields.CharField(max_length=1000)
    registration_date = fields.CharField(max_length=30)

    picture_file_path = fields.CharField(max_length=1000)

    class PydanticMeta:
        exclude = ['hashed_password']

    class Meta:
        table = 'User'


User_pydantic = pydantic_model_creator(User, name='User')
User_in_pydantic = pydantic_model_creator(User, name='User_in', exclude_readonly=True)
User_pydantic_list = pydantic_queryset_creator(User)