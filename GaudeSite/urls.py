from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home-view"),
    path('imgen/', views.imgGenerator, name="imgGenerator-view"),
    path('projeval/', views.projEval, name="projEval-view"),
    path('sketchimg/', views.sketchImg, name="sketchImg-view"),
    path('removebackground/', views.removeBackground, name="removeBackground-view"),
    path('masterplan/', views.masterPlan, name="masterPlan-view"),
    path('searchreplace/', views.searchReplace, name="searchReplace-view"),
    path('replacestructure/', views.replaceStructure, name="replaceStructure-view"),
    path('interior/', views.interiorImage, name="interiorImage-view"),
    path('exterior/', views.exteriorImage, name="exteriorImage-view"),
    path('outpaint/', views.outPaint, name="outPaint-view"),
    path('interiorredecoration/', views.interiorRedecoration, name="interiorRedecoration-view"),
    path('landscape/', views.landScape, name="landScape-view"),
    path('upscale/', views.upScale, name="upScale-view"),

    path('login/', views.login, name="login-view"),
    path('register/', views.register, name="register-view"),

    path('admin/', admin.site.urls ),
    path('accounts/', include('django.contrib.auth.urls'))


]