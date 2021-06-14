import tkinter as tk
import math

class Game:
    # Determines who starts the game
    # True - player starts the game.
    # False - Computer starts the game.
    start = True
    
    # Determines whose turn it is and ensures that player cannot act out of its turn.
    turn = True
    
    # Player points.
    p1points = 0
    p2points = 0
    
    # Current active node in the game.
    current_node = 0
    
    # Current active state in the game.
    # State is represented as (p1points, current_node, p2points).
    current_state = 0
    
    # Node radius for visual representation.
    r = 25
    
    # Visual representation parameter.
    l = 100
    
    # Width of canvas for visual representation.
    w = 3 * l
    
    # Height of canvas for visual representation.
    h = 4 * l
    
    # Main game window/frame.
    window = None
    
    # window canvas.
    canvas = None
    
    # Frames for visual positioning and representation of points.
    frame = None
    frame1 = None
    frame2 = None
    
    # Variable for changing text on canvas for p1points.
    p1_text = None
    
    # Variable for changing text on canvas for p2points.
    p2_text = None

    # Menu window/frame.
    menu_window = None
    
    # Help window/frame.
    help_window = None
    
    # End window/frame.
    end_window = None
    
    # List for containing all possible states of the game.
    states = []
    
    # list for containing the game tree.
    game_tree = []
    
    # List for containing minimax algorithm results
    # so that there is no need to run the algorithm
    # each time there is a new state.
    minimax_result = []
    
    # Variable that determinis how the minimax algorithm works.
    # True - the first move is maximizer's move.
    # False - the first move is minimizer's move.
    # This does not affect the outcome of the game.
    max_turn = True
    
    # Game representation.
    game = [[0, 1, 0, 2, 0, 0, 0],
            [0, 0, 2, 0, 3, 0, 0],
            [0, 0, 0, 0, 3, 1, 0],
            [0, 0, 2, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0]]
    
    # Creates the menu window from which the game can be started either with first move or second
    # and allows to view help/information on the game.
    def setup():
        # Menu window creation.
        Game.menu_window = tk.Tk()
        Game.menu_window.wm_title('Menu')
        
        # Greeting label creation.
        greeting = tk.Label(master = Game.menu_window, text = 'Welcome to the game!')
        greeting.pack(padx = 50, pady = 20)
        
        # Game start button creation(start first or second).
        b1 = tk.Button(master = Game.menu_window, text = 'Start first!', command = lambda: Game.startFirst(Game.menu_window))
        b1.pack(pady = 10)
        b2 = tk.Button(master = Game.menu_window, text = 'Start second!', command = lambda: Game.startSecond(Game.menu_window))
        b2.pack(pady = 10)
        
        # Show help button creation.
        b3 = tk.Button(master = Game.menu_window, text = '?', fg = 'blue', font = 'Courier 15', command = lambda: Game.create_help_window())
        b3.pack(side = tk.RIGHT)
        
        # Centers the window.
        Game.menu_window.eval('tk::PlaceWindow . center')
        
        Game.menu_window.mainloop()
        
    # Ensures the game to start player's move.
    def startFirst(window):
        # Destroys/closes the menu window.
        window.destroy()
        
        # Sets the game to start accordingly
        Game.start = True
        
        # Creates the  game window/form.
        Game.create_window() 
    
    # Ensures the game to start with Com move.
    def startSecond(window):
        # Destroys/closes the menu window.
        window.destroy()
        
        # Sets the game to start accordingly
        Game.start = False
        
        # Creates the  game window/form.
        Game.create_window() 
    
    # Creates the main game window.
    def create_window():
        # Creates the window/form for the main game.
        Game.window = tk.Tk()
        Game.window.wm_title('Game')
      
        # Create canvas.
        Game.canvas = tk.Canvas(Game.window, width = Game.w, height = Game.h, bg = 'white')
        Game.canvas.pack()
        
        # Create frames to put text in.
        Game.frame = tk.Frame(master = Game.window, width=300, height = 30)
        Game.frame.pack()
        Game.frame1 = tk.Frame(master = Game.frame, width=150, height = 30, bg='red')
        Game.frame1.pack(side = tk.LEFT)
        Game.frame2 = tk.Frame(master = Game.frame, width=150, height = 30, bg='blue')
        Game.frame2.pack(side = tk.RIGHT)
        
        # Creates labels that can change text.
        Game.p1_text = tk.StringVar()
        Game.p2_text = tk.StringVar()
            
        Game.p1label = tk.Label(master = Game.frame1, fg = 'blue', textvariable = Game.p1_text)
        Game.p1label.pack()
        Game.p2label = tk.Label(master = Game.frame2, fg = 'orange', textvariable = Game.p2_text)
        Game.p2label.pack()
        
        # Reset the components of Game class and draw all the items on canvas.
        Game.reset()

        # Centers the window.
        Game.window.eval('tk::PlaceWindow . center')
        
        # Ensures that the game exits after X is pressed.
        Game.window.protocol('WM_DELETE_WINDOW', lambda: Game.end())
        
        Game.window.mainloop()
    
    # Resets Game class parameters to fit the start of a game.
    def reset():
        Game.current_node = 0
        Game.current_state = 0
        
        if Game.start:
            Game.p1_text.set('Player = 0')
            Game.p2_text.set('COM = 0')
        else:
            Game.p1_text.set('COM = 0')
            Game.p2_text.set('Player = 0')
            
        Game.p1points = 0
        Game.p2points = 0
        
        Game.turn = True
        
        # Draws node0 and all arrows going out of it.
        Game.create_points('1', 1.5 * Game.l, 0.5 * Game.l, 0.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_line(1.5 * Game.l, 0.5 * Game.l, 0.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_points('2', 1.5 * Game.l, 0.5 * Game.l, 2.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_line(1.5 * Game.l, 0.5 * Game.l, 2.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        n0 = Game.create_circle(1.5 * Game.l - Game.r, 0.5 * Game.l - Game.r, 1.5 * Game.l + Game.r, 0.5 * Game.l + Game.r, Game.canvas, 'green')
        t0 = Game.canvas.create_text(1.5 * Game.l, 0.5 * Game.l, text = '0', font = 'Courier 10', fill = 'white')

        # Draws node1 and all arrows going out of it.
        Game.create_points('2', 0.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_line(0.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_points('3', 0.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, 'black')
        Game.create_line(0.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, 'black')
        n1 = Game.create_circle(0.5 * Game.l - Game.r, 1.5 * Game.l - Game.r, 0.5 * Game.l + Game.r, 1.5 * Game.l + Game.r, Game.canvas, 'black')
        t1 = Game.canvas.create_text(0.5 * Game.l, 1.5 * Game.l, text = '1', font = 'Courier 10', fill = 'white')

        # Draws node2 and all arrows going out of it.
        Game.create_points('3', 1.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, 'black')
        Game.create_line(1.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, 'black')
        Game.create_points('1', 1.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, 'black')
        Game.create_line(1.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, 'black')
        n2 = Game.create_circle(1.5 * Game.l - Game.r, 1.5 * Game.l - Game.r, 1.5 * Game.l + Game.r, 1.5 * Game.l + Game.r, Game.canvas, 'black')
        t2 = Game.canvas.create_text(1.5 * Game.l, 1.5 * Game.l, text = '2', font = 'Courier 10', fill = 'white')

        # Draws node3 and all arrows going out of it.
        Game.create_points('2', 2.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_line(2.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, 'black')
        Game.create_points('4', 2.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, 'black')
        Game.create_line(2.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, 'black')
        n3 = Game.create_circle(2.5 * Game.l - Game.r, 1.5 * Game.l - Game.r, 2.5 * Game.l + Game.r, 1.5 * Game.l + Game.r, Game.canvas, 'black')
        t3 = Game.canvas.create_text(2.5 * Game.l, 1.5 * Game.l, text = '3', font = 'Courier 10', fill = 'white')

        # Draws node4 and all arrows going out of it.
        Game.create_points('3', Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, 'black')
        Game.create_line(Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, 'black')
        n4 = Game.create_circle(Game.l - Game.r, 2.5 * Game.l - Game.r, Game.l + Game.r, 2.5 * Game.l + Game.r, Game.canvas, 'black')
        t4 = Game.canvas.create_text(Game.l, 2.5 * Game.l, text = '4', font = 'Courier 10', fill = 'white')
        
        # Draws node5 and all arrows going out of it.
        Game.create_points('3', 2 * Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, 'black')
        Game.create_line(2 * Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, 'black')
        n5 = Game.create_circle(2 * Game.l - Game.r, 2.5 * Game.l - Game.r, 2 * Game.l + Game.r, 2.5 * Game.l + Game.r, Game.canvas, 'black')
        t5 = Game.canvas.create_text(2 * Game.l, 2.5 * Game.l, text = '5', font = 'Courier 10', fill = 'white')

        # Draws node6.
        n6 = Game.create_circle(1.5 * Game.l - Game.r, 3.5 * Game.l - Game.r, 1.5 * Game.l + Game.r, 3.5 * Game.l + Game.r, Game.canvas, 'red')
        t6 = Game.canvas.create_text(1.5 * Game.l, 3.5 * Game.l, text = '6', font = 'Courier 10', fill = 'white')
        
        # Binding node circles to a method.
        Game.canvas.tag_bind(n1, '<Button-1>', lambda event: Game.onClick(event, 1))
        Game.canvas.tag_bind(n2, '<Button-1>', lambda event: Game.onClick(event, 2))
        Game.canvas.tag_bind(n3, '<Button-1>', lambda event: Game.onClick(event, 3))
        Game.canvas.tag_bind(n4, '<Button-1>', lambda event: Game.onClick(event, 4))
        Game.canvas.tag_bind(n5, '<Button-1>', lambda event: Game.onClick(event, 5))
        Game.canvas.tag_bind(n6, '<Button-1>', lambda event: Game.onClick(event, 6))
        
        # Binding node texts to a method.
        Game.canvas.tag_bind(t1, '<Button-1>', lambda event: Game.onClick(event, 1))
        Game.canvas.tag_bind(t2, '<Button-1>', lambda event: Game.onClick(event, 2))
        Game.canvas.tag_bind(t3, '<Button-1>', lambda event: Game.onClick(event, 3))
        Game.canvas.tag_bind(t4, '<Button-1>', lambda event: Game.onClick(event, 4))
        Game.canvas.tag_bind(t5, '<Button-1>', lambda event: Game.onClick(event, 5))
        Game.canvas.tag_bind(t6, '<Button-1>', lambda event: Game.onClick(event, 6))
        
        # In case the game was chosen to start on second move, this makes a computer move.
        if Game.start == False:
            Game.computer_move()
    
    # Reacts to a click on the game board. Accordingly progresses the game.
    def onClick(event, clicked_node):
        # Ensures that the player cannot move more than once in a row.
        if Game.turn == Game.start:
            # Assigns the move to a variable. 
            move = Game.game[Game.current_node][clicked_node]
            
            # Checks if move is possible.
            if move != 0:
                # Updates point label to fit just made move.
                Game.updatePoints(move)
                
                # Redraws the lines to show who made the move.
                Game.redraw_lines(Game.current_node, clicked_node)
                
                # Redraws the current node as grey.
                Game.redraw_nodes(Game.current_node, 'grey')
                
                Game.current_node = clicked_node
                
                # Advances the clicked node to the current.
                Game.current_state = Game.find_current_state()
                
                # Redraws the new current node as green/active.
                Game.redraw_nodes(Game.current_node, 'green')
                
                # Ensures that the following move is made by computer.
                Game.turn = Game.turn == False
                
                # Checks if the game has reached its end.
                if Game.current_node == 6:
                    Game.end_message()
            
                # Computer move.
                elif not Game.turn == Game.start:
                    Game.computer_move()
    
    # Executes a move by a computer.
    def computer_move():
        # Gets the best node.
        chosen_node = Game.get_best_move()[1]
        
        # Get the best move
        move = Game.game[Game.current_node][chosen_node]
        
        # Updates point label to fit just made move.
        Game.updatePoints(move)
        
        # Redraws the lines to show who made the move.
        Game.redraw_lines(Game.current_node, chosen_node)
        
        # Redraws the current node as grey.
        Game.redraw_nodes(Game.current_node, 'grey')
        
        # Changes the current node accordingly.
        Game.current_node = chosen_node
        
        # Finds current game state.
        Game.current_state = Game.find_current_state()
        
        # Redraws the new current node as green/active.
        Game.redraw_nodes(Game.current_node, 'green')
        
        # Checks if the game has reached its end.
        if Game.current_node == 6:
            Game.end_message()
            
        # Ensures that the player can make a move now.
        else:
            Game.turn = Game.turn == False
    
    # Creates the end window that displays the result of the game and provides options to retry or go back to menu.
    def end_message():
        # Determines the correct messgae to be displayed.
        if Game.p1points > Game.p2points:
            if Game.start:
                msg = 'Player wins!!!'
            else:
                msg = 'COM wins!!!'
        elif Game.p1points < Game.p2points:
            if Game.start:
                msg = 'COM wins!!!'
            else:
                msg = 'Player wins!!!'
        elif Game.p1points == Game.p2points:
            msg = 'It\'s a Draw!!!'
            
        # Creates the end window.
        Game.end_window = tk.Tk()
        Game.end_window.wm_title("Endgame!")
        
        # Creates a label that displays the end message.
        label = tk.Label(master = Game.end_window, text = msg, font = 'Courier 30')
        label.pack(padx = 50, pady = 50)
        
        # Creates a button for retrying the game.
        button1 = tk.Button(master = Game.end_window, text = "Retry", font = 'Calibri 15', command = lambda: Game.retry(Game.end_window))
        button1.pack(side = tk.LEFT)
        
        # Creates a button for going beck to the menu.
        button2 = tk.Button(master = Game.end_window, text = "Menu", font = 'Calibri 15', command = lambda: Game.menu(Game.end_window))
        button2.pack(side = tk.LEFT)
        
        # Creates a button for exiting the programm.
        button3 = tk.Button(master = Game.end_window, text = "Exit", font = 'Courier 15', command = lambda: Game.end())
        button3.pack(side = tk.RIGHT)
        
        # Ensures that the game exits after X is pressed.
        Game.end_window.protocol('WM_DELETE_WINDOW', lambda: Game.end())
        
        # Centers the window.
        Game.end_window.eval('tk::PlaceWindow . center')
        
        # Gives priority to the end window.
        #end_window.grab_set_global()
        
        Game.end_window.mainloop()
    
    # Creates help window which shows information about the game.
    def create_help_window():
        # Creates help window.
        Game.help_window = tk.Tk()
        Game.help_window.wm_title('Help')
        
        # Creates game decription label.
        description = tk.Label(master = Game.help_window, text = 'Game description:\nThis game is very simple!\nThe game board is a bunch of nodes connected via paths that have certain points.\n' + 
                                  'This game is pve.\nIt can be chosen to make the first move or second move in the menu window.\nThe player with the most points at the end wins!',
                                  anchor='e', font = 'Calibri 10')
        description.pack(pady = 10)
        
        # Creates game visuals information label.
        nodes_info = tk.Label(master = Game.help_window, text = 'Green node displays the current posiotion on the board.\nBlack node displays a position that has not been accessed.\n' +
                                 'Grey node displays a posiotion that has been accessed.\n Red node displays the "game end" posiotion.', font = 'Calibri 10')
        nodes_info.pack(pady = 10)
        
        # Creates a title for the canvas label.
        game_tree_label = tk.Label(master = Game.help_window, text = 'Game tree and minimax values.', font = 'Courier 12')
        game_tree_label.pack()
        
        width = 1000
        height = 500
        
        # Creates canvas.
        canvas = tk.Canvas(master = Game.help_window, width = width, height = height, bg = 'white')
        canvas.pack(padx = 10)
        
        # Draws the game tree on the canvas.
        Game.draw_lines(1, 0, width / 2, int(width / 2), 20, int(width / 2), 20, canvas, True)
        Game.draw_text(1, 0, width / 2,  int(width / 2), 20, canvas)
        Game.draw_min_max(Game.max_turn, width, height, 20, 120, canvas)
        
        # Centers the window.
        Game.help_window.eval('tk::PlaceWindow . center')
        
        Game.help_window.mainloop()

    # Generates game states.
    def gen_states(current_node, p1, p2, turn):
        # Appends Found state to the list of states.
        if not (p1, current_node, p2) in Game.states:
            Game.states.append((p1, current_node, p2))
        
        # Checks if it is 1st player's move.
        if turn:
            # Iterates over possible game moves.
            for node in range(0, len(Game.game[current_node])):
                # Checks if a move is possible.
                if Game.game[current_node][node] != 0:
                    # Calls the method on the move that was found possible.
                    Game.gen_states(node, p1 + Game.game[current_node][node], p2, False)
        
        # Chekcs if it is 2nd player's move.
        else:
            # Iterates over possible game moves.
            for node in range(0, len(Game.game[current_node])):
                # Checks if a move is possible.
                if Game.game[current_node][node] != 0:
                    # Calls the method on the move that was found possible.
                    Game.gen_states(node, p1, p2 + Game.game[current_node][node], True)

    # Generates the game tree.
    def gen_tree(current_node, p1, p2, turn):
        # Checks if it is 1 st player's turn.
        if turn:
            # Iterates over all possible moves.
            for node in range(0, len(Game.game[current_node])):
                # Checks if a move is possible.
                if Game.game[current_node][node] != 0:
                    # Gets the index of current state.
                    index_current = Game.states.index((p1, current_node, p2))
                    
                    # Gets the index of the next state according to the move.
                    index_next = Game.states.index((p1 + Game.game[current_node][node], node, p2))
                    
                    # Inserts the move into the game tree.
                    Game.game_tree[index_current][index_next] = 1
                    
                    # Looks for possbile moves from the state that was just looked at.
                    Game.gen_tree(node, p1 + Game.game[current_node][node], p2, False)
        
        # Checks if it is 2 nd player's turn.
        else:
            # Iterates over all possible moves.
            for node in range(0, len(Game.game[current_node])):
                # Checks if a move is possible.
                if Game.game[current_node][node] != 0:
                    # Gets the index of current state.
                    index_current = Game.states.index((p1, current_node, p2))
                    
                    # Gets the index of the next state according to the move.
                    index_next = Game.states.index((p1, node, p2 + Game.game[current_node][node]))
                    
                    # Inserts the move into the game tree.
                    Game.game_tree[index_current][index_next] = 1
                    
                    # Looks for possbile moves from the state that was just looked at.
                    Game.gen_tree(node, p1, p2 + Game.game[current_node][node], True)
    
    # Returns the difference between player points
    def diff(state):
        if Game.max_turn:
            return state[0] - state[2]
        else:
            return state[2] - state[0]
    
    # Exectues the minimax algorithm and generates the minimax_result list, which contains each states minimax value.
    # Return given nodes minimax value.        
    def minimax(current_state, max_layer):
        
        # Checks if current state is final. 
        if Game.states[current_state][1] == 6:
            # Calculates the minimax value or difference between points.
            result = Game.diff(Game.states[current_state])
            
            # Adds appropriate value to the list that contains minimax algorithm results.
            Game.minimax_result[current_state] = result
            
            return result
         
        # Checks whther its maximizer's turn.
        if max_layer:
            # Creates a variable which contains the result of minimax algorithm.
            maxeval = -float('inf')
            
            # Iterates over all moves from current state.
            for state in range(1, len(Game.game_tree[current_state])):
                # Checks if a move is possible/allowed.
                if Game.game_tree[current_state][state] == 1:
                
                    # Assigns the minimax value of it's child.
                    temp = Game.minimax(state, False)
                    
                    # Compares whether the child's minimax value is higher than the one that this state already has.
                    # If it is bigger, it is assigned to the current state.
                    maxeval = max(temp, maxeval)        
            
            # Adds appropriate value to the list that contains minimax algorithm results.
            Game.minimax_result[current_state] = maxeval
            return maxeval
        
        # Checks whther its minimizer's turn.
        else:
            # Creates a variable which contains the result of minimax algorithm.
            mineval = float('inf')
            
            # Iterates over all moves from current state.
            for state in range(1, len(Game.game_tree[current_state])):
                # Checks if a move is possible/allowed.
                if Game.game_tree[current_state][state] == 1:
                    # Assigns the minimax value of it's child.
                    temp = Game.minimax(state, True)
                    
                    # Compares whether the child's minimax value is lower than the one that this state already has.
                    # If it is lower, it is assigned to the current state.
                    mineval = min(temp, mineval)
                    
            # Adds appropriate value to the list that contains minimax algorithm results.
            Game.minimax_result[current_state] = mineval
            
            return mineval
       
     
    # Generates everything neccessary for computer to make best moves.
    def gen_com_moves():
        # Resets the values for lists containing game_tree information.
        Game.states = []
        Game.game_tree = []
        Game.minimax_result = []
        
        # Generates the states of the game.
        Game.gen_states(0, 0, 0, True)
        
        # Prepares game_tree list and minimax_result list to be appropriate size.
        for n in range(0, len(Game.states)):
            Game.game_tree.append([0]*len(Game.states))
            Game.minimax_result.append(None)
        
        # Generates game tree.
        Game.gen_tree(0, 0, 0, True)
        
        # Applies minimax algorithm and assigns results a list.
        Game.minimax(0, Game.max_turn)
    
    # Returns the best possible move 
    def get_best_move():
        # Iterates over moves from current state.
        for state in range(0, len(Game.game_tree[Game.current_state])):
            if Game.game_tree[Game.current_state][state] != 0 and Game.minimax_result[Game.current_state] == Game.minimax_result[state]:
                return Game.states[state] 
    

    
    # Updates game points.
    def updatePoints(points):
        # Checks whose turn it is.
        if Game.turn:
            # Changes game poits accordingly.
            Game.p1points += points
            
            # Checks who started the game.
            if Game.start:
            
                # Changes the visual display of points to represent theri accurate new values.
                Game.p1_text.set('Player = {}'.format(Game.p1points))
                
            else:
            
                # Changes the visual display of points to represent theri accurate new values.
                Game.p1_text.set('COM = {}'.format(Game.p1points))
                
        else:
            # Changes game poits accordingly.
            Game.p2points += points
            
            # Checks who started the game.
            if Game.start:
                # Changes the visual display of points to represent theri accurate new values.
                Game.p2_text.set('COM = {}'.format(Game.p2points))
            else:
                # Changes the visual display of points to represent theri accurate new values.
                Game.p2_text.set('Player = {}'.format(Game.p2points))
    
   
     
    # Closes the given window and creates the setup window.
    def menu(window):
        window.destroy()
        Game.window.destroy()
        Game.setup()
        
    # Resets the game without going back to the setup window.
    # Destroys the given window.
    def retry(window):
        window.destroy()
        Game.reset()
    
    # Exits the programm.
    def end():
        try:
            Game.window.destroy()
        except:
           pass
        try:
             Game.end_window.destroy()
        except:
            pass
        try:
             Game.menu_window.destroy()
        except:
            pass
        try:
            Game.help_window.destroy()
        except:
            pass
      
    # Returns current game state based on given node and 
    def find_current_state():
        return Game.states.index((Game.p1points, Game.current_node, Game.p2points))
    
    # Draws a single given node.      
    def redraw_nodes(point, color):
        if point == 0:
            Game.create_circle(1.5 * Game.l - Game.r, 0.5 * Game.l - Game.r, 1.5 * Game.l + Game.r, 0.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(1.5 * Game.l, 0.5 * Game.l, text = '0', font = 'Courier 10', fill = 'white')
            
        if point == 1:
            Game.create_circle(0.5 * Game.l - Game.r, 1.5 * Game.l - Game.r, 0.5 * Game.l + Game.r, 1.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(0.5 * Game.l, 1.5 * Game.l, text = '1', font = 'Courier 10', fill = 'white')
            
        if point == 2:
            Game.create_circle(1.5 * Game.l - Game.r, 1.5 * Game.l - Game.r, 1.5 * Game.l + Game.r, 1.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(1.5 * Game.l, 1.5 * Game.l, text = '2', font = 'Courier 10', fill = 'white')
            
        if point == 3:
            Game.create_circle(2.5 * Game.l - Game.r, 1.5 * Game.l - Game.r, 2.5 * Game.l + Game.r, 1.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(2.5 * Game.l, 1.5 * Game.l, text = '3', font = 'Courier 10', fill = 'white')
            
        if point == 4:
            Game.create_circle(Game.l - Game.r, 2.5 * Game.l - Game.r, Game.l + Game.r, 2.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(Game.l, 2.5 * Game.l, text = '4', font = 'Courier 10', fill = 'white')
            
        if point == 5:
            Game.create_circle(2 * Game.l - Game.r, 2.5 * Game.l - Game.r, 2 * Game.l + Game.r, 2.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(2 * Game.l, 2.5 * Game.l, text = '5', font = 'Courier 10', fill = 'white')
            
        if point == 6:
            Game.create_circle(1.5 * Game.l - Game.r, 3.5 * Game.l - Game.r, 1.5 * Game.l + Game.r, 3.5 * Game.l + Game.r, Game.canvas, color)
            Game.canvas.create_text(1.5 * Game.l, 3.5 * Game.l, text = '6', font = 'Courier 10', fill = 'white')
    
    # Redraws the lines between two given nodes in color
    # representing the player who made the move.
    def redraw_lines(node1, node2):
        # Checks if it is 1st player's move.
        if Game.turn:
            color = 'blue'
        
        # Checks if it is 2nd player's move.
        else:
            color = 'orange'
        
        # Redraws the lines and points with the chosen color.
        if node1 == 0 and node2 == 1:
            Game.create_points('1', 1.5 * Game.l, 0.5 * Game.l, 0.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
            Game.create_line(1.5 * Game.l, 0.5 * Game.l, 0.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
        elif node1 == 0 and node2 == 3:
            Game.create_points('2', 1.5 * Game.l, 0.5 * Game.l, 2.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
            Game.create_line(1.5 * Game.l, 0.5 * Game.l, 2.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
        elif node1 == 1 and node2 == 2:
            Game.create_points('2', 0.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
            Game.create_line(0.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
        elif node1 == 1 and node2 == 4:
            Game.create_points('3', 0.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, color)
            Game.create_line(0.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, color)
        elif node1 == 2 and node2 == 4:
            Game.create_points('3', 1.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, color)
            Game.create_line(1.5 * Game.l, 1.5 * Game.l, Game.l, 2.5 * Game.l, Game.canvas, color)
        elif node1 == 2 and node2 == 5:
            Game.create_points('1', 1.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, color)
            Game.create_line(1.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, color)
        elif node1 == 3 and node2 == 2:
            Game.create_points('2', 2.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
            Game.create_line(2.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, 1.5 * Game.l, Game.canvas, color)
        elif node1 == 3 and node2 == 5:
            Game.create_points('4', 2.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, color)
            Game.create_line(2.5 * Game.l, 1.5 * Game.l, 2 * Game.l, 2.5 * Game.l, Game.canvas, color)
        elif node1 == 4:
            Game.create_points('3', Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, color)
            Game.create_line(Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, color)
        elif node1 == 5:
            Game.create_points('3', 2 * Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, color)
            Game.create_line(2 * Game.l, 2.5 * Game.l, 1.5 * Game.l, 3.5 * Game.l, Game.canvas, color)
    
    # Draws a circle on given canvas and returns it.
    def create_circle(x1, y1, x2, y2, canvas, color):
        return canvas.create_oval(x1, y1, x2, y2, fill = color)
    
    # Creates a text of points in between two points.
    def create_points(msg, x1, y1, x2, y2, canvas, color):
        x_offset = -5
        y_offset = -5
        if y2 == y1:
            x_offset = 0
            y_offset = 7
        elif x2 > x1:
            y_offset = -5
            x_offset = 5
        return canvas.create_text(int(x1 + (x2-x1)/2) + x_offset, int(y1 + (y2-y1)/2) + y_offset, text = msg, font='Courier 10', fill = color)
    
    # Draws an arrow from one point to another with a radius clip and returns it.
    def create_line(x1, y1, x2, y2, canvas, color):
        distance = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        cos = (x2 - x1) / distance
        sin = (y2 - y1) / distance
        x1 += cos * Game.r
        x2 -= cos * Game.r
        y1 += sin * Game.r
        y2 -= sin * Game.r
        return canvas.create_line(x1, y1, x2, y2, fill = color, arrow=tk.LAST)
    
    # Draws lines for visual display of game_tree.
    def draw_lines(depth, current_state, width, x1, y1, x2, y2, canvas, winning_path):
        # Checks if this is the very first point.
        if depth !=1:
            if winning_path:
                # If it is not the first node, an arrow is drawn from the previous point to the current point
                canvas.create_line(x1, y1 + 20, x2, y2 - 20, fill = 'green', arrow=tk.LAST)
            else:
                # If it is not the first node, an arrow is drawn from the previous point to the current point
                canvas.create_line(x1, y1 + 20, x2, y2 - 20, fill = 'black', arrow=tk.LAST)

        
        # Counts the amount children.
        count = 0
        
        # Iterates over all moves.
        for state in range(0, len(Game.game_tree[current_state])):
            # Checks if a move is possible from the current state
            if Game.game_tree[current_state][state] != 0:
                count += 1
                
        # A variable that calculates the x offset from parent point.
        diff = 0
        
        # Checks if current point is a leaf.
        if count != 0:
                # Assigns the appropriate diff value.
                diff = (width/depth)/count
        
        # Checks if there is exactly one child.
        if count == 1:
            i = 0
        else:
            i = 0 - count/2
            
        # A variable that helps even out children points.
        step = 0
        
        # Checks if current poitn has more than one child. 
        if count > 1:
            # Calculates the appropriate step.
            step = count / (count - 1)

        # Iterates over all moves.
        for state in range(0, len(Game.game_tree[current_state])):
            # Checks if a move is possible.
            if Game.game_tree[current_state][state] != 0:
                if Game.minimax_result[current_state] == Game.minimax_result[state] and winning_path:
                    # If a move is possible drawsLines for current points children.
                    Game.draw_lines(depth + 1, state, width, x2, y2, x2 + int(i*diff), y2 + 100, canvas, True)
                else:
                    # If a move is possible drawsLines for current points children.
                    Game.draw_lines(depth + 1, state, width, x2, y2, x2 + int(i*diff), y2 + 100, canvas, False)
                i += step
    
    # Draws nodes for visual display of game tree.
    def draw_text(depth, current_state, width, x, y, canvas):
        # Draws the node on canvas.
        canvas.create_text(x, y, text = str(Game.states[current_state]) + '\nminimax=' + str(Game.minimax_result[current_state]), font = 'Courier 10', fill = 'black')
       
        # Variable containing the amount of direct children nodes for current node.
        count = 0
        
        # Iterates over all moves.
        for state in range(0, len(Game.game_tree[current_state])):
            # Checks if a move is possible.
            if Game.game_tree[current_state][state] != 0:
                count += 1
                
        # A variable that calculates the x offset from parent node.
        diff = 0
        # Checks if node is a leaf.
        if count != 0:
                # Assigns the appropriate diff value.
                diff = (width/depth)/count
                
        # Checks if there is exactly one child.
        if count == 1:
            i = 0
        else:
            i = 0 - count/2
        
        # A variable that helps even out children points.
        step = 0
        
        # Checks if current poitn has more than one child. 
        if count > 1:
            # Calculates the appropriate step.
            step = count / (count - 1)
            
        # Iterates over all moves.
        for state in range(0, len(Game.game_tree[current_state])):
            # Checks if a move is possible.
            if Game.game_tree[current_state][state] != 0:
                # If a move is possible drawsLines for current points children.
                Game.draw_text(depth + 1, state, width, x + int(i*diff), y + 100, canvas)
                i += step
    
    # Draws MAX MIN lines in the help window for better visualization of minimax algorithm.
    def draw_min_max(max_turn, width, height, y1, y2, canvas):
        # Middle y point between two points.
        y0 = int((y2 + y1) / 2)
        
        # Checks if the y goes beyond canvas height.
        # If it does, the n the method stops and return nothing.
        if y0 >= height:
            return
        
        # Checks if it is a MAX layer.
        if max_turn:
            # Creates line for MAX layer.
            canvas.create_line(0, y0, width, y0, fill = 'red')
            
            # Creates tex MAX for the MAX line.
            canvas.create_text(20, y0 - 10, text = 'MAX', font = 'Courier 13', fill = 'red')
            
            # Draws next MIN line.
            Game.draw_min_max(False, width, height, y2, y2 + 100, canvas)
        
        # Checks if it is a MIN layer.
        else:
            # Creates line for MIN layer.
            canvas.create_line(0, y0, width, y0, fill = 'blue')
            
            # Creates tex MIN for the MIN line.
            canvas.create_text(20, y0 - 10, text = 'MIN', font = 'Courier 13', fill = 'blue')
            
            # Draws next MAX line.
            Game.draw_min_max(True, width, height, y2, y2 + 100, canvas)

def main():
    Game.gen_com_moves()                
    Game.setup()

main()
