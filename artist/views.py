from http.client import HTTPResponse
from django.shortcuts import render
from album.models import Artist
from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ArtistSerializer, Artist_type_Serializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
# Create your views here.

# 관심 아티스트 리스트 조회
class my_artist_list(APIView):
    @csrf_exempt
    def get(self, request):
        user = get_object_or_404(User, pk = request.user.pk)
        artist_list = Artist_type_Serializer(user)
        output = artist_list.data['userSubartist_type_List']
        return Response(output)


# 관심 아티스트 리스트에서 원하는 아티스트를 제거
@method_decorator(csrf_exempt, name = 'dispatch')
@api_view(['DELETE'])
def delete_my(request, artist_id):
    user = get_object_or_404(User, pk = request.user.pk)
    artist = Artist.objects.get(id = artist_id)
    user.userSubartist_type_List.remove(artist)
    return Response({"message" : "원하는 아티스트 제거에 성공했습니다."})

'''
class delete_my_artist(APIView):
    #@csrf_exempt
    def delete(self, request, artist_id):
        user = get_object_or_404(User, pk = request.user.pk)
        artist = Artist.objects.get(id = artist_id)
        user.userSubartist_type_List.remove(artist)
'''
