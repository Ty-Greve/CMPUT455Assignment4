'''
Assignment4.py will provide a space to override class commands from gtp_connection and GoBoard
for the use in Assignment 4 and will help streamline and organize things hopefully

Changes:
---- Kade ----

----  Ty  ----

-- Sebastian --
'''


### Imports ###
import time
from gtp_connection import (
    GtpConnection,
    point_to_coord,
    format_point,
    move_to_coord,
    color_to_int
    )

from board import GoBoard

 ### GtpConnection imports
import traceback
import numpy as np
import re
from sys import stdin, stdout, stderr
from typing import Any, Callable, Dict, List, Tuple

from board_base import (
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    GO_COLOR, GO_POINT,
    PASS,
    MAXSIZE,
    coord_to_point,
    opponent
)
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine

 ### Board Imports ###
import numpy as np
from typing import List, Tuple

from board_base import (
    board_array_size,
    coord_to_point,
    is_black_white,
    is_black_white_empty,
    opponent,
    where1d,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    MAXSIZE,
    NO_POINT,
    PASS,
    GO_COLOR,
    GO_POINT,
)




### Overwrites for GoBoard Class here

class A4GoBoard(GoBoard):
    def __init__(self, size: int) -> None:
        """
        Creates a Go board of given size
        Adds a change stack to the Board
        """
        assert 2 <= size <= MAXSIZE
        self.reset(size)
        self.calculate_rows_cols_diags() #removed for new implementation
        self.black_captures = 0
        self.white_captures = 0

        ### Student implemented ###                                                         
        # if there is no capture from the move then the move is just stored as a list with one point
        # if there is multiple captures, all captured pieces are listed after the move that captured them
        #[[color, point, cap,...], [color, point, cap,...], ...]
        self.change_stack = [] # Stack containing data as [[Color of current player, GoPoint for first move, GoPoint for capture, GoPoint for capture,...], ...]



### Overwrites for gtp_connection Class here

class A4GtpConnection(GtpConnection):
    def __init__(self, go_engine: GoEngine, board: GoBoard, debug_mode: bool = False) -> None:
        """
        Manage a GTP connection for a Go-playing engine

        Parameters
        ----------
        go_engine:
            a program that can reply to a set of GTP commandsbelow
        board: 
            Represents the current board state.
        """
        self._debug_mode: bool = debug_mode
        self.go_engine = go_engine
        self.board: GoBoard = board

        self.policy = "random"

        self.commands: Dict[str, Callable[[List[str]], None]] = {
            "protocol_version": self.protocol_version_cmd,
            "quit": self.quit_cmd,
            "name": self.name_cmd,
            "boardsize": self.boardsize_cmd,
            "showboard": self.showboard_cmd,
            "clear_board": self.clear_board_cmd,
            "komi": self.komi_cmd,
            "version": self.version_cmd,
            "known_command": self.known_command_cmd,
            "genmove": self.genmove_cmd,
            "list_commands": self.list_commands_cmd,
            "play": self.play_cmd,
            "legal_moves": self.legal_moves_cmd,
            "gogui-rules_legal_moves": self.gogui_rules_legal_moves_cmd,
            "gogui-rules_final_result": self.gogui_rules_final_result_cmd,
            "gogui-rules_captured_count": self.gogui_rules_captured_count_cmd,
            "gogui-rules_game_id": self.gogui_rules_game_id_cmd,
            "gogui-rules_board_size": self.gogui_rules_board_size_cmd,
            "gogui-rules_side_to_move": self.gogui_rules_side_to_move_cmd,
            "gogui-rules_board": self.gogui_rules_board_cmd,
            "gogui-analyze_commands": self.gogui_analyze_cmd,
            "timelimit": self.timelimit_cmd,
            "solve": self.solve_cmd,
            # New Added functions for A3
            #"policy": self.policy_cmd,
            #"policy_moves": self.policy_moves_cmd
            }

        # argmap is used for argument checking
        # values: (required number of arguments,
        #          error message on argnum failure)
        self.argmap: Dict[str, Tuple[int, str]] = {
            "boardsize": (1, "Usage: boardsize INT"),
            "komi": (1, "Usage: komi FLOAT"),
            "known_command": (1, "Usage: known_command CMD_NAME"),
            "genmove": (1, "Usage: genmove {w,b}"),
            "play": (2, "Usage: play {b,w} MOVE"),
            "legal_moves": (1, "Usage: legal_moves {w,b}"),
        }



### The player for the A4 Project

class A4Player(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, "A4Player", 1.0)
        self.start_time = time.time()
        self.time_limit = 45

    def start_timer(self):
        self.start_time = time.time()

    def is_time_up(self) -> bool:
        return self.start_time > self.time_limit

    def get_move(self, state: GoBoard) -> GO_POINT:
        '''
        return a move for the A4 Player as a go point (int)
        '''
        pass

    def get_policy_moves(self) -> list:
        '''
        return a list of moves for the policies we decide to implement.
        Possible policies:
        'Win', 'Block Win', 'OpenFour', 'Block open four', 'random'
        '''


### These effectively allow this file to replace the Ninuki.py file ###
def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    size = 7
    board: A4GoBoard = GoBoard(size)
    con: GtpConnection = A4GtpConnection(A4Player(), board)
    con.start_connection()

if __name__ == "__main__":
    run()