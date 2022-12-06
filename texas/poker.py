import random
from itertools import combinations


class Card:

    def __init__(self, value, suit):
        """initialization of card with value and suit"""
        self.value = value  # the value of the card

        if value == 14:
            self.name = "A"
        elif value == 13:
            self.name = "K"
        elif value == 12:
            self.name = "Q"
        elif value == 11:
            self.name = "J"
        else:
            self.name = str(value)

        self.suit = suit  # the suit of the card

        if suit.lower() == "c":
            self.name += "♣"
        elif suit.lower() == "s":
            self.name += "♠"
        elif suit.lower() == "h":
            self.name += "♥"
        else:
            self.name += "♦"

    def __str__(self):
        """return name in the format of value+suit"""
        return self.name

    def __eq__(self, other):
        """Allows comparison with =="""
        equal = self.value == other.value and self.suit == other.suit
        return equal


class Player:
    """Class representing a poker player"""

    def __init__(self, chips):
        """initialization of a player instance with a given number of chips"""
        self.role = -1  # -1: no role, 0: dealer, 1: small blind, 2: big blind
        self.cards_holding = []  # list of cards holding on hand
        self.chips = chips  # the amount of chips holding
        self.bet = 0  # the amount of bet now
        self.folded = False  # if the player folded at this time
        self.allin = False  # if the player plays all in at this time

    def reset(self, deck):
        """Remove cards from player back to deck, resets round specific attributes"""
        deck += self.cards_holding
        self.cards_holding.clear()

        self.bet = 0
        self.folded = False
        self.allin = False


def split_cards(cards):
    """return a string list of cards"""
    card = ""
    arr = []
    for c in cards:
        card += c
        if c in ["♣", "♠", "♥", "♦"]:
            arr.append(card)
            card = ""
    return arr

def random_draw_x_cards(x, deck):
    """Randomly remove x cards from a deck list and returns cards drawn as a list"""
    hand = []
    for i in range(x):
        card_to_remove = random.choice(deck)
        deck.remove(card_to_remove)
        hand.append(card_to_remove)
    return hand


def get_deck():
    """get a full deck of with 13*4 cards"""
    deck = []
    suits = ["c", "s", "h", "d"]
    for suit in suits:
        for val in range(2, 15):
            deck.append(Card(val, suit))
    return deck


def get_player_list(n, chips):
    """Return a list of n player objects with equal chips"""
    player_list = []
    for i in range(n):
        player_list.append(Player(chips))
    return player_list


