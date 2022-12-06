from django.shortcuts import render
from texas.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import Storage

from django.utils import timezone 

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden

import json

import random

import texas.poker as poker

from django.views.decorators.csrf import csrf_exempt

import traceback

# Create your views here.
def access_main(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'texas/main_page.html', context)

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

def profile_action(request):
    context={}
    return render(request, 'texas/profile.html', context)

@login_required
def my_profile(request):
    if request.method=="GET":
        context= {'profile': request.user.profile, "form": ProfileForm(initial = {'tokens': request.user.profile.tokens})}
        return render(request, 'texas/profile.html', context)

    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        print('error occurred!')
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'texas/profile.html', context)

    pic = form.cleaned_data['picture']
    print('Upload picture {} (type={}) succefully'.format(pic, type(pic)))
    profile = request.user.profile
    profile.picture = pic
#     profile.tokens = form.cleaned_data['tokens']
    profile.content_type = form.cleaned_data['picture'].content_type
    profile.save()
    context = {'profile': request.user.profile, 'form': ProfileForm()}
    return render(request, 'texas/profile.html', context)

@login_required
def my_profile_name(request):
    if request.method=="GET":
        context= {'profile': request.user.profile, "form": UsernameForm()}
        return render(request, 'texas/profile_name.html', context)

    form = UsernameForm(request.POST, request.FILES)
    if not form.is_valid():
        print('error occurred!')
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'texas/profile_name.html', context)

    username = form.cleaned_data['username']
    request.user.username=username

    request.user.save()
    context = {'profile': request.user.profile, 'form': UsernameForm()}
    return redirect(reverse('profile'))

@login_required
def my_profile_token(request):
    if request.method=="GET":
        context= {'profile': request.user.profile, "form": tokensAddForm()}
        return render(request, 'texas/profile_token.html', context)

    form = tokensAddForm(request.POST, request.FILES)
    if not form.is_valid():
        print('error occurred!')
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'texas/profile_token.html', context)

    profile = request.user.profile
    charge = int(form.cleaned_data['tokens'])
    profile.tokens+=charge

    profile.save()
    context = {'profile': profile, 'form': tokensAddForm()}
    return redirect(reverse('profile'))


@login_required
def get_photo(request, id):
    user = get_object_or_404(User, id=id)
    item = user.profile

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.picture:
        raise Http404
    print("geting photo of ",user.id)
    return HttpResponse(item.picture, content_type=item.content_type)



def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'texas/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'texas/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('main'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'texas/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'texas/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_profile = Profile(user=User.objects.get(username=form.cleaned_data['username']), rank=-1, tokens=0)
    new_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('login'))

def get_leaderboard_users(request):
    context = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                users = Profile.objects.order_by('rank')[:3]
                top_three_users = list(users.values())
                for user in top_three_users:
                    user_object = Profile.objects.get(id=user['user_id'])
                    user['username'] = user_object.user.username
                    user['picture_url'] = ''
                    if user_object.picture:
                        user['picture_url'] = user_object.picture.url

                return HttpResponse(json.dumps(top_three_users), content_type="application/json", status=200)
            except Exception:
                error_body = {
                    'message': 'Error occurred when retriving leaderboard user info.'
                }
                return HttpResponseServerError(json.dumps(error_body), content_type='application/json')

def assign_seat(seat_set):
    for i in range(constants.NUM_SEATS_PER_TABLE):
        if i not in seat_set:
            return i
    return -1

