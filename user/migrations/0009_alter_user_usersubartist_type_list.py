# Generated by Django 4.0.5 on 2022-08-18 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0007_remove_album_music_list_remove_albumfrime_music_list_and_more'),
        ('user', '0008_alter_user_usersubartist_type_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userSubartist_type_List',
            field=models.ManyToManyField(default=True, related_name='sub_user', to='album.artist'),
        ),
    ]
