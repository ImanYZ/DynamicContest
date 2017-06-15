from django.contrib import admin

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


class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['vesion', 'training_number', 'contest_number', 'game_number', 'player_number',
                    'training_earning', 'contest_earning', 'training_contest_earning',
                    'game_max_minutes', 'game_max_seconds', 'game_minutes_to_reveal',
                    'game_seconds_to_reveal', 'total_minutes', 'total_seconds',
                    'total_training_minutes', 'total_training_seconds', 'initializing',
                    'group1_initializing', 'group2_initializing', 'group3_initializing', 'group4_initializing',
                    'no_information', 'intermediate_information', 'complete_information',
                    'infeasibility_chance', 'created', 'updated']

    search_fields = ['vesion']

admin.site.register(Experiment, ExperimentAdmin)


class GametypeAdmin(admin.ModelAdmin):
    list_display = ['experiment', 'capacity', 'value_0', 'weight_0', 'optimal_0',
                    'value_1', 'weight_1', 'optimal_1', 'value_2', 'weight_2', 'optimal_2',
                    'value_3', 'weight_3', 'optimal_3', 'value_4', 'weight_4', 'optimal_4',
                    'value_5', 'weight_5', 'optimal_5', 'value_6', 'weight_6', 'optimal_6',
                    'value_7', 'weight_7', 'optimal_7', 'value_8', 'weight_8', 'optimal_8',
                    'value_9', 'weight_9', 'optimal_9', 'value_10', 'weight_10', 'optimal_10',
                    'value_11', 'weight_11', 'optimal_11', 'for_training', 'for_contest', 'difficulty_level',
                    'contest_index', 'difficulty', 'max_seconds', 'max_minutes', 'winning_score', 'max_score_ratio',
                    'min_score_ratio', 'seconds_to_reveal', 'minutes_to_reveal', 'created', 'updated']

    search_fields = ['capacity']
    readonly_fields = ('id', )

admin.site.register(Gametype, GametypeAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['experiment', 'username', 'total_training_score', 'skill', 'group', 'total_game_score',
                    'waiting_for_game', 'started_training', 'finished_training', 'started_study', 'finished_study',
                    'age', 'male', 'female', 'siblings', 'major', 'undergraduate', 'graduate', 'notstudent',
                    'programyear', 'participatedbefore', 'white', 'asian', 'africanamerican', 'hispanic',
                    'multiracial', 'nativeamerican', 'caucasian', 'otherethnicity', 'stickopinion',
                    'achievement', 'changeopinion', 'strategies', 'GroupSize3', 'GroupSize4', 'GroupSize12',
                    'GroupSizeNotSure', 'SameOpponentYes', 'SameOpponentNo', 'SameOpponentNotSure',
                    'InfeasibleIsSolvableTrue', 'InfeasibleIsSolvableFalse', 'InfeasibleIsSolvableNotSure',
                    'SureGameTrue', 'SureGameFalse', 'SureGameNotSure', 'Feasible60Infeasible40', 'Feasible60Target40',
                    'Feasible60NotSure', 'quizscore', 'quit_question_earning',
                    'created', 'updated']

    search_fields = ['experiment__capacity', 'username']

admin.site.register(User, UserAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ['experiment', 'gametype', 'capacity', 'player_number', 'infeasible',
                    'infeasiblility20Percent', 'infeasiblility40Percent', 'value_0', 'weight_0', 'optimal_0',
                    'value_1', 'weight_1', 'optimal_1', 'value_2', 'weight_2', 'optimal_2',
                    'value_3', 'weight_3', 'optimal_3', 'value_4', 'weight_4', 'optimal_4',
                    'value_5', 'weight_5', 'optimal_5', 'value_6', 'weight_6', 'optimal_6',
                    'value_7', 'weight_7', 'optimal_7', 'value_8', 'weight_8', 'optimal_8',
                    'value_9', 'weight_9', 'optimal_9', 'value_10', 'weight_10', 'optimal_10',
                    'value_11', 'weight_11', 'optimal_11',
                    'max_seconds', 'max_minutes', 'winning_score', 'optimal_score', 'difficulty',
                    'no_information', 'intermediate_information', 'complete_information',
                    'seconds_to_reveal', 'minutes_to_reveal', 'created', 'updated']

    search_fields = ['capacity', 'player_number']

admin.site.register(Game, GameAdmin)


class UsertrainingAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'score', 'started',
                    'finished', 'submitted', 'created', 'updated']

    search_fields = ['user', 'game']

admin.site.register(Usertraining, UsertrainingAdmin)


class UsertrainingitemAdmin(admin.ModelAdmin):
    list_display = ['usertraining', 'item_index', 'to_knapsack',
                    'from_knapsack', 'move_time', 'created', 'updated']

    search_fields = ['usertraining']

admin.site.register(Usertrainingitem, UsertrainingitemAdmin)


class UsergameAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'score', 'youWon', 'opponentWon',
                    'started', 'finished', 'submitted', 'quit',
                    'created', 'updated']

    search_fields = ['user', 'game']

admin.site.register(Usergame, UsergameAdmin)


class UsergameitemAdmin(admin.ModelAdmin):
    list_display = ['usergame', 'item_index', 'to_knapsack',
                    'from_knapsack', 'move_time', 'created', 'updated']

    search_fields = ['usergame']

admin.site.register(Usergameitem, UsergameitemAdmin)


class ContestAdmin(admin.ModelAdmin):
    list_display = ['experiment', 'index', 'no_information', 'intermediate_information',
                    'complete_information',  'infeasible', 'infeasiblility20Percent',
                    'infeasiblility40Percent', 'created', 'updated']

    search_fields = ['experiment']

admin.site.register(Contest, ContestAdmin)


class ContestusertrainingAdmin(admin.ModelAdmin):
    list_display = ['contest', 'usertraining',
                    'score', 'created', 'updated']

    search_fields = ['usertraining']

admin.site.register(Contestusertraining, ContestusertrainingAdmin)


class ContestusergameAdmin(admin.ModelAdmin):
    list_display = ['contest', 'usergame',
                    'score', 'created', 'updated']

    search_fields = ['usergame']

admin.site.register(Contestusergame, ContestusergameAdmin)


class UserquitquestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'usergame',
                    'why_quit', 'feasible', 'infeasible', 'correct', 'notsure', 'created', 'updated']

    search_fields = ['usergame']

admin.site.register(Userquitquestion, UserquitquestionAdmin)

