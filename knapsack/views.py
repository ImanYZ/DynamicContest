import json
from random import randint
import itertools
import random
from datetime import timedelta
import time
import math
import csv

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404, StreamingHttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Experiment
from .models import Gametype
from .models import User
from .models import Game
from .models import Usertraining
from .models import Usertrainingitem
from .models import Usergame
from .models import Usergameitem
from .models import Contest
from .models import Contestusertraining
from .models import Contestusergame
from .models import Userquitquestion


@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        if 'username' in request.POST and request.POST['username'] != '':
            username = request.POST['username']

            if request.method == 'POST' and 'experiment' in request.POST:
                current_experiment = request.POST['experiment']
                experiment = Experiment.objects.get(vesion=current_experiment)
            else:
                experiment = Experiment.objects.last()
            user = User.objects.filter(username=username)
            if len(user) != 0:
                user = user.filter(experiment=experiment)
                # print ("User found.")
                if len(user) == 0:
                    context = {'username': username, 'participatedBefore': 1}
                    return render(request, 'knapsack/index.html', context)
            else:
                usersInExperiment = User.objects.filter(experiment=experiment)
                usersInExperimentNum = usersInExperiment.count()
                if usersInExperimentNum >= experiment.total_participants_number:
                    context = {'username': username, 'excessSubjects': 1}
                    return render(request, 'knapsack/index.html', context)

            request.session['username'] = username

    return index(request)


def logout(request):
    try:
        del request.session['username']

    except:
        if 'username' in request.POST and request.POST['username'] != '':
            username = request.POST['username']
            request.session['username'] = username

    return index(request)


def index(request):
    context = {'username': ''}
    if request.method == 'GET' and 'experiment' in request.GET:
        context['current_experiment'] = request.GET['experiment']
    if request.session.get('username', False):
        if request.method == 'POST' and 'experiment' in request.POST:
            current_experiment = request.POST['experiment']
            experiment = Experiment.objects.get(vesion=current_experiment)
        else:
            experiment = Experiment.objects.last()
        username = request.session['username']
        user, created = User.objects.get_or_create(username=username, experiment=experiment)
        training_number = experiment.training_number
        training_earning = experiment.training_earning
        contest_number = experiment.contest_number
        contest_earning = experiment.contest_earning
        game_number = experiment.game_number
        player_number = experiment.player_number
        game_max_minutes = experiment.game_max_minutes
        game_max_seconds = experiment.game_max_seconds
        game_minutes_to_reveal = experiment.game_minutes_to_reveal
        game_seconds_to_reveal = experiment.game_seconds_to_reveal
        total_minutes = experiment.total_minutes
        total_seconds = experiment.total_seconds
        user.started_study = timezone.now()
        user.finished_study = timezone.now()
        user.save()
        context = {'username': username, 'training_number': training_number, 'training_earning': round(training_earning),
                   'contest_number': contest_number, 'game_number': game_number, 'player_number': player_number - 1,
                   'contest_earning': contest_earning, 'game_max_minutes': game_max_minutes,
                   'game_max_seconds': game_max_seconds, 'current_experiment': experiment.vesion,
                   'game_minutes_to_reveal': game_minutes_to_reveal, 'game_seconds_to_reveal': game_seconds_to_reveal,
                   'total_minutes': total_minutes, 'total_seconds': total_seconds,
                   'total_participants_number': experiment.total_participants_number}
        usersInExperiment = User.objects.filter(experiment=experiment)
        usersInExperimentNum = usersInExperiment.count()
        if usersInExperimentNum < experiment.total_participants_number:
            context['needMoreSubjects'] = 1
        else:
            context['needMoreSubjects'] = 0
        if request.method == 'POST' and 'experiment' in request.POST:
            jsonResponseObj = JsonResponse(context)
            # print ("\n\n\nJsonResponse.content " + str(jsonResponseObj.content))
            return jsonResponseObj
    return render(request, 'knapsack/index.html', context)


def trainingintro(request):
    context = {'username': ''}
    if request.session.get('username', False):
        username = request.session['username']
        user = User.objects.get(username=username)
        experiment = user.experiment
        training_number = experiment.training_number
        training_earning = experiment.training_earning
        contest_number = experiment.contest_number
        game_number = experiment.game_number
        player_number = experiment.player_number
        total_training_minutes = experiment.total_training_minutes
        total_training_seconds = experiment.total_training_seconds
        game_minutes_to_reveal = experiment.game_minutes_to_reveal
        game_seconds_to_reveal = experiment.game_seconds_to_reveal
        total_minutes = experiment.total_minutes
        total_seconds = experiment.total_seconds
        context = {'username': username, 'training_number': training_number, 'training_earning': round(training_earning),
                   'contest_number': contest_number, 'game_number': game_number, 'player_number': player_number - 1,
                   'total_training_minutes': total_training_minutes, 'total_training_seconds': total_training_seconds,
                   'game_minutes_to_reveal': game_minutes_to_reveal, 'game_seconds_to_reveal': game_seconds_to_reveal,
                   'total_minutes': total_minutes, 'total_seconds': total_seconds}
    return render(request, 'knapsack/training_intro.html', context)


def OptimalSolutionFinder(gameType):
    optimalSolution = gameType.optimal_0 * gameType.value_0
    optimalSolution += gameType.optimal_1 * gameType.value_1
    optimalSolution += gameType.optimal_2 * gameType.value_2
    optimalSolution += gameType.optimal_3 * gameType.value_3
    optimalSolution += gameType.optimal_4 * gameType.value_4
    optimalSolution += gameType.optimal_5 * gameType.value_5
    optimalSolution += gameType.optimal_6 * gameType.value_6
    optimalSolution += gameType.optimal_7 * gameType.value_7
    optimalSolution += gameType.optimal_8 * gameType.value_8
    optimalSolution += gameType.optimal_9 * gameType.value_9
    optimalSolution += gameType.optimal_10 * gameType.value_10
    optimalSolution += gameType.optimal_11 * gameType.value_11

    return optimalSolution


def difficultyCalculator(gameType):
    if gameType.difficulty == 0:
        itemsNum = 0
        if gameType.value_0 != 0 and gameType.weight_0 != 0:
            itemsNum = 1
            if gameType.value_1 != 0 and gameType.weight_1 != 0:
                itemsNum = 2
                if gameType.value_2 != 0 and gameType.weight_2 != 0:
                    itemsNum = 3
                    if gameType.value_3 != 0 and gameType.weight_3 != 0:
                        itemsNum = 4
                        if gameType.value_4 != 0 and gameType.weight_4 != 0:
                            itemsNum = 5
                            if gameType.value_5 != 0 and gameType.weight_5 != 0:
                                itemsNum = 6
                                if gameType.value_6 != 0 and gameType.weight_6 != 0:
                                    itemsNum = 7
                                    if gameType.value_7 != 0 and gameType.weight_7 != 0:
                                        itemsNum = 8
                                        if gameType.value_8 != 0 and gameType.weight_8 != 0:
                                            itemsNum = 9
                                            if gameType.value_9 != 0 and gameType.weight_9 != 0:
                                                itemsNum = 10
                                                if gameType.value_10 != 0 and gameType.weight_10 != 0:
                                                    itemsNum = 11
                                                    if gameType.value_11 != 0 and gameType.weight_11 != 0:
                                                        itemsNum = 12
        gameType.difficulty = math.log(gameType.capacity, 2) * itemsNum
        gameType.save()
        return gameType.difficulty
    return gameType.difficulty


def getRandomGameType(userGames):
    randomGametypes = Gametype.objects.filter(for_contest=1)
    for userGame in userGames:
        gameObj = userGame.game
        randomGametypes = randomGametypes.exclude(
            capacity=gameObj.capacity, value_0=gameObj.value_0,
            weight_0=gameObj.weight_0, value_1=gameObj.value_1,
            weight_1=gameObj.weight_1, value_2=gameObj.value_2,
            weight_2=gameObj.weight_2, value_3=gameObj.value_3,
            weight_3=gameObj.weight_3, value_4=gameObj.value_4,
            weight_4=gameObj.weight_4, value_5=gameObj.value_5,
            weight_5=gameObj.weight_5, value_6=gameObj.value_6,
            weight_6=gameObj.weight_6, value_7=gameObj.value_7,
            weight_7=gameObj.weight_7, value_8=gameObj.value_8,
            weight_8=gameObj.weight_8, value_9=gameObj.value_9,
            weight_9=gameObj.weight_9, value_10=gameObj.value_10,
            weight_10=gameObj.weight_10, value_11=gameObj.value_11,
            weight_11=gameObj.weight_11, max_seconds=gameObj.max_seconds,
            max_minutes=gameObj.max_minutes)

    # grab the max pk in the database
    max_pk = randomGametypes.order_by('-pk')[0].pk

    # grab a random possible pk. we don't know if this pk does exist in the database, though
    random_pk = random.randint(1, max_pk)

    # return an object with that pk, or the first object with an pk greater than that one
    # this is a fast lookup, because your primary key probably has a RANGE index.
    randomGametypes = randomGametypes.filter(pk__gte=random_pk)

    return randomGametypes[0]


