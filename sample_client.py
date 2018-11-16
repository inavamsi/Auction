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


### Returns players who still have wealth left
def get_active_players(wealth_table):
    active_players = list(wealth_table.keys())
    for key in active_players:
        if wealth_table[key] == 0:
            active_players.remove(key)
    return active_players, active_players.__len__()


### TODO Put your bidding algorithm here
def calculate_bid(game_state, wealth, wealth_table,state):
    '''
    'game_state': current game state
    'wealth': your current wealth
    'wealth_table': dictionary of wealth of each player like {'player_name': wealth, ...}
                    *Notice that player_name is a string. Invalid player will have wealth of -1.*
    '''

    if game_state:
        print("*********WEALTH TABLE********")
        print(game_state['wealth_table'])

    return 1

def printstate(state):
    print("Item being auctioned :",state["cur_item"])
    print("Iterator : ",state["iterator"])

    for i in state["p_portfolio"]:
        print("     ",i," : ",state["p_portfolio"][i])

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

    my_tuple=(100,[])

    p_items={}  #tuple of wealth,list of paintings
    for i in wealth_table:
        p_items[i]=(wealth_table[i],[])

    state ={"name":name,"iterator":0,"cur_item":auction_items[0],"allitems":auction_items,"k":artists_num,"n":required_count,"p_portfolio":p_items,"my_portfolio":my_tuple}

    current_round = 0
    wealth = 100
    while True:
        print("")
        print("")
        print("")
        printstate(state)
        if current_round == 0:
            bid_amt = calculate_bid(None, wealth, wealth_table,state)
        else:
            bid_amt = calculate_bid(game_state, wealth, game_state['wealth_table'],state)
        client.make_bid(auction_items[current_round], bid_amt)

        # after sending bid, wait for other player
        game_state = client.receive_round()
        game_state['remain_time'] = game_state['remain_time'][name]
        if game_state['bid_winner'] == name:
            wealth -= game_state['winning_bid']
        check_game_status(game_state)

        (p_w,p_l)=state["p_portfolio"][game_state['bid_winner']]
        p_w=p_w-game_state['winning_bid']
        p_l.append(state["allitems"][state["iterator"]])
        state["p_portfolio"][game_state['bid_winner']]=(p_w,p_l)
        state["curitem"]=state["allitems"][state["iterator"]]
        if name==game_state['bid_winner']:
            state["my_portfolio"]=(p_w,p_l)
        state["iterator"]+=1
        current_round += 1
