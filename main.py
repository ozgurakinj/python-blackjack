# Python Console Blackjack
# Supports up to 5 players
#
# Feel free to leave a star
# Please report found bugs
# @ozgurakinj at github

import random
import time
import sys

class Card:
    
    def __init__(self, num, suit, rev):
        self.number = num
        self.value = 0

        if self.number == 11 or self.number == 12 or self.number == 13:
            self.value = 10
        else:
            self.value = self.number

        self.suit = suit
        self.revealed = rev
    symbols={"1":"A","11":"J","12:"Q",13:"K"}
    def show(self):
        if str(self.number) in symbols.keys():
             card_symbol=symbols[str(self.number)]
        else:
             card_symbol=self.number
        time.sleep(1)
        print(self.number, "of", self.suit)
        print("_____")
        print("|{}  |".format(card_symbol))
        print("|   |")
        print("| {} |".format(self.suit[0]))
        print("|   |")
        print("|  {}|".format(card_symbol))
        print("|___|")



class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["spades", "hearts", "diamonds", "clubs"]:
            for number in range(1, 14):
                self.cards.append(Card(number, suit, 1))
        self.shuffle()

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        random.shuffle(self.cards)


class Player:

    def __init__(self, name, chips):
        self.name = name
        self.hand = []
        self.chips = chips
        self.bet = 0
        self.status = "in"

    def draw(self, deck, count=1):
        for x in range(0, count):
            try:
                self.hand.append(deck.cards.pop())
            except IndexError:
                print("deck empty. addinga new deck.")
                deck.build()
                deck.shuffle()

    def show_hand(self):
        time.sleep(1)
        print("## player {} 's hand ##".format(self.name))
        try:
            for card in self.hand:
                if card.revealed:
                    card.show()
                else:
                    time.sleep(1)
                    print("a card face down")


            if len(self.hand) == 0:
                time.sleep(1)
                print("empty hand")
            time.sleep(1)
            print("value : {}".format(self.value()))

        except IndexError:
            time.sleep(1)

    def value(self):
        value = 0
        aces_count = 0

        # Value without aces

        for card in self.hand:
            if card.number == 1:
                aces_count += 1
            else:
                value += card.value

        # Aces values added

        for ace in range(0, aces_count):
            if value > 10:
                value += 1
            else:
                value += 11

        return value

    def bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            self.bet += amount
        else:
            time.sleep(1)
            print("insufficient chips")

    def is_bust(self):
        if self.value() > 21:
            self.show_hand()
            self.status = "bust"
            self.lose()
            time.sleep(1)
            print("## player {} bust ##".format(self.name))

    def is_blackjack(self):
        if self.value() == 21:
            self.show_hand()
            time.sleep(1)
            print("## player {} blackjack ##".format(self.name))

    def lose(self):
        self.bet = 0


class Dealer(Player):

    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_closed(self, deck, count=1):
        for x in range(0, count):
            card = deck.cards.pop()
            card.revealed = 0
            self.hand.append(card)

    def reveal(self):
        self.hand[1].revealed = 1

    def show_hand(self):
        time.sleep(1)
        print("## {} 's hand ##".format(self.name))
        try:
            for card in self.hand:
                if card.revealed:
                    card.show()
                else:
                    time.sleep(1)
                    print("a card face down")
                    print("_____")
                    print("|# #|")
                    print("| # |")
                    print("|# #|")
                    print("| # |")
                    print("|# #|")
                    print("_____")
            if len(self.hand) == 0:
                time.sleep(1)
                print("empty hand")

        except IndexError:
            time.sleep(1)
            print("deck empty")

    def is_bust(self):
        if self.value() > 21:
            time.sleep(1)
            print("## dealer bust ##")
            return True
        else:
            return False


class Game:

    def __init__(self, min_bet):
        self.players = []
        self.deck = Deck()
        self.min_bet = min_bet
        self.dealer = Dealer("dealer")

    def create_player(self, name):
        if len(self.players) < 5:
            player = Player(name, int(self.min_bet) * 10)
            self.players.append(player)
        else:
            time.sleep(1)
            print("can't create more than 5 players")

    def deal(self):
        for player in self.players:
            player.draw(self.deck)
        self.dealer.draw(self.deck)

        for player in self.players:
            player.draw(self.deck)
        self.dealer.draw_closed(self.deck)

        self.show_dealer_hand()
        self.show_player_hands()

    def get_bets(self):

        for player in self.players:
            time.sleep(1)
            print("## player {} ## chips : {}".format(player.name, player.chips))
            player.bet = self.min_bet - 1
            while player.bet < self.min_bet:
                player.bet = int(input("place your bet ( Minimum bet: {} )".format(self.min_bet)))
                if player.bet >= self.min_bet:
                    if player.bet > player.chips:
                        time.sleep(1)
                        print("## insufficient chips ##")
                        player.bet = self.min_bet - 1
                    else:
                        player.chips -= player.bet
                else:
                    time.sleep(1)
                    print("## you need to bet more than {}. ##".format(self.min_bet))
                    player.bet = self.min_bet - 1

    def pay(self, player):
        if player.value() == 21:
            pay = player.bet + player.bet * 3 / 2
            player.chips += pay
            player.bet = 0
            player.status = "bj"
            time.sleep(1)
            print("## player {} won {} ##".format(player.name, pay))
        else:
            pay = player.bet + player.bet * 2 / 1
            player.chips += pay
            player.bet = 0
            player.status = "win"
            time.sleep(1)
            print("## player {} won {} ##".format(player.name, pay))

    def tie(self, player):
        pay = player.bet
        player.chips += pay
        player.bet = 0
        player.status = "tie"
        time.sleep(1)
        print("## player {} tie. returned {} ##".format(player.name, pay))

    def check_blackjacks(self):
        for player in self.players:
            if player.value() == 21:
                self.pay(player)
                player.status = "startbj"

    def check_losers(self):
        for player in self.players:
            if player.chips == 0:
                print("## player {} out of chips. you lost! ##".format(player.name))
                self.remove_player(player)

    def remove_player(self, player):
        self.players.remove(player)

    def show_player_hands(self):
        for player in self.players:
            player.show_hand()
            time.sleep(1)

    def show_dealer_hand(self):
        self.dealer.show_hand()

    def players_in_game(self):
        count = 0
        for player in self.players:
            if player.status == "stand" or player.status == "bj":
                count += 1
        return count

    def reset_players(self):
        for player in self.players:
            player.status = "in"
            player.hand = []
            player.bet = []
        self.dealer.hand = []

    def turn(self):

        self.check_blackjacks()

        # Ask each player for their plays

        for player in self.players:
            while player.status == "in":
                time.sleep(1)
                print("## player {} 's turn ##".format(player.name))
                player.show_hand()
                choice = input("[h]it or [s]tand [e]xit ")
                if choice == "h":
                    player.draw(self.deck)
                    player.is_bust()
                    player.is_blackjack()
                elif choice == "s":
                    player.status = "stand"
                elif choice == "e":
                    print("## player {} left the table ##".format(player.name))
                    player.status = "out"
                    self.remove_player(player)
                else:
                    time.sleep(1)
                    print("invalid input")

        # Dealer's turn

        if self.players_in_game() == 0:
            print("## everyone bust ##")
        else:
            self.dealer.reveal()
            self.dealer.show_hand()
            time.sleep(1)
            print("value : {}".format(self.dealer.value()))

            while self.dealer.value() < 17:
                self.dealer.draw(self.deck)
                self.dealer.show_hand()
                time.sleep(1)
                print("value : {}".format(self.dealer.value()))

            # If pay everyone if dealer busts, if not, pay players valued higher than the dealer

            if self.dealer.is_bust():
                for player in self.players:
                    if player.status == "stand":
                        self.pay(player)

            else:
                for player in self.players:
                    if player.value() > self.dealer.value() and player.status == "stand":
                        self.pay(player)
                    if player.value() < self.dealer.value() and player.status == "stand":
                        self.pay(player)
                    if player.value() == self.dealer.value() and player.status == "stand":
                        self.tie(player)

        # Remove players that are out of chips

        self.check_losers()

        # Reset player status

        self.reset_players()


def play():
    time.sleep(1)
    game = Game(int(input("minimum bet of table?")))
    time.sleep(1)
    player_count = int(input("how many players?"))
    for count in range(0, player_count):
        time.sleep(1)
        print('# player {} #'.format(count + 1))
        game.create_player(input("enter player name:"))

    while len(game.players) > 0:
        game.get_bets()
        game.deal()
        game.turn()

    time.sleep(1)
    print("## no players left ##")
    time.sleep(1)
    print("## thanks for playing ##")


def main_menu():
    while True:
        print("## welcome to python blackjack ##")
        time.sleep(1)
        command = input("## [p]lay or [e]xit ##")
        if command == "p":
            play()
        elif command == "e":
            time.sleep(1)
            print("## good bye! ###")
            sys.exit()
        else:
            time.sleep(1)
            print("## invalid command ##")


if __name__ == "__main__":
    main_menu()
