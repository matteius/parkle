## Parkle 0.0
##
## Bradley Zeis
## Zoli Kahn

import random
rand = random.Random()

class ParkleView(object):
    def __init__(self):
        self.game = None
        self.current_player = None
        self.winning_player = None

    def start_game(self):
        """Setup the player list and the view environmant, if necessary.
        
        Always end this method with a call to begin_game.
        """
        pass

    def begin_game(self, players):
        """Instantiate the game and begin it.
        
        Do not override in subclasses.
        """
        self.game = Parkle(self)
        self.game.players = players
        self.current_player = None
        self.winning_player = None
        self.winning_player = self.game.start_game()
        self.end_game()

    def end_game(self):
        pass

    def start_round(self):
        pass

    def end_round(self):
        pass

    def start_turn(self):
        pass

    def end_turn(self):
        pass

    def roll(self, dice):
        pass

    def decide(self):
        pass

    def invalid_decision(self):
        pass


class Parkle(object):
    def __init__(self, view):
        self.view = view
        self.goal = 10000
        self.players = []
    
    def roll(self, n):
        """Return list of n  (1 <= n <= 6) random numbers from 1 to 6.

        Return value will be sorted by increasing value
        
        Return:
            [[value, number of value], ...]

            [[3, 2], [4, 4]] == Pair of 3s, four 4s.
        """
        l = []
        for i in range(0, n):
            l.append(rand.randint(1,6))

        d = []
        for i in range(1, 7):
            c = l.count(i)
            if c == 0:
                continue

            d.append([i, c])
            
        return d

    def start_game(self):
        """Return winning player.
        
        Return: ParklePlayer
        """
        if len(self.players) == 0:
            return None

        for p in self.players:
            p.game = self
            p.score = 0
        
        rand.seed()
        while 1:

            self.view.start_round()

            for p in self.players:
                r = self.turn(p)
                if r == -1:
                    return None

            self.view.end_round()

            for p in self.players:
                if p.score >= self.goal:
                    return p
    
    def turn(self, player):
        self.view.current_player = player
        self.view.start_turn()
        player.rolls = 0
        player.kept = []
        player.begin_turn()

        res = 0

        n = 6
        round_score = 0
        reroll = True
        lost = False
        while 1:
            if reroll:
                d = self.roll(n);
                player.rolls += 1

            reroll = True

            self.view.roll(list(d))

            if not self.points_possible(list(d)):
                player.kept = []
                round_score = 0
                lost = True
                break

            result = player.decide(list(d), round_score)
            self.view.decide()

            #if r == 0:
            #   break

            if result == -1:
                res = -1;
                break

            ## Determine if newest kept-sets are valid
            ## If invalid, remove new sets from kept, start over with same roll
            try:
                group = player.kept[-1]
            except:
                self.view.invalid_decision()
                reroll = False
                continue

            c = 0

            groupscore = 0
            for keptset in group:
                setscore = self.calculate_one_keptset(keptset)
                c += len(keptset)
                if not setscore:
                    self.view.invalid_decision()
                    player.kept = player.kept[:-1]
                    reroll = False
                    break
                else:
                    groupscore += setscore

            if not reroll:
                continue

            round_score += groupscore

            if result == 0:
                break

            n -= c
            if n == 0:
                n = 6
            elif n < 0 or n > 6:
                player.kept = []
                s = 0
                break

        if not lost:
            player.score += round_score
        self.view.end_turn(round_score)
        return res

    def points_possible(self, dice):
        """Determine if it is possible to score points with dice.
        
        Return: boolean
        """
        num_pairs = 0
        for i in dice:
            if i[0] == 1 or i[0] == 5:
                return True

            if i[1] >= 3:
                return True

            if i[1] == 2:
                num_pairs += 1

            if num_pairs == 3:
                return True

        return False

    def calculate_one_keptset(self, kset):
        """Calculate number of points for a single item in a kept set.
        
        Return: int
        """
        if len(kset) == 1:
            if kset[0] == 1:
                return 100
            if kset[0] == 5:
                return 50
            return 0

        elif len(kset) == 2:
            s = 0
            for i in kset:
                if i == 1:
                    s += 100

                elif i == 5:
                    s += 50

                else:
                    return 0

            return s

        elif len(kset) == 3:
            if kset[0] == kset[1] and kset[0] == kset[2]:
                if kset[0] == 1:
                    return 300;
                elif 2 <= kset[0] <= 6:
                    return 100 * kset[0]
            return 0

        elif len(kset) == 4:
            if kset[0] == kset[1] and kset[0] == kset[2] and kset[0] == kset[3]:
                return 1000
            return 0

        elif len(kset) == 5:
            if kset[0] == kset[1] and kset[0] == kset[2] and kset[0] == kset[3] and kset[0] == kset[4]:
                return 2000
            return 0

        elif len(kset) == 6:
            if kset[0] == kset[1] and kset[0] == kset[2] and kset[0] == kset[3] and kset[0] == kset[4] and kset[0] == kset[5]:
                return 3000
            else:
                num_pairs = 0
                num_triples = 0
                num = {}

                for i in range(1,7):
                    c = kset.count(i)
                    num[i] = c
                    if c == 2:
                        num_pairs += 1
                    if c == 3:
                        num_triples += 1

                ## Three Pairs
                if num_pairs == 3:
                    return 1500

                ## Two Triples
                if num_triples == 2:
                    return 1500

                ## Straight
                if num.values().count(1) == 6:
                    return 3000

                return 0

        return 0;


