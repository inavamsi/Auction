import atexit
import sys
import random
import copy
import time
import math

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


# Returns list of artists in the order of nth item appearance (basically whose items I can pick up the earliest at
# every state)
def get_sorted_artists_dynamic(state):
    artists = state['artists']
    ordered_artists = []
    iterator = state['iterator']
    remaining_auction_items = state["aucitems"][iterator:]
    counter = dict.fromkeys(artists)
    left_items_per_artist = {artist: left_to_win(state, artist) for artist in artists}
    for item in remaining_auction_items:
        if item in ordered_artists:
            continue
        else:
            if counter[item]:
                counter[item] += 1
            else:
                counter[item] = 1
        if counter[item] >= left_items_per_artist[item]:
            ordered_artists.append(item)
    return ordered_artists



# Returns players who still have wealth left
def get_active_players(wealth_table):
    active_players = list(wealth_table.keys())
    for key in active_players:
        if wealth_table[key] == 0:
            active_players.remove(key)
    return active_players, active_players.__len__()

def get_next_strategy(n, p):
    #TODO: Which strategy to use - it's an integer between 1-5 (eg. 1 for first turn, 2 for number of players=2,
    # 3 for number of players = 3, 4 for )
    next_strategy = 0
    return next_strategy

# TODO Put your bidding algorithm here
def calculate_bid(game_state, wealth, wealth_table,state):

    # 'game_state': current game state
    # 'wealth': your current wealth
    # 'wealth_table': dictionary of wealth of each player like {'player_name': wealth, ...}
    #                 *Notice that player_name is a string. Invalid player will have wealth of -1.*

    #if game_state:
     #   print("*********WEALTH TABLE********")
     #   print(game_state['wealth_table'])
     #   print("**********BID ITEM***********")
     #   print(game_state['bid_item'])

    # my_bid =
    if state['strategy'] == 'all_out':
        bid = state['my_wealth']
        return makebid(state, bid)

    if state['strategy'] == 'patience':
        bid = 1
        return makebid(state,bid)

    if state['strategy'] == 'first':
        bid= random.randint(1,2)
        return makebid(state,bid)

    if state['strategy'] == 'block':
        if state['p']==2:
            opp=state['risk'][0]
            bid=state['p_portfolio'][opp]['wealth']+0.1
            return makebid(state,bid)
        else:
            maxbid=0
            for opp in state['risk']:
                maxbid = max(state['p_portfolio'][opp]['wealth']>maxbid)
            time.sleep(2)
            return makebid(state,maxbid+1)

    if state['strategy'] == 'greedy':
        bid=state['i_wanna_bid'][state['cur_item']]
        return makebid(state,bid)

    # if state['strategy'] == 'main_strategy':


    return makebid(state,1)


def makebid(state, bid):
    return math.ceil(max(0,min(bid, state['my_wealth'])))


def left_to_win(state, a):
    return state['n'] - state['items_i_have'][a]


def opp_winning(state):
    winners=[]
    for p in state['players']:
        for a in state['artists']:
            if state['p_portfolio'][p][a] == state['n']-1 and state['cur_item'] == a:
                winners.append(p)

    return winners


