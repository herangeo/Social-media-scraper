from django.contrib import admin
from django.urls import path, include

from twitter_app.views import delete_history, delete_tweet, fun, history_fun, login_page, logout_page, register, saved, update_saved,display_sentiments

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name="login_page"),
    path('reddit/', include("reddit_app.urls")),
    path('monitor/', include('linkedin.urls')), 
    path('youtube/', include("youtubee.urls")),
    path('daily/', include("dailymotionn.urls")),
    path('news/', include("newsarticless.urls")),
    path('register/', register, name="register_page"),
    path('saved/', saved, name="saved_page"),
    path('update_saved/', update_saved, name="update_saved_page"),
    path('history_fun/', history_fun, name="history_page"),
    path('delete/<int:id>/', delete_tweet, name="delete"),
    path('delete_history/<int:id>/', delete_history, name="delete_history"),
    path('logout/', logout_page, name="logout"),
    path('login/', login_page, name="login_page"),
    path('fun/', fun, name="fun"),
    path('twitter_sentiment/', display_sentiments, name="display_sentiments"),

]
