# Author: Fern Burke
# GitHub username: burkeOSU
# Date: 03/14/2025
# Description: A "King of the Hill" variant of chess. Game can be won be either:
# 1.) Capturing the opponent's king, or
# 2.) Moving your king to one of the 4 center squares (d4, e4, d5 or e5).
# There is no check, checkmate, castling, en passant, or pawn promotion.
# White goes first.

class ChessVar:
    """Implements "King of the Hill" variant of chess:
    - Manages game state (unfinished, black or white won)
    - Validates/plays moves
    - Tracks turn order
    - Determines winner based on whether king is captured or king is in one of 4 central squares."""

    def __init__(self):
        """Initializes game with Board class object (stores initial piece positions)."""
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._turn = "WHITE"  # White always starts first

    def get_game_state(self):
        """Returns 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'."""
        return self._game_state

    def get_board(self):
        """Returns board as nested list:
        lowercase letters represent black pieces;
        uppercase letters represent white pieces;
        and empty squares are represented by ' '."""
        return self._board.get_board()

    def get_turn(self):
        """Returns current player's turn."""
        return self._turn

    def get_piece_at(self, position):
        """Returns piece at given position on board."""
        return self._board.get_piece_at(position)

    def make_move(self, current_square, next_square):
        """Moves piece from current_square to next_square:
        - Checks if move is legal based on current player's turn and piece movement rules
        - Captures opponent's piece if present
        - Updates board state and turn order
        - Checks if game has ended

        Parameters:
        - current_square: Current square piece is on; uses a-h for x-axis and 1-8 for y-axis (e.g. "e1")
        - next_square: Square piece is moving to (e.g. "e2")

        Returns:
        - True if the move is valid and performed
        - False if the move is invalid."""
        # Invalid move: Game already over
        if self._game_state != "UNFINISHED":
            return False

        # Invalid move: Current or next square chosen is out of bounds
        if not Board.is_within_bounds(current_square) or not Board.is_within_bounds(next_square):
            return False

        # Invalid move: No piece at current/starting square
        piece = self._board.get_piece_at(current_square)
        if not piece:
            return False

        # Invalid move: Not player's turn
        if (self._turn == "WHITE" and piece.islower()) or (self._turn == "BLACK" and piece.isupper()):
            return False

        # Invalid move: Does not follow rules of chess piece
        if not Piece(piece).is_valid_move(current_square, next_square, self._board):
            return False

        # Valid move
        self._board.move_piece(current_square, next_square)

        # Win condition: King in center squares ('d4', 'e4', 'd5', 'e5')
        # Black wins
        if piece == 'k' and next_square in ['d4', 'e4', 'd5', 'e5']:
            self._game_state = "BLACK_WON"
            return True
        # White wins
        elif piece == 'K' and next_square in ['d4', 'e4', 'd5', 'e5']:
            self._game_state = "WHITE_WON"
            return True

        # Win condition: King captured
        if not self._board.king_exists("WHITE"):
            self._game_state = "BLACK_WON"
        elif not self._board.king_exists("BLACK"):
            self._game_state = "WHITE_WON"

        # Switch players for next turn
        if self._game_state == "UNFINISHED":
            self._turn = "BLACK" if self._turn == "WHITE" else "WHITE"

        return True


class Board:
    """Represents an 8x8 chessboard, maintains current game state:
    - Stores positions of all chess pieces
    - Checks board boundaries
    - Updates board when moves are made."""

    def __init__(self):
        """Initializes board as 8x8 nested list, sets up initial piece positions."""
        self._board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def get_board(self):
        """Prints current board state."""
        return self._board

    @staticmethod
    def is_within_bounds(position):
        """Checks if given position is within valid board range (1-8, a-h).

        Parameters:
        - position: The board position (e.g. "e1").

        Returns:
        - True if within bounds
        - False if out of bounds."""
        return len(position) == 2 and position[0] in "abcdefgh" and position[1] in "12345678"

    @staticmethod
    def notation_to_index(notation):
        """Converts chess notations (e.g., 'e2') to board indices (row, col)."""
        if len(notation) != 2:  # Must be 2 characters
            return None
        col, row = notation[0], notation[1]
        if col not in "abcdefgh" or row not in "12345678":
            return None
        return 8 - int(row), ord(col) - ord('a')

    def get_piece_at(self, position):
        """Identifies piece at a given position.

        Parameters:
        - position: The board position (e.g. "e1")

        Returns:
        - Piece object at chosen position, or None if empty (e.g. 'K')."""
        x, y = Board.notation_to_index(position)
        return self._board[x][y]

    def move_piece(self, current_square, next_square):
        """Moves piece from one square to another if valid.

        Parameters:
        - current_square: The starting position
        - next_square: The destination position

        Returns:
        - True if move was valid
        - False if move was invalid."""
        from_x, from_y = Board.notation_to_index(current_square)
        to_x, to_y = Board.notation_to_index(next_square)

        if from_x is None or to_x is None:
            return False

        # Piece movement
        self._board[to_x][to_y] = self._board[from_x][from_y]  # Next square becomes current square
        self._board[from_x][from_y] = ' '  # Current/past square is now blank

    def king_exists(self, color):
        """Checks if either a black or white king is still on the board."""
        king_symbol = 'K' if color == "WHITE" else 'k'
        return any(king_symbol in row for row in self._board)