def hand_recognition(hand):
    """Takes a list of 5 Card objects and classifies it as a poker hand"""
    hand.sort(key=lambda cur_card: cur_card.value)  # sorts hand by value asc

    rankings = [0, 0, 0, 0, 0, 0]

    # ---flush /straight flush---
    flush = True
    suit = hand[0].suit
    for card in hand[1:]:
        if card.suit != suit:
            flush = False
            break
    if flush:
        rankings[1] = hand[4].value

    # ---straight / straight flush---
    straight = True

    # ace counts as low card
    if hand[4].value == 14 and hand[0].value == 2:
        mid_vals = []
        for i in range(1, 4):
            mid_vals.append(hand[i].value)
        if mid_vals != [3, 4, 5]:
            straight = False

        if straight:
            rankings[1] = 5

    # typical case, ace is high card if it exists
    else:
        for i in range(4):
            if hand[i].value + 1 != hand[i + 1].value:
                straight = False
                break

        if straight:
            rankings[1] = hand[4].value

    # ---four of a kind---
    four = False
    four_value = 0
    for i in range(2):
        if hand[i].value == hand[i + 1].value and \
                hand[i].value == hand[i + 2].value and \
                hand[i].value == hand[i + 3].value:
            four = True
            four_value = hand[i].value
            break

    # ---three of a kind / full house three---
    three = False
    three_value = 0
    for i in range(3):
        if hand[i].value == hand[i + 1].value and \
                hand[i].value == hand[i + 2].value:
            three = True
            three_value = hand[i].value
            break

    # ---pair / 2 pair / Full house pair---
    pairs = 0
    pair_values = []
    for i in range(4):
        if hand[i].value == hand[i + 1].value:
            pairs += 1
            pair_values.append(hand[i].value)

    # ---rank assignment + tie-breaker values---
    if straight and flush:
        rankings[0] = 9

        msg = "Straight Flush"

    elif four:
        rankings[0] = 8
        rankings[1] = four_value
        for card in hand[0::4]:
            if card.value != four_value:
                rankings[2] = card.value
                break

        msg = "Four of a Kind"

    elif three and pairs >= 3:
        rankings[0] = 7
        rankings[1] = three_value
        for val in pair_values:
            if val != three_value:
                rankings[2] = val
                break

        msg = "Full House"

    elif flush:
        rankings[0] = 6

        msg = "Flush"

    elif straight:
        rankings[0] = 5

        msg = "Straight"

    elif three:
        rankings[0] = 4
        rankings[1] = three_value
        kickers = [x for x in hand if x.value != three_value]
        rankings[2] = kickers[-1].value
        rankings[3] = kickers[-2].value

        msg = "Three of a Kind"

    elif pairs == 2:
        rankings[0] = 3
        rankings[1] = pair_values[-1]
        rankings[2] = pair_values[-2]
        rankings[3] = [x for x in hand if x.value not in pair_values][0].value

        msg = "Two Pair"

    elif pairs == 1:
        rankings[0] = 2
        rankings[1] = pair_values[0]
        kickers = [x for x in hand if x.value not in pair_values]
        rankings[2] = kickers[-1].value
        rankings[3] = kickers[-2].value
        rankings[4] = kickers[-3].value

        msg = "Pair"

    else:
        rankings[0] = 1
        for i in range(1, 6):
            rankings[i] = hand[-i].value

        msg = "High Card"

    return rankings, msg


def card_value_to_string(value):
    """Helper for handRankToString. Converts card value
    to name string, e.g. 13 -> King"""
    if value == 14:
        return "Ace"
    elif value == 13:
        return "King"
    elif value == 12:
        return "Queen"
    elif value == 11:
        return "Jack"
    else:
        return str(value)

def card_list_to_string(cards):
    return "".join([str(card) for card in cards])

def card_string_to_list(s):
    word = ""
    cards = []
    for c in s:
        word += c
        if c in ["♣", "♠", "♥", "♦"]:
            value = word[:-1]
            if value == "A":
                value = 14
            elif value == "K":
                value = 13
            elif value == "Q":
                value = 12
            elif value == "J":
                value = 11
            else:
                value = int(word[:-1])
            if c == "♣":
                cards.append(Card(value, "c"))
            elif c == "♠":
                cards.append(Card(value, "s"))
            elif c == "♥":
                cards.append(Card(value, "h"))
            else:
                cards.append(Card(value, "d"))
            word = ""
    return cards


def hand_rank_to_string(rank):
    """Gives a detailed string describing a hand's rank"""
    msg = ""
    kicker = ""
    if rank[0] == 9:
        msg += "Straight Flush"

    elif rank[0] == 8:
        msg += "Four of a kind"
        four = card_value_to_string(rank[1])
        kicker = card_value_to_string(rank[2])
        msg += (" (four " + four + "s")

    elif rank[0] == 7:
        msg += "Full House"
        house = card_value_to_string(rank[1])
        full = card_value_to_string(rank[2])
        msg += " (house of " + house + "s full of " + full + "s)"

    elif rank[0] == 6:
        msg += "Flush"

    elif rank[0] == 5:
        msg += "Straight"

    elif rank[0] == 4:
        msg += "Three of a kind"
        three = card_value_to_string(rank[1])
        kicker = card_value_to_string(rank[2])
        kicker += " and " + card_value_to_string(rank[3])
        msg += " (three " + three + "s"

    elif rank[0] == 3:
        msg += "Two pair"
        pair1 = card_value_to_string(rank[1])
        pair2 = card_value_to_string(rank[2])
        kicker = card_value_to_string(rank[3])
        msg += " (pair of " + pair1 + "s and " + pair2 + "s"

    elif rank[0] == 2:
        msg += "Pair"
        pair = card_value_to_string(rank[1])
        kicker = card_value_to_string(rank[2])
        kicker += ", " + card_value_to_string(rank[3])
        kicker += " and " + card_value_to_string(rank[4])
        msg += " (pair of " + pair + "s"

    elif rank[0] == 1:
        msg += "High Card"

    if rank[0] in [9, 6, 5, 1]:
        high = card_value_to_string(rank[1])
        msg += " with " + high + " high"
    elif rank[0] in [8, 4, 3, 2]:
        msg += " with " + kicker + " kicker)"

    return msg


