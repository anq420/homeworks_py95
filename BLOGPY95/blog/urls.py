from django.urls import path
from blog.views import main_view, add_article_view, full_article_view, edit_article_view, author_view
from users.views import sign_up_view, sign_in_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", main_view, name="main"),
    path('article_page/<int:id>/', full_article_view, name='article_page'),
    path('add_article/', add_article_view, name='add_article'),
    path('article_page/<int:id>/edit_article/', edit_article_view, name='edit_article'),
    path('author/<int:id>/articles/', author_view, name='authors_articles'),
    path('sign-up/', sign_up_view, name='signup'),
    path('sign-in/', sign_in_view, name='signin'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
