from django.contrib import admin
from django.urls import path, include
from tracker import views
# --- AJOUTE CES DEUX IMPORTS ---
from django.conf import settings
from django.conf.urls.static import static
# ------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'), 
    
    path('accounts/', include('django.contrib.auth.urls')), 
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-meal/', views.add_meal, name='add_meal'),
    path('add-weight/', views.add_weight, name='add_weight'),
    path('update-goals/', views.update_goals, name='update_goals'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)