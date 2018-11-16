import atexit
import sys

from client import Client


def check_game_status(state):
    if state['finished']:
        exit(0)


'''
The client will receive the following initial states from server.
    'artists_num': number of artists
    'required_count': number of items for artist to win
    'auction_items': list of auction items
    'player_count': number of players in the auction
-------------------------------------------------------------------
Then for each round, you will receive the game_state and current wealth,
game_state: 'finished': whether the game has finished
            'bid_item': auction item in last round
            'bid_winner': winner in last round (player_name(str))
            'winning_bid': winning bid in last round
            'remain_time': the time you have left
-------------------------------------------------------------------
You should return a whole number as the bid per turn.
'''

def get_bid(strategy):
    if strategy == 0:
        bid = 0
    elif strategy == 1:
        bid = 1
    # elif strategy == 2:
        # bid something else


# Returns list of artists in the order of nth item appearance (basically whose items I can pick up the earliest)
def get_sorted_artists(auction_items, artists, n):
    ordered_artists = []
    counter = dict.fromkeys(artists)
    for item in auction_items:
        if item in ordered_artists:
            continue
        else:
            if counter[item]:
                counter[item] += 1
            else:
                counter[item] = 1
        if counter[item] == n:
            ordered_artists.append(item)
    return ordered_artists


# Returns players who still have wealth left
def get_active_players(wealth_table):
    active_players = list(wealth_table.keys())
    for key in active_players:
        if wealth_table[key] == 0:
            active_players.remove(key)
    return active_players, active_players.__len__()


# Updates my_items
def update_my_items(game_state, my_state):
    if game_state['bid_winner'] == "kiwi_engine":
        items_i_have = my_state['items_i_have']
        items_i_have[game_state['bid_item']] += 1
        my_state['items_i_have'] = items_i_have
    return my_state


def get_next_strategy(n, p):
    #TODO: Which strategy to use - it's an integer between 1-5 (eg. 1 for first turn, 2 for number of players=2,
    # 3 for number of players = 3, 4 for )
    next_strategy = 0
    return next_strategy



def get_kiwi_state(previous_state, game_state, previous_game_state):
    #TODO: Code to get current state from previous state and game_state
    my_state = {}
    return my_state


# TODO Put your bidding algorithm here
def calculate_bid(game_state, wealth, wealth_table):

    # 'game_state': current game state
    # 'wealth': your current wealth
    # 'wealth_table': dictionary of wealth of each player like {'player_name': wealth, ...}
    #                 *Notice that player_name is a string. Invalid player will have wealth of -1.*

    if game_state:
        print("*********WEALTH TABLE********")
        print(game_state['wealth_table'])
        print("**********BID ITEM***********")
        print(game_state['bid_item'])

    # my_bid =

    return 1


def initialize():
    my_state = {}

    players = []
    artists = []
    for i in range(0, player_count):
        players.append("p" + str(i))

    for i in range(0, artists_num):
        artists.append("t" + str(i))

    items_i_have = {}
    for ele in artists:
        items_i_have[ele] = 0

    my_state['iterator']: 0
    my_state['items_i_have'] = items_i_have
    my_state['my_wealth'] = 100
    my_state['strategy'] = 0
    my_state['players_active']: (players, player_count)

    return my_state

def printstate(state):
    print("")
    print("")
    print("")
    #print("Item being auctioned :",state["cur_item"])
    print("Iterator : ",state["iterator"])

    for i in state["p_portfolio"]:
        print("     ",i," : ",state["p_portfolio"][i])

def intialise_state(name,client):
    my_tuple = (100, [])

    p_items = {}  # tuple of wealth,list of paintings
    for i in client.wealth_table:
        p_items[i] = (client.wealth_table[i], [])

    state = {"name": name, "iterator": 0, "cur_item": client.auction_items[0], "allitems": client.auction_items, "k": client.artists_num,
             "n": client.required_count, "p_portfolio": p_items, "my_portfolio": my_tuple}
    return state

def update_state(game_state,state):
    (p_w, p_l) = state["p_portfolio"][game_state['bid_winner']]
    p_w = p_w - game_state['winning_bid']
    p_l.append(state["allitems"][state["iterator"]])
    state["p_portfolio"][game_state['bid_winner']] = (p_w, p_l)
    state["curitem"] = state["allitems"][state["iterator"]]
    if name == game_state['bid_winner']:
        state["my_portfolio"] = (p_w, p_l)
    state["iterator"] += 1
    return state

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3] if len(sys.argv) == 4 else 'DiDi'

    client = Client(name, (ip, port))
    atexit.register(client.close)

    artists_num = client.artists_num
    required_count = client.required_count
    auction_items = client.auction_items
    player_count = client.player_count
    wealth_table = client.wealth_table

    current_round = 0
    wealth = 100

    # to be initialised after 1st turn
    previous_state = {}
    kiwi_state = initialize()

    state = intialise_state(name, client)
    while True:
        printstate(state)
        if current_round == 0:
            bid_amt = calculate_bid(None, wealth, wealth_table)
        else:
            bid_amt = calculate_bid(game_state, wealth, game_state['wealth_table'])
        client.make_bid(auction_items[current_round], bid_amt)

        # after sending bid, wait for other player
        game_state = client.receive_round()
        game_state['remain_time'] = game_state['remain_time'][name]
        if game_state['bid_winner'] == name:
            wealth -= game_state['winning_bid']
        check_game_status(game_state)

        state = update_state(game_state, state)
        current_round += 1
