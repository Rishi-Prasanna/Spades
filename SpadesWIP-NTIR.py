# Spades
# Programmed in Python by Rishi Prasanna
# NTIR: Need To Implement Results
import sys, os, time, random

class Card:
    # suit, value and number value
    def __init__(self, suit, value, nvalue):
        self.suit = suit
        self.value = value
        self.nvalue = nvalue

class Player:
    # number of tricks
    def __init__(self, name, deck, numT, bidded, team):
        self.name = name
        self.deck = deck
        self.numT = numT
        self.bidded = bidded
        self.team = team

class Team:
    def __init__(self, points, bags):
        self.points = points
        self.bags = bags

PlayerYou = Player("You", [], 0, -1, "A") # You
PlayerLion = Player("Lion", [], 0, -1, "B") # Engine, enemy team
PlayerShark = Player("Shark", [], 0, -1, "A") # Engine, your team
PlayerSnake = Player("Snake", [], 0, -1, "B") # Engine, enemy team

stack = [] # Stack of cards. This is how you deal to players.
order = [] # Order of players.
broken = False # Are spades broken yet?

def start():
    defCards()
    shuffleCards(1000)

    # Typing text effect.
    for char in "Spade Titans!":
        sys.stdout.write(char)
        time.sleep(0.05)
    print("")


    while True:
        print("n - new game")
        print("c - credits")
        print("e - exit")
        choice = input("Pick an option: ")
        if choice == "n":
            newGame()
            shuffleCards(100)
        elif choice == "e":
            break
        else:
            print("\nError: " + choice + " is not a valid character! Try again.")
    return

def newGame():
    print("\nNew Game")
    print("Loading...")
    defCards()
    num = random.randint(10, 10000)
    # print(num)
    shuffleCards(num)
    dealCards()
    GIP()
    return

def defCards():
    # First clear the stack.
    stack.clear()

    # Step 1: Spades.
    # Create the 2-10 for spades.
    for x in range(2, 11):
        C = Card("spades",str(x),x)
        stack.append(C)
        C = Card("hearts", str(x), x)
        stack.append(C)
        C = Card("diamonds", str(x), x)
        stack.append(C)
        C = Card("clubs", str(x), x)
        stack.append(C)
    # Jack, Queen, King, Ace
    J = Card("spades", "J", 11)
    Q = Card("spades", "Q", 12)
    K = Card("spades", "K", 13)
    A = Card("spades", "A", 14)
    stack.append(J)
    stack.append(Q)
    stack.append(K)
    stack.append(A)
    J = Card("hearts", "J", 11)
    Q = Card("hearts", "Q", 12)
    K = Card("hearts", "K", 13)
    A = Card("hearts", "A", 14)
    stack.append(J)
    stack.append(Q)
    stack.append(K)
    stack.append(A)
    J = Card("diamonds", "J", 11)
    Q = Card("diamonds", "Q", 12)
    K = Card("diamonds", "K", 13)
    A = Card("diamonds", "A", 14)
    stack.append(J)
    stack.append(Q)
    stack.append(K)
    stack.append(A)
    J = Card("clubs", "J", 11)
    Q = Card("clubs", "Q", 12)
    K = Card("clubs", "K", 13)
    A = Card("clubs", "A", 14)
    stack.append(J)
    stack.append(Q)
    stack.append(K)
    stack.append(A)
    return

def shuffleCards(num): # Shuffle cards using Fisher-Yates algorithm.
    for x in range(0, num):
        for acc in range(len(stack) - 1, 0, -1):
            # Get a random index from 0 to accumulator
            rand = random.randint(0, acc)

            # Swap arr[i] with the element at random index, luckily, very easy in Python
            stack[acc], stack[rand] = stack[rand], stack[acc]
    return

def dealCards():
    for x in range(0, 13):
        PlayerYou.deck.append(stack.pop())
        PlayerLion.deck.append(stack.pop())
        PlayerShark.deck.append(stack.pop())
        PlayerSnake.deck.append(stack.pop())
    return

def PAC(): # Print all cards in stack.
    print("")
    for C in stack:
        print(C.value + " of " + C.suit)
    print("")
    return

