"""
Assignment 5

A Blackjack game between one player and the computer.

Written by Steve Walker
Conestoga College Student #: 4360392

Original date for Rel 0: 04 AUG 2020
Current release: 4
Current release date: 10 AUG 2020

"""

import random       # random integer generator
import sys          # sys.exit() used in my program


def main():
    ''' All of my code follows within this function. I don't fully understand
        why I should do this as my program runs the same if I don't put it in
        a main(): and by doing this it does cause me to get several "Too many.."
        Pylint warnings related to the def main(): line.... hopefully I can get
        this figured out in the next course.'''

    def draw_card(how=0):   # A function to draw one card and return the card
                            # face (A-K), card value (2-11) and card ID.

        if how == "Manual":     # if Manual then the card draw waits for player
                                # input to control the pace of the game play.
            while True:
                go_ahead = input("\n Press <ENTER> to deal the card.")
                if go_ahead == '':
                    break
                continue

        card_id = random.randint(1, 13)

        if card_id == 1:
            face_value = 11  # sets ACE to 11
            the_card = 'A'
        elif card_id >= 11:     # sets J, Q or K to 10.
            face_value = 10
            if card_id == 11:
                the_card = 'J'
            elif card_id == 12:
                the_card = 'Q'
            else:
                the_card = 'K'
        else:
            face_value = card_id
            the_card = str(card_id)   # all number card are their face value.

        # print(the_card, face_value)  # comment out or remove after testing.
        return the_card, face_value


    def showing(name, p_hand, p_value, d_hand, d_value):

        print("\n\t" + name + ", you are holding:  "
              + '  '.join(p_hand) + '  for ' + str(p_value))
        print("\n\tThe Dealer is showing:  " + '  '.join(d_hand) + ' for '
              + str(d_value))


    def win_loss_avg(win, loss):
        if win or loss:
            print()     # print a blank line for better readability....
            line('=', 60)
            print(f'\tYou\'ve won {win:.0f} and lost {loss:.0f} '
                  + 'game(s) in this round.')
            print(f'\t\t*** Your win rate is {(win)/(win+loss):.1%} ***')
            line('=', 60)


    def line(character, count):     # prints a line of specified length of
                                    # a specified character
        print(' ' + character * count)


    """
    The following section finds out if a new player wants to play, and if so,
    gets their name. If not, exits the program, and if there is bad user
    feedback, will loop until a valid response is given.
    """

    print("\n Do you want to play Blackjack?\n")

    while True:
        play_or_not = input(' Y to play or <ENTER> to quit: ')

        if play_or_not.upper() == 'Y':
            p1_name = input("\n Great! First let's get your name: ").title()
            print("\n OK " + p1_name +", let's play some Blackjack.....")
            print("\n\n Dealing you two cards, then myself two cards...")

            games_won = 0    # set the number of games the player wins to zero.
            games_lost = 0   # set the number of games the player loses to zero.
            break

        if play_or_not == '':
            print('\n Maybe next time..... goodbye!')
            sys.exit()
            break

        print('\n Not a valid choice. Try again.')
        continue

    """
    Let's actually play some Blackjack now...
    """
    while True:

        # Player opening two card deal
        player_hand = [] # create an empty hand for the player
        player_hand_value = 0
        player_high_ace = 0     # track the qty of aces at 11 (needed for Busts)
        while len(player_hand) < 2:
            card, value = draw_card()  # will draw two cards without waiting
            if card == "A":
                player_high_ace += 1
            player_hand.append(card)    # add dealt card to the players hand
            player_hand_value += value  # update the value of the hand

        # Dealer opening hand (one card, 2nd is face down so don't bother yet.)
        dealer_hand = [] # create an empty hand for the dealer
        dealer_hand_value = 0
        dealer_high_ace = 0     # track the qty of aces at 11 (needed for Busts)
        card, value = draw_card()       # one card without waiting
        if card == "A":
            dealer_high_ace += 1
        dealer_hand.append(card)
        dealer_hand_value += value
        who = 'player'      # sets the next play as back to the player

        # PLAYER's HAND
        while who == "player":

            showing(p1_name, player_hand, player_hand_value, dealer_hand,
                    dealer_hand_value)

            if (player_hand_value) > 21:    # bust if there is no ACE.
                if player_high_ace:     # is an ACE worth 11 is in the hand.
                    player_hand_value -= 10    # subtract 10 from the hand value.
                    player_high_ace -= 1    # remove the high value ACE
                    print("\n I made one of your ACEs worth one. "
                          + "Your new hand value is...")
                    continue

                print("\n You busted with " + str(player_hand_value)
                      +". The Dealer won this hand.")
                games_lost += 1
                who = ''    # this hand has ended. No player has control.
                break

            if (player_hand_value) == 21:
                print("\n " + p1_name + ", you've got 21!! Dealer's turn....")
                who = 'dealer'      # control transfers to the dealer
                break

            if (player_hand_value) < 21:

                hit_or_stand = input("\n\n S <ENTER> to stand. "
                                     +"<ENTER> to hit...\n")
                if hit_or_stand.upper() == "S":
                    print(' ' + p1_name + ' stands on '
                          + str(player_hand_value))
                    who = 'dealer'
                    break
                if hit_or_stand.upper() == '':
                    card, value = draw_card()  # will draw one card
                    print()
                    line('=', 50)  # print a line of 50 '='
                    if card == "A":
                        player_high_ace += 1

                    if card in ('A', '8'):  # use proper grammar...
                        print("\n You drew an " + card)
                    else:
                        print("\n You drew a " + card)

                    player_hand.append(card)
                    player_hand_value += value
                continue
            continue



        # DEALER's hand
        while who == 'dealer':

            if dealer_hand_value > 21:  # dealer has busted (maybe....)
                # Are there ACE cards to make a 1 instead of 11?
                if dealer_high_ace:  # at least one '11' ACE exists....
                    dealer_hand_value = dealer_hand_value - 10
                    dealer_high_ace -= 1
                    continue   # while loop again based on ACE worth 1 point...
                games_won += 1
                print("\n The dealer busted!! A win for YOU, " + p1_name)
                break

            if dealer_hand_value >= 17: # dealer must hold on 17 or higher....

                showing(p1_name, player_hand, player_hand_value, dealer_hand,
                        dealer_hand_value)

                if dealer_hand_value > player_hand_value:
                    print("\n The DEALER wins this game.")
                    games_lost += 1  # dealer wins
                    break
                if dealer_hand_value == player_hand_value:
                    print("\n No pushes in this game...tie goes to the DEALER!")
                    games_lost += 1  # dealer wins
                    break
                if dealer_hand_value < player_hand_value:
                    games_won += 1
                    print("\n " + p1_name + ", YOU win this hand!! ")
                    break

            if dealer_hand_value < 17:  # dealer must hit on less than 17...

                showing(p1_name, player_hand, player_hand_value, dealer_hand,
                        dealer_hand_value)

                print()
                line('=', 50)

                if (len(dealer_hand)) == 1:
                    print("\n Let's flip over the dealer's hole card...\n")
                    card, value = draw_card()
                    print("\n Dealer\'s hole card was a " + card)
                if (len(dealer_hand)) > 1:
                    print("\n Dealer must draw another card....\n")
                    card, value = draw_card("Manual")
                    print("\n Dealer draws a " + card + "\n")

                if card == "A":
                    dealer_high_ace += 1

                dealer_hand.append(card)
                dealer_hand_value += value
                continue

        who = ""    # the hand is over. Neither player has control.....
        win_loss_avg(games_won, games_lost)

        # to keep playing or to quit the game?
        play_or_quit = input("\n Q to quit. <ENTER> to keep playing...")
        if play_or_quit.upper() == "Q":
            print("\n\n\tThanks for playing " + p1_name + "\n\n")
            sys.exit()
        print('\n OK, let\'s play another hand...\n\n')
        continue    # any response other than q or Q will keep playing.....

# Do not edit below
if __name__ == '__main__':
    main()
