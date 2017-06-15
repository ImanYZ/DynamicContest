import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # only if you need to support Python 2
class Experiment(models.Model):
    vesion = models.IntegerField(default=0)
    training_number = models.IntegerField(default=0)
    contest_number = models.IntegerField(default=0)
    game_number = models.IntegerField(default=0)
    player_number = models.IntegerField(default=0)
    training_earning = models.FloatField(default=1)
    contest_earning = models.FloatField(default=5)
    quit_question_earning = models.FloatField(default=0.5)
    quiz_question_earning = models.FloatField(default=0.2)
    training_contest_earning = models.FloatField(default=1)
    game_max_minutes = models.IntegerField(default=0)
    game_max_seconds = models.IntegerField(default=0)
    game_minutes_to_reveal = models.IntegerField(default=0)
    game_seconds_to_reveal = models.IntegerField(default=0)
    total_minutes = models.IntegerField(default=0)
    total_seconds = models.IntegerField(default=0)
    total_training_minutes = models.IntegerField(default=0)
    total_training_seconds = models.IntegerField(default=0)
    initializing = models.BooleanField(default=False)
    group1_initializing = models.BooleanField(default=False)
    group2_initializing = models.BooleanField(default=False)
    group3_initializing = models.BooleanField(default=False)
    group4_initializing = models.BooleanField(default=False)
    infeasibility_chance = models.IntegerField(default=50)
    no_information = models.BooleanField(default=False)
    intermediate_information = models.BooleanField(default=False)
    complete_information = models.BooleanField(default=False)


    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Vesion: " + str(self.vesion)


@python_2_unicode_compatible  # only if you need to support Python 2
class Gametype(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    value_0 = models.IntegerField(default=0)
    weight_0 = models.IntegerField(default=0)
    optimal_0 = models.BooleanField(default=False)
    value_1 = models.IntegerField(default=0)
    weight_1 = models.IntegerField(default=0)
    optimal_1 = models.BooleanField(default=False)
    value_2 = models.IntegerField(default=0)
    weight_2 = models.IntegerField(default=0)
    optimal_2 = models.BooleanField(default=False)
    value_3 = models.IntegerField(default=0)
    weight_3 = models.IntegerField(default=0)
    optimal_3 = models.BooleanField(default=False)
    value_4 = models.IntegerField(default=0)
    weight_4 = models.IntegerField(default=0)
    optimal_4 = models.BooleanField(default=False)
    value_5 = models.IntegerField(default=0)
    weight_5 = models.IntegerField(default=0)
    optimal_5 = models.BooleanField(default=False)
    value_6 = models.IntegerField(default=0)
    weight_6 = models.IntegerField(default=0)
    optimal_6 = models.BooleanField(default=False)
    value_7 = models.IntegerField(default=0)
    weight_7 = models.IntegerField(default=0)
    optimal_7 = models.BooleanField(default=False)
    value_8 = models.IntegerField(default=0)
    weight_8 = models.IntegerField(default=0)
    optimal_8 = models.BooleanField(default=False)
    value_9 = models.IntegerField(default=0)
    weight_9 = models.IntegerField(default=0)
    optimal_9 = models.BooleanField(default=False)
    value_10 = models.IntegerField(default=0)
    weight_10 = models.IntegerField(default=0)
    optimal_10 = models.BooleanField(default=False)
    value_11 = models.IntegerField(default=0)
    weight_11 = models.IntegerField(default=0)
    optimal_11 = models.BooleanField(default=False)

    for_training = models.BooleanField(default=False)
    for_contest = models.BooleanField(default=False)
    difficulty_level = models.IntegerField(default=0)
    contest_index = models.IntegerField(default=0)
    difficulty = models.FloatField(default=0)
    max_seconds = models.IntegerField(default=0)
    max_minutes = models.IntegerField(default=0)
    seconds_to_reveal = models.IntegerField(default=0)
    minutes_to_reveal = models.IntegerField(default=0)
    winning_score = models.FloatField(default=0)
    max_score_ratio = models.FloatField(default=0)
    min_score_ratio = models.FloatField(default=0)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.capacity)


