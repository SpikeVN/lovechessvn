from dataclasses import dataclass

import chess


@dataclass
class GameContext:
    player: str
    opponent: str
    player_color: chess.Color
    move: chess.Move
