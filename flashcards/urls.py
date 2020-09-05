from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('cards/<str:category>', views.get_cards_by_category, name='get_cards_by_category'),
    path('add_card', views.add_card, name='add_card'),
    path('edit_card/<id>', views.edit_card, name='edit_card'),
    path('search_keywords', views.search_keywords, name='search_keywords'),
    path('learn', views.learn, name='learn'),
    path('mark_known/<id>', views.mark_known, name='mark_known'),
    path('mark_liked/<id>', views.mark_liked, name='mark_liked'),
    path('dump_csv', views.dump_csv, name='dump_csv'),
]