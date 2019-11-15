##############################################################################
#   Computer Project #10
#   Algorithm
#       Run the Nine Men's Morris Game.
#           Display the rules commands, and board for the game.
#           PHASE 1:
#           Update the board after putting a piece on the board.
#           Remove a piece if prompted.
#           PHASE 2:
#           Update the board after moving a piece to a new spot on the board.
#           Remove a piece if prompted.
#       Display the banner once a winner is reached.
##############################################################################
import NMM


BANNER = """
    __        _____ _   _ _   _ _____ ____  _ _ _ 
    \ \      / /_ _| \ | | \ | | ____|  _ \| | | |
     \ \ /\ / / | ||  \| |  \| |  _| | |_) | | | |
      \ V  V /  | || |\  | |\  | |___|  _ <|_|_|_|
       \_/\_/  |___|_| \_|_| \_|_____|_| \_(_|_|_)

"""


RULES = """
  _   _ _              __  __            _       __  __                 _     
 | \ | (_)_ __   ___  |  \/  | ___ _ __ ( )___  |  \/  | ___  _ __ _ __(_)___ 
 |  \| | | '_ \ / _ \ | |\/| |/ _ \ '_ \|// __| | |\/| |/ _ \| '__| '__| / __|
 | |\  | | | | |  __/ | |  | |  __/ | | | \__ \ | |  | | (_) | |  | |  | \__ \
 |_| \_|_|_| |_|\___| |_|  |_|\___|_| |_| |___/ |_|  |_|\___/|_|  |_|  |_|___/
                                                                                        
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    
    The game is ends when a player (the loser) has less than three 
    pieces on the board.

"""


MENU = """

    Game commands (first character is a letter, second is a digit):
    
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game
    
"""


def count_mills(board, player):
    """
    Counts how many mills are held by the player in the current state of the board.
    board: the game board containing the pieces.
    player: the player that has the mills.
    returns how many mills the player has (mill_count)
    """
    # initialize a count of mills.
    mill_count = 0
    # get the list of mills.
    mills = board.MILLS
    # get the dictionary of points
    points = board.points
    # iterate through the list of mills
    for mill in mills:
        # if a player has a mill,
        if points[mill[0]]== points[mill[1]] == points[mill[2]] == player:
            # increase the mill count.
            mill_count += 1
    # return the mill count.
    return mill_count

            
def place_piece_and_remove_opponents(board, player, destination):
    """
    Places a piece on a board & removes it if a mill is formed.
    board: The game board containing the pieces.
    player: The player that owns the corresponding pieces.
    destination: Where the piece is located.
    returns 
    """
    # get all the points on the board.
    points = board.points
    # get the amount of mills on the board.
    current_mill_count = count_mills(board, player)
    # if a point on the board is empty, put a piece on it.
    if points[destination] == " ":
        board.assign_piece(player,destination)
    # update the mill count.
        updated_mill_count = count_mills(board, player)
        # if the mill count is updated, remove a piece from the opponents.
        if updated_mill_count > current_mill_count:
            p2 = get_other_player(player)
            remove_piece(board,p2)
    # if the point is invalid, raise a RuntimeError.
    else:
        raise RuntimeError("Invalid command: Not a valid point")
    


def move_piece(board, player, origin, destination):
    """
    Moves a piece from it's original spot to an adjacent spot.
    board: The game board.
    player: The player that has a piece on the board
    origin: The starting point of the piece
    destination: the point that the peice is moving.
    """
    # get all the pieces on the board.
    occupied = placed(board,player)
    # get the dictionary of points.
    points = board.points
    # get the set of adjacent points
    adjacency = board.ADJACENCY
    # if the origin point isn't occupied by a piece, raise a RuntimeError.
    if origin not in occupied:
        raise RuntimeError("Invalid command: Origin point does not belong to player")
    # if the destination entered isn't in the board, raise a RuntimeError.
    if destination not in points:
        raise RuntimeError("Invalid command: Not a valid point")
    # if the destination point is already occupied, raise a RuntimeError.
    elif points[destination] != " ":
        raise RuntimeError("Invalid command: Destination point already taken")
    # if the destination point isn't adjacent, raise a RuntimeError.
    elif destination not in adjacency[origin]:
        raise RuntimeError("Invalid command: Destination is not adjacent")
    # if the input is valid, the origin is cleared, and the piece gets moved.
    else:
        board.clear_place(origin)
        place_piece_and_remove_opponents(board, player, destination)


        
            
            
def points_not_in_mills(board, player):
    """
    Returns a set of points that aren't forming a mill.
    board: the game board.
    player: the player that has a peice on the board.
    returns a set of points that aren't in mills (occupied_sets).
    """
    # call the list of a list of mills
    mills = board.MILLS
    # call the placed function to see which points on the board have pieces.
    occupied = placed(board,player)
    # convert the set of occupied pieces to a tuple.
    occupied_tup = tuple(occupied)
    # initialize an empty set for pieces that form mills.
    points_in_mills = set()
    # convert the tuple into a set. 
    occupied_sets = set(occupied_tup)
    # iterate through the list of mills.
    for mill in mills:
        # convert each mill to a tuple.
        mills_tup = tuple(mill)
        # check if the mills are a inside the tuple of occupied points.
        if set(mills_tup).issubset(occupied_tup):
            # if so, add those mills to the set of points in mills.
            points_in_mills.add(mills_tup)
    # iterate through each tuple in the points in mills.
    for tup in points_in_mills:
        # convert each tuple to a set.
        millpoints = set(tup)
        #iterate through every element in the set.
        for points in millpoints:
            #remove every point that is in a mill from the set of occupied points
            occupied_sets.discard(points)
    #return the points that aren't in mills.
    points_not_in_mills_set = occupied_sets
    return points_not_in_mills_set