@python_2_unicode_compatible  # only if you need to support Python 2
class User(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    username = models.CharField(max_length=400)
    total_training_score = models.FloatField(default=0)
    skill = models.FloatField(default=0)
    group = models.IntegerField(default=0)
    total_game_score = models.FloatField(default=0)
    quit_question_earning = models.FloatField(default=0)
    quiz_earning = models.FloatField(default=0)
    waiting_for_game = models.BooleanField(default=False)

    started_training = models.DateTimeField(default=timezone.now)
    finished_training = models.DateTimeField(default=timezone.now)
    started_study = models.DateTimeField(default=timezone.now)
    finished_study = models.DateTimeField(default=timezone.now)

    age = models.IntegerField(default=-1)
    male = models.BooleanField(default=False)
    female = models.BooleanField(default=False)
    siblings = models.IntegerField(default=-1)
    major = models.CharField(max_length=127, default="")
    undergraduate = models.BooleanField(default=False)
    graduate = models.BooleanField(default=False)
    notstudent = models.BooleanField(default=False)
    programyear = models.IntegerField(default=-1)
    participatedbefore = models.BooleanField(default=False)
    white = models.BooleanField(default=False)
    asian = models.BooleanField(default=False)
    africanamerican = models.BooleanField(default=False)
    hispanic = models.BooleanField(default=False)
    multiracial = models.BooleanField(default=False)
    nativeamerican = models.BooleanField(default=False)
    caucasian = models.BooleanField(default=False)
    otherethnicity = models.CharField(max_length=127, default="")
    stickopinion = models.IntegerField(default=-1)
    achievement = models.IntegerField(default=-1)
    changeopinion = models.IntegerField(default=-1)
    strategies = models.TextField(null=True, blank=True)

    GroupSize3 = models.BooleanField(default=False)
    GroupSize4 = models.BooleanField(default=False)
    GroupSize12 = models.BooleanField(default=False)
    GroupSizeNotSure = models.BooleanField(default=False)
    SameOpponentYes = models.BooleanField(default=False)
    SameOpponentNo = models.BooleanField(default=False)
    SameOpponentNotSure = models.BooleanField(default=False)
    InfeasibleIsSolvableTrue = models.BooleanField(default=False)
    InfeasibleIsSolvableFalse = models.BooleanField(default=False)
    InfeasibleIsSolvableNotSure = models.BooleanField(default=False)
    SureGameTrue = models.BooleanField(default=False)
    SureGameFalse = models.BooleanField(default=False)
    SureGameNotSure = models.BooleanField(default=False)
    Feasible60Infeasible40 = models.BooleanField(default=False)
    Feasible60Target40 = models.BooleanField(default=False)
    Feasible60NotSure = models.BooleanField(default=False)
    quizscore = models.FloatField(default=0)
    quit_question_earning = models.FloatField(default=0)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.username)


