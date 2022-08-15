from dataclasses import field
from rest_framework import serializers
from .models import *

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumFrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumFrime
        fields = '__all__'

class PhotocardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photocard
        fields = '__all__'

class PhotocardFrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotocardFrime
        fields = '__all__'


class ShowSubAlbumListSerializer(serializers.ModelSerializer):
    usersSubalbum_type_List = AlbumSerializer(many = True) # many
    class Meta:
        model = User
        fields = ('usersSubalbum_type_List',)    

'''
class Artist_type_id_serializer(serializers.ModelSerializer):
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

class ArtistTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class Artist_type_id_serializer(serializers.ModelSerializer):
    userSubartist_type_List = ArtistTypeSerializer(many = True)
    class Meta:
        model = User
        fields = ('userSubartist_type_List',)

class AlbumListSerializer(serializers.Serializer):
    userBuyalbum_type_List = AlbumSerializer(many = True) # many
    class Meta:
        model = User
        fields = ('userBuyalbum_type_List',)
    

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Count
        fields = '__all__'    #추후 앨범 이미지 ..


class BuyAlbum_type_id_serializer(serializers.ModelSerializer):
    #userBuyalbum_type_List = AlbumSerializer(many = True)
    class Meta:
        model = User
        fields = ('userBuyalbum_type_List',)