def join_room(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                room_number = request.POST.get('roomNumber', '')
                if room_number:
                    room_object = Room.objects.get(id=room_number)
                    room_users = room_object.user_room_set
                    exit_room_with_user(request.user)
                    # existing_entries = User_Room.objects.filter(user=request.user)
                    # if len(existing_entries) > 0:
                    #     existing_entries.delete()
                    taken_seats = set(list(room_users.values_list('seat_number', flat=True)))
                    new_seat = assign_seat(taken_seats)
                    new_user_room_entry = User_Room(user=request.user, room=room_object, seat_number=new_seat)
                    new_user_room_entry.save()
                    response_body = {
                        'user_info': User_Room.objects.filter(id=new_user_room_entry.id).values()[0],
                        'room_info': Room.objects.filter(id=room_object.id).values()[0]
                    }
                    return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
            except Exception:
                error_body = {
                    'message': 'Please double check if room exists.'
                }
                return HttpResponseBadRequest(json.dumps(error_body), content_type="application/json")


def create_room(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            exit_room_with_user(request.user)
            # room_users = User_Room.objects.filter(user=request.user)
            # if len(room_users) > 0:
            #     room_users.delete()
            new_room = Room()
            new_room.save()
            new_user_room = User_Room(user=request.user, room=new_room, seat_number=0)
            new_user_room.save()

            response_body = {
                'user_info': User_Room.objects.filter(id=new_user_room.id).values()[0],
                'room_info': Room.objects.filter(id=new_room.id).values()[0]
            }
            return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)

# exit room helper function
def exit_room_with_user(user):
    room_users = User_Room.objects.filter(user=user)
    room_ids = list(room_users.values_list('room', flat=True))
    if len(room_users) > 0:
        room_users.delete()
    
    rooms = Room.objects.filter(id__in=room_ids)
    for room in rooms:
        if room.user_room_set.count() == 0:
            room.delete()

def exit_room(request):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            exit_room_with_user(request.user)
            print('exiting')
            response_body = {
                "status": "success."
            }
            return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)

def get_room_game_info(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            room_user = User_Room.objects.get(user=request.user)
            room_object = room_user.room
            response_body = {
                "room_info": {
                    "room_number": room_object.id
                }
            }
            return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)

