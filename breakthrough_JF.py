# In[1]:
import nbimporter
from breakthrough_game_code_and_agents_for_robot import *
from my_robot_functions_JF_for_robot import *
from classy import *
from pylab import imread,imsave,imshow
from image_defs import *


# In[2]:
BP=True

if BP is None:
    print("Running on the laptop.")
    on_laptop=True
else:
    print("Running on the robot.")
    on_laptop=False


# # Agent

# In[3]:
def read_state_from_file(filename):
    text = open(filename).read()
    text = text.strip()
    lines = [line.strip() for line in text.split('\n')]  # get rid of \n
    
    row = lines[0].split()
    R, C = len(lines), len(row)
    print(f"{R}x{C} board")
    state = Board(R, C)
    state.board = [int(val) for val in text.split()]
    print(state)
    return state


# In[4]:
def get_move(state,player):
    if player==2:
        Q=SmallTable("small_breakthrough_skittles2.json")
    else:
        Q=SmallTable("small_breakthrough_skittles1.json")

    if state not in Q:
        print("State not in the table: ",state)
        move=random_move(state,player)
    else:
        move=top_choice(Q[state])

    return move

read_state=read_state_from_file


# # Make Move

# In[5]:
def make_move(state,player,move):
    start,end=move
    row,col=state.row(start),state.col(start)

    # depends on where the robot starts
    number_cols_to_move=1+col
    number_rows_to_move=5-row


    go_forward_squares_yellow(number_cols_to_move)
    rot90()
    forward1()
    go_forward_squares_blue(number_rows_to_move)

    #  0  1  2  3  4
    #  5  6  7  8  9
    # 10 11 12 13 14
    # 15 16 17 18 19
    # 20 21 22 23 24
    
    if start-end==4:
        diagonal_right()
    elif start-end==6:
        diagonal_left()
    elif start-end==5:
        print('Reverse off board')
        off_board()
    else:
        raise ValueError("You can't get there from here")

    print("Making move ",move)


# In[6]:
import ijson   # install with pip install ijson on both laptop and robot
from Game.tables import make_immutable,str2table


# In[7]:
class SmallTable(object):

    def __init__(self,filename):
        self.filename=filename

    def __getitem__(self, key):
        key=make_immutable(key)
        with open(self.filename, "rb") as f:
            for record in ijson.items(f, str(key)):
                return str2table(record)

        raise KeyError

    def __contains__(self, key):
        keyi=make_immutable(key)
        try:
            value=self[keyi]
            return True
        except KeyError:
            print(key)
            print(keyi.__repr__())
            return False


# # Read State

# In[8]:
def read_state():
    from pylab import imread,imsave
    from numpy import atleast_2d
    import os
    from numpy import atleast_2d
    import cv2

    state=Board(5,5)      #<========= change the size
    nr,nc=state.shape

    
    corners=array([
    [ 317.,  65.],        # These are the specific corners that my images are inside
    [1235.,  45.],        # This was done because I was running into issues with thresholding the image
    [1290.,  735.],
    [ 298.,  755.]],dtype=np.float32)
    
    # load the classifier
    classifier=NaiveBayes()
    classifier.load('naive_bayes_trained_JF.json')
    
    
    # get the picture
    filename='current_board.jpg'              # for the robot
    take_picture(filename)


    # this part comes from your Make Training Squares script
    image=imread(filename)

    # these 5 lines are specific to your image
    image=image[60:790,250:1375,:]
    gray,black_and_white=get_gray_and_threshold_image(image,threshold=90)
    im3=straighten_image(image,corners)
    squares=get_board_squares_from_image(im3,state.shape)


    count=0
    values=[]
    for r in range(nr):
        for c in range(nc):
            # convert the square image to a data vector for the classifier
            resized_square = cv2.resize(squares[count], (80, 80))  # ChatGPT was used for these 2 lines of code because the vector it
                                                                   # the function returned was not the same size as my images (80,80,3)
            vector = resized_square.ravel()
            prediction=classifier.predict(atleast_2d(vector))[0]
        
            values.append(prediction)
    
            # for debugging
            imsave('predicted/square %d predicted as piece %d.jpg' % (count,prediction),squares[count])
        
            count+=1

    
    # reconstruct the state from the predictions
    state.board=values

    print("Current state is:")
    print(state)

    x=input("""
    Hit return if this is correct, otherwise type a character 
    and the state will be read from board-JF.txt.""")

    if x:
        print("Reading from file...")
        state=read_state_from_file('board-JF.txt')

    print("Using")
    print(state)

    
    return state


# In[9]:
classifier=NaiveBayes()
classifier.load('naive_bayes_trained_JF.json')


# In[10]:
C=CSC()
C.load('CSC_trained_JF.json')


# In[11]:
if on_laptop:
    image=imread("current_board.jpg")
    imshow(image)


# In[12]:
if on_laptop:
    state=read_state()


# In[13]:
player=2 # or player=2 depending on which you want
state=read_state() # read the pieces, and construct the state
move=get_move(state,player) # replace with minimax,skitles, Q, etc...
make_move(state,player,move) # actually move the pieces