def GIP():
    pl = FTOC()
    determineOrder(pl) # Puts players in order in array.
    """
    for x in range(0, 4):
        # print("\nPlayer " + str(x+1) + "\'s deck")
        # PPC(x)
        input("Press Enter to continue")
    """
    bid = 0
    while True:
        try:
            bid = int(float(input("How much would you like to bid? 0-13: ")))
        except ValueError:
            print("\nError: Not a number. Try again!")
            continue
        if bid < 0 or bid > 13:
            print("\nError: Must be 0 to 13!")
            continue
        else:
            break
    # print(bid)
    PlayerYou.bidded = bid

    # Each engine bids a certain number of tricks.
    PlayerLion.bidded = bidEnemy()
    PlayerSnake.bidded = bidEnemy()
    PlayerShark.bidded = bidAlly()

    # Now that you've bidded, time to start the round.

    """
    Log:
    12/29/2020: Engines automatically play a card from their deck.
    However, not of the same suit.
    I must configure the engines to play a card of the same suit, unless spades are broken.
    If spades are broken,
    and the engine has no card of the same suit,
    and the engine has spades, then make it play spades.
    If the engine has no spades, play a random card from another suit.
    If the engine has cards of the same suit, play a random card from that suit.
    If spades are not broken, play a random card from the same suit.
    """
    TN = 1
    global broken, order
    while True:
        print("\n\nTurn number: " + str(TN))
        print("Tricks bidded:")
        print("|", end='')
        for P in order:
            print(" " + P.name + ": " + str(P.bidded) + " |", end='')
        print("\nTricks won:")
        print("|", end = '')
        for P in order:
            print(" " + P.name + ": " + str(P.numT) + " |", end = '')
        print("")

        FC = Card("none","none",-1) # First card played in round, initialized.
        C = Card("none","none",-1) # Card played by each player, initialized.
        CAR = [] # Card Array to be used for determining who wins a trick.

        index = 0
        for P in order:
            if P == PlayerYou:
                print("Your deck:")
                PPC(index)
                which = -1
                while True:
                    try:
                        which = int(float(input("Which card would you like to play? 1-13: "))) - 1
                    except ValueError:
                        print("\nError: Not a number. Try again!")
                        continue
                    if which < 0 or which > 12:
                        print("\nError: Must be between 1 and 13!")
                        continue
                    else:
                        C = P.deck[which]

                        # First, check if you are the first.
                        # If you are first,
                        # and your card is a spade,
                        # and if spades are not broken,
                        # and if you do not have only spades,
                        # you cannot play spades.
                        if FC.nvalue == -1:
                            if C.suit == "spades":
                                if not broken:
                                    if not HOS(P):
                                        print("\nError: You are going first this round. Spades are not broken yet!")
                                        print("You need to only have spades to break spades if you're going first!")
                                        continue
                                    else:
                                        print("Spades are broken!")
                                        broken = True
                                        C = P.deck.pop(which)
                                        print("You played: " + C.value + " of " + C.suit)
                                        CAR.append(C)
                                        break
                                else:
                                    C = P.deck.pop(which)
                                    print("You played: " + C.value + " of " + C.suit)
                                    CAR.append(C)
                                    break
                            else:
                                C = P.deck.pop(which)
                                print("You played: " + C.value + " of " + C.suit)
                                CAR.append(C)
                                break

                        else: # If you aren't going first.
                            # Now, if you have a card of the same suit,
                            # and the card you picked is not of the same suit,
                            # you cannot play the card.
                            if HCSS(FC, P):
                                if FC.suit != C.suit:
                                    print("\nError: Card is not of the same suit as first card!")
                                    continue
                                else:
                                    C = P.deck.pop(which)
                                    print("You played: " + C.value + " of " + C.suit)
                                    CAR.append(C)
                                    break
                            # If you don't have a card of the same suit,
                            # you can play any card, including spades.
                            # If it is spades, then spades are broken!
                            else:
                                if C.suit == "spades":
                                    print("Spades are broken!")
                                    broken = True
                                    C = P.deck.pop(which)
                                    print("You played: " + C.value + " of " + C.suit)
                                    CAR.append(C)
                                    break
                                else:
                                    print("You played: " + C.value + " of " + C.suit)
                                    CAR.append(C)
                                    break
            else: # Engine's turn.
                if P == PlayerLion:
                    C = engineEnemy(FC, P)
                    print("Lion played: " + C.value + " of " + C.suit)
                    CAR.append(C)
                elif P == PlayerSnake:
                    C = engineEnemy(FC, P)
                    print("Snake played: " + C.value + " of " + C.suit)
                    CAR.append(C)
                else:
                    C = engineAlly(FC, P)
                    print("Shark played: " + C.value + " of " + C.suit)
                    CAR.append(C)
            if index == 0:
                FC = C

            index = index + 1
        TN = TN + 1

        # Now, determine who wins the trick and change positions of order.
        # If a card at a specific index of CAR is bigger than the maximum,
        # Then rotate the order until the player at a specific index of order
        # is the maximum.

        """
        Say we have:
        I go first.
        You: 8 diamonds
        Lion: K diamonds
        Shark: 3 diamonds
        Snake: J diamonds
        
        Iter 1
        You Lion Shark Snake
        
        Iter 2
        Snake You Lion Shark
        Shark Snake You Lion
        Lion Shark Snake You
        
        
        
        """
        max = 0
        ind = 0
        sind = -1
        smax = 0
        x = 0
        for A in CAR:
            # If you are dealing with a spade,
            # then smax takes over.
            if A.suit == "spades":
                if A.nvalue > smax:
                    smax = A.nvalue
                    ind = x
                    sind = x
            else:
                # If you are not dealing with spades,
                # then only cards that are the same suit as the FC
                # can be considered.
                if A.suit != FC.suit:
                    continue
                else:
                    if A.nvalue > max:
                        max = A.nvalue
                        if sind < 0:
                            ind = x
            x = x + 1
        if sind > -1:
            print(order[sind].name + " won the trick.")
            order[sind].numT = order[sind].numT + 1
            order = newOrder(order[sind])
        else:
            print(order[ind].name + " won the trick.")
            order[ind].numT = order[ind].numT + 1
            order = newOrder(order[ind])



        input("Press Enter to continue")
    return

