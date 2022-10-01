from django.urls import path, include

from . import views

urlpatterns = [
   path('', views.home, name = 'home'),
   path('register/', views.register_request, name = 'register'),
   path('<username>', views.profile, name = 'profile'),
   path('inbox/', views.inbox, name = 'inbox'),
   path('direct/<username>/', views.Directs, name = 'direct'),
   path('new/', views.UserSearch, name = 'search'),
   path('new/<username>/', views.NewConversation, name='newconversation'),
   path('send/', views.SendDirect, name='send_direct'),
   path('profile/edit/', views.EditProfile, name='edit-profile'),
   path('ajax-posting/', views.ajax_posting, name='ajax_posting'),
  
   
]