@python_2_unicode_compatible  # only if you need to support Python 2
class Game(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    gametype = models.ForeignKey(Gametype, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(default=0)
    player_number = models.IntegerField(default=0)
    infeasiblility20Percent = models.BooleanField(default=False)
    infeasiblility40Percent = models.BooleanField(default=False)
    infeasible = models.BooleanField(default=False)

    value_0 = models.IntegerField(default=0)
    weight_0 = models.IntegerField(default=0)
    optimal_0 = models.BooleanField(default=False)
    value_1 = models.IntegerField(default=0)
    weight_1 = models.IntegerField(default=0)
    optimal_1 = models.BooleanField(default=False)
    value_2 = models.IntegerField(default=0)
    weight_2 = models.IntegerField(default=0)
    optimal_2 = models.BooleanField(default=False)
    value_3 = models.IntegerField(default=0)
    weight_3 = models.IntegerField(default=0)
    optimal_3 = models.BooleanField(default=False)
    value_4 = models.IntegerField(default=0)
    weight_4 = models.IntegerField(default=0)
    optimal_4 = models.BooleanField(default=False)
    value_5 = models.IntegerField(default=0)
    weight_5 = models.IntegerField(default=0)
    optimal_5 = models.BooleanField(default=False)
    value_6 = models.IntegerField(default=0)
    weight_6 = models.IntegerField(default=0)
    optimal_6 = models.BooleanField(default=False)
    value_7 = models.IntegerField(default=0)
    weight_7 = models.IntegerField(default=0)
    optimal_7 = models.BooleanField(default=False)
    value_8 = models.IntegerField(default=0)
    weight_8 = models.IntegerField(default=0)
    optimal_8 = models.BooleanField(default=False)
    value_9 = models.IntegerField(default=0)
    weight_9 = models.IntegerField(default=0)
    optimal_9 = models.BooleanField(default=False)
    value_10 = models.IntegerField(default=0)
    weight_10 = models.IntegerField(default=0)
    optimal_10 = models.BooleanField(default=False)
    value_11 = models.IntegerField(default=0)
    weight_11 = models.IntegerField(default=0)
    optimal_11 = models.BooleanField(default=False)

    max_seconds = models.IntegerField(default=0)
    max_minutes = models.IntegerField(default=0)
    seconds_to_reveal = models.IntegerField(default=0)
    minutes_to_reveal = models.IntegerField(default=0)
    winning_score = models.FloatField(default=0)
    optimal_score = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    no_information = models.BooleanField(default=False)
    intermediate_information = models.BooleanField(default=False)
    complete_information = models.BooleanField(default=False)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.capacity)


@python_2_unicode_compatible  # only if you need to support Python 2
class Usertraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    score = models.FloatField(default=0)
    started = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(default=timezone.now)
    submitted = models.BooleanField(default=False)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "User: " + str(self.user.username) + ", training: " + str(self.game)


@python_2_unicode_compatible  # only if you need to support Python 2
class Usertrainingitem(models.Model):
    usertraining = models.ForeignKey(Usertraining, on_delete=models.CASCADE)

    item_index = models.IntegerField(default=0)
    to_knapsack = models.BooleanField(default=False)
    from_knapsack = models.BooleanField(default=False)
    move_time = models.DateTimeField(default=timezone.now)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.usertraining) + ", item: " + str(self.item_index)


@python_2_unicode_compatible  # only if you need to support Python 2
class Usergame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    score = models.FloatField(default=0)
    started = models.DateTimeField(default=timezone.now)
    finished = models.DateTimeField(default=timezone.now)
    submitted = models.BooleanField(default=False)
    quit = models.BooleanField(default=False)
    youWon = models.BooleanField(default=False)
    opponentWon = models.BooleanField(default=False)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Game: " + str(self.game) + ", User: " + str(self.user)


@python_2_unicode_compatible  # only if you need to support Python 2
class Usergameitem(models.Model):
    usergame = models.ForeignKey(Usergame, on_delete=models.CASCADE)

    item_index = models.IntegerField(default=0)
    to_knapsack = models.BooleanField(default=False)
    from_knapsack = models.BooleanField(default=False)
    move_time = models.DateTimeField(default=timezone.now)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.usergame) + ", item: " + str(self.item_index)


@python_2_unicode_compatible  # only if you need to support Python 2
class Contest(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True)
    index = models.IntegerField(default=0)

    no_information = models.BooleanField(default=False)
    intermediate_information = models.BooleanField(default=False)
    complete_information = models.BooleanField(default=False)
    infeasiblility20Percent = models.BooleanField(default=False)
    infeasiblility40Percent = models.BooleanField(default=False)
    infeasible = models.BooleanField(default=False)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.index)


@python_2_unicode_compatible  # only if you need to support Python 2
class Contestusertraining(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    usertraining = models.ForeignKey(Usertraining, on_delete=models.CASCADE)

    score = models.FloatField(default=0)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Usertraining: " + str(self.usertraining)


@python_2_unicode_compatible  # only if you need to support Python 2
class Contestusergame(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    usergame = models.ForeignKey(Usergame, on_delete=models.CASCADE)

    score = models.FloatField(default=0)

    # auto_now_add=True means it will return the date and time when the user signedup,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Usergame: " + str(self.usergame)


@python_2_unicode_compatible  # only if you need to support Python 2
class Userquitquestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usergame = models.ForeignKey(Usergame, on_delete=models.CASCADE)

    why_quit = models.TextField(null=True, blank=True)
    feasible = models.BooleanField(default=False)
    infeasible = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)
    notsure = models.BooleanField(default=False)

    # auto_now_add=True means it will return the date and time when the user signed up,
    # and auto_now means it will return the date and time when it's updated.
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "User: " + str(self.user.username) + ", usergame: " + str(self.usergame)