class ParklePlayer(object):
    def __init__(self):
        self.game = None
        self.name = ""
        self.score = 0;
        self.kept = []; # [[[1, 1], [5]], [[3, 3, 3]]] = Pair of 2s and a 5 kept first roll, triple 3s kept second roll
                        # Each sublist is called a "kept-set"
        self.rolls = 0

    def begin_turn(self):
        """User-defined setup method for the beginning of a turn.
        
        No altering of kept should be done here, only pre-calculations.

        Return: None
        """
        pass

    def decide(self, dice, round_score):
        """Create a group of keptsets, append the group to self.kept.
        
        Do NOT:
            Change any scores or roll counts
            Call any methods of a Parkle instance
        
        Return: int
        """
        pass

    def copy_dice(self, dice):
       d = []
       for i in dice:
           d.append(list(i))
       return d


class ParkleConsoleView(ParkleView):
    def start_game(self):
        print "Parkle\n----------------\n"

        players = []
        while(1):
            print "Add Player:"
            if len(players) < 2:
                print "\t(h)uman player\n\t(a)i player\n\t(q)it\n"

            else:
                print "\tAdd (h)uman player\n\t(a)i player\n\t(s)tart game\n\t(q)uit\n"

            r = raw_input(":")

            if r.lower() == "q":
                return

            elif r.lower() == "s":
                if len(players) >= 2:
                    break
                print "You must have at least two players to start."
                continue

            elif r.lower() == "h":
                p = ParkleRealPlayer()
                p.name = raw_input("Player Name: ")
                players.append(p)
                continue

            elif r.lower() == "a":
                path = raw_input("File path: ")
                class_name = raw_input("Class Name: ")
                ## Load ai player
                continue

            else:
                continue

        self.begin_game(players)

    def start_round(self):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        for p in self.game.players:
            print p.name,
            print ": ", p.score

        print

    def start_turn(self):
        print "--------------------------------------------------------------------------------"
        print "{0}'s turn.\n\tScore: {1}".format(self.current_player.name, self.current_player.score)

    def end_turn(self, round_score):
        print "\nRound Score: {0}\nTotal Score: {1}\n".format(round_score, self.current_player.score)

    def roll(self, dice):
        print "Roll {0}:\n\t".format(self.current_player.rolls),
        for i in dice:
            for j in range(i[1]):
                print i[0],
        print

#    def decide(self):
#        for i in self.current_player.kept:
#            print i,
#
#        print
    
    def invalid_decision(self):
        print "Decision invalid, please select something else."


class ParkleRealPlayer(ParklePlayer):
    def begin_turn(self):
        pass

    def decide(self, dice, round_score):
        d = self.copy_dice(dice)
        group = []      ## Group of keptsets from this roll
        keptset = []
        group.append(keptset)
        first = True
        while 1:

            if not first:
                print "\t",
                for i in d:
                    for j in range(i[1]):
                        print i[0],

                print

            first = False

            for i in self.kept:
                for j in i:
                    print j,

            if len(self.kept):
                print "|",

            for k in group:
                print k,
            
            print "\n(Round Score: {0})".format(round_score)

            print "\nWhat would you like to keep?"
            k = raw_input(":")

            if k == "c":
                self.kept.append(group)
                print "----------------\n"
                return 1

            elif k == "s":
                self.kept.append(group)
                return 0

            elif k == "n":
                keptset = []
                group.append(keptset)
                continue

            elif k == "q":
                return -1

            elif k == "p":
                d = self.copy_dice(dice)
                group = []
                keptset = []
                group.append(keptset)
                continue
            
            else:
                try:
                    i = int(k)
                except:
                    continue

                for j in d:
                    if j[0] == i and j[1] >= 1:
                        j[1] -= 1
                        keptset.append(i)
                        break