def placed(board, player):
    """
    Returns a list of points where player's pieces have been placed.
    board: the game board.
    player: the player that has the pieces.
    """
    # initialize an empty list.
    points_set = set()
    # get the dictionary of points.
    points = board.points
    # iterate through the dictionary, taking the key and value as arguments.
    for key, value in points.items():
        # If the player has a piece on that point,
        if player == value:
            # add the point to the list
            points_set.add(key)
    # return the list of points for the player.
    return points_set

    
def remove_piece(board, player):
    """
    Removes a piece on the board that aren't in mills.
    board: The game board.
    player: the player that owns the pieces. 
    """
    print("A mill was formed!")
    print(board)
    # prompt for a piece to remove from the board in a while loop.
    while True:
        # get the pieces that aren't in mills.
        not_millpoints = points_not_in_mills(board,player)
        # get all the points on the board.
        points = board.points
        # get all the points that have pieces on them.
        occupied = placed(board,player)
        #prompt for a piece to be removed.
        piece_remove = input("Remove a piece at :> ")
        # if the input is on the board,
        if piece_remove in points:
            # if there are only points in mills,
             if len(not_millpoints) == 0:
                 # if the input point has a piece on it, remove it.
                if piece_remove in occupied:
                    board.clear_place(piece_remove)
                    break
             # if the input isn't an opponent's piece, print an error. 
             elif piece_remove not in occupied:
                print("Invalid command: Point does not belong to player")
                print("Try again.")
            # if the input is in a mill, print an error. 
             elif piece_remove not in not_millpoints:
                print("Invalid command: Point is in a mill")
                print("Try again.")
            # if all requirements are met, remove the input piece.
             else:
                board.clear_place(piece_remove)
                break
        # if the input isn't on the board, print an error.
        else:
            print("Invalid command: Not a valid point")
            print("Try again.")
            continue



def is_winner(board, player):
    """
    Checks who the winner of the game is.
    board: the game board.
    player: the player being evaluated.
    """
    # initialize the value for the other player.
    player_2 = get_other_player(player)
    # create an empty list for both players.
    player_list = []
    player2_list = []
    # call the dictionary of points from the board.
    points = board.points
    # iterate through the dictionary.
    for key,value in points.items():
        # if a player has a piece on the board,
        if player == value:
            # add it to their corresponding lists.
            player_list.append(key)
        if player_2 == value:
            player2_list.append(key)
    # if both players have more than 2 pieces on the board, the game isn't over.
    if len(player_list) > 2 and len(player2_list) > 2:
        return False
    else:
        return True


def get_other_player(player):
    """
    Get the other player.
    """
    return "X" if player == "O" else "O"


def main():
    # Loop so that we can start over on reset.
    while True:
        # Print the rules of the game.
        print(RULES)
        # Print the commands.
        print(MENU)
        # Initialize and print the board.
        board = NMM.Board()
        print(board)
        # Initialize the first player.
        player = "X"
        placed_count = 0 # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent
        # Get all the points on the board.
        points = board.points
        # PHASE 1
        print(player + "'s turn!")
        # Prompt to place a piece.
        command = input("Place a piece at :> ").strip().lower()
        print()
        # Until someone quits or we place all 18 pieces,
        while command != 'q' and placed_count != 18:
            try:
                # If the user needs help, display the available commands.
                if command == "h":
                    print(MENU)
                    command = input("Place a piece at :> ").strip().lower()
                    continue
                # if the user wants to restart, break the loop.
                if command == "r":
                    break
                # if the input isn't on the board, print an error message.
                if command not in points:
                    print("Invalid command: Not a valid point")
                    print("Try again.")
                # else, proceed with the program.
                else:
                    place_piece = place_piece_and_remove_opponents(board, player, command)
                    placed_count += 1
                    player = get_other_player(player)
        
                
            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            # Prompt again
            print(board)
            print(player + "'s turn!")
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
            print()
        
        # Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.split()
            try:
                # if the command doesn't have two valid points,
                if len(command) != 2:
                    # print an error message and reprompt.
                    print("Invalid number of points")
                    print("Try again.")
                # if neither command is a point on a board,
                elif command[0] not in points or command[1] not in points:
                    # print an error message and repromt.
                    print("Invalid command: Not a valid point")
                    print("Try again.")
                # else, continue with the game and print a winner once reached.
                else:
                    move_piece(board, player, command[0], command[1])
                    if is_winner(board,player) == True:
                        print(BANNER)
                        return
                    player = get_other_player(player)
                
            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))         
            # Display and reprompt
            print(board)
            # display_board(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()
            
        # If we ever quit we need to return
        if command == 'q':
            return
        
if __name__ == "__main__":
    main()
