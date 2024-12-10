# In[1]:
from Game import *
from Game.minimax import *
from copy import deepcopy
from tqdm.notebook import tqdm


# In[2]:
def initial_state():
    state=Board(5,5)
    row=0
    for col in range(5):
        state[row, col] = 1
    row=4
    for col in range(5):
        state[row, col] = 2
    return state


# In[3]:
def valid_moves(state, player):
    moves=[]
    player1Column1down=[0,5,10,15]
    player2Column1up=[5,10,15,20]
    player1Column5down=[4,9,14,19]
    player2Column5up=[9,14,19,24]

    # Player 1 valid forward moves
    if player==1:
        for location in range(20):
            if state[location]==1:
                newLocation=location+5
                if newLocation<len(state) and state[newLocation]==0:
                    moves.append((location,newLocation))

    # Player 2 valid forward moves
    if player==2:
        for location in range(5, 25):
            if state[location]==2:
                newLocation=location-5
                if newLocation>=0 and state[newLocation]==0:
                    moves.append((location,newLocation))
                
    # Player 1 valid diagonal moves right
    if player==1:
        for location in range(20):
            if state[location]==1:
                if location%5==4:
                    continue
                newLocation=location+6
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                
    # Player 1 valid diagonal moves left
    if player==1:
        for location in range(5,25):
            if state[location]==1:
                if location%5==0:
                    continue
                newLocation=location+4
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                    
    # Player 1 valid diagonal moves down column 1 (0 index)
    if player==1:
        for location in player1Column1down:
            if state[location]==1:
                newLocation=location+6
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                    
    # Player 1 valid diagonal moves down column 5 (4 index)
    if player==1:
        for location in player1Column5down:
            if state[location]==1:
                newLocation=location+4
                if newLocation<len(state) and state[newLocation]==2:
                    moves.append((location,newLocation))
                
    # Player 2 valid diagonal moves right
    if player==2:
        for location in range(20):
            if state[location]==2:
                if location%5==4:
                    continue
                newLocation=location-6
                if newLocation>=0 and state[newLocation]==1:
                    moves.append((location,newLocation))
                
    # Player 2 valid diagonal moves left
    if player==2:
        for location in range(20):
            if state[location]==2:
                if location%5==0:
                    continue
                newLocation=location-4
                if newLocation>=0 and state[newLocation]==1:
                    moves.append((location,newLocation))
                    
    # Player 2 valid diagonal moves up column 1 (0 index)
    if player==2:
        for location in player2Column1up:
            if state[location]==2:
                newLocation=location-4
                if newLocation<len(state) and state[newLocation]==1:
                    moves.append((location,newLocation))
                    
    # Player 2 valid diagonal moves up column 5 (4 index)
    if player==2:
        for location in player2Column5up:
            if state[location]==2:
                newLocation=location-6
                if newLocation<len(state) and state[newLocation]==1:
                    moves.append((location,newLocation))

                    
    moves=[ [start,end] for start,end in moves]
                    
    return moves


# In[4]:
def update_state(state,player,move):
    start,end=move
    newState=state
    newState[start]=0
    newState[end]=player
    
    return newState


# In[5]:
def win_status(state,player):
    # Win by reaching opposing players start row
    for col in range(5):
        if state[4, col]==1:
            return "win"
    for col in range(5):
        if state[0, col]==2:
            return "win"
    # Win by blocking and win by eliminating all opposing players' pieces
    if player==1 and not valid_moves(state,2):
        return "win"
    if player==2 and not valid_moves(state,1):
        return "win"

    return None


# In[6]:
def show_state(state,player):
    print(state)


# In[7]:
def monkey_move(state,player):
    return random.choice(valid_moves(state,player))
monkey_agent=Agent(monkey_move)
random_move=monkey_move


# In[8]:
def human_move(state,player):
    while True:
        moves=eval(input("Enter your move"))
        if moves not in valid_moves(state,player):
            print("That is not a valid move")
        else:
            break 
    return moves
human_agent=Agent(human_move)


# In[9]:
def minimax_move(state,player):
    values,actions=minimax_values(state,player,display=True,maxdepth=5)
    return top_choice(actions,values)
minimax_agent=Agent(minimax_move)


