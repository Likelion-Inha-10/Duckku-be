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
    path('Signup/', csrf_exempt(views.Signup.as_view())),
    path('Login/', csrf_exempt(views.Login.as_view())),
    path('Logout/', views.Logout),
    path('my_artist_list', artist_views.my_artist_list.as_view()),
    path('my_artist_list/delete/<int:artist_id>', artist_views.delete_my),
    path('show_album_info/<int:sang_album_id>', album_views.AlbumInfo.as_view()),
    path('buy_albums/<int:sang_album_id>', album_views.BuyAlbum.as_view()),
    path('show_subalbum_list', album_views.ShowSubAlbumList.as_view()),
    path('add_subalbum/<int:sang_album_id>', album_views.AddSubAlbum.as_view()),
    path('my_artist_list/show_album_list', album_views.Show_my_artist_AlbumList.as_view()),
    path('my_artist_list/show_album_list/sort_popular', album_views.Show_artist_list_album_list_sort_popular.as_view()),
    path('my_artist_list/show_album_list/sort_created_at', album_views.Show_artist_list_album_list_sort_created_at.as_view()),
    #path('ShowSubAlbumList', album_views.Show_my_artist_AlbumList),
    path("<int:artist_id>/buy_album_list", album_views.buy_album_list.as_view()),
    path("<int:artist_id>/buy_photo_card_list", album_views.buy_photo_card_list.as_view()),
    path('<int:artist_id>/buy_ticket_count', album_views.buy_ticket_count.as_view()),
    path('<int:artist_id>/ticket_use_complete', album_views.ticket_use_complete.as_view()),
    path('qr/<int:photocard_id>', album_views.about_photocard_pr.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)