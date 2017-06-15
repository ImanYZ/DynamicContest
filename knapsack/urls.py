from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.conf import settings

from . import views

app_name = 'knapsack'

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'knapsack/media/blockm.png')),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^training/$', views.training, name='training'),
    url(r'^training/introduction/$', views.trainingintro, name='trainingintro'),
    url(r'^training/submit/$', views.trainingsubmit, name='trainingsubmit'),
    url(r'^contest/introduction/$', views.contestintro, name='contestintro'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^quizsubmit/$', views.quizsubmit, name='quizsubmit'),
    url(r'^quizresults/$', views.quizresults, name='quizresults'),
    url(r'^waitingroom/$', views.waitingroom, name='waitingroom'),
    url(r'^game/$', views.game, name='game'),
    url(r'^game/status/$', views.gamestatus, name='gamestatus'),
    url(r'^game/submit/$', views.gamesubmit, name='gamesubmit'),
    url(r'^quit/$', views.quit, name='quit'),
    url(r'^quitquestion/$', views.quitquestion, name='quitquestion'),
    url(r'^results/$', views.results, name='results'),
    url(r'^survey/$', views.survey, name='survey'),
    url(r'^surveysubmit/$', views.surveysubmit, name='surveysubmit'),
    url(r'^final/$', views.final, name='final'),
    url(r'^deletegamesofexperiment/$', views.deletegamesofexperiment, name='deletegamesofexperiment'),
    url(r'^(?i)downloadCSV/(?P<part>.+)', views.downloadCSV, name='downloadCSV'),
]