# Author: Ellie Davila
# Date: 11.22.20
# Description: This program allows the user to begin a two-player game of Focus.

class FocusGame:
    """
    This class creates a Focus game instance for two players on a 6x6 game board. The Focus game
    instance allows the players to play an entire game of Focus. Each player moves their game piece
    on top of another game piece to create a stack that is controlled by the player's piece that is on top.
    If a player moves a piece that has other pieces stacked underneath the player's chosen piece, the player
    may move the amount of spaces that is the number of pieces stacked. A player may move either forward,
    backward, left, or right, but are not allowed to move diagonally. Once a piece-stack has over 5 pieces,
    the bottom pieces of a piece-stack over 5 are taken by the player who stacked the pieces higher than 5
    in their move. A player wins if they capture 6 opponent pieces. Players may also use their own reserve
    pieces from a stack they "captured" that had over 5 pieces in a move instead of stacking pieces already
    on the board.

    In order to play a Focus game, there needs to be a player class to hold player instances and a board
    class to "create" the board. This class will have to communicate with the Board class and the Player
    class in order to play a full game.
    """
    def __init__(self, _player1, _player2):
        """
        This method initializes the Focus game instance by identifying the two players and their chosen piece
        colors. The init class calls the player class to create the player instances and calls the Board
        class to create a board for the Focus game.
        """
        # Player attributes
        self._player1 = Player(_player1)
        self._player2 = Player(_player2)
        self._player1_name = self._player1.get_player_name()
        self._player2_name = self._player2.get_player_name()
        self._player1_color = self._player1.get_player_color()
        self._player2_color = self._player2.get_player_color()

        # Call the board class to create the board instance.
        self._board = Board(_player1, _player2)

    def get_player_from_name(self, name):
        """
        Returns the player instance from a player name.
        """

        if self._player1_name.lower() == name.lower():
            return self._player1
        if self._player2_name.lower() == name.lower():
            return self._player2

    def move_piece(self, name, start, end, number_of_pieces):
        """
        This method moves the player piece to represent a turn in the Focus game. This method checks for
        various errors and checks if the move is valid. If the move is valid, the pieces will be moved.
        This method returns "Move successful" and also checks for win conditions if the move is valid.
        """

        # Checks if the name argument is a player of the Focus game instance.
        if name.lower() in self._board.get_names_list():
            turn = self._board.check_turn().lower()
            if turn == name.lower():
                player = self.get_player_from_name(name)

                # Checks if the name given (case-insensitive) is the correct player's turn and if the move
                # is valid for start location, end location, and number of pieces being moved. Other functions
                # are called to move the game piece if the move passes validation checks.
                self._board.start_validation(player, start, end, number_of_pieces)
                check_for_win = self._board.check_win(player)
                if check_for_win == 'win':
                    return name + 'wins!'
                if check_for_win == 'successfully moved':
                    return 'successfully moved'

            # Returns an error message if the name given is the wrong player's turn.
            if turn != name.lower():
                raise PlayerTurnError("not your turn")

        # Returns an error message if the player name is not a player in the Focus game instance.
        elif name.lower() not in self._board.get_names_list():
            raise PlayerNameError("invalid player name")

    def show_pieces(self, position):
        """
        This method takes a position of the Focus game board instance and finds the piece elements of the
        position. It returns a list of the pieces at the tuple argument position.
        """

        position_x = position[0]
        position_y = position[1]

        # Checks to make sure the position argument is valid.
        if len(position) != 2:
            raise InvalidLocation('invalid location on the board')
        else:
            return self._board.get_board_position(position_x, position_y)

    def show_reserve(self, player_name):
        """
        This method accesses the Player class's player instance from the player's name in the argument
        (which is case-insensitive), and returns the number of pieces the player has in their reserve holdings.
        """

        # Checks if the player is a valid player in the game instance.
        if player_name not in self._board.get_names_list():
            return False
        player = self.get_player_from_name(player_name)
        return player.get_reserves()

    def show_captured(self, player_name):
        """
        This method accesses the Player class's player instance from the player's name in the argument
        (which is case-insensitive), and returns the number of opponent pieces the player has captured.
        """

        player = self.get_player_from_name(player_name)
        return player.get_captures()

    def reserved_move(self, player_name, position):
        """
        This method accesses the Player class's player instance from the player's name in the argument
        (which is case-insensitive), and takes a reserve piece from the player's reserve piece list
        and places the reserved piece on the board at the location argument provided. After placing the
        reserved piece onto the board, the number of the player's reserved pieces decreases by 1. If
        the player has no reserve pieces the move is not considered valid. If the move is not valid, an
        error is raised that returns "no pieces in reserve."
        """

        player = self.get_player_from_name(player_name)
        color = player.get_player_color()
        position_x = position[0]
        position_y = position[1]

        # Checks if the position passed is a valid x-y tuple coordinate.
        if len(position) != 2:
            raise InvalidLocation('invalid location on the board')
        # Checks if the player has reserve pieces.
        if player.get_reserves() == 0:
            raise PlayerPieceError('no pieces in reserve')

        # Checks if the piece can be placed on the board.
        if self._board.get_board_position(position_x, position_y) is True:
            if self._board.check_turn().lower() == player_name.lower():

                # Makes the reserve move.
                self._board.make_reserved_move(color, position_x, position_y, player)

                # Checks for a win.
                check_for_win = self._board.check_win(player)
                if check_for_win == 'win':
                    return player_name + 'wins!'
                if check_for_win == 'successfully moved':
                    return 'successfully moved'
                return self._board.update_turn(player)

            else:
                raise PlayerTurnError('not your turn')

        else:
            raise InvalidLocation('invalid location on board')


