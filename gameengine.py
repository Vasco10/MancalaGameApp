import easyAI
from copy import copy
import random
from characters import AI_LIST

USER = 1
AI = 2

PLAYER_LIST = [USER, AI]

#
#   BOARD LAYOUT
#
#     13   12   11   10   09   08        AI
# 14                               07
#     01   02   03   04   05   06        USER
#
# HAND = 00

HOUSE_LIST = {
    USER: [1, 2, 3, 4, 5, 6],
    AI: [8, 9, 10, 11, 12, 13]
}
STORE_IDX = {
    USER: 7,
    AI: 14
}
HAND = 0


OWNER = 0
NEXT = 1
ROLE = 2
OPP = 3
DISTPIT = 4

HOUSE=88
STORE=99

#     13   12   11   10   09   08        AI
# 14                               07
#     01   02   03   04   05   06        USER
P = {
     1: {OWNER: USER, NEXT: {USER:  2, AI:  2}, ROLE: HOUSE, OPP: 13, DISTPIT: {USER:  6, AI: 12}},
     2: {OWNER: USER, NEXT: {USER:  3, AI:  3}, ROLE: HOUSE, OPP: 12, DISTPIT: {USER:  5, AI: 11}},
     3: {OWNER: USER, NEXT: {USER:  4, AI:  4}, ROLE: HOUSE, OPP: 11, DISTPIT: {USER:  4, AI: 10}},
     4: {OWNER: USER, NEXT: {USER:  5, AI:  5}, ROLE: HOUSE, OPP: 10, DISTPIT: {USER:  3, AI:  9}},
     5: {OWNER: USER, NEXT: {USER:  6, AI:  6}, ROLE: HOUSE, OPP:  9, DISTPIT: {USER:  2, AI:  8}},
     6: {OWNER: USER, NEXT: {USER:  7, AI:  8}, ROLE: HOUSE, OPP:  8, DISTPIT: {USER:  1, AI:  7}},
     7: {OWNER: USER, NEXT: {USER:  8, AI:  8}, ROLE: STORE, OPP: -1, DISTPIT: None},
     8: {OWNER: AI  , NEXT: {USER:  9, AI:  9}, ROLE: HOUSE, OPP:  6, DISTPIT: {USER: 12, AI:  6}},
     9: {OWNER: AI  , NEXT: {USER: 10, AI: 10}, ROLE: HOUSE, OPP:  5, DISTPIT: {USER: 11, AI:  5}},
    10: {OWNER: AI  , NEXT: {USER: 11, AI: 11}, ROLE: HOUSE, OPP:  4, DISTPIT: {USER: 10, AI:  4}},
    11: {OWNER: AI  , NEXT: {USER: 12, AI: 12}, ROLE: HOUSE, OPP:  3, DISTPIT: {USER:  9, AI:  3}},
    12: {OWNER: AI  , NEXT: {USER: 13, AI: 13}, ROLE: HOUSE, OPP:  2, DISTPIT: {USER:  8, AI:  2}},
    13: {OWNER: AI  , NEXT: {USER:  1, AI: 14}, ROLE: HOUSE, OPP:  1, DISTPIT: {USER:  7, AI:  1}},
    14: {OWNER: AI  , NEXT: {USER:  1, AI:  1}, ROLE: STORE, OPP: -1, DISTPIT: None},
}
ALL_PITS = range(1, 15)

ACTION = "action"
COUNT = "count"
LOC = "loc"

BALANCE = 0
GREED = 1
CAUTION = 2

class MancalaAI(easyAI.Negamax, object):

    def __init__(self, settings):
        self.settings = settings
        self.set_character()
        super(MancalaAI, self).__init__(self.character['lookahead'])

    def _random_move(self, game):
        possible_moves = game.possible_moves()
        return random.choice(possible_moves)

    def set_character(self):
        self.character = AI_LIST[self.settings["ai_chosen"]]
        self.depth = self.character['lookahead']

    def __call__(self, game):
        if self.character['strategy'] == "random":
            return self._random_move(game)
        if self.character['error_rate'] > 0.0:
            chance = random.random()
            if chance < self.character['error_rate']:
                return self._random_move(game)
        return super(MancalaAI, self).__call__(game)


