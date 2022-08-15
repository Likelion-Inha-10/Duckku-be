import re
from django.shortcuts import get_object_or_404, render, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import *
from artist.serializers import Artist_type_Serializer
#from .models import *
#from user.views import User
from .models import User
import random
from rest_framework.decorators import api_view
from rest_framework import generics
import json
from django.http import JsonResponse
from django.core import serializers

# ======== admin 작업 가능 ======

# class CreateAlbum(CreateAPIView):
#     model = Album()
#     serializer_class = AlbumSerializer

# class CreateAlbumFrime(CreateAPIView):
#     model = AlbumFrime()
#     serializer_class = AlbumFrimeSerializer

# class CreatePhotocard(CreateAPIView):
#     model = Photocard()
#     serializer_class = PhotocardSerializer

# class CreatePhotocard(CreateAPIView):
#     model = Photocard()
#     serializer_class = PhotocardSerializer

# ============================


# 상징성 앨범에 관한 정보 불러오기
class AlbumInfo(APIView):
    def get(self, request, sang_album_id):
        ab = get_object_or_404(Album, pk = sang_album_id)
        serialized_rooms = AlbumSerializer(ab)
        return Response(serialized_rooms.data)


# 구매한 앨범에 관한 정보 불러오기  (필요 없을지도?)
class AlbumFrimeInfo(APIView):
    def get(self, request, abf_id):
        abf = get_object_or_404(AlbumFrime, pk = abf_id)
        serialized_rooms = AlbumFrimeSerializer(abf)
        return Response({"frime album":serialized_rooms.data})


