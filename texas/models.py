from django.db import models
from django.contrib.auth.models import User

import texas.constants as constants

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT)
    picture = models.ImageField(blank = True)
#     rank = models.CharField(max_length = 10, blank = True)
    rank = models.IntegerField()
    content_type = models.CharField(max_length = 50, blank = True)
    tokens = models.IntegerField(editable = True)
    def __str__(self):
        return self.user

# room model
class Room(models.Model):
    game = models.CharField(max_length=50, blank=True) # This should be a Game model in the future.
    gameStart = models.IntegerField(default=constants.NOTREADY) # if all users ready, then start the game

    #game fields
    round = models.IntegerField(default=constants.ROUND[0]) # record the betting round (preflop/flop/turn/river)
    player_to_bet_id = models.IntegerField(null=True) # the player waiting to bet
    community_card = models.CharField(max_length=15, default='') # String denoting the community cards
    dealer_id = models.IntegerField(default=0) # int of user id of the deal
    small_blind_id = models.IntegerField(default=0) # user id of the small blind
    big_blind_id = models.IntegerField(default=0) # user id of the big blind
    highest_bet = models.IntegerField(default=0) # current highest bet amount
    pot = models.IntegerField(default=0) # current pot amount
    won = models.BooleanField(default=False) # if one player has won the game
    players_ready = models.IntegerField(default=0)
    winner_id = models.IntegerField(null=True)
    reward = models.IntegerField(default=0)
    display_card = models.BooleanField(default=True)

# user room information
class User_Room(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    # not ready, ready, in game
    status = models.IntegerField(default=constants.NOTREADY)

    # player fields
    role = models.IntegerField(default=constants.ROLE[0]) # -1: no role, 0: dealer, 1: small blind, 2: big blind
    cards_holding = models.CharField(max_length=10, default='') # string denoting cards holding on hand
    chips = models.IntegerField(default=100) # the amount of chips holding
    bet = models.IntegerField(default=0) # the amount of bet now
    last_choice = models.CharField(max_length=10, default='not') # indicate the last choice of player (call/check/raise/fold)
    # folded = models.BooleanField(default=False) # if the player folded at this time
    # allin = models.BooleanField(default=False) # if the player plays all in at this time
    buttons = models.IntegerField(default=constants.BUTTON[0])
    allin = models.BooleanField(default=False)
    folded = models.BooleanField(default=False)