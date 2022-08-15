from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
#from album.models import Album, Artist
from django.apps import apps

#유저모델
#회원가입[이름, 이메일, 비밀번호, 비밀번호 확인](아이디 따로 없음 ,이메일을 아이디로 사용)
#로그인[이메일, 비밀번호]

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, userName, userEmail, password):
    
        user = self.model(
            userName = userName,
            userEmail = userEmail,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, userEmail, password):
        superuser = self.create_user(userName = userName, userEmail = userEmail, password = password)
        #superuser.set_password(password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        
        return superuser

# myModel = apps.get_model()

class User(AbstractBaseUser, PermissionsMixin):
    userName = models.CharField(max_length=50)
    userEmail = models.EmailField(max_length=100,unique=True)
    userSubartist_type_List = models.ManyToManyField(to = 'album.Artist', related_name = 'sub_user', default = True)  #  'app_name.Model_name' # circular import error 
    userBuyalbum_type_List = models.ManyToManyField(to = 'album.Album', related_name = 'buy_user', default = True)   # => 모든 ManyToMany 필드 related_name  다르게 해야 error 발생 x
    usersSubalbum_type_List = models.ManyToManyField(to = 'album.Album', related_name = 'sub_user2', default = True) 
    ticket_apply_complete = models.BooleanField(null = True, default = False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'userEmail'
    REQUIRED_FIELDS = ['userName']

    class Meta:
        db_table = 'user'



