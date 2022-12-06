"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from texas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_action, name='login'),
    path('main', views.access_main, name='main'),
    path('game', views.game, name='game'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('profile', views.my_profile, name='profile'),
    path('my_profile', views.my_profile, name = 'my_profile'),
    path('my_profile_name', views.my_profile_name, name = 'my_profile_name'),
    path('profile_name', views.my_profile_name, name = 'profile_name'),
    path('my_profile_token', views.my_profile_token, name = 'my_profile_token'),
    path('profile_token', views.my_profile_token, name = 'profile_token'),
    path('get_photo/<int:id>', views.get_photo, name = 'get_photo'),
    path('texas/leaders', views.get_leaderboard_users, name='leaders'),
    path('texas/join', views.join_room, name='join_room'),
    path('texas/createRoom', views.create_room, name='create_room'),
    path('texas/exitRoom', views.exit_room, name='exit_room'),
    path('texas/roomGameInfo', views.get_room_game_info, name='get_room_game_info'),
    path('texas/availableRooms', views.get_available_rooms_info, name='get_available_rooms_info'),
    path('game/ready', views.userReady, name='userReady'),
    path('game/unready', views.userCancelReady, name='userCancelReady'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