class Board:
    """
    The Board class creates a 6x6 Board instance for the Focus game. The FocusGame class creates the Board class.
    The Board class interacts with the Player and the Game class by holding/recording/updating all board
    variables and attributes. The Board class is integral to the focus game because the Game class checks
    player move validity via the Board class methods.
    """
    def __init__(self, player1, player2):
        """
        The initialization class that takes two player tuples that contain player names and player piece colors
        as well as an empty list variable. The board is created on the empty board list.
        """

        self.player1 = Player(player1)
        self.player2 = Player(player2)

        # Set up the board.
        self._board = [[[] for y in range(6)] for x in range(6)]

        # Add player pieces to the board.
        count = 0
        for board_list in self._board:
            for i in board_list:
                if count >= 2:
                    i.append(self.player2.get_player_color())
                    count += 1
                if count < 2:
                    i.append(self.player1.get_player_color())
                    count += 1
                if count == 4:
                    count = 0

        # Creates a variable that will record the last player who had a successful move.
        self._last_move = ''
        self._names_list = [self.player1.get_player_name().lower(), self.player2.get_player_name().lower()]


    def get_names_list(self):
        """
        Returns the private list that holds the name of each player.
        """

        return self._names_list

    def get_board_position(self, x_coord, y_coord):
        """
        Returns the board position for the x and y coordinates of the board.
        """

        return self._board[x_coord][y_coord]

    def check_turn(self):
        """
        Returns the private data variable of the player that moved last.
        """

        # Returns the first player if it is the first move of the game.
        if self._last_move == '':
            return self.player1.get_player_name()

        # Returns the player whose turn it is after checking the _last_move variable.

        else:
            # Returns player 2 if the last move was by player 1.
            if self._last_move == self.player1.get_player_name():
                return self.player2.get_player_name().lower()

            # Returns player 1 if the last move was by player 2.
            if self._last_move == self.player2.get_player_name():
                return self.player1.get_player_name()

    def start_validation(self, player, start, end, pieces):
        """
        This method checks the start and end location validity of the move. If the move passes the checks
        and is deemed viable, another function is called to verify that checks the movement's direction.
        """

        # Gets the x and y coordinates for start and end positions.
        start_x = start[0]
        start_y = start[1]
        end_x = end[0]
        end_y = end[1]
        stack_start = self._board[start_x][start_y]

        # Checks that the positions on the board passed are x-y coordinates.
        if (len(start)) != 2 or (len(end)) != 2:
            raise InvalidLocation('invalid location')

        # Checks that the move has a player piece on the start location.
        if stack_start == []:
            raise InvalidLocation('no piece on start location')

        # Affirms that the player's piece is at the top of the piece stack on the board's start position.
        if player.get_player_color() not in stack_start[-1]:
            raise PlayerPieceError('not your piece')

        # Makes sure the start position and end position are on the board.
        if start_x > 5 or start_x < 0:
            raise InvalidLocation('invalid location')
        if start_y > 5 or start_y < 0:
            raise InvalidLocation('invalid location')
        if end_x > 5 or end_x < 0:
            raise InvalidLocation('invalid location')
        if end_y > 5 or end_y < 0:
            raise InvalidLocation('invalid location')

        # Two types of valid movement is specified: forward and backward. Both movement directions
        # have their own function.
        if end > start:
            self.forward_piece_validation(player, start, end, pieces, start_x, start_y, end_x, end_y)
        if start > end:
            self.backward_piece_validation(player, start, end, pieces, start_x, start_y, end_x, end_y)

        # Confirms that the move does not stay in the same place.
        if end == start:
            raise InvalidLocation('piece does not move')

    def forward_piece_validation(self, player, start, end, pieces, start_x, start_y, end_x, end_y):
        """
        This function checks the validity of the move that travels forward on the board, or if the piece starts at a
        board location that is less than its end location. If the piece passes the validity checks, then it is
        passed to a movement function.
        """

        # Determines the x-y coordinate movement of the piece.
        vertical = end_x - start_x
        horizontal = end_y - start_y

        # Affirms the validity of a move that is horizontal.
        if vertical == 0 and horizontal > 0:

            # Ensures the pieces moved equal the amount of proposed board movement.
            if pieces == horizontal:
                if pieces <= len(self._board[start_x][start_y]):
                    self.make_horizontal_move(player, start, end, pieces, horizontal, start_x, start_y, end_x,
                                              end_y, temp=0, count=0)
                else:
                    raise PlayerPieceError('invalid number of pieces')

            else:
                raise PlayerPieceError('invalid number of pieces')

        # Affirms the validity of a move that is vertical.
        if horizontal == 0 and vertical > 0:

            # Ensures the pieces moved equal the amount of proposed board movement.
            if pieces == vertical:
                if pieces <= len(self._board[start_x][start_y]):
                    self.make_vertical_move(player, start, end, pieces, vertical, start_x, start_y, end_x,
                                            end_y, temp=0, count=0)
                else:
                    raise PlayerPieceError('invalid number of pieces')

            else:
                raise PlayerPieceError('invalid number of pieces')

        # Does not allow diagonal moves.
        if horizontal != 0:
            if vertical != 0:
                raise InvalidLocation('diagonal moves not allowed')

    def backward_piece_validation(self, player, start, end, pieces, start_x, start_y, end_x, end_y):
        """
        This function checks the validity of the move that travels backwards on the board, or if the piece starts at a
        board location that is greater than its end location. If the piece passes the validity checks, then it is
        passed to a movement function.
        """

        # Obtains the vertical and horizontal movement of the piece.
        vertical = start_x - end_x
        horizontal = start_y - end_y

        # Checks a horizontal move.
        if vertical == 0 and horizontal > 0:
            if pieces == horizontal:
                if pieces <= len(self._board[start_x][start_y]):
                    self.make_horizontal_move(player, start, end, pieces, -horizontal, start_x, start_y, end_x,
                                              end_y, temp=0, count=0)
                else:
                    raise PlayerPieceError('invalid number of pieces')

            if pieces > horizontal or pieces < horizontal:
                raise PlayerPieceError('invalid number of pieces')

        # Checks a vertical move.
        if horizontal == 0 and vertical > 0:
            if pieces == vertical:
                if pieces >= len(self._board[start_x][start_y]):
                    # print(pieces >= len(self._board[start_x][start_y]))
                    self.make_vertical_move(player, start, end, pieces, -vertical, start_x, start_y, end_x,
                                            end_y, temp=0, count=0)
                else:
                    raise PlayerPieceError('invalid number of pieces')

            if pieces < vertical or pieces > vertical:
                raise PlayerPieceError('invalid number of pieces')

        # Does not allow a diagonal move.
        if horizontal != 0:
            if vertical != 0:
                raise InvalidLocation('diagonal moves not allowed')

    def make_vertical_move(self, player, start, end, pieces, vertical, start_x, start_y, end_x, end_y, temp, count):
        """
        This is a recursive function that vertically moves a piece from its start position to the end position.
        It returns "successfully moved" or "player wins."
        """

        position = self._board[start_x][start_y]

        if (start_x, start_y) == (end_x, end_y):
            self.push(position, temp)

            # Takes pieces from the bottom of the stack at the final position that are more than 5 and
            # puts them in the player's reserve or player's capture holdings.
            if len(position) > 5:
                length = len(position)
                over = 5 - length
                confiscated_pieces = position[0: over]
                player.add_reserves_or_captures(confiscated_pieces)

            # Updates the player turn.
            self.update_turn(player)
            check_for_win = self.check_win(player)
            if check_for_win == 'win':
                return player + 'wins!'
            if check_for_win == 'successfully moved':
                return 'successfully moved'

        if (start_x, start_y) != (end_x, end_y):
            if count == 0:
                if len(position) > 1:
                    piece_holder = []
                    for game_pieces in range(len(position)):
                        piece_holder.append(self.pop(position))
                        temp = piece_holder[::-1]

                else:
                    temp = self.pop(position)

            # Recursive call for the function.
            if vertical > 0:
                self.make_vertical_move(player, start, end, pieces, vertical, start_x+1, start_y, end_x,
                                        end_y, temp, count + 1)
            if vertical < 0:
                self.make_vertical_move(player, start, end, pieces, vertical, start_x-1, start_y, end_x,
                                        end_y, temp, count + 1)

    def make_horizontal_move(self, player, start, end, pieces, horizontal, start_x, start_y, end_x, end_y, temp, count):
        """
        This is a recursive function that horizontally moves a piece from its start position to the end position.
        It returns "successfully moved" or "player wins."
        """

        position = self._board[start_x][start_y]

        if (start_x, start_y) == (end_x, end_y):
            self.push(position, temp)

            # Takes pieces from the bottom of the stack at the final position that are more than 5 and
            # puts them in the player's reserve or player's capture holdings.
            if len(position) > 5:
                length = len(position)

                over = length - 5

                confiscated_pieces = position[0: over]
                player.add_reserves_or_captures(confiscated_pieces)
                del position[0: over]

            # Updates the player turn.
            self.update_turn(player)

            # Checks the win conditions for the player.
            check_for_win = self.check_win(player)
            if check_for_win == 'win':
                return player + 'wins!'
            if check_for_win == 'successfully moved':
                return 'successfully moved'

        if (start_x, start_y) != (end_x, end_y):
            if count == 0:
                if len(position) > 1:
                    piece_holder = []
                    for game_pieces in range(len(position)):
                        piece_holder.append(self.pop(position))
                        temp = piece_holder[::-1]

                else:
                    temp = self.pop(position)

            # Recursive call for moving another space on the board.
            if horizontal > 0:
                self.make_horizontal_move(player, start, end, pieces, horizontal, start_x, start_y+1, end_x,
                                          end_y, temp, count + 1)
            if horizontal < 0:
                self.make_horizontal_move(player, start, end, pieces, horizontal, start_x, start_y-1, end_x,
                                          end_y, temp, count + 1)


    def make_reserved_move(self, color, location_x, location_y, player):
        """
        Makes a reserve move for the player from the player's reserve pieces.
        """

        # Checks the location on the board
        location = self._board[location_x][location_y]
        location.append(color)

        # Takes the pieces over 5 at the end position and adds them to reserves/captures.
        if len(location) > 5:
            length = len(location)
            over = length - 5
            confiscated_pieces = location[0: over]
            player.add_reserves_or_captures(confiscated_pieces)
            del location[0: over]

        # Removes a reserve piece from the player's reserve holdings.
        player.remove_1reserve()

    def pop(self, stack):
        """
        Pops a piece of the stack off of the top. Returns the top piece.
        """

        val = stack[-1]
        del stack[-1]
        return val

    def push(self, position, stack):
        """
        Pushes a piece or pieces onto the piece stack at the top or end of the piece list.
        """

        for element in stack:
            position.append(element)

    def update_turn(self, player):
        """
        Updates the _last_move variable to the player that just moved.
        """

        self._last_move = player.get_player_name()

    def check_win(self, player):
        """
        Checks the win conditions for the game. Returns "successfully moved" or "win."
        """

        # Collects the number of player captures.
        captures = player.get_captures()

        # If the player captures 6 enemy pieces, the game is won. "Win" is returned.
        if captures > 5:
            return "win"
        if captures < 5:
            return "successfully moved"