class Piece:
    """Represents a chess piece and tracks its type, color, and movement rules:
    - Determines valid moves for chess piece based on its type
    - Interacts with Board class to verify moves."""

    def __init__(self, piece_type):
        """Initializes piece class object with type and color.

        Parameters:
        - piece_type: Type of piece (e.g., pawn = 'P' or 'p', king = 'k' or 'K')
        - color: Color of piece (e.g., white king = 'K', black king = 'k')."""
        self._piece_type = piece_type
        self._piece_lower = piece_type.lower()  # Store lowercase version separately

    @staticmethod
    def _path_is_clear(from_x, from_y, to_x, to_y, board):
        """Checks if there are no obstacles in the path between two squares (excluding the start and end squares)."""
        distance_x = to_x - from_x
        distance_y = to_y - from_y

        step_x = 0 if distance_x == 0 else (1 if distance_x > 0 else -1)
        step_y = 0 if distance_y == 0 else (1 if distance_y > 0 else -1)

        x, y = from_x + step_x, from_y + step_y  # Move one step from the starting square

        while (x, y) != (to_x, to_y):  # Check every square until the destination
            if board.get_piece_at(chr(y + ord('a')) + str(8 - x)) != ' ':
                return False  # Path is blocked
            x += step_x
            y += step_y

        return True  # No pieces blocking the path

    def is_valid_move(self, current_square, next_square, board):
        """Checks if a move is legal based on piece type and ensures it does not move onto its own color."""
        from_x, from_y = Board.notation_to_index(current_square)
        to_x, to_y = Board.notation_to_index(next_square)
        distance_x, distance_y = to_x - from_x, to_y - from_y  # Calculates distance

        # Get piece at destination
        piece_at_destination = board.get_piece_at(next_square)

        # Prevent moving onto a square occupied by the same color
        if piece_at_destination != ' ':
            if (self._piece_type.isupper() and piece_at_destination.isupper()) or \
                    (self._piece_type.islower() and piece_at_destination.islower()):
                return False  # Can't move onto own piece

        # Pawn rules
        if self._piece_lower == 'p':
            direction = -1 if self._piece_type.isupper() else 1  # White pawns (-1 = up), Black pawns (+1 = down)
            start_row = 6 if self._piece_type.isupper() else 1 # White starts at row 6, Black at row 1

            if distance_y == 0 and distance_x == direction:
                return board.get_piece_at(next_square) == ' '  # Must move forward to an empty space

            if distance_y == 0 and distance_x == 2 * direction and from_x == start_row:
                between_square = chr(from_y + ord('a')) + str(8 - (from_x + direction))  # Square in between
                return board.get_piece_at(between_square) == ' ' and board.get_piece_at(next_square) == ' '  # Both must be empty

            if abs(distance_y) == 1 and distance_x == direction:
                return piece_at_destination != ' ' and piece_at_destination.isupper() != self._piece_type.isupper()  # Pawns can only capture diagonally
            return False

        # Rook rules
        if self._piece_lower == 'r':
            if from_x == to_x or from_y == to_y:  # Moves vertically or horizontally
                return Piece._path_is_clear(from_x, from_y, to_x, to_y, board)  # Check for obstacles
            return False

        # Bishop rules
        if self._piece_lower == 'b':
            if abs(distance_x) == abs(distance_y):  # Moves diagonally
                return Piece._path_is_clear(from_x, from_y, to_x, to_y, board)  # Check for obstacles
            return False

        # Knight rules
        if self._piece_lower == 'n':
            if (abs(distance_x), abs(distance_y)) in [(2, 1), (1, 2)]:  # Moves in "L" shape
                return piece_at_destination == ' ' or piece_at_destination.isupper() != self._piece_type.isupper()
            return False

        # Queen rules
        if self._piece_lower == 'q':
            if from_x == to_x or from_y == to_y or abs(distance_x) == abs(
                    distance_y):  # Moves vertically, horizontally and diagonally
                return Piece._path_is_clear(from_x, from_y, to_x, to_y, board)  # Check for obstacles
            return False

        # King rules
        if self._piece_lower == 'k':
            if max(abs(distance_x), abs(distance_y)) == 1:  # Moves 1 square in any direction
                return piece_at_destination == ' ' or piece_at_destination.isupper() != self._piece_type.isupper()
            return False

        return False

    def get_valid_moves(self, position, board):
        """Prints all valid moves for chosen piece based on movement rules.

        Parameters:
        - position: Piece's current position
        - board: Board state

        Returns:
        - List of valid move positions."""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                next_square = chr(col + ord('a')) + str(8 - row)
                if self.is_valid_move(position, next_square, board):
                    valid_moves.append(next_square)
        return valid_moves


