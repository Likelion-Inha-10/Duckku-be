from distutils.command.upload import upload
from django.db import models
from user.models import User

class Artist(models.Model):
    artist_name = models.CharField(max_length=20, null=True)
    agency = models.CharField(max_length = 20, null = True)
    artist_image = models.URLField(blank = True, null = True)
    logo_image = models.URLField(blank = True, null = True)
    gradient_color_1 = models.TextField(blank = True, null = True)
    gradient_color_2 = models.TextField(blank = True, null = True)

    def __str__(self): 
        return self.artist_name

class Album(models.Model):
    name = models.CharField(max_length=20, null=True)
    agency = models.CharField(max_length=20, null=True)
    created_at = models.DateField(null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    album_image = models.URLField(blank = True, null = True)
    #music_list = models.TextField(null = True)
    #music_list = models.ManyToManyField(Music, related_name = 'sang_music_list', blank = True)
    price_with_ticket = models.IntegerField(null = True, default = 0)
    price_without_ticket = models.IntegerField(null = True, default = 0)
    purchased_count = models.IntegerField(null = True, default = 0)
    album_type = models.CharField(max_length=20, null=True)
    artist_name = models.CharField(max_length = 20, null = True)

    def __str__(self): 
        return self.name

class Music(models.Model):
    music_name = models.CharField(max_length = 20, null = True)
    play_time = models.CharField(max_length = 20, null = True)
    album = models.ForeignKey(Album, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.music_name



class AlbumFrime(models.Model):
    album_id =  models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    agency = models.CharField(max_length=20, null=True)
    created_at = models.DateField(null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    album_image = models.URLField(blank = True, null = True)
    #music_list = models.ManyToManyField(Music, related_name = 'my_music_list', blank = True)
    music_list = models.TextField(null = True)
    #price_with_ticket = models.IntegerField(null = True, default = 0)
    #price_without_ticket = models.IntegerField(null = True, default = 0)
    purchased_date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contains_ticket = models.BooleanField(null=True)
    #buyNumber = models.DateTimeField(auto_now_add = True, null = True)
    buyNumber = models.IntegerField(null = True, default = 0)
    album_type = models.CharField(max_length=20, null=True)
    artist_name = models.CharField(max_length = 20, null = True)

    def __str__(self): 
        return self.name


class Photocard(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)    #
    # img = models.ImageField(null=True)
    img = models.URLField(blank = True, null = True)    # 임시로 경로 설정, 카드 보여주기 용
    name = models.CharField(null = True, max_length = 20)
    QR_image = models.ImageField(blank = True, null = True, upload_to = 'QR_image')

class PhotocardFrime(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)    #
    img = models.URLField(blank = True, null = True)
    name = models.CharField(max_length =20, null = True)
    albumfrime_id = models.ForeignKey(AlbumFrime, on_delete=models.CASCADE) # 시리얼넘버의 개념
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    QR_image = models.ImageField(blank = True, null = True, upload_to = 'QR_image')
    QR_used = models.BooleanField(null = True, default = False)
    register_at = models.DateTimeField(auto_now_add = True, null = True)

class Count(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album_name = models.TextField(null=True)
    album_image = models.URLField(blank = True, null = True)
    count = models.IntegerField(default = 0, null=True)

# Create your models here.