class KalahHumanPlayer(easyAI.Human_Player):
    pass

class KalahAIPlayer(easyAI.AI_Player):
    
    def set_character(self):
        self.AI_algo.set_character()

class KalahGame(easyAI.TwoPlayersGame):

    def __init__(self, settings):
        self.settings = settings
        self.players = [
            KalahHumanPlayer(),
            KalahAIPlayer(MancalaAI(self.settings))
        ]
        self.set_character()
        self.nplayer = self.settings['first_player']
        self.animate = []
        self.want_animation = False
        self.board = [0]*15
        self.reset_board(empty=True)

    def set_character(self):
        self.character = AI_LIST[self.settings["ai_chosen"]]
        self.players[1].set_character()

    def is_stopping_in_own_store(self, pit):
        count = self.board[pit] % 13  # if seeds > 12 then they wrap around board; so modulo 13
        return count == P[pit][DISTPIT][self.nplayer]
        
    def possible_moves(self):
        move_list = [[pit] for pit in self.possible_moves_choices()]
        completed_list = []
        self.recurse_moves(move_list, completed_list)
        return completed_list

    def recurse_moves(self, move_list, completed_list):
        for move in move_list:
            last_pit = move[-1]
            if self.is_stopping_in_own_store(last_pit):
                board_copy = copy(self.board)
                self.make_move_choice(last_pit)
                more_choices = self.possible_moves_choices()
                if more_choices:
                    next_todo = []
                    for pit in more_choices:
                        next_todo.append(move+[pit])
                    self.recurse_moves(next_todo, completed_list)
                else:
                    completed_list.append(move)
                self.board = board_copy
            else:
                completed_list.append(move)

    def possible_moves_choices(self):
        possible = []
        for house in HOUSE_LIST[self.nplayer]:
            if self.board[house]:
                possible.append(house)
        return possible

    def judge_best_of_equal_moves(self, move_tuples):
        best_move, board = move_tuples[0]  # setting default
        lowest_count = 9999
        for move, board in move_tuples:
            if board[STORE_IDX[AI]] < lowest_count:
                lowest_count = board[STORE_IDX[AI]]
        best_score = -9999
        for index, tup in enumerate(move_tuples):
            move, board = tup
            score = self.judge_a_board(board, lowest_count)
            print "JUDGE", move, board, score
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def judge_a_board(self, board, base_score):
        # we will judge a board on
        #   1. each seed above base in AI store: +5
        #   2. empty pit 13: +8
        #   3. empty pit 12: +4
        #   4. pit 12 with 1: +2
        # if capture allowed:
        #   5. each pit with seeds across from empty: -1 per seed
        #   6. easy next capture seen: 4 per seed
        score = 0
        score += (board[STORE_IDX[AI]] - base_score) * 5
        if board[13] == 0:
            score += 8
        if board[12] == 0:
            score += 4
        if board[12] == 1:
            score += 2
        if self.settings['capture_rule'] != 0:
            return score
        for pit in HOUSE_LIST[AI]:
            seeds = board[pit]
            if seeds:
                # each pit with seeds across from empty
                opp_seeds = board[P[pit][OPP]]
                if opp_seeds == 0:
                    score -= seeds * 1
                # easy next capture
                future_pit = pit
                for _ in range(seeds):
                    future_pit = P[future_pit][NEXT][AI]
                if board[future_pit] == 0:
                    if P[future_pit][OWNER] == AI:
                        if P[future_pit][ROLE] == HOUSE:
                            opp_seeds = board[P[future_pit][OPP]]
                            score += opp_seeds * 4
        return score
        

    def animated_play_move(self, move):
        self.want_animation = True
        self.play_move(move)
        self.want_animation = False

    def make_move(self, move):
        self.animate = []
        for pit in move:
            self.make_move_choice(pit)

    def make_move_choice(self, house):
        if self.want_animation:
            self.animate.append({ACTION: "normal_move"})
        # scoop up the house chosen
        self._scoop(house)
        current_house = house
        # drop the seeds into the pits
        for ctr in range(self.board[HAND]):
            next_house = P[current_house][NEXT][self.nplayer]
            self._drop(next_house)
            current_house = next_house
        #
        # capture if possible
        #
        if self.settings['capture_rule'] == 0:  # capture if opposite is full
            if self.board[current_house] == 1:
                if P[current_house][OWNER] == self.nplayer:
                    if P[current_house][ROLE] == HOUSE:
                        if self.board[P[current_house][OPP]]:
                            if self.want_animation:
                                self.animate.append({ACTION: "steal"})
                            self._scoop(current_house)
                            self._scoop(P[current_house][OPP])
                            self._drop_all(STORE_IDX[self.nplayer])
        elif self.settings['capture_rule'] == 1: # capture even if opposite is empty       
            if self.board[current_house] == 1:
                if P[current_house][OWNER] == self.nplayer:
                    if P[current_house][ROLE] == HOUSE:
                        if self.want_animation:
                            self.animate.append({ACTION: "steal"})
                        self._scoop(current_house)
                        if self.board[P[current_house][OPP]]:
                            self._scoop(P[current_house][OPP])
                        self._drop_all(STORE_IDX[self.nplayer])
        # elif settings['capture_rule'] == 2: # no capture
        #     pass
        #
        # end of game scooping
        #
        if self.is_over():
            if self.want_animation:
                self.animate.append({ACTION: "game_over"})
            if self.settings['eog_rule'] == 0:
                # traditional end-of-game handling: both players scoop own houses into store
                for player in PLAYER_LIST:
                    for house in HOUSE_LIST[player]:
                        if self.board[house]:
                            self._scoop(house)
                    if self.board[HAND]:
                        self._drop_all(STORE_IDX[player])
            elif self.settings['eog_rule'] == 1:
                # put seed in store of player who does not have seeds
                if any([self.board[house] for house in HOUSE_LIST[USER]]):
                    empty_player = AI
                else:
                    empty_player = USER
                for player in PLAYER_LIST:
                    for house in HOUSE_LIST[player]:
                        if self.board[house]:
                            self._scoop(house)
                    if self.board[HAND]:
                        self._drop_all(STORE_IDX[empty_player])
            elif self.settings['eog_rule'] == 2:
                # put seeds in store of player who ended game (current player)
                for player in PLAYER_LIST:
                    for house in HOUSE_LIST[player]:
                        if self.board[house]:
                            self._scoop(house)
                    if self.board[HAND]:
                        self._drop_all(STORE_IDX[self.nplayer])
            # elif self.settings['eog_rule'] == 3:
            #     # leave seeds alone
            #     pass
    
    def is_over(self):
        for player in PLAYER_LIST:
            has_seed = False
            for house in HOUSE_LIST[player]:
                if self.board[house]:
                    has_seed = True
            if has_seed is False:
                return True
        return False

    def show(self):
        print "player: {} with score {}".format(self.nplayer, self.scoring())
        print "hand: {}".format(self.board[HAND])
        print "board:\n"
        print "          13   12   11   10   09   08      AI"
        print "         "+" ".join(
            ["[{:02d}]".format(self.board[pit]) for pit in reversed(HOUSE_LIST[AI])]
        )
        print "    [{:02d}]                               [{:02d}]".format(
            self.board[STORE_IDX[AI]], self.board[STORE_IDX[USER]]
        )
        print "         "+" ".join(
            ["[{:02d}]".format(self.board[pit]) for pit in HOUSE_LIST[USER]]
        )
        print "          01   02   03   04   05   06      USER"

    def scoring(self, player=None):
        if player is None:
            player = self.nplayer
        other = USER if player==AI else AI        
        return self.board[STORE_IDX[player]] - self.board[STORE_IDX[other]]

