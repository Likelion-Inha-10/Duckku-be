"""Duckku_be URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views
from album import views as album_views
from artist import views as artist_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Signup', csrf_exempt(views.Signup.as_view())),
    path('Login', views.Login.as_view()),
    path('Logout', views.Logout),
    path('userinfo/<int:user_id>', csrf_exempt(views.userinfo.as_view())),  #승찬
    path('sub_artist/<int:user_id>', csrf_exempt(views.SubArtist.as_view())),   #승찬
    path('my_artist_list/<int:user_id>', artist_views.my_artist_list.as_view()),    #승찬
    path('my_artist_list/delete/<int:artist_id>/<int:user_id>', artist_views.delete_my),    #승찬
    path('show_album_info/<int:sang_album_id>', album_views.AlbumInfo.as_view()),
    path('buy_albums/<int:sang_album_id>/<int:user_id>', album_views.BuyAlbum.as_view()),
    path('show_subalbum_list/<int:user_id>', album_views.ShowSubAlbumList.as_view()),
    path('add_subalbum/<int:sang_album_id>/<int:user_id>', album_views.AddSubAlbum.as_view()),
    path('my_artist_list/show_album_list/<int:user_id>', album_views.Show_my_artist_AlbumList.as_view()),
    path('my_artist_list/show_album_list/sort_popular/<int:user_id>', album_views.Show_artist_list_album_list_sort_popular.as_view()),
    path('my_artist_list/show_album_list/sort_created_at/<int:user_id>', album_views.Show_artist_list_album_list_sort_created_at.as_view()),
    #path('ShowSubAlbumList', album_views.Show_my_artist_AlbumList),
    path("<int:artist_id>/buy_album_list/<int:user_id>", album_views.buy_album_list.as_view()),
    path("<int:artist_id>/buy_photo_card_list/<int:user_id>", album_views.buy_photo_card_list.as_view()),
    path('<int:artist_id>/buy_ticket_count/<int:user_id>', album_views.buy_ticket_count.as_view()),
    path('<int:artist_id>/ticket_use_complete/<int:user_id>', album_views.ticket_use_complete.as_view()),
    path('qr/<int:photocard_id>', album_views.about_photocard_pr.as_view()),
    path('album_music_list_info/<int:sang_album_id>', album_views.Album_music_list_info.as_view()),
    path('show_all_artist_info', album_views.show_all_artist_info.as_view()),
    path('get_all_albums', album_views.GetAllAlbums.as_view()),
    path('get_all_purchased_albums/<int:user_id>', album_views.GetAllPurchasedAlbums.as_view()),
    #path('send_email', album_views.send_email.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)