def want_2bid(state, a):
    #my_bid_history  # my bid history for this artist
    #won_artist_latest  # did i win the latest item of this artist
    #my_prev_winbid  # my prev winning amt for this bid
    #prev_winner_fora  # person who won this artist last
    #prev_win_bid  # prev winning amt for this item
    l=get_sorted_artists_dynamic(state)
    ptarget=l[0]
    starget=l[1]
    prev_winner=state['prev_winner_fora'][a]
    if(prev_winner==None):
        prev_winner_short_of=state['n']
        opp_avg_bid=100/state['n']
    else:
        prev_winner_short_of = state['n'] - state['p_portfolio'][prev_winner][a]
        opp_avg_bid = (state['p_portfolio'][prev_winner]['wealth'] / prev_winner_short_of)

    prev_winning_bid=state['prev_win_bid'][a]
    my_bid_his_a=state['my_bid_history'][a]
    me_short_of=left_to_win(state,a)
    my_avg_bid=(state['my_wealth']/me_short_of)


    if(prev_winner==state['name']):
        if (ptarget == a):
            ratio = (state['n'] + 1 - me_short_of) / state['n']
            ratio = ratio * ratio / state['n']

            maxbid=0
            for p in state['players']:
                pd=state['p_portfolio'][p]
                if(state['n']-pd[a] < state['n']/2 and p!=state['name']):
                    maxbid=(pd['wealth']/(state['n']-pd[a]))

            c=0
            d=0
            if(maxbid<my_avg_bid):
                c=maxbid+1

            if (me_short_of == 2):
                d = state['my_wealth'] / 3

            state['i_wanna_bid'][a] = max(ratio * state['my_wealth'],c, d)

        elif (starget == a):
            ratio = (state['n'] + 1 - me_short_of) / state['n']
            ratio = ratio * ratio / state['n']
            c = 0
            d = 0
            if (me_short_of == 2):
                d = state['my_wealth'] / 3

            state['i_wanna_bid'][a] = 0.5 * max(ratio * state['my_wealth'], d)

        else:
            state['i_wanna_bid'][a] = 0
            if (me_short_of == 2):
                state['i_wanna_bid'][a] -=2
                state['i_wanna_bid']=min(state['i_wanna_bid'],state['my_wealth']/6)
            if (state['n'] > 30):
                state['i_wanna_bid'][a] = 0.1


    else:
        if(ptarget==a):
            ratio=(state['n']+1 -me_short_of)/state['n']
            ratio=ratio*ratio/state['n']
            c=0
            d=0
            if(prev_winner_short_of==2):
                if(my_avg_bid>opp_avg_bid):
                    c=opp_avg_bid+random.random()
            if(me_short_of==2):
                d=state['my_wealth']/3

            maxbid = 0
            for p in state['players']:
                pd = state['p_portfolio'][p]
                if (state['n'] - pd[a] < state['n'] / 2 and p!=state['name']):
                    maxbid = (pd['wealth'] / (state['n'] - pd[a]))

            e = 0
            if (maxbid < my_avg_bid):
                e = maxbid + 1

            state['i_wanna_bid'][a]=max(ratio*state['my_wealth'],c,d,e)

        elif (starget == a):
            ratio = (state['n'] + 1 - me_short_of) / state['n']
            ratio = ratio * ratio / state['n']
            c=0
            if (prev_winner_short_of == 2):
                if (my_avg_bid > opp_avg_bid):
                    c = opp_avg_bid + random.randomint(0, 1)
            d=0
            if (me_short_of == 2):
                d = state['my_wealth'] / 3

            state['i_wanna_bid'][a] = 0.5*max(ratio * state['my_wealth'], c, d)

        else :
            state['i_wanna_bid'][a]=0.1
            if(me_short_of==2):
                state['i_wanna_bid'][a]=state['my_wealth']/4
            if(my_avg_bid>opp_avg_bid and prev_winner_short_of<3):
                state['i_wanna_bid'][a]=opp_avg_bid-my_avg_bid
            if(state['n']>30):
                state['i_wanna_bid'][a] = 0

    return state

def set_strategy(state):
    for a in state['artists']:
        if state['cur_item']==a and left_to_win(state,a)==1:
            state['strategy']='all_out'
            return state

    if(state['iterator']<10 and state['n']<20):
        state['startegy']='first'
        return state

    if(state['iterator']<state['n']):
        state['strategy']='patience'
        return state



    opp_winners=opp_winning(state)
    if(opp_winners!=[]):
        state['strategy']='block'
        state['risk']=opp_winners
        return state



    state['strategy']='greedy'
    for a in state['artists']:
        state=want_2bid(state,a)
    return state