def newOrder(P): # Create new order.
    temp = []
    # Order: You, Lion, Shark, Snake
    if P == PlayerYou:
        temp.append(PlayerYou)
        temp.append(PlayerLion)
        temp.append(PlayerShark)
        temp.append(PlayerSnake)
    elif P == PlayerLion:
        temp.append(PlayerLion)
        temp.append(PlayerShark)
        temp.append(PlayerSnake)
        temp.append(PlayerYou)
    elif P == PlayerShark:
        temp.append(PlayerShark)
        temp.append(PlayerSnake)
        temp.append(PlayerYou)
        temp.append(PlayerLion)
    else:
        temp.append(PlayerSnake)
        temp.append(PlayerYou)
        temp.append(PlayerLion)
        temp.append(PlayerShark)
    return temp

def FCID(x, C): # Find Card in Deck of a given player index.
    P = order[x]
    for card in P.deck:
        if C == card:
            return C
    return Card("none","none",-1)

def PPC(x): # Print Player's Cards.
    oneindex = 1
    for C in order[x].deck:
        print(str(oneindex) + ": " + C.value + " of " + C.suit)
        oneindex = oneindex + 1
    return

def FTOC(): # Find 2 of clubs.
    # Return the player who has the 2 of clubs.
    for C in PlayerYou.deck:
        if C.suit == "clubs" and C.nvalue == 2:
            return "PlayerYou"
    for C in PlayerLion.deck:
        if C.suit == "clubs" and C.nvalue == 2:
            return "PlayerLion"
    for C in PlayerShark.deck:
        if C.suit == "clubs" and C.nvalue == 2:
            return "PlayerShark"
    for C in PlayerSnake.deck:
        if C.suit == "clubs" and C.nvalue == 2:
            return "PlayerSnake"
    return "none"