def get_winning_hands(rank_list, compare_index=0, to_compare=[]):
    """Takes a list of outputted arrays from hand recognition and outputs
       the indices of the winners"""
    highest = -1
    winners = []

    if compare_index == 0:
        to_compare = list(range(len(rank_list)))

    comp_copy = to_compare.copy()
    for i in comp_copy:

        # if new highest, remove lowers from contention
        if rank_list[i][compare_index] > highest:
            for win in winners:
                to_compare.remove(win)
            winners.clear()

            highest = rank_list[i][compare_index]
            winners.append(i)

        elif rank_list[i][compare_index] == highest:
            winners.append(i)

        else:
            to_compare.remove(i)

    # if a single winner has been found / there's a tie
    if len(winners) == 1 or highest == 0 or compare_index == 5:
        return winners

    else:
        return get_winning_hands(rank_list, compare_index + 1, to_compare)


def get_best(hole_cards, community_cards):
    """Take list of 2 hole cards and list of 5 community cards best,
    return the rankList of the best hand, also works with >=3 community cards"""
    best = [0, 0, 0, 0, 0, 0]
    # 21 iterations for full 7 cards
    for hand in combinations(hole_cards + community_cards, 5):
        # gets the higher ranking of the two hands
        compare2 = [best]
        compare2.append(hand_recognition(list(hand))[0])
        best_index = get_winning_hands(compare2)[0]
        best = compare2[best_index]

    return best