def get_available_rooms_info(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            room_info_list = []
            if Room.objects.exists():
                rooms = Room.objects.all()
                for room in rooms:
                    room_info = {
                        'room_number': room.id,
                        'number_of_players': room.user_room_set.count()
                    }
                    room_info_list.append(room_info)
            response_body = {
                'available_rooms': room_info_list
            }
            return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
        else:
            return HttpResponseForbidden()

@login_required
@csrf_exempt
def game(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    if request.method == 'GET':
        return render(request, 'texas/game.html', {})
    elif request.method == 'POST':
        response_data = []
        if request.user.is_authenticated:
                try:
                    # refresh the page
                    if 'choice' not in request.POST or not request.POST['choice']:
                        # room_number = request.POST.get('roomNumber', '')
                        room_user = User_Room.objects.get(user=request.user)
                        room_number = room_user.room.id
                        if room_number and room_user:

                            room_object = Room.objects.get(id=room_number)

                            if room_object.gameStart == constants.NOTREADY:
                                
                                gameInfo = {
                                    "status" : "unready",
                                    "won" : room_object.won,
                                    "community_cards" : room_object.community_card,
                                    "winner_id" : room_object.winner_id,
                                    "displaycard" : room_object.display_card,
                                }
                            elif room_object.gameStart == constants.READY:
                                community_cards = poker.split_cards(room_object.community_card)
                                gameInfo = {
                                    "status" : "start",
                                    "round" : room_object.round,
                                    "player_to_bet_id" : room_object.player_to_bet_id,
                                    "community_cards" : community_cards,
                                    "dealer_id" : room_object.dealer_id,
                                    "small_blind_id" : room_object.small_blind_id,
                                    "big_blind_id" : room_object.big_blind_id,
                                    "highest_bet" : room_object.highest_bet,
                                    "pot" : room_object.pot,
                                    "won" : room_object.won,
                                    "winner_id" : room_object.winner_id,
                                }
                            response_data.append(gameInfo)

                            room_users = room_object.user_room_set.values()
                            for seat_number in room_users:
                                user_room_entry = User_Room.objects.get(user=seat_number["user_id"], room=room_object)
                                profile_object = Profile.objects.get(user=user_room_entry.user)
                                if user_room_entry.status == constants.NOTREADY:
                                    ready = "Not"
                                elif user_room_entry.status == constants.READY:
                                    ready = "Ready"
                                
                                # set buttons

                                # if not his turn, disable all the buttons
                                if user_room_entry.user.id != room_object.player_to_bet_id:
                                    user_room_entry.buttons = constants.BUTTON[0]
                                else:
                    
                                    if user_room_entry.allin:
                                        user_room_entry.buttons = constants.BUTTON[5]
                                    elif user_room_entry.folded:
                                        user_room_entry.buttons = constants.BUTTON[6]
                                    elif user_room_entry.bet < room_object.highest_bet:
                                        user_room_entry.buttons = constants.BUTTON[3]
                                    else:
                                        user_room_entry.buttons = constants.BUTTON[4]

                                    # SB and 1st bet
                                    if user_room_entry.role == constants.ROLE[2] and user_room_entry.bet == 0:
                                        user_room_entry.buttons = constants.BUTTON[1]
                                    # BB and 1st bet
                                    if user_room_entry.role == constants.ROLE[3] and user_room_entry.bet == 0:
                                        user_room_entry.buttons = constants.BUTTON[2]
                                        
                                user_room_entry.save()
                                #profile_object.save() 

                                playerInfo = {
                                    'user': profile_object.user.id,
                                    'firstname': profile_object.user.first_name,
                                    'lastname': profile_object.user.last_name,
                                    'picture': "to add picture",
                                    'ready': ready,
                                    'role' : user_room_entry.role,
                                    'cards_holding' : poker.split_cards(user_room_entry.cards_holding),
                                    'chips' : user_room_entry.chips,
                                    'bet' : user_room_entry.bet,
                                    'last_choice' : user_room_entry.last_choice,
                                    'buttons' : user_room_entry.buttons,
                                    'folded' : user_room_entry.folded,
                                    'allin' : user_room_entry.allin,
                                    'seat_number': user_room_entry.seat_number,
                                }
                                response_data.append(playerInfo)
                            # room_object.pot = 0
                            room_object.save()
                    else:
                        choice = request.POST['choice']
                        print("Hahahahahahah", choice)
                        room_user = User_Room.objects.get(user=request.user)
                        room = Room.objects.get(id=room_user.room.id)

                        round = int(room.round)
                        players_ready = room.players_ready
                        players = room.user_room_set.values()

                        room_user.last_choice = choice.capitalize()

                        # changes
                        raised = False
                        if choice == "call" or choice == "check":
                            if room.highest_bet - room_user.bet > room_user.chips:
                                room_user.bet += room_user.chips
                                room.pot += room_user.chips
                                room_user.allin = True
                            else:
                                room_user.chips -= room.highest_bet - room_user.bet
                                room.pot += room.highest_bet - room_user.bet
                                room_user.bet = room.highest_bet
                            
                        elif choice == "fold":
                            room_user.folded = True
                            room.pot += 0
                        
                        elif "raise" in choice:
                            raised = True
                            amount = int(choice[5:])
                            previous_bet = room_user.bet
                            room_user.bet += room.highest_bet - room_user.bet + amount
                            room_user.chips -= room.highest_bet - previous_bet + amount
                            room.pot += room.highest_bet - previous_bet + amount
                            room.highest_bet += amount
                            room.save()

                            if room_user.chips == 0:
                                room_user.allin = True
                        room_user.save()
                        if choice != "fold":
                            room.players_ready += 1

                        if raised:
                            room.players_ready = 1
                        print("cur player", room.player_to_bet_id)
                        # find next active player
                        next_player_id = 0
                        index = 0
                        for j in range(len(players)):
                            if players[j]["user_id"] == room.player_to_bet_id:
                                index = j
                                break
                        count = 0
                        while True:
                            index += 1
                            print("index", index)
                            index = index % len(players)
                            user_room_entry = User_Room.objects.get(user=players[index]["user_id"])
                            if not user_room_entry.folded and not user_room_entry.allin:
                                next_player_id = players[index]["user_id"]
                                break
                            count += 1
                            if count > len(players):
                                break
                        room.player_to_bet_id = next_player_id
                        print("next player", room.player_to_bet_id)
                        room.save()

                        # check game won
                        players_in = 0
                        notWin = False
                        win = 0
                        for seat_number in players:
                            #print(seat_number["user_id"])

                            user_room_entry = User_Room.objects.get(user=seat_number["user_id"])
                            if not user_room_entry.folded:
                                win = user_room_entry.user.id
                                players_in += 1
                            if players_in > 1:
                                notWin = True
                                break

                        if not notWin:
                            room.won = True
                            room.display_card = False
                            room.gameStart = constants.NOTREADY
                            room.winner_id = win

                        elif not room.won:

                            active_players = 0
                            for player in players:
                                user_room_entry = User_Room.objects.get(user=player["user_id"])
                                if not user_room_entry.folded and not user_room_entry.allin:
                                    active_players += 1
                            print("active player ", active_players)
                            print("ready players", room.players_ready)
                            if room.players_ready >= active_players:
                                
                                #room.player_to_bet_id = next_player_id
                                if room.round < constants.ROUND[3]:
                                    room.round = round + 1
                                    room.players_ready = 0
                                
                                else:
                                    room.won = True
                                    # compare and compute the winner
                                    inContention = []
                                    rankList = []
                                    for player in players:
                                        if not player['folded']:
                                            inContention.append(player)
                                            holding_cards = poker.card_string_to_list(player['cards_holding'])
                                            comm_cards = poker.card_string_to_list(room.community_card)
                                            rankList.append(poker.get_best(holding_cards, comm_cards))
                                    winnerIndicies = poker.get_winning_hands(rankList)
                                    room.winner_id = players[winnerIndicies[0]]['user_id']
                            #else:
                                #room.player_to_bet_id = next_player_id
                            
                        if room.won:
                            room.gameStart = constants.NOTREADY
                            # if game is over, add/subtract chips to their tokens
                            if room.won and room.reward == 0:
                                room.reward += room.pot
                            for player in players:
                                user_room_entry = User_Room.objects.get(user=player["user_id"])
                                profile_object = Profile.objects.get(user=user_room_entry.user)
                                # if game is over and the pot is not rewarded to the winner, add them to the winner's tokens
                                if room.won and player["user_id"] == room.winner_id:
                                    profile_object.tokens += (room.reward + user_room_entry.chips)
                                    #room.pot = 0
                                # if game is over and the pot is not rewarded to the winner, add chips to player's tokens
                                elif room.won and player["user_id"] != room.winner_id:
                                    profile_object.tokens += user_room_entry.chips
                                # initialize for the new game
                                print("Initialization success", user_room_entry.user.id)
                                user_room_entry.status = constants.NOTREADY
                                user_room_entry.role = constants.ROLE[0]
                                # user_room_entry.cards_holding = ""
                                user_room_entry.chips = 100
                                user_room_entry.bet = 0
                                user_room_entry.last_choice = ""
                                user_room_entry.buttons = constants.BUTTON[0]
                                user_room_entry.allin = False
                                user_room_entry.folded = False
                                user_room_entry.save()
                                profile_object.save()
                        #print(room.player_to_bet_id)

                        #room_user.save()
                        room.save()
                    response_json = json.dumps(response_data)
                    #print(response_json)
                    return HttpResponse(response_json, content_type='application/json')
                except Exception:
                    traceback.print_exc()
                    error_body = {
                        'message': 'Game Update Error.'
                    }
                    return HttpResponseBadRequest(json.dumps(error_body), content_type="application/json")

def userReady(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                room_number = request.POST.get('roomNumber', '')
                room_user = User_Room.objects.get(user=request.user)
                if room_number and room_user:
                    room_number = room_number.split(" ")[-1]
                    room_object = Room.objects.get(id=room_number)
                    if room_object.won:
                        room_object.won = False
                        room_object.save()
                    # get ready and check if all users are ready
                    room_user.status = constants.READY
                    room_user.last_choice = "Ready"
                    room_user.save()
                    room_users = room_object.user_room_set.values()
                    response_body = None
                    if(len(room_users) < 4):
                        return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
                    for seat_number in room_users:
                        #print(seat_number)
                        user_room_entry = User_Room.objects.get(user=seat_number["user_id"], room=room_object)
                        if user_room_entry.status == constants.NOTREADY:
                            #print("some not ready")
                            return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
                    # Start game when more than 4 users are ready

                    room_object.gameStart = constants.READY
                    # room_object.won = False

                    # initialize game fields
                    deck = poker.get_deck()
                    room_object.round = constants.ROUND[0] # preflop betting round
                    room_object.community_card = poker.card_list_to_string(poker.random_draw_x_cards(5, deck))
                    room_object.highest_bet = 0
                    room_object.pot = 0
                    room_object.winner_id = 0
                    room_object.reward = 0
                    room_object.display_card = True
                    user_ids = []
                    for room_user in room_users:
                        user_ids.append(room_user["user_id"])
                        user_room_object = User_Room.objects.get(user=room_user["user_id"])
                        cards = poker.card_list_to_string(poker.random_draw_x_cards(2, deck))
                        user_room_object.cards_holding = cards
                        # print(cards)
                        user_room_object.last_choice = "Ready"
                        # user_room_object.buttons = constants.BUTTON[0]
                        user_room_object.save()

                        # subtract chips from tokens
                        profile_object = Profile.objects.get(user=room_user["user_id"])
                        # profile_object.tokens -= 100
                        profile_object.save()
                    if room_object.dealer_id == 0:
                        dealer_index = random.randint(0, len(user_ids) - 1)
                        #small_blind_index = dealer_index + 1 if dealer_index < len(user_ids) - 1 else 0
                        #big_blind_index = small_blind_index + 1 if small_blind_index < len(user_ids) -1 else 0
                    else:
                        dealer_index, i = 0, 0
                        for room_user in room_users:
                            if room_user["user_id"] == room_object.dealer_id:
                                dealer_index = i
                                break
                            i+=1
                    small_blind_index = dealer_index + 1 if dealer_index < len(user_ids) - 1 else 0
                    big_blind_index = small_blind_index + 1 if small_blind_index < len(user_ids) -1 else 0

                    room_object.dealer_id = user_ids[dealer_index] # TODO
                    room_object.small_blind_id = user_ids[small_blind_index] # TODO
                    room_object.big_blind_id = user_ids[big_blind_index] # TODO

                    room_object.player_to_bet_id = room_object.small_blind_id # start from small blind

                    room_object.save()
                    
                    dealer_object = User_Room.objects.get(user=user_ids[dealer_index])
                    dealer_object.role = constants.ROLE[1]
                    dealer_object.save()

                    small_blind_object = User_Room.objects.get(user=user_ids[small_blind_index])
                    small_blind_object.role = constants.ROLE[2]
                    small_blind_object.buttons = constants.BUTTON[1]
                    small_blind_object.save()

                    big_blind_object = User_Room.objects.get(user=user_ids[big_blind_index])
                    big_blind_object.role = constants.ROLE[3]
                    big_blind_object.buttons = constants.BUTTON[2]
                    big_blind_object.save()
                      #  print("HAHAHAHAHAHA")
                     #   print(room_number, room_object.gameStart)
                    return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
            except Exception:
                error_body = {
                    'message': 'Cannot get ready.'
                }
                return HttpResponseBadRequest(json.dumps(error_body), content_type="application/json")

def userCancelReady(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                room_number = request.POST.get('roomNumber', '')
                room_user = User_Room.objects.get(user=request.user)
                room_number = room_number.split(" ")[-1]
                room_object = Room.objects.get(id=room_number)
                if room_number and room_user and room_object.gameStart == constants.NOTREADY:
                    # cancel ready only if game haven't started
                    print("cancel ready")
                    room_user.status = constants.NOTREADY
                    room_user.save()
                    response_body = None
                    return HttpResponse(json.dumps(response_body), content_type="application/json", status=200)
            except Exception:
                error_body = {
                    'message': 'Cannot cancel ready.'
                }
                return HttpResponseBadRequest(json.dumps(error_body), content_type="application/json")