# Generated by Django 4.1 on 2022-08-15 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0006_photocard_qr_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='music_list',
        ),
        migrations.RemoveField(
            model_name='albumfrime',
            name='music_list',
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.TextField(null=True)),
                ('album_image', models.ImageField(blank=True, null=True, upload_to='sang_album_img')),
                ('count', models.IntegerField(default=0, null=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='album.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='album.artist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='music_list',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='albumfrime',
            name='music_list',
            field=models.TextField(null=True),
        ),
    ]