def determineOrder(pl): # Determine order of players, given the one that goes first.
    if pl == "PlayerYou":
        order.append(PlayerYou)
        order.append(PlayerLion)
        order.append(PlayerShark)
        order.append(PlayerSnake)
    elif pl == "PlayerLion":
        order.append(PlayerLion)
        order.append(PlayerShark)
        order.append(PlayerSnake)
        order.append(PlayerYou)
    elif pl == "PlayerShark":
        order.append(PlayerShark)
        order.append(PlayerSnake)
        order.append(PlayerYou)
        order.append(PlayerLion)
    elif pl == "PlayerSnake":
        order.append(PlayerSnake)
        order.append(PlayerYou)
        order.append(PlayerLion)
        order.append(PlayerShark)
    return

def bidEnemy():
    num = random.randint(0, 13)
    return num

def bidAlly():
    num = random.randint(0, 13)
    return num

def engineEnemy(C, P): # Returns the card to be played.
    # First check whether you are the first to move.
    # If you are, then check whether spades are broken.
    # If not, play a random card of another suit.
    global broken
    if C.nvalue == -1:
        for R in P.deck:
            # If spades are not broken...
            if not broken:
                # If spade is tried, don't play it.
                if R.suit == "spades":
                    # ... unless you have only spades.
                    if HOS(P):
                        print("Spades are broken!")
                        broken = True
                        P.deck.remove(R)
                        return R
                    # If you have any other suit, play it.
                    else:
                        continue
                # Any other suit is still fair game.
                else:
                    P.deck.remove(R)
                    return R
            # Play a card of any suit if spades are broken, since it doesn't matter anymore.
            else:
                P.deck.remove(R)
                return R

    # Now, the case if you are not first.
    # First check whether you have a card of that same suit.
    # Next, check whether spades are broken.
    # If spades are not broken, play a random card from another suit.
    if HCSS(C, P):
        for R in P.deck:
            if R.suit == C.suit:
                P.deck.remove(R)
                return R
    # You don't have card of same suit.
    else:
        for R in P.deck:
            if R.suit == "spades":
                print("Spades are broken!")
                broken = True
                P.deck.remove(R)
                return R
            else:
                P.deck.remove(R)
                return R

    R = P.deck.pop()

    return R

def engineAlly(C, P):
    # First check whether you are the first to move.
    # If you are, then check whether spades are broken.
    # If not, play a random card of another suit.
    # First check whether you are the first to move.
    # If you are, then check whether spades are broken.
    # If not, play a random card of another suit.
    global broken
    if C.nvalue == -1:
        for R in P.deck:
            # If spades are not broken...
            if not broken:
                # If spade is tried, don't play it.
                if R.suit == "spades":
                    # ... unless you have only spades.
                    if HOS(P):
                        print("Spades are broken!")
                        broken = True
                        P.deck.remove(R)
                        return R
                    # If you have any other suit, play it.
                    else:
                        continue
                # Any other suit is still fair game.
                else:
                    P.deck.remove(R)
                    return R
            # Play a card of any suit if spades are broken, since it doesn't matter anymore.
            else:
                P.deck.remove(R)
                return R

    # Now, the case if you are not first.
    # First check whether you have a card of that same suit.
    # Next, check whether spades are broken.
    # If spades are not broken, play a random card from another suit.
    if HCSS(C, P):
        for R in P.deck:
            if R.suit == C.suit:
                P.deck.remove(R)
                return R
    # You don't have card of same suit.
    else:
        for R in P.deck:
            if R.suit == "spades":
                print("Spades are broken!")
                broken = True
                P.deck.remove(R)
                return R
            else:
                P.deck.remove(R)
                return R

    R = P.deck.pop()

    return R

def HCSS(C, P): # Has Card of Same Suit.
    for R in P.deck:
        if R.suit == C.suit:
            return True
    return False

def HOS(P): # Has Only Spades.
    for R in P.deck:
        if R.suit != "spades":
            return False
    return True


try:
    start()
except KeyboardInterrupt:
    print("\n\n\nForce quit.")
finally:
    print("Exiting...")