class Game:
    """class of a game process, with given number of players"""

    def __init__(self, players):
        self.players = players
        self.deck = get_deck()
        self.community_card = []
        self.dealer_pos = 0
        self.small_blind_pos = 0
        self.big_blind_pos = 0
        self.highest_bet = 0
        self.pot = 0
        self.won = False

    def set_roles(self):
        """select dealer, small blind and big blind"""
        # no history positions, randomly select one player to play as dealer
        if self.dealer_pos == self.small_blind_pos:
            self.dealer_pos = random.randint(0, len(self.players) - 1)
        # next player play as the dealer
        else:
            self.dealer_pos = self.dealer_pos + 1 if self.dealer_pos < len(self.players) - 1 else 0
        self.small_blind_pos = self.dealer_pos + 1 if self.dealer_pos < len(self.players) - 1 else 0
        self.big_blind_pos = self.small_blind_pos + 1 if self.small_blind_pos < len(self.players) - 1 else 0

    def deal(self):
        """assign 2 hole cards to each of active player"""
        for player in self.players:
            player.cards_holding += random_draw_x_cards(2, self.deck)

    def set_community_card(self):
        """assign 5 cards as community card"""
        self.community_card = random_draw_x_cards(5, self.deck)

    def call(self, player):
        """Player matches the highest bet or does as best they can and goes all in, return updated pot"""
        # all-in
        if self.highest_bet - player.bet > player.chips:
            player.bet += player.chips
            self.pot += player.chips
            player.allin = True

        # normal call
        else:
            player.chips -= self.highest_bet - player.bet
            self.pot += self.highest_bet - player.bet
            player.bet = self.highest_bet

    def fold(self, player):
        player.folded = True
        self.pot += 0

    def _raise(self, player, amount):
        """Takes current highest bet and amount to raise, adjusts chip count and returns new highest bet"""
        if self.highest_bet - player.bet + amount > player.chips:
            return -1
        else:
            previous_bet = player.bet
            player.bet += self.highest_bet - player.bet + amount
            player.chips -= self.highest_bet - previous_bet + amount
            self.pot += self.highest_bet - previous_bet + amount
            self.highest_bet += amount

        if player.chips == 0:
            player.allin = True

        return 0

    def check_game_won(self):
        """Check to see if there is a winner"""
        players_in = 0
        for i in range(len(self.players)):
            if not players[i].folded:
                win = i
                players_in += 1
            if players_in > 1:
                return -1
        self.won = True
        return win

    def betting_round(self, round_name):
        """Handles a betting round of a single poker game"""
        players_ready = 0
        player_pos = self.small_blind_pos
        if round_name.lower() == "preflop":
            player_pos = (self.big_blind_pos + 1) % len(self.players)  # start betting from the player next to big blind
        while players_ready < len(self.players):
            print("Current player: " + str(player_pos))
            player = self.players[player_pos]
            if player.folded or player.allin:
                player_pos = (player_pos + 1) % len(self.players)
                print("This player has folded/allin.")
                players_ready += 1
                print(str(players_ready) + " players ready")
                continue

            raised = False
            folded = False

            # if player need to call
            if player.bet < self.highest_bet:
                print("Your current bet is " + str(player.bet) + ", Please input your choice (call, fold or raise): ")
                choice = input().lower()

                if choice == "call":
                    self.call(player)
                    raised = False

                elif choice == "raise":
                    print("Please input your amount to raise: ")
                    amount = int(input())
                    self._raise(player, amount)
                    raised = True

                elif choice == "fold":
                    self.fold(player)
                    raised = False
                    folded = True

            # if player doesn't need to call
            elif player.bet == self.highest_bet:
                print("Please input your choice (raise/check): ")
                choice = input().lower()

                if choice == "raise":
                    print("Please input your amount to raise: ")
                    amount = int(input())
                    self._raise(player, amount)
                    raised = True
                elif choice == "check":
                    raised = False

            if raised:
                players_ready = 1

            elif folded:
                players_ready += 1
                if self.check_game_won() > -1:
                    print("Game finished. The winner is player" + str(self.check_game_won()))
                    break

            else:
                players_ready += 1

            player_pos = (player_pos + 1) % len(self.players)
            print(str(players_ready) + " players ready")


if __name__ == "__main__":
    """Test game with 6 players"""
    """Players should have more than 100 tokens, and bring 100 as chips"""

    # Set all the players in player list
    player1 = Player(100)
    player2 = Player(100)
    player3 = Player(100)
    player4 = Player(100)
    player5 = Player(100)
    player6 = Player(100)
    players = [player1, player2, player3, player4, player5, player6]

    # start game with player list
    game = Game(players)
    # set roles (dealer, small blind, big blind)
    game.set_roles()
    # force small blind to bet for $5
    small_blind = game.players[game.small_blind_pos]
    small_blind.chips -= 5
    small_blind.bet += 5
    # force big blind to bet for $10
    big_blind = game.players[game.big_blind_pos]
    big_blind.chips -= 10
    big_blind.bet += 10

    game.highest_bet = 10

    game.deal()
    game.set_community_card()

    print("Big blind position: " + str(game.big_blind_pos))

    if not game.won:
        print("------------------Preflop betting round------------------")
        game.betting_round("Preflop")

    if not game.won:
        print("------------------Flop betting round------------------")
        game.betting_round("Flop")

    if not game.won:
        print("------------------Turn betting round------------------")
        game.betting_round("Turn")

    if not game.won:
        print("------------------River betting round------------------")
        game.betting_round("River")

    if not game.won:
        inContention = []
        rankList = []
        for player in game.players:
            if not player.folded:
                inContention.append(player)
                rankList.append(get_best(player.cards_holding, game.community_card))

        winnerIndices = get_winning_hands(rankList)

        winnings = game.pot / len(winnerIndices)

        for i in winnerIndices:
            print("Player", i, "Wins!")
            inContention[i].chips += winnings