def initialize(name,client):
    my_state = {}

    players = []
    artists = []
    for i in client.wealth_table:
        players.append(i)

    for i in range(0, client.artists_num):
        artists.append("t" + str(i))

    items_i_have = {}
    for ele in artists:
        items_i_have[ele] = 0

    p_items = {}  # tuple of wealth,list of paintings
    for i in client.wealth_table:
        p_items[i] = {}
        p_items[i]['wealth']=100
        p_items[i]['all_items']=[]
        p_items[i]['win_bids']=[]
        for ele in artists:
            p_items[i][ele] = 0

    prev_win_bid={}
    for a in artists:
        prev_win_bid[a]=0

    prev_winner_fora={}
    for a in artists:
        prev_winner_fora[a]=None

    my_bid_history={}
    for a in artists:
        my_bid_history[a]=[0]

    won_artist_latest={}
    for a in artists:
        won_artist_latest[a]=False

    i_wanna_bid={}
    for a in artists:
        i_wanna_bid[a]=0

    my_prev_winbid={}
    for a in artists:
        my_prev_winbid[a]=0


    my_state['my_bid_history']=my_bid_history               #my bid history for this artist
    my_state['won_artist_latest'] = won_artist_latest          # did i win the latest item of this artist
    my_state['my_prev_winbid'] = my_prev_winbid         #my prev winning amt for this bid
    my_state['prev_winner_fora']=prev_winner_fora       #person who won this artist last
    my_state['i_wanna_bid']=i_wanna_bid
    my_state['prev_bid']=0

    my_state['prev_win_bid']=prev_win_bid       #prev winning amt for this item
    my_state['strategy']="patience"
    my_state['risk']=[]
    my_state['players']=players
    my_state['artists']=artists

    my_state['iterator']=0
    my_state['items_i_have'] = items_i_have
    my_state['my_wealth'] = 100
    my_state['strategy'] = 0
    my_state['players_active']=(players, player_count)
    my_state["name"]=name
    my_state["cur_item"]=client.auction_items[0]
    my_state["aucitems"]= client.auction_items
    my_state["k"]= client.artists_num
    my_state["n"]= client.required_count
    my_state['p']=player_count
    my_state["p_portfolio"]= p_items

    return my_state

def printstate(state):
    print("")
    print("")
    print("")
    print("Item being auctioned :",state["cur_item"])
    print("Iterator : ",state["iterator"])

    for i in state["p_portfolio"]:
        print("     ",i," : ",state["p_portfolio"][i])


def update_state(game_state,state):
    state['iterator'] += 1
    cur_artist=(int)(state['cur_item'][1])
    prev_artist=state['aucitems'][state['iterator']-1]
    pstate = state["p_portfolio"][game_state['bid_winner']]
    pstate['wealth'] =pstate['wealth'] - game_state['winning_bid']
    pstate['all_items'].append(state["cur_item"])
    pstate['win_bids'].append(game_state['winning_bid'])
    pstate[state['cur_item']]= pstate[state['cur_item']]+1
    state["p_portfolio"][game_state['bid_winner']] = pstate

    state['prev_win_bid'][prev_artist] = game_state['winning_bid']
    state['my_bid_history'][prev_artist].append(state['prev_bid'])
    state['won_artist_latest'][prev_artist]= (game_state['bid_winner'] == state['name'])
    state['prev_winner_fora'][prev_artist]=game_state['bid_winner']
    if(game_state['bid_winner'] == state['name']):
        state['won_artist_latest'][prev_artist] = True
        state['my_prev_winbid']['prev_artist'] = game_state['winning_bid']
    else:
        state['won_artist_latest'][prev_artist]=False


    if state["name"] == game_state['bid_winner']:
        state['my_wealth']= state['my_wealth'] - game_state['winning_bid']
        state['items_i_have'][cur_artist] = state['items_i_have'][state['cur_item']] + 1

    state["cur_item"] = state["aucitems"][state["iterator"]]

    state=set_strategy(state)
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

    kiwi_state = initialize(name,client)

    while True:
        printstate(kiwi_state)
        if current_round == 0:
            bid_amt = calculate_bid(None, wealth, wealth_table,kiwi_state)
            kiwi_state['prev_bid']=bid_amt
        else:
            bid_amt = calculate_bid(game_state, wealth, game_state['wealth_table'],kiwi_state)
            kiwi_state['prev_bid'] = bid_amt
        client.make_bid(auction_items[current_round], bid_amt)

        # after sending bid, wait for other player
        game_state = client.receive_round()
        game_state['remain_time'] = game_state['remain_time'][name]
        if game_state['bid_winner'] == name:
            wealth -= game_state['winning_bid']
        check_game_status(game_state)

        kiwi_state = update_state(game_state, kiwi_state)
        current_round += 1