class Player:
    """
    The Player class creates the two player instances for the Focus game. The Player class contains the color of
    the pieces for each player. This class also holds the reserve pieces and the captured pieces
    for each player. The Player class interacts with the Board and the Game classes in order to play the Focus game.
    """
    def __init__(self, _player):
        """
        This method initializes the player's private attributes from the player tuple argument.
        """

        self._player = _player
        self._player_name = self._player[0]
        self._player_color = self._player[1]
        self._reserves = []
        self._captures = []

    def get_player_name(self):
        """
        This method is the "getter" method that returns the private name data attribute for the player.
        """

        return self._player[0]

    def get_player_color(self):
        """
        This method is the "getter" method that returns the private color data attribute for the player.
        """

        return self._player_color

    def get_player_from_name(self, name):
        """
        Returns the player instance from the player name.
        """

        if name.lower() in self._player.lower():
            return self._player

    def get_captures(self):
        """
        The method returns the number of captured opponent pieces.
        """

        if len(self._captures) == 0:
            return 0
        else:
            return len(self._captures)

    def get_reserves(self):
        """
        Returns the number of reserve pieces a player holds.
        """

        if len(self._reserves) == 0:
            return 0
        else:
            return len(self._reserves)

    def remove_1reserve(self):
        """
        Removes the number of reserved pieces by one.
        """

        if len(self._reserves) > 0:
            del self._reserves[-1]

    def add_reserves_or_captures(self, pieces_list):
        """
        Adds captured or reserve pieces into a player's holdings.
        """

        for i in pieces_list:
            if i == self._player_color:
                self._reserves.append(i)
            else:
                self._captures.append(i)


class PlayerTurnError(Exception):
    """
    This is an error message that is raised if a player is attempting to make a move out of turn.
    """
    pass


class PlayerNameError(Exception):
    """
    This is an error message that is raised if the player's name is not found in the Player instances of
    the Focus game.
    """
    pass


class InvalidLocation(Exception):
    """
    This is an error message when an invalid location has been entered as an argument.
    """
    pass


class PlayerPieceError(Exception):
    """
    This error message occurs when a player's piece is not playable.
    """
    pass


# playa1 = ("Drew", 'r')
# playa2 = ("Ellie", 'g')
# game1 = FocusGame(playa1, playa2)

# game1.move_piece("dREw", (2, 1), (2, 0), 1)
# game1.move_piece("ellie", (3, 0), (1, 0), 1)
# game1.move_piece("drew", (0, 1), (1, 1), 1)
# game1.move_piece("eLLie", (2, 0), (2, 2), 2)
# game1.move_piece("DREW", (1, 1), (1, 0), 1)
# game1.move_piece("ELlIE", (2, 2), (3, 2), 1)
# game1.move_piece("DreW", (5, 3), (5, 4), 1)
# game1.move_piece("Ellie", (3, 2), (3, 3), 1)