def training(request):
    context = {'username': ''}
    if request.method == 'GET' and request.session.get('username', False):
        username = request.session['username']
        user = User.objects.get(username=username)
        experiment = user.experiment
        userGamesNum = user.usergame_set.count()
        contestMode = 0
        contestusertrainingsNum = -1
        if userGamesNum != 0 and 'userGameId' in request.GET:
            contestMode = 1
            currentuserGame = Usergame.objects.get(pk=request.GET['userGameId'])
            contestusergameObj = Contestusergame.objects.get(usergame=currentuserGame)
            contestObj = contestusergameObj.contest
            contestusertrainingsNum = Contestusertraining.objects.filter(contest=contestObj, usertraining__user=user).count()

        userTrainings = user.usertraining_set.all()
        currentTrainingNum = len(userTrainings)
        for userTraining in userTrainings:
            youWon = False
            if userTraining.score >= userTraining.game.winning_score:
                youWon = True
            secondsPast = (timezone.now() - user.started_training).total_seconds()
            if ((experiment.total_training_minutes * 60 + experiment.total_training_seconds) > secondsPast and
                    not userTraining.submitted and not youWon):
                minutes = experiment.total_training_minutes - (secondsPast // 60)
                seconds = experiment.total_training_seconds - (secondsPast % 60)
                items = userTraining.usertrainingitem_set.all().order_by('move_time')
                inBag = [False] * 12
                for item in items:
                    if item.to_knapsack:
                        inBag[item.item_index] = True
                    elif item.from_knapsack:
                        inBag[item.item_index] = False
                context = {'username': username, 'capacity': userTraining.game.capacity,
                           'value_0': userTraining.game.value_0, 'weight_0': userTraining.game.weight_0, 'inBag_0': inBag[0],
                           'value_1': userTraining.game.value_1, 'weight_1': userTraining.game.weight_1, 'inBag_1': inBag[1],
                           'value_2': userTraining.game.value_2, 'weight_2': userTraining.game.weight_2, 'inBag_2': inBag[2],
                           'value_3': userTraining.game.value_3, 'weight_3': userTraining.game.weight_3, 'inBag_3': inBag[3],
                           'value_4': userTraining.game.value_4, 'weight_4': userTraining.game.weight_4, 'inBag_4': inBag[4],
                           'value_5': userTraining.game.value_5, 'weight_5': userTraining.game.weight_5, 'inBag_5': inBag[5],
                           'value_6': userTraining.game.value_6, 'weight_6': userTraining.game.weight_6, 'inBag_6': inBag[6],
                           'value_7': userTraining.game.value_7, 'weight_7': userTraining.game.weight_7, 'inBag_7': inBag[7],
                           'value_8': userTraining.game.value_8, 'weight_8': userTraining.game.weight_8, 'inBag_8': inBag[8],
                           'value_9': userTraining.game.value_9, 'weight_9': userTraining.game.weight_9, 'inBag_9': inBag[9],
                           'value_10': userTraining.game.value_10, 'weight_10': userTraining.game.weight_10,
                           'inBag_10': inBag[10], 'value_11': userTraining.game.value_11,
                           'weight_11': userTraining.game.weight_11, 'inBag_11': inBag[11], 'max_seconds': seconds,
                           'max_minutes': minutes, 'optimal_score': userTraining.game.optimal_score,
                           'winning_score': userTraining.game.winning_score, 'contestMode': contestMode,
                           'userTrainingId': userTraining.pk, 'trainingNum': currentTrainingNum,
                           'totalTrainingNum': user.experiment.training_number,
                           'quitTrainingNum': currentTrainingNum - user.experiment.training_number}
                if userGamesNum != 0 and 'userGameId' in request.GET:
                    context['userGameId'] = request.GET['userGameId']
                return render(request, 'knapsack/training.html', context)

        secondsPast = (timezone.now() - user.started_training).total_seconds()
        if ((currentTrainingNum < experiment.training_number and
            (experiment.total_training_minutes * 60 +
             experiment.total_training_seconds) > secondsPast) or contestusertrainingsNum == 0):
            if currentTrainingNum == 0:
                user.started_training = timezone.now()
                user.finished_training = timezone.now()
                user.save()
            minutes = experiment.total_training_minutes - (secondsPast // 60)
            seconds = experiment.total_training_seconds - (secondsPast % 60)
            randomGameType = Gametype.objects.filter(for_training=1)
            randomGameType = randomGameType.get(difficulty_level=currentTrainingNum + 1)
            optimal_score = OptimalSolutionFinder(randomGameType)
            difficulty = difficultyCalculator(randomGameType)
            trainingObj = Game.objects.create(
                experiment=user.experiment,
                gametype=randomGameType,
                capacity=randomGameType.capacity,
                player_number=1,
                value_0=randomGameType.value_0,
                weight_0=randomGameType.weight_0,
                optimal_0=randomGameType.optimal_0,
                value_1=randomGameType.value_1,
                weight_1=randomGameType.weight_1,
                optimal_1=randomGameType.optimal_1,
                value_2=randomGameType.value_2,
                weight_2=randomGameType.weight_2,
                optimal_2=randomGameType.optimal_2,
                value_3=randomGameType.value_3,
                weight_3=randomGameType.weight_3,
                optimal_3=randomGameType.optimal_3,
                value_4=randomGameType.value_4,
                weight_4=randomGameType.weight_4,
                optimal_4=randomGameType.optimal_4,
                value_5=randomGameType.value_5,
                weight_5=randomGameType.weight_5,
                optimal_5=randomGameType.optimal_5,
                value_6=randomGameType.value_6,
                weight_6=randomGameType.weight_6,
                optimal_6=randomGameType.optimal_6,
                value_7=randomGameType.value_7,
                weight_7=randomGameType.weight_7,
                optimal_7=randomGameType.optimal_7,
                value_8=randomGameType.value_8,
                weight_8=randomGameType.weight_8,
                optimal_8=randomGameType.optimal_8,
                value_9=randomGameType.value_9,
                weight_9=randomGameType.weight_9,
                optimal_9=randomGameType.optimal_9,
                value_10=randomGameType.value_10,
                weight_10=randomGameType.weight_10,
                optimal_10=randomGameType.optimal_10,
                value_11=randomGameType.value_11,
                weight_11=randomGameType.weight_11,
                optimal_11=randomGameType.optimal_11,
                max_seconds=randomGameType.max_seconds,
                max_minutes=randomGameType.max_minutes,
                winning_score=randomGameType.winning_score,
                optimal_score=optimal_score,
                difficulty=difficulty)
            userTraining = Usertraining.objects.create(
                user=user,
                game=trainingObj,
                started=timezone.now(),
                finished=timezone.now())
            context = {'username': username, 'capacity': randomGameType.capacity,
                       'value_0': randomGameType.value_0, 'weight_0': randomGameType.weight_0,
                       'value_1': randomGameType.value_1, 'weight_1': randomGameType.weight_1,
                       'value_2': randomGameType.value_2, 'weight_2': randomGameType.weight_2,
                       'value_3': randomGameType.value_3, 'weight_3': randomGameType.weight_3,
                       'value_4': randomGameType.value_4, 'weight_4': randomGameType.weight_4,
                       'value_5': randomGameType.value_5, 'weight_5': randomGameType.weight_5,
                       'value_6': randomGameType.value_6, 'weight_6': randomGameType.weight_6,
                       'value_7': randomGameType.value_7, 'weight_7': randomGameType.weight_7,
                       'value_8': randomGameType.value_8, 'weight_8': randomGameType.weight_8,
                       'value_9': randomGameType.value_9, 'weight_9': randomGameType.weight_9,
                       'value_10': randomGameType.value_10, 'weight_10': randomGameType.weight_10,
                       'value_11': randomGameType.value_11, 'weight_11': randomGameType.weight_11,
                       'userTrainingId': userTraining.pk, 'trainingNum': currentTrainingNum + 1,
                       'optimal_score': trainingObj.optimal_score, 'contestMode': contestMode,
                       'winning_score': trainingObj.winning_score, 'max_seconds': seconds,
                       'max_minutes': minutes, 'totalTrainingNum': user.experiment.training_number,
                       'quitTrainingNum': currentTrainingNum - user.experiment.training_number + 1}
            if userGamesNum != 0 and 'userGameId' in request.GET:
                context['userGameId'] = request.GET['userGameId']
                contestusertraining = Contestusertraining.objects.create(
                    contest=contestObj,
                    usertraining=userTraining,
                    score=0,
                )
                currentuserGame.quit = True
                currentuserGame.finished = timezone.now()
                currentuserGame.save()
            return render(request, 'knapsack/training.html', context)
        else:
            if userGamesNum == 0:
                user.finished_training = timezone.now()
            user.total_training_score = 0
            total_difficulty = 0
            trainingCounter = 0
            for userTraining in userTrainings:
                trainingCounter += 1
                user_training_score = userTraining.score / userTraining.game.winning_score
                if user_training_score >= 0.99:
                    user.total_training_score += 1
                # if trainingCounter <= user.experiment.training_number:
                #     user.total_training_score += user_training_score
                # else:
                #     user.total_training_score += math.floor(user_training_score)
                if userGamesNum == 0 and (userTraining.finished - userTraining.started).seconds != 0:
                    # user.skill += (user_training_score * userTraining.game.difficulty /
                    #                (userTraining.finished - userTraining.started).seconds)
                    total_difficulty += userTraining.game.difficulty
            # if userGamesNum == 0:
            #     user.skill = user.skill / total_difficulty
            user.total_training_score = round(user.total_training_score, 2)
            user.total_earning = math.ceil(user.total_training_score + 5)
            user.save()
            contest_number = user.experiment.contest_number
            game_number = user.experiment.game_number
            player_number = user.experiment.player_number
            game_max_minutes = user.experiment.game_max_minutes
            game_max_seconds = user.experiment.game_max_seconds
            game_minutes_to_reveal = user.experiment.game_minutes_to_reveal
            game_seconds_to_reveal = user.experiment.game_seconds_to_reveal

            context = {'username': username, 'total_training_score': user.total_training_score,
                       'total_earning': user.total_earning,
                       'contestsNum': contest_number, 'game_number': game_number,
                       'player_number': player_number - 1, 'game_max_minutes': game_max_minutes,
                       'game_max_seconds': game_max_seconds, 'game_minutes_to_reveal': game_minutes_to_reveal,
                       'game_seconds_to_reveal': game_seconds_to_reveal}
            if userGamesNum != 0:
                context['quiz_score'] = round(user.quizscore, 2)
                context['quit_question_earning'] = round(user.quit_question_earning, 2)
                context['total_game_score'] = round(user.total_game_score, 2)
                context['contest_score'] = contestusergameObj.score
                user.total_earning = math.ceil(user.total_training_score + user.quizscore + user.total_game_score
                                                     + user.quit_question_earning + 5)
                user.save()
                context['total_earning'] = user.total_earning
                context['phase'] = 'game'
                if contestObj.index == user.experiment.contest_number:
                    context['phase'] = 'contest'
                currentuserGame = user.usergame_set.latest('created')
                currentContestIndex = Contestusergame.objects.get(usergame=currentuserGame).contest.index
                context['contestIndex'] = currentContestIndex
            else:
                context['phase'] = 'training'
            return render(request, 'knapsack/results.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/training.html', context)


def trainingsubmit(request):
    if request.method == 'POST':
        requestPost = json.loads(request.body.decode('utf-8'))
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            userGamesNum = user.usergame_set.count()
            userTraining = Usertraining.objects.get(pk=requestPost['userTrainingId'])
            userTraining.finished = timezone.now()
            userTrainings = user.usertraining_set.all()
            currentTrainingNum = len(userTrainings)
            youWon = False
            if 'item_index' in requestPost:
                userTrainingItems = Usertrainingitem.objects.filter(usertraining=userTraining,
                                                                    item_index=requestPost['item_index'])
                if requestPost['to_knapsack'] and len(userTrainingItems) % 2 == 0:
                    userTraining.score += requestPost['item_value']
                    userTrainingItem = Usertrainingitem.objects.create(
                        usertraining=userTraining,
                        item_index=requestPost['item_index'],
                        to_knapsack=requestPost['to_knapsack'],
                        from_knapsack=requestPost['from_knapsack'],
                        move_time=timezone.now())
                    if userTraining.score >= userTraining.game.winning_score:
                        youWon = True
                elif requestPost['from_knapsack'] and len(userTrainingItems) % 2 == 1:
                    userTraining.score -= requestPost['item_value']
                    userTrainingItem = Usertrainingitem.objects.create(
                        usertraining=userTraining,
                        item_index=requestPost['item_index'],
                        to_knapsack=requestPost['to_knapsack'],
                        from_knapsack=requestPost['from_knapsack'],
                        move_time=timezone.now())
            elif 'submitted' in requestPost:
                userTraining.submitted = True
            userTraining.save()
            context = {'youWon': youWon}
            return JsonResponse(context)
    context = {'username': ''}
    return render(request, 'knapsack/training.html', context)


def results(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            userGames = user.usergame_set.all()
            currentGameNum = len(userGames)
            contestMode = 0
            if currentGameNum != 0:
                contestMode = 1
            if 'userTrainingId' in request.GET:
                userTrainings = user.usertraining_set.all()
                currentTrainingNum = len(userTrainings)
                userTraining = Usertraining.objects.get(pk=request.GET['userTrainingId'])
                items = userTraining.usertrainingitem_set.all().order_by('move_time')
                inBag = [False] * 12
                for item in items:
                    if item.to_knapsack:
                        inBag[item.item_index] = True
                    elif item.from_knapsack:
                        inBag[item.item_index] = False
                context = {'username': username,
                           'capacity': userTraining.game.capacity,
                           'score': round(userTraining.score / userTraining.game.winning_score, 2),
                           'value_0': userTraining.game.value_0, 'weight_0': userTraining.game.weight_0, 'inBag_0': inBag[0],
                           'optimal_0': userTraining.game.optimal_0,
                           'value_1': userTraining.game.value_1, 'weight_1': userTraining.game.weight_1, 'inBag_1': inBag[1],
                           'optimal_1': userTraining.game.optimal_1,
                           'value_2': userTraining.game.value_2, 'weight_2': userTraining.game.weight_2, 'inBag_2': inBag[2],
                           'optimal_2': userTraining.game.optimal_2,
                           'value_3': userTraining.game.value_3, 'weight_3': userTraining.game.weight_3, 'inBag_3': inBag[3],
                           'optimal_3': userTraining.game.optimal_3,
                           'value_4': userTraining.game.value_4, 'weight_4': userTraining.game.weight_4, 'inBag_4': inBag[4],
                           'optimal_4': userTraining.game.optimal_4,
                           'value_5': userTraining.game.value_5, 'weight_5': userTraining.game.weight_5, 'inBag_5': inBag[5],
                           'optimal_5': userTraining.game.optimal_5,
                           'value_6': userTraining.game.value_6, 'weight_6': userTraining.game.weight_6, 'inBag_6': inBag[6],
                           'optimal_6': userTraining.game.optimal_6,
                           'value_7': userTraining.game.value_7, 'weight_7': userTraining.game.weight_7, 'inBag_7': inBag[7],
                           'optimal_7': userTraining.game.optimal_7,
                           'value_8': userTraining.game.value_8, 'weight_8': userTraining.game.weight_8, 'inBag_8': inBag[8],
                           'optimal_8': userTraining.game.optimal_8,
                           'value_9': userTraining.game.value_9, 'weight_9': userTraining.game.weight_9, 'inBag_9': inBag[9],
                           'optimal_9': userTraining.game.optimal_9,
                           'value_10': userTraining.game.value_10, 'weight_10': userTraining.game.weight_10,
                           'inBag_10': inBag[10], 'optimal_10': userTraining.game.optimal_10,
                           'value_11': userTraining.game.value_11, 'weight_11': userTraining.game.weight_11,
                           'inBag_11': inBag[11], 'optimal_11': userTraining.game.optimal_11,
                           'optimal_score': round(userTraining.game.optimal_score), 'contestMode': contestMode,
                           'userTrainingId': userTraining.pk, 'trainingNum': currentTrainingNum,
                           'totalTrainingNum': user.experiment.training_number,
                           'quitTrainingNum': currentTrainingNum - user.experiment.training_number}
                if userTraining.score / userTraining.game.winning_score >= 0.99:
                    context['score'] = 1
                else:
                    context['score'] = 0
                if currentGameNum != 0 and 'userGameId' in request.GET:
                    context['userGameId'] = request.GET['userGameId']
            elif 'userGameId' in request.GET:
                currentuserGame = user.usergame_set.latest('created')
                currentContestIndex = Contestusergame.objects.get(usergame=currentuserGame).contest.index
                userGame = Usergame.objects.get(pk=request.GET['userGameId'])
                items = userGame.usergameitem_set.all().order_by('move_time')
                inBag = [False] * 12
                for item in items:
                    if item.to_knapsack:
                        inBag[item.item_index] = True
                    elif item.from_knapsack:
                        inBag[item.item_index] = False
                context = {'username': username,
                           'capacity': userGame.game.capacity,
                           'score': round(userGame.score / userGame.game.winning_score, 2),
                           'value_0': userGame.game.value_0, 'weight_0': userGame.game.weight_0, 'inBag_0': inBag[0],
                           'optimal_0': userGame.game.optimal_0,
                           'value_1': userGame.game.value_1, 'weight_1': userGame.game.weight_1, 'inBag_1': inBag[1],
                           'optimal_1': userGame.game.optimal_1,
                           'value_2': userGame.game.value_2, 'weight_2': userGame.game.weight_2, 'inBag_2': inBag[2],
                           'optimal_2': userGame.game.optimal_2,
                           'value_3': userGame.game.value_3, 'weight_3': userGame.game.weight_3, 'inBag_3': inBag[3],
                           'optimal_3': userGame.game.optimal_3,
                           'value_4': userGame.game.value_4, 'weight_4': userGame.game.weight_4, 'inBag_4': inBag[4],
                           'optimal_4': userGame.game.optimal_4,
                           'value_5': userGame.game.value_5, 'weight_5': userGame.game.weight_5, 'inBag_5': inBag[5],
                           'optimal_5': userGame.game.optimal_5,
                           'value_6': userGame.game.value_6, 'weight_6': userGame.game.weight_6, 'inBag_6': inBag[6],
                           'optimal_6': userGame.game.optimal_6,
                           'value_7': userGame.game.value_7, 'weight_7': userGame.game.weight_7, 'inBag_7': inBag[7],
                           'optimal_7': userGame.game.optimal_7,
                           'value_8': userGame.game.value_8, 'weight_8': userGame.game.weight_8, 'inBag_8': inBag[8],
                           'optimal_8': userGame.game.optimal_8,
                           'value_9': userGame.game.value_9, 'weight_9': userGame.game.weight_9, 'inBag_9': inBag[9],
                           'optimal_9': userGame.game.optimal_9,
                           'value_10': userGame.game.value_10, 'weight_10': userGame.game.weight_10, 'inBag_10': inBag[10],
                           'optimal_10': userGame.game.optimal_10,
                           'value_11': userGame.game.value_11, 'weight_11': userGame.game.weight_11, 'inBag_11': inBag[11],
                           'optimal_11': userGame.game.optimal_11,
                           'optimal_score': round(userGame.game.optimal_score),
                           'userGameId': userGame.pk, 'gameNum': currentGameNum,
                           'totalGameNum': user.experiment.game_number, 'contestIndex': currentContestIndex,
                           'totalContestsNum': user.experiment.contest_number}
                if currentGameNum != 0:
                    context['score'] = math.floor(userGame.score / userGame.game.winning_score)
            return render(request, 'knapsack/GameResults.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/training.html', context)


def contestintro(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            experiment = user.experiment
            contest_number = experiment.contest_number
            player_number = experiment.player_number
            game_number = experiment.game_number
            game_max_minutes = experiment.game_max_minutes
            game_max_seconds = experiment.game_max_seconds
            contest_earning = experiment.contest_earning
            training_contest_earning = experiment.training_contest_earning
            no_information = experiment.no_information
            intermediate_information = experiment.intermediate_information
            complete_information = experiment.complete_information
            context = {'username': username, 'player_number': player_number - 1,
                       'contest_number': contest_number, 'game_number': game_number,
                       'game_max_minutes': game_max_minutes, 'game_max_seconds': game_max_seconds,
                       'contest_earning': contest_earning, 'training_contest_earning': training_contest_earning,
                       'no_information': no_information, 'intermediate_information': intermediate_information,
                       'complete_information': complete_information}
            return render(request, 'knapsack/ContestIntro.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def quiz(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            context = {'username': username, }
            return render(request, 'knapsack/Quiz.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def quizsubmit(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)

            GroupSize3 = request.GET['GroupSize3']
            GroupSize4 = request.GET['GroupSize4']
            GroupSize12 = request.GET['GroupSize12']
            GroupSizeNotSure = request.GET['GroupSizeNotSure']
            SameOpponentYes = request.GET['SameOpponentYes']
            SameOpponentNo = request.GET['SameOpponentNo']
            SameOpponentNotSure = request.GET['SameOpponentNotSure']
            InfeasibleIsSolvableTrue = request.GET['InfeasibleIsSolvableTrue']
            InfeasibleIsSolvableFalse = request.GET['InfeasibleIsSolvableFalse']
            InfeasibleIsSolvableNotSure = request.GET['InfeasibleIsSolvableNotSure']
            SureGameTrue = request.GET['SureGameTrue']
            SureGameFalse = request.GET['SureGameFalse']
            SureGameNotSure = request.GET['SureGameNotSure']
            Feasible60Infeasible40 = request.GET['Feasible60Infeasible40']
            Feasible60Target40 = request.GET['Feasible60Target40']
            Feasible60NotSure = request.GET['Feasible60NotSure']

            user.quizscore = 0
            user.GroupSize3 = convertNum2Bool(GroupSize3)
            user.GroupSize4 = convertNum2Bool(GroupSize4)
            user.GroupSize12 = convertNum2Bool(GroupSize12)
            user.GroupSizeNotSure = convertNum2Bool(GroupSizeNotSure)
            GroupSize4 = 1
            GroupSize3 = -1
            GroupSize12 = -1
            GroupSizeNotSure = -1
            if (not user.GroupSize3) and user.GroupSize4 and (not user.GroupSize12) and (not user.GroupSizeNotSure):
                user.quizscore += 0.2
                GroupSize4 = 2
            elif user.GroupSize3:
                GroupSize3 = -2
            elif user.GroupSize12:
                GroupSize12 = -2
            elif user.GroupSizeNotSure:
                GroupSizeNotSure = -2
            user.SameOpponentYes = convertNum2Bool(SameOpponentYes)
            user.SameOpponentNo = convertNum2Bool(SameOpponentNo)
            user.SameOpponentNotSure = convertNum2Bool(SameOpponentNotSure)
            SameOpponentYes = -1
            SameOpponentNo = 1
            SameOpponentNotSure = -1
            if (not user.SameOpponentYes) and user.SameOpponentNo and (not user.SameOpponentNotSure):
                user.quizscore += 0.2
                SameOpponentNo = 2
            elif user.SameOpponentYes:
                SameOpponentYes = -2
            elif user.SameOpponentNotSure:
                SameOpponentNotSure = -2
            user.InfeasibleIsSolvableTrue = convertNum2Bool(InfeasibleIsSolvableTrue)
            user.InfeasibleIsSolvableFalse = convertNum2Bool(InfeasibleIsSolvableFalse)
            user.InfeasibleIsSolvableNotSure = convertNum2Bool(InfeasibleIsSolvableNotSure)
            InfeasibleIsSolvableTrue = -1
            InfeasibleIsSolvableFalse = 1
            InfeasibleIsSolvableNotSure = -1
            if ((not user.InfeasibleIsSolvableTrue) and user.InfeasibleIsSolvableFalse and
                    (not user.InfeasibleIsSolvableNotSure)):
                user.quizscore += 0.2
                InfeasibleIsSolvableFalse = 2
            elif user.InfeasibleIsSolvableTrue:
                InfeasibleIsSolvableTrue = -2
            elif user.InfeasibleIsSolvableNotSure:
                InfeasibleIsSolvableNotSure = -2
            user.SureGameTrue = convertNum2Bool(SureGameTrue)
            user.SureGameFalse = convertNum2Bool(SureGameFalse)
            user.SureGameNotSure = convertNum2Bool(SureGameNotSure)
            SureGameTrue = 1
            SureGameFalse = -1
            SureGameNotSure = -1
            if user.SureGameTrue and (not user.SureGameFalse) and (not user.SureGameNotSure):
                user.quizscore += 0.2
                SureGameTrue = 2
            elif user.SureGameFalse:
                SureGameFalse = -2
            elif user.SureGameNotSure:
                SureGameNotSure = -2
            user.Feasible60Infeasible40 = convertNum2Bool(Feasible60Infeasible40)
            user.Feasible60Target40 = convertNum2Bool(Feasible60Target40)
            user.Feasible60NotSure = convertNum2Bool(Feasible60NotSure)
            Feasible60Infeasible40 = 1
            Feasible60Target40 = -1
            Feasible60NotSure = -1
            if user.Feasible60Infeasible40 and (not user.Feasible60Target40) and (not user.Feasible60NotSure):
                user.quizscore += 0.2
                Feasible60Infeasible40 = 2
            elif user.Feasible60Target40:
                Feasible60Target40 = -2
            elif user.Feasible60NotSure:
                Feasible60NotSure = -2
            user.total_earning = math.ceil(user.quizscore + user.total_training_score + 5)
            user.save()

            context = {'username': username, 'phase': 'quiz',
                       'GroupSize3': GroupSize3,
                       'GroupSize4': GroupSize4,
                       'GroupSize12': GroupSize12,
                       'GroupSizeNotSure': GroupSizeNotSure,
                       'SameOpponentYes': SameOpponentYes,
                       'SameOpponentNo': SameOpponentNo,
                       'SameOpponentNotSure': SameOpponentNotSure,
                       'InfeasibleIsSolvableTrue': InfeasibleIsSolvableTrue,
                       'InfeasibleIsSolvableFalse': InfeasibleIsSolvableFalse,
                       'InfeasibleIsSolvableNotSure': InfeasibleIsSolvableNotSure,
                       'SureGameTrue': SureGameTrue,
                       'SureGameFalse': SureGameFalse,
                       'SureGameNotSure': SureGameNotSure,
                       'Feasible60Infeasible40': Feasible60Infeasible40,
                       'Feasible60Target40': Feasible60Target40,
                       'Feasible60NotSure': Feasible60NotSure, }
            return render(request, 'knapsack/Quiz.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def quizresults(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)

            context = {'username': username, 'phase': 'quiz', 'quiz_score': round(user.quizscore, 2),
                       'total_game_score': round(user.total_game_score, 2),
                       'total_training_score': round(user.total_training_score, 2),
                       'total_earning': user.total_earning}
            return render(request, 'knapsack/results.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


# Partition a list into sets of equal size.
def equipart(s, p):
    if len(s) % p != 0:
        raise ValueError("Set must be of a length which is a multiple of p")
    com = map(set, set(itertools.combinations(s, p)))
    res = [x for x in itertools.combinations(com, int(len(s) / p)) if set().union(*x) == s]
    return res


def waitingroom(request):
    if request.session.get('username', False):
        username = request.session['username']
        user = User.objects.get(username=username)
        experiment = user.experiment
        contest_number = experiment.contest_number
        quit_question_earning = experiment.quit_question_earning
        currentuserGamesNum = user.usergame_set.count()
        currentContestIndex = 0
        if currentuserGamesNum != 0:
            currentuserGame = user.usergame_set.latest('created')
            # print(str(Contestusergame.objects.all()))
            # If the last use call has generated the userGame, but not the Contestusergame yet:
            notFoundCurrentContest = True
            while notFoundCurrentContest:
                try:
                    currentContest = Contestusergame.objects.get(usergame=currentuserGame).contest
                    notFoundCurrentContest = False
                except:
                    time.sleep(0.1)
            currentContestIndex = currentContest.index
            currentContestUsergames = Contestusergame.objects.filter(contest=currentContest)
        # print("username: " + username)
        # print("contest_number: " + str(contest_number))
        # print("currentContestIndex: " + str(currentContestIndex))
        if (contest_number > currentContestIndex or
            (currentuserGamesNum != 0 and (not currentuserGame.quit) and
             ((currentuserGame.finished - currentuserGame.started).total_seconds() < 1) and
             (not currentuserGame.youWon) and (not currentuserGame.opponentWon))):
            player_number = experiment.player_number
            game_number = experiment.game_number
            game_max_minutes = experiment.game_max_minutes
            game_max_seconds = experiment.game_max_seconds
            contest_earning = experiment.contest_earning
            training_contest_earning = experiment.training_contest_earning
            usersInExperiment = User.objects.filter(experiment=user.experiment)
            usersInExperimentNum = usersInExperiment.count()
            notGroupedYet = False
            if user.group == 0:
                usersInExperimentWithoutGroupNum = User.objects.filter(experiment=user.experiment, group=0).count()
                if usersInExperimentNum == usersInExperimentWithoutGroupNum:
                    notGroupedYet = True
            if notGroupedYet is False:
                usersInExperiment = User.objects.filter(experiment=user.experiment, group=user.group)
                # print("\nusersInExperiment: " + str(usersInExperiment))
                # print("\n notGroupedYet is False. But usersInExperiment: " + str(usersInExperiment.count()))
                usersInExperimentNum = usersInExperiment.count()
            usersWaiting = usersInExperiment.filter(waiting_for_game=True)
            usersWaitingNum = usersWaiting.count()
            lastUser = False
            if (not user.waiting_for_game) and (usersInExperimentNum - usersWaitingNum == 1):
                lastUser = True
            user = User.objects.get(username=username)
            if user.waiting_for_game is False:
                user.waiting_for_game = True
                user.save()

            initializing = False
            if notGroupedYet is True:
                initializing = experiment.initializing
            elif user.group == 1:
                initializing = experiment.group1_initializing
            elif user.group == 2:
                initializing = experiment.group2_initializing
            elif user.group == 3:
                initializing = experiment.group3_initializing
            elif user.group == 4:
                initializing = experiment.group4_initializing
            # print ("initializing: " + str(initializing))
            # print ("usersInExperimentNum: " + str(usersInExperimentNum))
            # print ("usersWaitingNum: " + str(usersWaitingNum))
            # print ("usersInExperimentNum - usersWaitingNum: " + str(usersInExperimentNum - usersWaitingNum))

            if (not lastUser) or initializing:
                if request.method == 'GET':
                    context = {'username': username, 'player_number': player_number - 1, 'game_number': game_number,
                               'game_max_minutes': game_max_minutes, 'game_max_seconds': game_max_seconds,
                               'contest_earning': contest_earning, 'training_contest_earning': training_contest_earning,
                               'otherPlayersNumWanted': usersInExperimentNum - usersWaitingNum,
                               'quit_question_earning': quit_question_earning,
                               'contestIndex': currentContestIndex + 1}
                    # print ("(not lastUser) or initializing GET response.")
                    return render(request, 'knapsack/PleaseWait.html', context)
                if request.method == 'POST':
                    requestPOSTObj = request.POST  # force reading of POST data
                    # print ("currentuserGamesNum: " + str(currentuserGamesNum))
                    if (initializing or currentuserGamesNum == 0 or currentuserGame.quit or
                            ((currentuserGame.finished - currentuserGame.started).total_seconds() >= 1) or
                            currentuserGame.youWon or currentuserGame.opponentWon or
                            len(currentContestUsergames) > player_number):
                        # print("post and initializing: " + str(initializing))
                        otherPlayerNumWantedTemp = usersInExperimentNum - usersWaitingNum
                        if otherPlayerNumWantedTemp == 0:
                            otherPlayerNumWantedTemp = 1
                        context = {'otherPlayersNumWanted': otherPlayerNumWantedTemp}
                    else:
                        time.sleep(0.4)

                        context = {'no_information': currentuserGame.game.no_information,
                                   'intermediate_information': currentuserGame.game.intermediate_information,
                                   'complete_information': currentuserGame.game.complete_information,
                                   'infeasiblility20Percent': currentuserGame.game.infeasiblility20Percent,
                                   'infeasiblility40Percent': currentuserGame.game.infeasiblility40Percent,
                                   'game_seconds_to_reveal': currentuserGame.game.seconds_to_reveal,
                                   'game_minutes_to_reveal': currentuserGame.game.minutes_to_reveal,
                                   'otherPlayersNumWanted': 0, 'quit_question_earning': quit_question_earning,
                                   'contestIndex': currentContestIndex + 1}
                    # print("post and not initializing: " + str(initializing))
                    # print("user: " + str(user))
                    # print("user.group: " + str(user.group))
                    # print ("currentuserGame Duration: " + str((currentuserGame.finished - currentuserGame.started).total_seconds()))
                    jsonResponseObj = JsonResponse(context)
                    # print ("\n\n\nJsonResponse.content " + str(jsonResponseObj.content))
                    return jsonResponseObj
            else:
                # print ("Entered the last player section.")
                if user.group == 0:
                    usersInExperiment = User.objects.filter(experiment=user.experiment)
                    usersInExperimentNum = usersInExperiment.count()
                    gameTypes = Gametype.objects.all()
                    for gameType in gameTypes:
                        gameTypeMaxScoreRatio = 0
                        gameTypeMinScoreRatio = 0
                        for userInExperiment in usersInExperiment:
                            userTrainings = userInExperiment.usertraining_set.filter(game__gametype=gameType)
                            for userTraining in userTrainings:
                                userTrainingScoreRatio = 0
                                userTrainingDuration = (userTraining.finished - userTraining.started).seconds
                                if userTrainingDuration != 0:
                                    userTrainingScoreRatio = userTraining.score / userTrainingDuration
                                    if gameTypeMaxScoreRatio < userTrainingScoreRatio:
                                        gameTypeMaxScoreRatio = userTrainingScoreRatio
                                    if gameTypeMinScoreRatio > userTrainingScoreRatio:
                                        gameTypeMinScoreRatio = userTrainingScoreRatio
                        gameType.max_score_ratio = gameTypeMaxScoreRatio
                        gameType.min_score_ratio = gameTypeMinScoreRatio
                        gameType.save()
                        for userInExperiment in usersInExperiment:
                            userTrainings = userInExperiment.usertraining_set.filter(game__gametype=gameType)
                            for userTraining in userTrainings:
                                userTrainingScoreRatio = 0
                                userTrainingDuration = (userTraining.finished - userTraining.started).seconds
                                if userTrainingDuration != 0:
                                    userTrainingScoreRatio = userTraining.score / userTrainingDuration
                                if (gameType.max_score_ratio - gameType.min_score_ratio) != 0:
                                    userInExperiment.skill += ((userTrainingScoreRatio - gameType.min_score_ratio) /
                                                               (gameType.max_score_ratio - gameType.min_score_ratio))
                            userInExperiment.save()
                    usersInExperiment = usersInExperiment.order_by('skill')
                    if usersInExperimentNum % 4 == 0:
                        groupCounter = 0
                        for userCounter, userInExperiment in enumerate(usersInExperiment):
                            if userCounter % 4 == 0:
                                groupCounter += 1
                            userInExperiment.group = groupCounter
                            userInExperiment.save()
                    # print("usersInExperiment: " + str(usersInExperiment))
                    # for userCounter, userInExperiment in enumerate(usersInExperiment):
                    #     print("userCounter: " + str(userCounter))
                    #     print("userInExperiment: " + str(userInExperiment))
                    #     print("userInExperiment.group: " + str(userInExperiment.group))

                    usersInExperimentTotal = []
                    for groupIndex in range(1,5):
                        usersInExperimentGroup = usersInExperiment.filter(group=groupIndex)
                        # print("usersInExperimentGroup: " + str(usersInExperimentGroup))
                        playersPartitions = list(list(equipart(set(usersInExperimentGroup), player_number))[currentContestIndex])
                        # print("playersPartitions: " + str(playersPartitions))
                        for playersPartition in playersPartitions:
                            for playerPartition in playersPartition:
                                usersInExperimentTotal.append(playerPartition)
                    usersInExperiment = usersInExperimentTotal

                else:
                    # Creating partitions of sets such that each partition is the same length.
                    # E.g., equipart({1,2,3,4}, 2)
                    # [({1, 2}, {3, 4}), ({1, 3}, {2, 4}), ({1, 4}, {2, 3})]
                    playersPartitions = list(list(equipart(set(usersInExperiment), player_number))[currentContestIndex])
                    # print("playersPartitions: " + str(playersPartitions))
                    usersInExperiment = []
                    for playersPartition in playersPartitions:
                        for playerPartition in playersPartition:
                            usersInExperiment.append(playerPartition)

                if notGroupedYet is True:
                    experiment.initializing = True
                elif user.group == 1:
                    experiment.group1_initializing = True
                elif user.group == 2:
                    experiment.group2_initializing = True
                elif user.group == 3:
                    experiment.group3_initializing = True
                elif user.group == 4:
                    experiment.group4_initializing = True
                experiment.save()
                thisUserGame = None

                # print ("In last player, currentContestIndex: " + str(currentContestIndex))
                # print ("contest_number > currentContestIndex: " + str(contest_number > currentContestIndex))

                for userIndex in range(0, len(usersInExperiment), player_number):
                    # print ("userIndex: " + str(userIndex))
                    players = []
                    for playerIndex in range(player_number):
                        # print("playerIndex: " + str(playerIndex))
                        player = usersInExperiment[userIndex + playerIndex]
                        players.append(player)

                    # print ("len(players): " + str(len(players)))

                    no_information = experiment.no_information
                    intermediate_information = experiment.intermediate_information
                    complete_information = experiment.complete_information
                    # randomCondition = random.randint(0, 2)
                    # if randomCondition < 0.5:
                    #     no_information = True
                    # elif randomCondition < 1.5:
                    #     intermediate_information = True
                    # elif randomCondition < 2.5:
                    #     complete_information = True

                    userGames = players[0].usergame_set.all()
                    currentGameNum = len(userGames)
                    randomGameType = Gametype.objects.filter(for_contest=1).exclude(for_training=1)
                    newContestGameIndex = currentGameNum + 1
                    randomGameTypeList = randomGameType.filter(difficulty_level=newContestGameIndex,
                                                               contest_index=currentContestIndex + 1)
                    # If the player has not played the second game of the contest yet, newContestGameIndex
                    # will show the second game of the current contest. So, we should go to the next
                    # difficulty level that is the first game of the next contest.
                    while (len(randomGameTypeList) == 0):
                        newContestGameIndex += 1
                        randomGameTypeList = randomGameType.filter(difficulty_level=newContestGameIndex,
                                                                   contest_index=currentContestIndex + 1)
                    randomGameType = randomGameTypeList[0]
                    difficulty = difficultyCalculator(randomGameType)
                    optimal_score = OptimalSolutionFinder(randomGameType)

                    winning_score = randomGameType.winning_score

                    # Generate the infeasibility probability Latin square.
                    contestsInfeasibility0PercentNum = Contest.objects.filter(experiment=experiment, infeasiblility20Percent=False,
                                                                              infeasiblility40Percent=False).count()
                    contestsInfeasibility20PercentNum = Contest.objects.filter(experiment=experiment, infeasiblility20Percent=True).count()
                    contestsInfeasibility40PercentNum = Contest.objects.filter(experiment=experiment, infeasiblility40Percent=True).count()
                    infeasiblility20Percent = False
                    infeasiblility40Percent = False
                    if contestsInfeasibility20PercentNum < contestsInfeasibility0PercentNum:
                        infeasiblility20Percent = True
                    elif contestsInfeasibility40PercentNum < contestsInfeasibility0PercentNum:
                        infeasiblility40Percent = True

                    infeasible = False
                    randomInfeasible = random.random() * 100
                    randomIncrease = int(random.random() * 19) + 1
                    if infeasiblility20Percent is True:
                        if randomInfeasible < 20:
                            infeasible = True
                            winning_score += randomIncrease
                    elif infeasiblility40Percent is True:
                        if randomInfeasible < 40:
                            infeasible = True
                            winning_score += randomIncrease

                    contestObj = Contest.objects.create(
                        experiment=experiment,
                        index=currentContestIndex + 1,
                        no_information=no_information,
                        intermediate_information=intermediate_information,
                        complete_information=complete_information,
                        infeasiblility20Percent=infeasiblility20Percent,
                        infeasiblility40Percent=infeasiblility40Percent,
                        infeasible=infeasible,
                    )
                    gameObj = Game.objects.create(
                        experiment=experiment,
                        gametype=randomGameType,
                        capacity=randomGameType.capacity,
                        player_number=player_number,
                        value_0=randomGameType.value_0,
                        weight_0=randomGameType.weight_0,
                        optimal_0=randomGameType.optimal_0,
                        value_1=randomGameType.value_1,
                        weight_1=randomGameType.weight_1,
                        optimal_1=randomGameType.optimal_1,
                        value_2=randomGameType.value_2,
                        weight_2=randomGameType.weight_2,
                        optimal_2=randomGameType.optimal_2,
                        value_3=randomGameType.value_3,
                        weight_3=randomGameType.weight_3,
                        optimal_3=randomGameType.optimal_3,
                        value_4=randomGameType.value_4,
                        weight_4=randomGameType.weight_4,
                        optimal_4=randomGameType.optimal_4,
                        value_5=randomGameType.value_5,
                        weight_5=randomGameType.weight_5,
                        optimal_5=randomGameType.optimal_5,
                        value_6=randomGameType.value_6,
                        weight_6=randomGameType.weight_6,
                        optimal_6=randomGameType.optimal_6,
                        value_7=randomGameType.value_7,
                        weight_7=randomGameType.weight_7,
                        optimal_7=randomGameType.optimal_7,
                        value_8=randomGameType.value_8,
                        weight_8=randomGameType.weight_8,
                        optimal_8=randomGameType.optimal_8,
                        value_9=randomGameType.value_9,
                        weight_9=randomGameType.weight_9,
                        optimal_9=randomGameType.optimal_9,
                        value_10=randomGameType.value_10,
                        weight_10=randomGameType.weight_10,
                        optimal_10=randomGameType.optimal_10,
                        value_11=randomGameType.value_11,
                        weight_11=randomGameType.weight_11,
                        optimal_11=randomGameType.optimal_11,
                        max_seconds=randomGameType.max_seconds,
                        max_minutes=randomGameType.max_minutes,
                        seconds_to_reveal=randomGameType.seconds_to_reveal,
                        minutes_to_reveal=randomGameType.minutes_to_reveal,
                        winning_score=winning_score,
                        no_information=no_information,
                        intermediate_information=intermediate_information,
                        complete_information=complete_information,
                        optimal_score=optimal_score,
                        difficulty=difficulty,
                        infeasiblility20Percent=infeasiblility20Percent,
                        infeasiblility40Percent=infeasiblility40Percent,
                        infeasible=infeasible
                    )
                    waitingroomDelay = 1
                    if currentContestIndex + 1 == 1:
                        waitingroomDelay = 2
                    for playerIndex in range(player_number):
                        userGameObj = Usergame.objects.create(
                            user=players[playerIndex],
                            game=gameObj,
                            started=timezone.now() + timedelta(minutes=waitingroomDelay, seconds=3),
                            finished=timezone.now() + timedelta(minutes=waitingroomDelay, seconds=3),
                        )
                        if user in players and thisUserGame is None:
                            thisUserGame = userGameObj
                        contestusergame = Contestusergame.objects.create(
                            contest=contestObj,
                            usergame=userGameObj,
                            score=0,
                        )

                if notGroupedYet is True:
                    experiment.initializing = False
                elif user.group == 1:
                    experiment.group1_initializing = False
                elif user.group == 2:
                    experiment.group2_initializing = False
                elif user.group == 3:
                    experiment.group3_initializing = False
                elif user.group == 4:
                    experiment.group4_initializing = False
                experiment.save()
                currentGame = user.usergame_set.latest('created').game
                if request.method == 'GET':
                    context = {'username': username, 'player_number': player_number - 1, 'game_number': game_number,
                               'game_max_minutes': game_max_minutes, 'game_max_seconds': game_max_seconds,
                               'contest_earning': contest_earning, 'training_contest_earning': training_contest_earning,
                               'no_information': currentGame.no_information,
                               'intermediate_information': currentGame.intermediate_information,
                               'complete_information': currentGame.complete_information,
                               'infeasiblility20Percent': currentGame.infeasiblility20Percent,
                               'infeasiblility40Percent': currentGame.infeasiblility40Percent,
                               'infeasible': currentGame.infeasible, 'quit_question_earning': quit_question_earning,
                               'game_seconds_to_reveal': currentGame.seconds_to_reveal,
                               'game_minutes_to_reveal': currentGame.minutes_to_reveal,
                               'otherPlayersNumWanted': usersInExperimentNum - usersWaitingNum,
                               'contestIndex': currentContestIndex + 1}
                    return render(request, 'knapsack/PleaseWait.html', context)
                if request.method == 'POST':
                    context = {'no_information': currentGame.no_information,
                               'intermediate_information': currentGame.intermediate_information,
                               'complete_information': currentGame.complete_information,
                               'infeasiblility20Percent': currentGame.infeasiblility20Percent,
                               'infeasiblility40Percent': currentGame.infeasiblility40Percent,
                               'infeasible': currentGame.infeasible, 'quit_question_earning': quit_question_earning,
                               'game_seconds_to_reveal': currentGame.seconds_to_reveal,
                               'game_minutes_to_reveal': currentGame.minutes_to_reveal,
                               'otherPlayersNumWanted': usersInExperimentNum - usersWaitingNum,
                               'contestIndex': currentContestIndex + 1}
                    return JsonResponse(context)
        else:
            # print ("Contests Finished.")
            user.waiting_for_game = False
            user.total_game_score = 0
            userContestGames = Contestusergame.objects.filter(usergame__user=user)
            for userContestGame in userContestGames:
                user.total_game_score += userContestGame.score
            user.total_game_score = round(user.total_game_score / 2)
            user.total_earning = math.ceil(user.total_game_score + user.quizscore + user.total_training_score + 5)
            user.save()
            experiment.initializing = False
            experiment.save()
            context = {'username': username, 'phase': 'contest', 'quiz_score': round(user.quizscore, 2),
                       'total_game_score': round(user.total_game_score, 2),
                       'total_training_score': round(user.total_training_score, 2),
                       'total_earning': user.total_earning}
            if request.method == 'GET':
                return render(request, 'knapsack/results.html', context)
            if request.method == 'POST':
                return JsonResponse(context)


def transposeListOfLists(opponentsScoresTrans):
    maxCol = len(opponentsScoresTrans[0])
    for row in opponentsScoresTrans:
        rowLength = len(row)
        if rowLength > maxCol:
            maxCol = rowLength
    opponentsScores = []
    for colIndex in range(maxCol):
        opponentsScores.append([])
        for row in opponentsScoresTrans:
            if colIndex < len(row):
                opponentsScores[colIndex].append(row[colIndex])
    return opponentsScores


def game(request):
    context = {'username': ''}
    if request.session.get('username', False):
        username = request.session['username']
        user = User.objects.get(username=username)
        user.waiting_for_game = False
        user.save()
        currentuserGame = user.usergame_set.latest('created')
        contestusergameObj = Contestusergame.objects.get(usergame=currentuserGame)
        currentContestIndex = contestusergameObj.contest.index
        # print ("user.usergame_set.all(): " + str(user.usergame_set.all()))
        # print ("currentContestIndex: " + str(currentContestIndex))
        
        contestObj = contestusergameObj.contest
        contestusergames = Contestusergame.objects.filter(contest=contestObj, usergame__user=user).order_by('created')
        # print ("contestusergames.count(): " + str(contestusergames.count()))
        
        totalUserGames = user.usergame_set.count()
        player_number = user.experiment.player_number
        game_number = user.experiment.game_number
        quit_question_earning = user.experiment.quit_question_earning
        totalGameIndices = range(user.experiment.game_number)
        players = User.objects.filter(usergame__game=currentuserGame.game)
        otherPlayers = players.exclude(username=username)
        # print ("players.count(): " + str(players.count()))
        # print ("otherPlayers.count(): " + str(otherPlayers.count()))
        
        userscores = []
        opponentsScoresTrans = []
        userGames = []
        for contestusergame in contestusergames:
            userGames.append(contestusergame.usergame)
            userscores.append(contestusergame.usergame.score)
            opponentsusergameScores = []
            for otherPlayer in otherPlayers:
                otherUserGame = Usergame.objects.get(user=otherPlayer, game=contestusergame.usergame.game)
                opponentsusergameScores.append(otherUserGame.score)
            opponentsScoresTrans.append(opponentsusergameScores)

        opponentsScores = transposeListOfLists(opponentsScoresTrans)

        # We calculate the remaining time for information revelation in a contest based on the first game of the contest.
        contestSecondsPast = int((timezone.now() - userGames[0].started).total_seconds())
        remainingSecondsToReveal = (userGames[0].game.minutes_to_reveal * 60 +
                                    userGames[0].game.seconds_to_reveal - contestSecondsPast)
        if remainingSecondsToReveal <= 0:
            minutes_to_reveal = 0
            seconds_to_reveal = 0
        else:
            seconds_to_reveal = remainingSecondsToReveal % 60
            minutes_to_reveal = remainingSecondsToReveal // 60

        currentGameNum = 0
        for counter, userGame in enumerate(userGames):
            currentGameNum = counter + 1
            # print ("currentGameNum: " + str(currentGameNum))
            currentGame = userGame.game
            opponentWon = False
            youWon = False
            if userGame.score >= currentGame.winning_score:
                youWon = True

            lastGame = len(userGames) == game_number
            for otherPlayer in otherPlayers:
                otherUserGame = Usergame.objects.get(user=otherPlayer, game=currentuserGame.game)
                if otherUserGame.score >= currentuserGame.game.winning_score:
                    opponentWon = True

            secondsPast = int((timezone.now() - userGame.started).total_seconds())
            if ((userGame.game.max_minutes * 60 + userGame.game.max_seconds) > secondsPast and
                    not userGame.submitted and not youWon and not (lastGame and opponentWon)):
                # print ("Enterred the current game.")

                remainingSeconds = userGame.game.max_minutes * 60 + userGame.game.max_seconds - secondsPast
                minutes = remainingSeconds // 60
                seconds = remainingSeconds % 60
                items = userGame.usergameitem_set.all().order_by('move_time')
                inBag = [False] * 12
                for item in items:
                    if item.to_knapsack:
                        inBag[item.item_index] = True
                    elif item.from_knapsack:
                        inBag[item.item_index] = False
                # print ("seconds_to_reveal: " + str(seconds_to_reveal))
                context = {'username': username, 'capacity': userGame.game.capacity,
                           'value_0': userGame.game.value_0, 'weight_0': userGame.game.weight_0,
                           'inBag_0': inBag[0],
                           'value_1': userGame.game.value_1, 'weight_1': userGame.game.weight_1,
                           'inBag_1': inBag[1],
                           'value_2': userGame.game.value_2, 'weight_2': userGame.game.weight_2,
                           'inBag_2': inBag[2],
                           'value_3': userGame.game.value_3, 'weight_3': userGame.game.weight_3,
                           'inBag_3': inBag[3],
                           'value_4': userGame.game.value_4, 'weight_4': userGame.game.weight_4,
                           'inBag_4': inBag[4],
                           'value_5': userGame.game.value_5, 'weight_5': userGame.game.weight_5,
                           'inBag_5': inBag[5],
                           'value_6': userGame.game.value_6, 'weight_6': userGame.game.weight_6,
                           'inBag_6': inBag[6],
                           'value_7': userGame.game.value_7, 'weight_7': userGame.game.weight_7,
                           'inBag_7': inBag[7],
                           'value_8': userGame.game.value_8, 'weight_8': userGame.game.weight_8,
                           'inBag_8': inBag[8],
                           'value_9': userGame.game.value_9, 'weight_9': userGame.game.weight_9,
                           'inBag_9': inBag[9],
                           'value_10': userGame.game.value_10, 'weight_10': userGame.game.weight_10,
                           'inBag_10': inBag[10],
                           'value_11': userGame.game.value_11, 'weight_11': userGame.game.weight_11,
                           'inBag_11': inBag[11],
                           'max_seconds': seconds, 'max_minutes': minutes, 'seconds_to_reveal': seconds_to_reveal,
                           'minutes_to_reveal': minutes_to_reveal, 'winning_score': userGame.game.winning_score,
                           'optimal_score': userGame.game.optimal_score,
                           'no_information': userGame.game.no_information,
                           'intermediate_information': userGame.game.intermediate_information,
                           'complete_information': userGame.game.complete_information,
                           'userGameId': userGame.pk, 'gameNum': currentGameNum, 'userscores': userscores,
                           'totalGameNum': user.experiment.game_number, 'totalGameIndices': totalGameIndices,
                           'opponentsScores': opponentsScores, 'contestIndex': currentContestIndex,
                           'totalContestsNum': user.experiment.contest_number,
                           'quit_question_earning': quit_question_earning, }
                return render(request, 'knapsack/training.html', context)

        if currentGameNum < user.experiment.game_number:
            # print ("currentGameNum < user.experiment.game_number: " + str(currentGameNum < user.experiment.game_number))
            
            randomGameType = Gametype.objects.filter(for_contest=1).exclude(for_training=1)
            newGameDifficultyLevel = (currentContestIndex - 1) * user.experiment.game_number + currentGameNum + 1
            randomGameType = randomGameType.get(difficulty_level=newGameDifficultyLevel)
            difficulty = difficultyCalculator(randomGameType)
            optimal_score = OptimalSolutionFinder(randomGameType)
            gameObj = Game.objects.create(
                experiment=user.experiment,
                gametype=randomGameType,
                capacity=randomGameType.capacity,
                player_number=player_number,
                value_0=randomGameType.value_0,
                weight_0=randomGameType.weight_0,
                optimal_0=randomGameType.optimal_0,
                value_1=randomGameType.value_1,
                weight_1=randomGameType.weight_1,
                optimal_1=randomGameType.optimal_1,
                value_2=randomGameType.value_2,
                weight_2=randomGameType.weight_2,
                optimal_2=randomGameType.optimal_2,
                value_3=randomGameType.value_3,
                weight_3=randomGameType.weight_3,
                optimal_3=randomGameType.optimal_3,
                value_4=randomGameType.value_4,
                weight_4=randomGameType.weight_4,
                optimal_4=randomGameType.optimal_4,
                value_5=randomGameType.value_5,
                weight_5=randomGameType.weight_5,
                optimal_5=randomGameType.optimal_5,
                value_6=randomGameType.value_6,
                weight_6=randomGameType.weight_6,
                optimal_6=randomGameType.optimal_6,
                value_7=randomGameType.value_7,
                weight_7=randomGameType.weight_7,
                optimal_7=randomGameType.optimal_7,
                value_8=randomGameType.value_8,
                weight_8=randomGameType.weight_8,
                optimal_8=randomGameType.optimal_8,
                value_9=randomGameType.value_9,
                weight_9=randomGameType.weight_9,
                optimal_9=randomGameType.optimal_9,
                value_10=randomGameType.value_10,
                weight_10=randomGameType.weight_10,
                optimal_10=randomGameType.optimal_10,
                value_11=randomGameType.value_11,
                weight_11=randomGameType.weight_11,
                optimal_11=randomGameType.optimal_11,
                max_seconds=randomGameType.max_seconds,
                max_minutes=randomGameType.max_minutes,
                seconds_to_reveal=randomGameType.seconds_to_reveal,
                minutes_to_reveal=randomGameType.minutes_to_reveal,
                winning_score=randomGameType.winning_score,
                no_information=contestObj.no_information,
                intermediate_information=contestObj.intermediate_information,
                complete_information=contestObj.complete_information,
                optimal_score=optimal_score,
                difficulty=difficulty,
            )
            thisUserGame = None
            for playerUser in players:
                userGameObj = Usergame.objects.create(
                    user=playerUser,
                    game=gameObj,
                    started=timezone.now() + timedelta(seconds=3),
                    finished=timezone.now() + timedelta(seconds=3),
                )
                if user.pk == playerUser.pk and thisUserGame is None:
                    thisUserGame = userGameObj
                contestusergame = Contestusergame.objects.create(
                    contest=contestObj,
                    usergame=userGameObj,
                    score=0,
                )

            context = {'username': username, 'otherPlayers': otherPlayers,
                       'capacity': randomGameType.capacity,
                       'no_information': thisUserGame.game.no_information,
                       'intermediate_information': thisUserGame.game.intermediate_information,
                       'complete_information': thisUserGame.game.complete_information,
                       'value_0': randomGameType.value_0, 'weight_0': randomGameType.weight_0,
                       'value_1': randomGameType.value_1, 'weight_1': randomGameType.weight_1,
                       'value_2': randomGameType.value_2, 'weight_2': randomGameType.weight_2,
                       'value_3': randomGameType.value_3, 'weight_3': randomGameType.weight_3,
                       'value_4': randomGameType.value_4, 'weight_4': randomGameType.weight_4,
                       'value_5': randomGameType.value_5, 'weight_5': randomGameType.weight_5,
                       'value_6': randomGameType.value_6, 'weight_6': randomGameType.weight_6,
                       'value_7': randomGameType.value_7, 'weight_7': randomGameType.weight_7,
                       'value_8': randomGameType.value_8, 'weight_8': randomGameType.weight_8,
                       'value_9': randomGameType.value_9, 'weight_9': randomGameType.weight_9,
                       'value_10': randomGameType.value_10, 'weight_10': randomGameType.weight_10,
                       'value_11': randomGameType.value_11, 'weight_11': randomGameType.weight_11,
                       'max_seconds': randomGameType.max_seconds, 'max_minutes': randomGameType.max_minutes,
                       'seconds_to_reveal': seconds_to_reveal,
                       'minutes_to_reveal': minutes_to_reveal,
                       'userGameId': thisUserGame.pk, 'gameNum': 2,
                       'winning_score': thisUserGame.game.winning_score, 'optimal_score': optimal_score,
                       'totalGameNum': user.experiment.game_number, 'totalGameIndices': totalGameIndices,
                       'userscores': userscores, 'opponentsScores': opponentsScores,
                       'contestIndex': currentContestIndex, 'totalContestsNum': user.experiment.contest_number,
                       'quit_question_earning': quit_question_earning, }
            return render(request, 'knapsack/training.html', context)
        else:
            # print ("Contest " + str(currentContestIndex) + " Finished.")
            
            wonGamesNum = 0
            for userGame in userGames:
                if userGame.score >= userGame.game.winning_score:
                    wonGamesNum += 1
            if wonGamesNum == currentGameNum:
                for contestusergame in contestusergames:
                    contestusergame.score = round(user.experiment.contest_earning)
                    contestusergame.save()
            user.total_game_score = 0
            userContestGames = Contestusergame.objects.filter(usergame__user=user)
            for userContestGame in userContestGames:
                user.total_game_score += userContestGame.score
            user.total_game_score = math.ceil(user.total_game_score / 2)
            user.total_earning = math.ceil(user.total_game_score + user.quizscore + user.total_training_score +
                                                  user.quit_question_earning + 5)
            user.save()

            context = {'username': username, 'phase': 'game', 'quiz_score': round(user.quizscore, 2),
                       'quit_question_earning': round(user.quit_question_earning, 2),
                       'contestIndex': currentContestIndex, 'contestsNum': user.experiment.contest_number,
                       'total_game_score': round(user.total_game_score, 2),
                       'total_training_score': round(user.total_training_score, 2),
                       'total_earning': user.total_earning}
            if user.experiment.contest_number == currentContestIndex:
                context['phase'] = 'contest'
            return render(request, 'knapsack/results.html', context)
    return render(request, 'knapsack/training.html', context)


def gamestatus(request):
    context = {'username': ''}
    requestPost = json.loads(request.body.decode('utf-8'))
    if request.session.get('username', False):
        username = request.session['username']
        user = User.objects.get(username=username)
        currentuserGame = user.usergame_set.latest('created')
        contestusergameObj = Contestusergame.objects.get(usergame=currentuserGame)
        currentContestIndex = contestusergameObj.contest.index
        # print ("user.usergame_set.all(): " + str(user.usergame_set.all()))
        # print ("currentContestIndex: " + str(currentContestIndex))

        contestObj = contestusergameObj.contest
        contestusergames = Contestusergame.objects.filter(contest=contestObj, usergame__user=user).order_by('created')
        # print ("contestusergames.count(): " + str(contestusergames.count()))

        totalUserGames = user.usergame_set.count()
        player_number = user.experiment.player_number
        game_number = user.experiment.game_number
        players = User.objects.filter(usergame__game=currentuserGame.game)
        otherPlayers = players.exclude(username=username)
        # print ("players.count(): " + str(players.count()))
        # print ("otherPlayers.count(): " + str(otherPlayers.count()))

        userscores = []
        opponentsScoresTrans = []
        opponentsSecondsTrans = []
        opponentsQuitsTrans = []
        userGames = []
        gamesWinningScores = []
        for contestusergame in contestusergames:
            userGames.append(contestusergame.usergame)
            userscores.append(contestusergame.usergame.score)
            gamesWinningScores.append(contestusergame.usergame.game.winning_score)
            opponentsusergameScores = []
            opponentsusergameSeconds = []
            opponentsusergameQuits = []
            for otherPlayer in otherPlayers:
                otherUserGame = Usergame.objects.get(user=otherPlayer, game=contestusergame.usergame.game)
                opponentsusergameScores.append(otherUserGame.score)
                opponentsusergameSeconds.append((timezone.now() - otherUserGame.finished).total_seconds())
                opponentsusergameQuits.append(otherUserGame.quit)
            opponentsScoresTrans.append(opponentsusergameScores)
            opponentsSecondsTrans.append(opponentsusergameSeconds)
            opponentsQuitsTrans.append(opponentsusergameQuits)

        opponentsScores = transposeListOfLists(opponentsScoresTrans)
        opponentsSeconds = transposeListOfLists(opponentsSecondsTrans)
        opponentsQuits = transposeListOfLists(opponentsQuitsTrans)
        # print ("\n\nuserscores: " + str(userscores) + "\n\n")
        # print ("\n\nopponentsScoresTrans: " + str(opponentsScoresTrans) + "\n\n")
        # print ("\n\nopponentsScores: " + str(opponentsScores) + "\n\n")
        # print ("\n\ngamesWinningScores: " + str(gamesWinningScores) + "\n\n")

        # currentGameNum = len(userGames)
        # print ("currentGameNum: " + str(currentGameNum))
        # print ("game_number: " + str(game_number))

        opponentWonFirstGame = 0
        opponentJustWonFirstGame = 0
        opponentQuitFirstGame = 0
        opponentJustQuitFirstGame = 0
        youWonLastGame = 0
        opponentWonLastGame = 0
        for i in range(len(opponentsScores)):
            if opponentsScores[i][0] >= gamesWinningScores[0]:
                opponentWonFirstGame = 1
                if len(opponentsSeconds[i]) == 1 or opponentsSeconds[i][0] < 2:
                    opponentJustWonFirstGame = 1
                if game_number == len(opponentsScores[i]) and opponentsScores[i][-1] >= gamesWinningScores[-1]:
                    opponentWonLastGame = 1
                    currentuserGame.opponentWon = True
                    currentuserGame.save()
            if opponentsQuits[i][0] or (len(opponentsQuits[i]) == 2 and opponentsQuits[i][1]):
                opponentQuitFirstGame = 1
                if len(opponentsSeconds[i]) == 1 or opponentsSeconds[i][0] < 2 or opponentsSeconds[i][1] < 2:
                    opponentJustQuitFirstGame = 1

        if opponentWonLastGame == 0 and game_number == len(userscores) and userscores[-1] >= gamesWinningScores[-1]:
            youWonLastGame = 1
        youWon = 0
        thisUserGame = Usergame.objects.get(pk=requestPost['userGameId'])
        if thisUserGame.score >= thisUserGame.game.winning_score:
            youWon = 1
            thisUserGame.youWon = True
            thisUserGame.save()

        context = {'userscores': userscores, 'youWon': youWon, 'youWonLastGame': youWonLastGame,
                   'opponentWonFirstGame': opponentWonFirstGame,
                   'opponentJustWonFirstGame': opponentJustWonFirstGame,
                   'opponentQuitFirstGame': opponentQuitFirstGame,
                   'opponentJustQuitFirstGame': opponentJustQuitFirstGame,
                   'opponentWonLastGame': opponentWonLastGame,
                   'gamesWinningScores': gamesWinningScores, 'opponentsScores': opponentsScores,
                   'game_number': game_number}
        return JsonResponse(context)

    return render(request, 'knapsack/training.html', context)


def gamesubmit(request):
    if request.method == 'POST':
        requestPost = json.loads(request.body.decode('utf-8'))
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            usergame = Usergame.objects.get(pk=requestPost['userGameId'])
            usergame.finished = timezone.now()
            if 'item_index' in requestPost:
                usergameItems = Usergameitem.objects.filter(usergame=usergame, item_index=requestPost['item_index'])
                if requestPost['to_knapsack'] and len(usergameItems) % 2 == 0:
                    usergame.score += requestPost['item_value']
                    usergameItem = Usergameitem.objects.create(
                        usergame=usergame,
                        item_index=requestPost['item_index'],
                        to_knapsack=requestPost['to_knapsack'],
                        from_knapsack=requestPost['from_knapsack'],
                        move_time=timezone.now())
                elif requestPost['from_knapsack'] and len(usergameItems) % 2 == 1:
                    usergame.score -= requestPost['item_value']
                    usergameItem = Usergameitem.objects.create(
                        usergame=usergame,
                        item_index=requestPost['item_index'],
                        to_knapsack=requestPost['to_knapsack'],
                        from_knapsack=requestPost['from_knapsack'],
                        move_time=timezone.now())
            elif 'submitted' in requestPost:
                usergame.submitted = True
            usergame.save()
            return gamestatus(request)
    context = {'username': ''}
    return render(request, 'knapsack/training.html', context)


def quitoption(request):
    # print("\n\nEntered Quit option.")
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            quit_question_earning = user.experiment.quit_question_earning
            currentuserGame = Usergame.objects.get(pk=request.GET['userGameId'])
            currentuserGame.quit = True
            currentuserGame.finished = timezone.now()
            currentuserGame.save()
            context = {'username': username, 'userGameId': request.GET['userGameId'],
                       'quit_question_earning': quit_question_earning}
            return render(request, 'knapsack/QuitQuestions.html', context)
    # print("\n\nEntered the if part.")
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def quitquestion(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            quit_question_earning = user.experiment.quit_question_earning
            usergame = Usergame.objects.get(pk=request.GET['userGameId'])
            infeasibility = usergame.game.infeasible
            correct = False
            responseInfeasible = convertNum2Bool(request.GET['infeasible'])
            responseFeasible = convertNum2Bool(request.GET['feasible'])
            responseNotSure = convertNum2Bool(request.GET['notSure'])
            WasFeasibleNo = -1
            WasFeasibleYes = -1
            WasFeasibleNotSure = -1
            if infeasibility and responseInfeasible:
                correct = True
                user.quit_question_earning += 0.5
                user.save()
                WasFeasibleNo = 2
            elif (not infeasibility) and responseFeasible:
                correct = True
                user.quit_question_earning += 0.5
                user.save()
                WasFeasibleYes = 2
            elif infeasibility and responseFeasible:
                WasFeasibleYes = -2
                WasFeasibleNo = 1
            elif (not infeasibility) and responseInfeasible:
                WasFeasibleNo = -2
                WasFeasibleYes = 1
            elif responseNotSure:
                WasFeasibleNotSure = -2
                if infeasibility:
                    WasFeasibleNo = 1
                elif (not infeasibility):
                    WasFeasibleYes = 1
            userquitquestion = Userquitquestion.objects.create(
                user=user,
                usergame=usergame,
                why_quit=request.GET['WhyQuit'],
                feasible=responseFeasible,
                infeasible=responseInfeasible,
                notsure=responseNotSure,
                correct=correct)
            context = {'username': username, 'userGameId': request.GET['userGameId'], 'WasFeasibleYes': WasFeasibleYes,
                       'WasFeasibleNo': WasFeasibleNo,
                       'WasFeasibleNotSure': WasFeasibleNotSure, 'why_quit': request.GET['WhyQuit'],
                       'phase': 'quitquestion', 'quit_question_earning': quit_question_earning}
            return render(request, 'knapsack/QuitQuestions.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/training.html', context)


def survey(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            context = {'username': username, }
            return render(request, 'knapsack/Survey.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def convertNum2Bool(numObj):
    if numObj == 1 or numObj == "1" or numObj == "true" or numObj == "True":
        return True
    elif numObj == 0 or numObj == "0" or numObj == "false" or numObj == "False":
        return False


def surveysubmit(request):
    if request.method == 'POST':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)

            age = request.POST['age']
            male = request.POST['male']
            female = request.POST['female']
            siblings = request.POST['siblings']
            major = request.POST['major']
            undergraduate = request.POST['undergraduate']
            graduate = request.POST['graduate']
            notstudent = request.POST['notstudent']
            programyear = request.POST['programyear']
            participatedbefore = request.POST['participatedbefore']
            white = request.POST['white']
            asian = request.POST['asian']
            africanamerican = request.POST['africanamerican']
            hispanic = request.POST['hispanic']
            multiracial = request.POST['multiracial']
            nativeamerican = request.POST['nativeamerican']
            # caucasian = request.POST['caucasian']
            otherethnicity = request.POST['otherethnicity']
            stickopinion = request.POST['stickopinion']
            achievement = request.POST['achievement']
            changeopinion = request.POST['changeopinion']
            strategies = request.POST['strategies']

            # print ('\n\n\nage = ' + str(request.POST['age']) +
            # ' male = ' + str(request.POST['male']) +
            # ' female = ' + str(request.POST['female']) +
            # ' siblings = ' + str(request.POST['siblings']) +
            # ' major = ' + str(request.POST['major']) +
            # ' undergraduate = ' + str(request.POST['undergraduate']) +
            # ' graduate = ' + str(request.POST['graduate']) +
            # ' notstudent = ' + str(request.POST['notstudent']) +
            # ' programyear = ' + str(request.POST['programyear']) +
            # ' participatedbefore = ' + str(request.POST['participatedbefore']) +
            # ' white = ' + str(request.POST['white']) +
            # ' asian = ' + str(request.POST['asian']) +
            # ' africanamerican = ' + str(request.POST['africanamerican']) +
            # ' hispanic = ' + str(request.POST['hispanic']) +
            # ' multiracial = ' + str(request.POST['multiracial']) +
            # ' nativeamerican = ' + str(request.POST['nativeamerican']) +
            # ' caucasian = ' + str(request.POST['caucasian']) +
            # ' otherethnicity = ' + str(request.POST['otherethnicity']) +
            # ' stickopinion = ' + str(request.POST['stickopinion']) +
            # ' achievement = ' + str(request.POST['achievement']) +
            # ' changeopinion = ' + str(request.POST['changeopinion']) +
            # ' strategies = ' + str(request.POST['strategies']))

            user.age = age
            user.male = convertNum2Bool(male)
            user.female = convertNum2Bool(female)
            user.siblings = siblings
            user.major = major
            user.undergraduate = convertNum2Bool(undergraduate)
            user.graduate = convertNum2Bool(graduate)
            user.notstudent = convertNum2Bool(notstudent)
            user.programyear = programyear
            user.participatedbefore = convertNum2Bool(participatedbefore)
            user.white = convertNum2Bool(white)
            user.asian = convertNum2Bool(asian)
            user.africanamerican = convertNum2Bool(africanamerican)
            user.hispanic = convertNum2Bool(hispanic)
            user.multiracial = convertNum2Bool(multiracial)
            user.nativeamerican = convertNum2Bool(nativeamerican)
            # user.caucasian = convertNum2Bool(caucasian)
            user.otherethnicity = otherethnicity
            user.stickopinion = stickopinion
            user.achievement = achievement
            user.changeopinion = changeopinion
            user.strategies = strategies
            user.finished_study = timezone.now()
            user.total_earning = math.ceil(user.total_game_score + user.quizscore + user.total_training_score +
                                                  user.quit_question_earning + 5)
            user.save()

            context = {'username': username, 'phase': 'survey', 'quiz_score': round(user.quizscore, 2),
                       'quit_question_earning': round(user.quit_question_earning, 2),
                       'total_game_score': round(user.total_game_score, 2),
                       'total_training_score': round(user.total_training_score, 2),
                       'total_earning': user.total_earning}
            return render(request, 'knapsack/results.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def final(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            user = User.objects.get(username=username)
            context = {'username': username, 'phase': 'survey', 'quiz_score': round(user.quizscore, 2),
                       'quit_question_earning': round(user.quit_question_earning, 2),
                       'total_game_score': round(user.total_game_score, 2),
                       'total_training_score': round(user.total_training_score, 2),
                       'total_earning': math.ceil(user.total_game_score + user.quizscore + user.total_training_score +
                                                  user.quit_question_earning + 5)}
            return render(request, 'knapsack/results.html', context)
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def deletegamesofexperiment(request):
    if request.method == 'GET':
        if request.session.get('username', False):
            username = request.session['username']
            experimentVersion = int(request.GET['version'])
            experiment = Experiment.objects.get(vesion=experimentVersion)
            users = User.objects.filter(experiment=experiment)
            contests = Contest.objects.filter(experiment=experiment)
            games = Game.objects.filter(experiment=experiment)
            if users.count() == 0 and contests.count() == 0:
                games.delete()
                experiment.initializing = False
                experiment.group1_initializing = False
                experiment.group2_initializing = False
                experiment.group3_initializing = False
                experiment.group4_initializing = False
                experiment.save()
            return redirect('knapsack:logout')
    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def downloadCSV(request, part):
    if request.method == 'GET':
        """A view that streams a large CSV file."""
        # Generate a sequence of rows. The range is based on the maximum number of
        # rows that can be handled by a single sheet in most spreadsheet
        # applications.

        rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        rows = generateCSVDataset(part)

        response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                         content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="DynamicContest.csv"'
        return response

    context = {'username': ''}
    return render(request, 'knapsack/index.html', context)


def generateCSVDataset(part):
    rows = []
    experiment = Experiment.objects.get(vesion=2)
    if part == "Pilot2":
        headerRow = ['Experiment', 'Username', 'total_earning', 'total_training_score',
                     'total_game_score', 'started_study', 'finished_study', 'study_duration',
                     'age', 'male', 'female', 'siblings', 'major', 'undergraduate', 'graduate',
                     'notstudent', 'programyear', 'participatedbefore', 'white', 'asian',
                     'africanamerican', 'hispanic', 'multiracial', 'nativeamerican',
                     'otherethnicity', 'stickopinion', 'achievement', 'changeopinion', 'strategies', 'group', 'skill',
                     'Contest_Num', 'Game_Type', 'Game_Order', 'rival', 'gameID', 'gameSpecificationID', 'difficulty', 'score', '# of Moves',
                     'started', 'finished', 'game_duration', 'submitted', 'infeasible', 'infeasiblility 20%', 'infeasiblility 40%',
                     'no_information', 'intermediate_information', 'complete_information',
                     'Quit', 'Found_Traget', 'Opponent_Found_Traget']
        rows.append(headerRow)

        allUsers = User.objects.filter(experiment=experiment)

        for user in allUsers:
            if user.skill == 0:
                usersInExperiment = User.objects.filter(experiment=user.experiment)
                usersInExperimentNum = usersInExperiment.count()
                gameTypes = Gametype.objects.all()
                for gameType in gameTypes:
                    gameTypeMaxScoreRatio = 0
                    gameTypeMinScoreRatio = 0
                    for userInExperiment in usersInExperiment:
                        userTrainings = userInExperiment.usertraining_set.filter(game__gametype=gameType)
                        for userTraining in userTrainings:
                            userTrainingScoreRatio = 0
                            if (userTraining.finished - userTraining.started).seconds != 0:
                                userTrainingScoreRatio = userTraining.score / (userTraining.finished - userTraining.started).seconds
                                if gameTypeMaxScoreRatio < userTrainingScoreRatio:
                                    gameTypeMaxScoreRatio = userTrainingScoreRatio
                                if gameTypeMinScoreRatio > userTrainingScoreRatio:
                                    gameTypeMinScoreRatio = userTrainingScoreRatio
                    gameType.max_score_ratio = gameTypeMaxScoreRatio
                    gameType.min_score_ratio = gameTypeMinScoreRatio
                    for userInExperiment in usersInExperiment:
                        userTrainings = userInExperiment.usertraining_set.filter(game__gametype=gameType)
                        for userTraining in userTrainings:
                            userTrainingScoreRatio = 0
                            if (userTraining.finished - userTraining.started).seconds != 0:
                                userTrainingScoreRatio = userTraining.score / (userTraining.finished - userTraining.started).seconds
                            if (gameType.max_score_ratio - gameType.min_score_ratio) != 0:
                                userInExperiment.skill += (userTrainingScoreRatio - gameType.min_score_ratio) / (gameType.max_score_ratio - gameType.min_score_ratio)
                                userInExperiment.save()

            usertrainingsCount = user.usertraining_set.count()
            if usertrainingsCount != 0:
                usertrainings = user.usertraining_set.all()
                for usertraining in usertrainings:
                    row = [user.experiment.vesion]
                    row.append(user.username)
                    row.append(math.ceil(user.total_game_score + user.total_training_score + 5))
                    row.append(user.total_training_score)
                    row.append(user.total_game_score)
                    row.append(user.started_study)
                    row.append(user.finished_study)
                    row.append((user.finished_study - user.started_study).total_seconds())
                    row.append(user.age)
                    row.append(int(user.male))
                    row.append(int(user.female))
                    row.append(user.siblings)
                    row.append(user.major)
                    row.append(int(user.undergraduate))
                    row.append(int(user.graduate))
                    row.append(int(user.notstudent))
                    row.append(user.programyear)
                    row.append(int(user.participatedbefore))
                    row.append(int(user.white))
                    row.append(int(user.asian))
                    row.append(int(user.africanamerican))
                    row.append(int(user.hispanic))
                    row.append(int(user.multiracial))
                    row.append(int(user.nativeamerican))
                    # row.append(user.caucasian)
                    row.append(user.otherethnicity)
                    row.append(user.stickopinion)
                    row.append(user.achievement)
                    row.append(user.changeopinion)
                    row.append(user.strategies)
                    row.append(user.group)
                    row.append(user.skill)
                    contestusertrainings = usertraining.contestusertraining_set.all()
                    if len(contestusertrainings) == 0:
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(usertraining.game.pk)
                        row.append(usertraining.game.gametype.pk)
                        row.append(usertraining.game.gametype.difficulty)
                        row.append(usertraining.score)
                        row.append(usertraining.usertrainingitem_set.count())
                        row.append(usertraining.started)
                        row.append(usertraining.finished)
                        row.append((usertraining.finished - usertraining.started).total_seconds())
                        row.append(int(usertraining.submitted))
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        rows.append(row)
                    else:
                        contestusertraining = contestusertrainings[0]
                        row.append(contestusertraining.contest.index)
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        row.append(contestusertraining.usertraining.game.pk)
                        row.append(contestusertraining.usertraining.game.gametype.pk)
                        row.append(contestusertraining.usertraining.game.gametype.difficulty)
                        row.append(contestusertraining.usertraining.score)
                        row.append(contestusertraining.usertraining.usertrainingitem_set.count())
                        row.append(contestusertraining.usertraining.started)
                        row.append(contestusertraining.usertraining.finished)
                        row.append((contestusertraining.usertraining.finished - contestusertraining.usertraining.started).total_seconds())
                        row.append(int(contestusertraining.usertraining.submitted))
                        row.append(int(contestusertraining.contest.infeasible))
                        row.append(int(contestusertraining.contest.infeasiblility20Percent))
                        row.append(int(contestusertraining.contest.infeasiblility40Percent))
                        row.append(int(contestusertraining.contest.no_information))
                        row.append(int(contestusertraining.contest.intermediate_information))
                        row.append(int(contestusertraining.contest.complete_information))
                        row.append(0)
                        row.append(0)
                        row.append(0)
                        rows.append(row)

            contestusergames = Contestusergame.objects.filter(usergame__user=user)
            contestusergamesCount = contestusergames.count()
            if contestusergamesCount != 0:
                for contestusergame in contestusergames:
                    row = [user.experiment.vesion]
                    row.append(user.username)
                    row.append(math.ceil(user.total_game_score + user.total_training_score + 5))
                    row.append(user.total_training_score)
                    row.append(user.total_game_score)
                    row.append(user.started_study)
                    row.append(user.finished_study)
                    row.append((user.finished_study - user.started_study).total_seconds())
                    row.append(user.age)
                    row.append(int(user.male))
                    row.append(int(user.female))
                    row.append(user.siblings)
                    row.append(user.major)
                    row.append(int(user.undergraduate))
                    row.append(int(user.graduate))
                    row.append(int(user.notstudent))
                    row.append(user.programyear)
                    row.append(int(user.participatedbefore))
                    row.append(int(user.white))
                    row.append(int(user.asian))
                    row.append(int(user.africanamerican))
                    row.append(int(user.hispanic))
                    row.append(int(user.multiracial))
                    row.append(int(user.nativeamerican))
                    # row.append(user.caucasian)
                    row.append(user.otherethnicity)
                    row.append(user.stickopinion)
                    row.append(user.achievement)
                    row.append(user.changeopinion)
                    row.append(user.strategies)
                    row.append(user.group)
                    row.append(user.skill)
                    contest = contestusergame.contest
                    row.append(contest.index)
                    row.append(1)
                    usergame = contestusergame.usergame
                    game = usergame.game
                    othercontestusergames = contest.contestusergame_set.all()
                    othergames = []
                    for othercontestusergame in othercontestusergames:
                        if othercontestusergame.usergame.game not in othergames:
                            othergames.append(othercontestusergame.usergame.game)
                    gameOrder = 0
                    for othergame in othergames:
                        if othergame.updated < game.updated:
                            gameOrder += 1
                    row.append(gameOrder)
                    sameUsergames = Usergame.objects.filter(game=game)
                    for sameUsergame in sameUsergames:
                        if sameUsergame != usergame:
                            row.append(sameUsergame.user.username)
                    row.append(game.pk)
                    row.append(game.gametype.pk)
                    row.append(game.gametype.difficulty)
                    row.append(usergame.score)
                    row.append(usergame.usergameitem_set.count())
                    row.append(usergame.started)
                    row.append(usergame.finished)
                    row.append((usergame.finished - usergame.started).total_seconds())
                    row.append(int(usergame.submitted))
                    row.append(int(contest.infeasible))
                    row.append(int(contest.infeasiblility20Percent))
                    row.append(int(contest.infeasiblility40Percent))
                    row.append(int(contest.no_information))
                    row.append(int(contest.intermediate_information))
                    row.append(int(contest.complete_information))
                    row.append(int(usergame.quit))
                    row.append(int(usergame.youWon))
                    row.append(int(usergame.opponentWon))
                    rows.append(row)

    elif part == "Pilot2Items":
        headerRow = ['Username', 'gameID', 'item_index',
                     'to_knapsack', 'from_knapsack', 'move_time']
        rows.append(headerRow)

        usertrainingitems = Usertrainingitem.objects.filter(usertraining__user__experiment=experiment)
        for usertrainingitem in usertrainingitems:
            row = []
            row.append(usertrainingitem.usertraining.user.username)
            row.append(usertrainingitem.usertraining.game.pk)
            row.append(usertrainingitem.item_index)
            row.append(int(usertrainingitem.to_knapsack))
            row.append(int(usertrainingitem.from_knapsack))
            row.append(usertrainingitem.move_time)
            rows.append(row)

        usergameitems = Usergameitem.objects.filter(usergame__user__experiment=experiment)
        for usergameitem in usergameitems:
            row = []
            row.append(usergameitem.usergame.user.username)
            row.append(usergameitem.usergame.game.pk)
            row.append(usergameitem.item_index)
            row.append(int(usergameitem.to_knapsack))
            row.append(int(usergameitem.from_knapsack))
            row.append(usergameitem.move_time)
            rows.append(row)

    elif part == "Pilot2GameSpecifications":
        headerRow = ['gameTypeID', 'capacity', 'value_0', 'weight_0', 'optimal_0',
                     'value_1', 'weight_1', 'optimal_1', 'value_2', 'weight_2', 'optimal_2',
                     'value_3', 'weight_3', 'optimal_3', 'value_4', 'weight_4', 'optimal_4',
                     'value_5', 'weight_5', 'optimal_5', 'value_6', 'weight_6', 'optimal_6',
                     'value_7', 'weight_7', 'optimal_7', 'value_8', 'weight_8', 'optimal_8',
                     'value_9', 'weight_9', 'optimal_9', 'value_10', 'weight_10', 'optimal_10',
                     'value_11', 'weight_11', 'optimal_11', 'difficulty_level', 'contest_index',
                     'difficulty', 'seconds_to_reveal', 'minutes_to_reveal', 'winning_score']
        rows.append(headerRow)

        gametypes = Gametype.objects.all()
        for gametype in gametypes:
            row = []
            row.append(gametype.pk)
            row.append(gametype.capacity)
            row.append(gametype.value_0)
            row.append(gametype.weight_0)
            row.append(int(gametype.optimal_0))
            row.append(gametype.value_1)
            row.append(gametype.weight_1)
            row.append(int(gametype.optimal_1))
            row.append(gametype.value_2)
            row.append(gametype.weight_2)
            row.append(int(gametype.optimal_2))
            row.append(gametype.value_3)
            row.append(gametype.weight_3)
            row.append(int(gametype.optimal_3))
            row.append(gametype.value_4)
            row.append(gametype.weight_4)
            row.append(int(gametype.optimal_4))
            row.append(gametype.value_5)
            row.append(gametype.weight_5)
            row.append(int(gametype.optimal_5))
            row.append(gametype.value_6)
            row.append(gametype.weight_6)
            row.append(int(gametype.optimal_6))
            row.append(gametype.value_7)
            row.append(gametype.weight_7)
            row.append(int(gametype.optimal_7))
            row.append(gametype.value_8)
            row.append(gametype.weight_8)
            row.append(int(gametype.optimal_8))
            row.append(gametype.value_9)
            row.append(gametype.weight_9)
            row.append(int(gametype.optimal_9))
            row.append(gametype.value_10)
            row.append(gametype.weight_10)
            row.append(int(gametype.optimal_10))
            row.append(gametype.value_11)
            row.append(gametype.weight_11)
            row.append(int(gametype.optimal_11))
            row.append(gametype.difficulty_level)
            row.append(gametype.contest_index)
            row.append(gametype.difficulty)
            row.append(gametype.seconds_to_reveal)
            row.append(gametype.minutes_to_reveal)
            row.append(gametype.winning_score)
            rows.append(row)

    return rows