def main():
    """Main function to play King of the Hill Chess with Unicode Chess Pieces (Tab-Aligned Board)."""
    game = ChessVar()

    # Unicode mapping for chess pieces
    unicode_pieces = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',  # White pieces
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',  # Black pieces
        ' ': '·'  # Represent empty squares with a small dot
    }

    print("\nWelcome to King of the Hill Chess!")
    print("Enter moves in algebraic notation (e.g., 'e2 e4').")
    print("Type 'moves __' to see possible moves for the piece at that square (e.g., 'moves e2').")
    print("Type 'quit' to quit.")

    while game.get_game_state() == "UNFINISHED":
        print("\nCurrent Board:")
        board = game.get_board()

        # Print column labels
        print("a\tb\tc\td\te\tf\tg\th")

        # Display board with row numbers aligned on the right
        for i, row in enumerate(board):
            unicode_row = [unicode_pieces.get(piece, piece) for piece in row]  # Replace with Unicode
            formatted_row = "\t".join(unicode_row)  # Use tabs between pieces
            print(f"{formatted_row}\t{8 - i}")  # Row numbers (8 to 1) aligned properly

        # Get input from the player
        current_turn = game.get_turn()
        king_symbol = '♔' if current_turn == "WHITE" else '♚'
        move_prompt = f"\n{current_turn}'s ({king_symbol}) turn. Enter move (e.g., 'e2 e4') or 'moves __' (e.g., moves e4'): "

        move = input(move_prompt).strip().lower()

        # Exit condition
        if move == "quit":
            print("\nThanks for playing! See you again soon!")
            break

        # Check for "moves __" command
        if move.startswith("moves"):
            try:
                _, position = move.split()  # Extract position (e.g., "e4")
                piece = game.get_piece_at(position)

                if piece and piece != ' ':
                    possible_moves = Piece(piece).get_valid_moves(position, game)

                    if possible_moves:
                        print(
                            f"Possible moves for {unicode_pieces.get(piece, piece)} at {position}: {', '.join(possible_moves)}")

                    else:
                        print(f"No legal moves for {unicode_pieces.get(piece, piece)} at {position}.")

                else:
                    print(f"No piece at {position}!")

            except ValueError:
                print("Invalid move command! Please enter 'moves __' (e.g., moves e4').")
            continue  # Restart loop without switching turns

        # Parse normal move command
        try:
            start, end = move.split()
        except ValueError:
            print("Invalid command! Please enter move (e.g., 'e2 e4') or 'moves __' (e.g., moves e4').")
            continue

        # Attempt move
        if not game.make_move(start, end):
            print("Invalid move! Please enter move (e.g., 'e2 e4').")
            continue

        # Check game state after move
        state = game.get_game_state()
        if state == "WHITE_WON":
            print("\nWHITE WINS! The game is over.")
            break
        elif state == "BLACK_WON":
            print("\nBLACK WINS! The game is over.")
            break

    print("\nThank you for playing King of the Hill Chess!")


# Run main function if the script is executed
if __name__ == '__main__':
    main()
