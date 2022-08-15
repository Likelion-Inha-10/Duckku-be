from dataclasses import field
from rest_framework import serializers
from user.models import User
from album.models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class Artist_type_Serializer(serializers.ModelSerializer):
    userSubartist_type_List = ArtistSerializer(many = True) # many
    class Meta:
        model = User
        fields = ('userSubartist_type_List',)

'''
class Artist_type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            #'id' : {'write_only' : True},
            'userName' : {'write_only' : True},
            'userEmail' : {'write_only' : True},
            'userBuyalbum_type_List' : {'write_only' : True},
            'usersSubalbum_type_List' : {'write_only' : True},
            'is_active' : {'write_only' : True},
            'is_admin' : {'write_only' : True},

            'last_login' : {'write_only' : True},
            'password' : {'write_only' : True},
            'groups' : {'write_only' : True}, 
            'is_staff' : {'write_only' : True},
            'is_superuser' : {'write_only' : True},
            'user_permissions' : {'write_only' : True},  
        }
'''