# In[10]:
def skittles_move(state,player,info):
    S=info.S
    last_state=info.last_state
    last_action=info.last_action
    verbose=info.verbose

    
    if verbose:
        print("\t","Player ",player," is thinking...")
        print("\t","State: ",state)
        print("\t","Table:",S)
        print("\t","Last state,action: ",last_state,last_action)
    
    # make/adjust the table

    if state not in S:
        # add a row to the table for each move
        S[state]=Table()
        moves=valid_moves(state,player)
        for action in moves:
            S[state][action]=1  # number of skittles/beads for each move
    
        if verbose:
            print("\t","State ",state,"unknown...added to table")
            print("\t","Table",S)
    
    move=weighted_choice(S[state])
    if verbose:
        print("\t","Choosing from S[",state,"]",S[state],"....Move: ",move)

    if move is None:  # there are no skittles in this row
        if last_state:
            if verbose:
                print("\t","No possible moves!")
                print("\t","Modifying the table: removing one skittle from (state,action) ",last_state,last_action)
            S[last_state][last_action]=S[last_state][last_action]-1
            
            if verbose:
                print("\t","Table:",S)
                
            if S[last_state][last_action]<0:                
                S[last_state][last_action]=0
                if verbose:
                    print("\t","Negative skittles...fixing.")
                    print("\t","Table:",S)                
        else:
            if verbose:
                print("\t","Started in a bad state ",state,"with no moves and no last state.  Won't modify table.")
                  
                  

        move=random_move(state,player)

    
    return move


# In[11]:
def skittles_after(status,player,info):
    S=info.S
    last_state=info.last_state
    last_action=info.last_action
    verbose=info.verbose

    if verbose:
        print("\t","End of Game adjustments")
        print("\t","Player ",player," is thinking...")
        print("\t","Win Status: ",status)
        print("\t","Table:",S)
        print("\t","Last state,action: ",last_state,last_action)
        
    if status=='lose':
        if last_state:
            S[last_state][last_action]=S[last_state][last_action]-1
            if S[last_state][last_action]<0:
                S[last_state][last_action]=0
                
            if verbose:
                print("\t","Modifying the table: removing one skittle from (state,action) ",last_state,last_action)
                print("\t","Table:",S)

                
        else:
            if verbose:
                print("\t","No last state, so nothing to learn.")
            
                
    else:
        if verbose:
            print("\t","No adjustments needed.")
        
    # does this double-count the learning if you lose on your own turn


# In[12]:
def Q_move(state,player,info):
    Q=info.Q
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    
    α=info.α  # learning rate
    ϵ=info.ϵ  # how often to take a random move
    γ=info.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)
    
    # \alpha <hit tab>    α
    # \epsilon <hit tab>  ϵ
    # \gamma <hit tab>    γ
    
    if state not in Q:
        actions=valid_moves(state,player)
        Q[state]=Table()
        for action in actions:
            Q[state][action]=0  # initial value of table
    
    if learning:
        if random.random()<ϵ:  # take a random move occasionally to explore the environment
            move=random_move(state,player)
        else:
            move=top_choice(Q[state])
    else:
        move=top_choice(Q[state])
    
    if not last_action is None:  # not the first move
        reward=0
        
        # learn
        if learning:
            Q[last_state][last_action]+=α*(reward +
                        γ*max([Q[state][a] for a in Q[state]]) - Q[last_state][last_action])
    
    return move


# In[13]:
def Q_after(status,player,info):
    Q=info.Q
    last_state=info.last_state
    last_action=info.last_action
    learning=info.learning
    
    α=info.α  # learning rate
    ϵ=info.ϵ  # how often to take a random move
    γ=info.γ  # memory constant -- how quickly does the table update back in time (earlier in the game)
    
    # \alpha <hit tab>    α
    # \epsilon <hit tab>  ϵ
    # \gamma <hit tab>    γ

    if status=='lose':
        reward=-1
    elif status=='win':
        reward=1
    elif status=='stalemate':
        reward=.5 # value stalemate a little closer to a win
    else:
        reward=0
    
    
    if learning:
        Q[last_state][last_action]+=α*(reward - Q[last_state][last_action])


# In[14]:
from Game.mcts import *
def mcts_move(state,player,info):
    T=info.T
    values,moves=mcts_values(state,player,T,info.seconds)
    return top_choice(moves,values)

mcts_agent=Agent(mcts_move)
mcts_agent.T=LoadTable(filename='mcts_data_breakthrough.json')
mcts_agent.seconds=1