# 앨범 구매하기
class BuyAlbum(APIView):
    def post(self, request, sang_album_id):
        # json 입력 값들
        ticket = int(request.data['album_with_ticket'])
        no_ticket = int(request.data['album_without_ticket'])
        user = request.user
        sang_album = get_object_or_404(Album, pk = sang_album_id)

        #if sang_album not in user.userBuyalbum_type_List:
        #user.userBuyalbum_type_List.add(sang_album)
        #user.save()

        # 응모권 포함된 앨범 구매하는 과정
        for i in range(ticket):
            sang_album.purchased_count += 1 # 상징성 앨범에 대한 총 판매량 수 증가시키기
            sang_album.save()
            ab = get_object_or_404(Album, pk = sang_album_id)   # 상징성 앨범 불러오기
            newab = AlbumFrime()    # 구매한 앨범 생성하기

            # 구매한 앨범의 상징성 앨범에 관한 정보 넣기
            newab.album_id = ab    
            newab.name = ab.name
            newab.agency = ab.agency
            newab.created_at = ab.created_at
            newab.artist = ab.artist
            newab.album_image = ab.album_image
            
            #list_store = [1,2,3,4,5,'도깨비불', '블랙맘바', 'savage']

            # 수록곡(music_list) 카피하기
            list_store = list(ab.music_list)
            str_list_store = ''.join(list_store)
            new_list = str_list_store.split(',')
            newab.music_list = json.dumps(new_list, ensure_ascii = False) # 한글 깨짐현상 방지 => ensure_ascii

            newab.buyNumber = random.randrange(10000000, 99999999) # 주문번호는 8자리로 설정
            newab.user = user    # 추후 로그인 구현되면 바꿀 부분
            newab.contains_ticket = True
            newab.save()

            photocards = Photocard.objects.filter(album_id = sang_album_id) # 앨범에 소속된 상징성 포토카드를 불러오기
            photocard = random.choice(photocards)   # 포토카드 랜덤 선택하기
            pcf = PhotocardFrime()  # 구매한 포토카드 생성하기

            # 구매한 포토카드에 상징성 포토카드에 관한 정보 넣기
            pcf.album_id = photocard.album_id  
            pcf.img = photocard.img
            pcf.albumfrime_id = newab
            pcf.user = user
            pcf.name = photocard.name
            pcf.artist = ab.artist

            pcf.QR_image = photocard.QR_image
            pcf.QR_used = False
            pcf.save()

        # 응모권 포함되지 않은 앨범 구매하는 과정
        for i in range(no_ticket):
            sang_album.purchased_count += 1 # 상징성 앨범에 대한 총 판매량 수 증가시키기
            sang_album.save()
            ab = get_object_or_404(Album, pk = sang_album_id)
            newab = AlbumFrime()

            newab.album_id = ab
            newab.name = ab.name
            newab.agency = ab.agency
            newab.created_at = ab.created_at
            newab.artist = ab.artist
            newab.album_image = ab.album_image

            # 수록곡(music_list) 카피하기
            list_store = list(ab.music_list)
            str_list_store = ''.join(list_store)
            new_list = str_list_store.split(',')
            newab.music_list = json.dumps(new_list, ensure_ascii = False) # 한글 깨짐현상 방지 => ensure_ascii

            newab.buyNumber = random.randrange(10000000, 99999999)
            newab.user = user   
            newab.contains_ticket = False   # 이 부분만 다름
            newab.save()

            photocards = Photocard.objects.filter(album_id = sang_album_id) # 앨범에 소속된 상징성 포토카드를 불러오기
            photocard = random.choice(photocards)   # 포토카드 랜덤 선택하기
            pcf = PhotocardFrime()  # 구매한 포토카드 생성하기

            # 구매한 포토카드에 상징성 포토카드에 관한 정보 넣기
            photocards = Photocard.objects.filter(album_id = sang_album_id)
            photocard = random.choice(photocards)
            pcf = PhotocardFrime()

            pcf.album_id = photocard.album_id
            pcf.img = photocard.img
            pcf.name = photocard.name
            pcf.albumfrime_id = newab
            pcf.artist = ab.artist
            pcf.user = user
            pcf.QR_image = photocard.QR_image
            pcf.QR_used = False
            pcf.save()

        
        # 이미 구매한 앨범일 때
        buy_album_id_list = BuyAlbum_type_id_serializer(request.user)
        my_buy_album_id_list = buy_album_id_list.data['userBuyalbum_type_List']

        check = 0 

        # final_buy_album_id_list = []

        for album_id in my_buy_album_id_list:
            print("album_id:", album_id)
            if sang_album_id == album_id: # [1,2,3,4]   => sang_album_id : 2
                check = 1

        ab = get_object_or_404(Album, pk = sang_album_id)

        if check == 1: # [1,2,3,4]   => sang_album_id : 2
            # cnt = get_object_or_404(Count, user = user, album = ab)
            # cnt = Count()
            # cnt = Count.objects.filter(user = request.user).filter(album = sang_album_id)
            cnt = get_object_or_404(Count, user = user, album = ab)
            print(cnt)
            print(cnt.count)
            cnt.count += ticket
            cnt.count += no_ticket
            cnt.save()
        else:
            #print('카운트 만들게~')
            cnt = Count()
            cnt.user = user
            cnt.album = ab
            cnt.album_name = ab.name
            cnt.album_image = ab.album_image
            cnt.count += (ticket + no_ticket)
            cnt.artist = ab.artist
            cnt.save()
        
        user.userBuyalbum_type_List.add(sang_album)
        user.save()

        return Response({"message":"구매 성공 축하염"})


# 내가 찜한 상징성 엘범 리스트를 조회
class ShowSubAlbumList(APIView):
    def get(self, request):
        #subalbum_list = user.usersSubalbum_type_List
        subalbum_list = ShowSubAlbumListSerializer(request.user)
        output_json = subalbum_list.data['usersSubalbum_type_List']
        return Response(output_json)
        #return Response(subalbum_list.data)