#    def unmake_move(self, move):
#        pass

    def ttentry(self):
        return "Mancala (Kalah) Game"

    def reset_board(self, restoration=False, empty=False):
        self.want_animation = True
        #
        # manipulate basic settings
        #
        self.seeds_per_house = self.settings['seeds_per_house']
        #
        # manipulate board
        #
        if self.want_animation:
            self.animate = [{ACTION: "setting_up"}]
        # determine new board
        if restoration:
            new_board = copy(self.board)
            self.board = [12*self.seeds_per_house] + [0]*14
        else:
            if empty:
                self.board = [12*self.seeds_per_house] + [0]*14
                new_board = copy(self.board)
            else:
                new_board = [0] + \
                            [self.seeds_per_house] * 6 + [0] + \
                            [self.seeds_per_house] * 6 + [0]
        for pit in ALL_PITS:
            if self.board[pit]:
                self._scoop(pit)
        for pit in ALL_PITS:
            if new_board[pit]:
                self._drop(pit, count=new_board[pit])
        self.board[HAND] = 0  # this is for error recovery. In theory, you
                              # should never needs this as the hand will be
                              # empty already.
        #
        # manipulate AI character
        #
        self.set_character()
        #
        # set nplayer
        #
        if not restoration:
            self.nplayer = self.settings['first_player']
        self.want_animation = False

    def _scoop(self, pit):
        self.board[HAND] += self.board[pit]
        self.board[pit] = 0
        if self.want_animation:
            self.animate.append({ACTION: "scoop", LOC: pit})

    def _drop(self, pit, count=1):
        self.board[HAND] -= count
        self.board[pit] += count
        if self.want_animation:
            self.animate.append({ACTION: "drop", LOC: pit, COUNT: count})

    def _drop_all(self, pit):
        count = self.board[HAND]
        self.board[pit] += self.board[HAND]
        self.board[HAND] = 0
        if self.want_animation:
            self.animate.append({ACTION: "drop_all", LOC: pit, COUNT: count})

    def get_winner(self):
        user_score = self.scoring(player=USER)
        ai_score = self.scoring(player=AI)
        if user_score>ai_score:
            return USER
        if user_score<ai_score:
            return AI
        return 0

    def get_animation(self):
        return self.animate

    def usermove_start_simulation(self):
        self.want_animation = True
        self.animate = []
        self.original_board = copy(self.board)

    def usermove_simulate_choice(self, choices_so_far):
        self.animate = []
        current_choice = choices_so_far[-1]
        self.make_move_choice(current_choice)

    def usermove_finish_simulation(self):
        self.animate = []
        self.board = self.original_board
        self.want_animation = False


if __name__=="__main__":
    settings = {
        "ai_chosen": 4,
        "who_plays_first": 0,
        "first_player": USER,
        "seeds_per_house_selection": 1,
        "seeds_per_house": 4,
        "capture_rule": 0,
        "eog_rule": 0,
        "seed_drop_rate": 0.4,
    }
    character = AI_LIST[settings['ai_chosen']]

    game = KalahGame(settings)
    game.reset_board()

    while not game.is_over():
        # print game.animate
        game.show()
        if game.nplayer==USER:
            poss = game.possible_moves()
            for index, move in enumerate(poss):
                print index, move
            index = int(input("enter move:"))
            move = poss[index]
        else:
            move = game.get_move()
            if "move_fitness_list" in dir(game):
                print "Move rankings:", game.move_fitness_list
            print "AI plays", move
        game.play_move(move)
    print
    print "GAME OVER!"
    print
    print game.show()
    print
    print "RESULT:", ["TIE", "USER WON", "AI WON"][game.get_winner()]