# 상징성 앨범 찜하기 버튼 
class AddSubAlbum(APIView):
    def post(self, request, sang_album_id):
        user = request.user
        if user.usersSubalbum_type_List.filter(pk = sang_album_id).exists(): # 이미 찜한 상태라면 찜 목록에서 제거
            user.usersSubalbum_type_List.remove(sang_album_id)
            return Response({"message" : "찜 목록에서 제거성공!"})
        else:   # 찜한 상태가 아니라면 찜하기
            user.usersSubalbum_type_List.add(sang_album_id) 
            return Response({"message" : "찜하기 성공!"})


# 관심 아티스트들의 상징성 앨범 리스트 조회 (스토어에서 나의 관심 아티스트의 앨범 조회 기능)
class Show_my_artist_AlbumList(APIView):
    def get(self, request):
        my_artist = Artist_type_id_serializer(request.user)
        my_artist_data = my_artist.data['userSubartist_type_List']
        my_artist_id_list = []  # 관심 아티스트의 id 값을 추출하고 저장하는 리스트
        for artist in my_artist_data:
            my_artist_id_list.append(artist['id'])  # 관심 아티스트의 id 값을 저장

        # 여러 쿼리셋을 병합하기 위해, 맨 앞에 위치한 하나의 쿼리셋을 queryset_list 에 할당
        particular_artist = get_object_or_404(Artist, id = my_artist_id_list[0])
        queryset_list = Album.objects.filter(artist = particular_artist)

        for artist_id in my_artist_id_list:
            particular_artist = get_object_or_404(Artist, id = artist_id)
            album_list = Album.objects.filter(artist = particular_artist) # 각 관심 아티스트에 대한 앨범 QuerySet 리스트를 추출
            queryset_list = queryset_list.union(album_list) # 기존 퀴리셋에 for문을 돌때마다 각 퀴리셋을 합침
            #queryset_list.append(album_list)
        
        # 합쳐진 Queryset 를 기반으로 시리얼라이징 진행
        result_album_list = AlbumSerializer(queryset_list, many = True)
        return Response(result_album_list.data)


#/ 관심 아티스트들의 상징성 앨범 리스트를 인기순(판매량 순) 정렬 (스토어에서 내 관심 아티스트 앨범 더보기 누를때)
class Show_artist_list_album_list_sort_popular(APIView):
   def get(self, request):
        my_artist = Artist_type_id_serializer(request.user)
        my_artist_data = my_artist.data['userSubartist_type_List']
        my_artist_id_list = []  # 관심 아티스트의 id 값을 추출하고 저장하는 리스트
        for artist in my_artist_data:
            my_artist_id_list.append(artist['id'])  # 관심 아티스트의 id 값을 저장

        # 여러 쿼리셋을 병합하기 위해, 맨 앞에 위치한 하나의 쿼리셋을 queryset_list 에 할당
        particular_artist = get_object_or_404(Artist, id = my_artist_id_list[0])
        queryset_list = Album.objects.filter(artist = particular_artist)

        for artist_id in my_artist_id_list:
            particular_artist = get_object_or_404(Artist, id = artist_id)
            album_list = Album.objects.filter(artist = particular_artist) # 각 관심 아티스트에 대한 앨범 QuerySet 리스트를 추출
            queryset_list = queryset_list.union(album_list) # 기존 퀴리셋에 for문을 돌때마다 각 퀴리셋을 합침
            #queryset_list.append(album_list)
                
        # 합쳐진 Queryset 를 기반으로 시리얼라이징 진행
        result_album_list = AlbumSerializer(queryset_list.order_by('-purchased_count'), many = True) # 인기순(총 판매량 순) 오름차순 정렬
        return Response(result_album_list.data)


# 관심 아티스트들의 상징성 앨범 리스트를 최신순으로 정랼 (스토어에서 내 관심 아티스트 앨범 더보기 누를때)
class Show_artist_list_album_list_sort_created_at(APIView):
   def get(self, request):
        my_artist = Artist_type_id_serializer(request.user)
        my_artist_data = my_artist.data['userSubartist_type_List']
        my_artist_id_list = []  # 관심 아티스트의 id 값을 추출하고 저장하는 리스트
        for artist in my_artist_data:
            my_artist_id_list.append(artist['id'])  # 관심 아티스트의 id 값을 저장

        # 여러 쿼리셋을 병합하기 위해, 맨 앞에 위치한 하나의 쿼리셋을 queryset_list 에 할당
        particular_artist = get_object_or_404(Artist, id = my_artist_id_list[0])
        queryset_list = Album.objects.filter(artist = particular_artist)

        for artist_id in my_artist_id_list:
            particular_artist = get_object_or_404(Artist, id = artist_id)
            album_list = Album.objects.filter(artist = particular_artist) # 각 관심 아티스트에 대한 앨범 QuerySet 리스트를 추출
            queryset_list = queryset_list.union(album_list) # 기존 퀴리셋에 for문을 돌때마다 각 퀴리셋을 합침 
            #=> union 특징 : 중복되는 원소가 여러개 존재할때 하나만 저장함
            #queryset_list.append(album_list)
        
        # 합쳐진 Queryset 를 기반으로 시리얼라이징 진행
        result_album_list = AlbumSerializer(queryset_list.order_by('-created_at'), many = True) # 최신순 오름차순 정렬
        return Response(result_album_list.data)


# 특정 아티스트에 대해 내가 구매한 상징성 앨범 리스트 종류를 조회 (이떄 각 앨범마다의 개수 정보도 띄울것)
# class buy_album_list(APIView):
#     def get(self, request, artist_id):
#         album_list = AlbumListSerializer(request.user)
#         my_album_list = album_list.data['userBuyalbum_type_List']
#         my_album_list_id = []
#         for album in my_album_list: # 앨범 리스트의 각 앨범 id 값을 my_album_list_id 에 저장
#             my_album_list_id.append(album['id'])
    
#         result_album_id_list = []
       
#         for album_id in my_album_list_id:
#             album = get_object_or_404(Album, pk = album_id)
#             if album.artist.id == artist_id: # 특정 아티스트에 해당하는 상징성 앨범이라면
#                 result_album_id_list.append(album.id) # 앨범 id 값 리스트에 추가
#                 #queryset_list.append(album.artist)
        
#         queryset_list = Album.objects.filter(pk = result_album_id_list[0]) # 앨범에 대한 쿼리셋
        
#         # 결과물 쿼리셋 만들기
#         for album_id in result_album_id_list:
#             album = get_list_or_404(Album, pk = album_id)
#             add_queryset = Album.objects.filter(pk = album_id) 
#             queryset_list = queryset_list.union(add_queryset) # 쿼리셋에 병합
        
#         result_album_list = AlbumSerializer(queryset_list, many = True)
#         return Response(result_album_list.data)

class buy_album_list(APIView):
    def get(self, request, artist_id):
        artist = get_object_or_404(Artist, pk = artist_id)
        cnt = Count.objects.filter(user = request.user).filter(artist = artist)
        serializerd_rooms = CountSerializer(cnt, many=True)
        return Response(serializerd_rooms.data)

'''
# 특정 아티스트에 대해 내가 구매한 상징성 앨범 리스트 종류를 조회 (이떄 각 앨범마다의 개수 정보도 띄울것)
class buy_album_list(APIView):
    def get(self, request, artist_id):
        #particular_artist = get_object_or_404(Artist, pk = artist_id)
        album_list = AlbumListSerializer(request.user) # artist = particular_artist
        input_json = album_list.data["userBuyalbum_type_List"]
        input_json = json.dumps(input_json)
        input_dict = json.loads(input_json)
        output_dict = [x for x in input_dict if x['artist'] == artist_id]
        output_dict = str(output_dict)
        #output_dict = output_dict.replace('\\n', '\n')
        #output_json = json.dumps(output_dict, ensure_ascii = False, indent = 4)
        return Response(output_dict)
'''

# 특정 아티스트에 대해 내가 구매한 포토카드 리스트를 조회
class buy_photo_card_list(APIView):
    def get(self, request, artist_id):
        particular_artist = get_object_or_404(Artist, pk = artist_id)
        photocard_frime_list = PhotocardFrime.objects.filter(artist = particular_artist, user = request.user)
        new_photocard_frime_list = PhotocardFrimeSerializer(photocard_frime_list, many = True)
        return Response(new_photocard_frime_list.data)


# 특정 아티스트에 대해 내가 구매한 응모권의 개수를 리턴
class buy_ticket_count(APIView):
    def get(self, request, artist_id):
        particular_artist = get_object_or_404(Artist, pk = artist_id)
        count = AlbumFrime.objects.filter(artist = particular_artist).filter(user = request.user).filter(contains_ticket = True).count()
        return Response({"tickets_count" : count})


# 특정 아티스트에 대한 응모권을 모두 응모처리 ("모두 응모하기" 버튼 기능)
class ticket_use_complete(APIView):
    def post(self, request, artist_id):
        particular_artist = get_object_or_404(Artist, pk = artist_id)
        # 이벤트 앨범일 경우 User 모델의 Boolean 필드를 True 로 변경
        if(artist_id == 1): # 이벤트 앨범의 pk 값은 1로 일단 생각함
            request.user.ticket_apply_complete = True # 응모 완료처리
            request.user.save()
        
        count = AlbumFrime.objects.filter(artist = particular_artist).filter(user = request.user).filter(contains_ticket = True).count()

        # 특정 유저의 특정 아티스트에 대한 contains_ticket 필드를 False 로 변경 (어짜피 응모권 없는것이나 마찬가지이므로)
        ticket_list = AlbumFrime.objects.filter(artist = particular_artist).filter(user = request.user).filter(contains_ticket = True)
        for ticket in ticket_list:
            print(ticket.pk)
            ticket.contains_ticket = False
            ticket.save()

        return Response({"message" : "총 {0}개의 응모권이 등록되었습니다!".format(count)})


# 특정 포토카드에 대한 QR 이미지 조회 및 사용완료 처리 (앨범 상세 페이지)
class about_photocard_pr(APIView):
    # 포토카드 조회
    def get(self, request, photocard_id):
        photocard = get_object_or_404(PhotocardFrime, pk = photocard_id)
        photocard_serializer = PhotocardFrimeSerializer(photocard)
        return Response(photocard_serializer.data)
    
    # QR 사용처리
    def post(self, request, photocard_id):
        photocard = get_object_or_404(PhotocardFrime, pk = photocard_id)
        if photocard.QR_used == True: # 이미 교환완료한 포토카드라면
            return Response({"message" : "이미 교환처리한 포토카드입니다."}) 

        photocard.QR_used = True
        photocard.save()
        return Response({"message" : "포토카드 교환 완료"})



##############################################################################


# 상징성 앨범에 속한 상징성 포토카드 모두 불러오기
class GetPhotocardsInAlbum(APIView):
    def get(self, request, ab_id):
        pc = Photocard.objects.filter(album_id = ab_id)
        serialized_rooms = PhotocardSerializer(pc, many=True)
        return Response(serialized_rooms.data)

# 특정 앨범에 속한 포토카드 중, 특정 유저가 구매한 포토카드 불러오기
class GetPhotocardsFrime(APIView):
    def get(self, request, ab_id):
        user_id = request.data['user_id']   # 유저 정보 불러오기
        pc = PhotocardFrime.objects.filter(album_id = ab_id)    # 특정 앨범에 속한 구매된 포토카드 불러오기
        pc = pc.filter(user = user_id)  # 특정 유저가 구매한 포토카드 불러오기
        serialized_rooms = PhotocardFrimeSerializer(pc, many=True)
        return Response(serialized_rooms.data)