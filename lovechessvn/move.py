import random

import chess

from . import GameContext, security, utils

TEXT = {
    chess.PAWN: [
        "đẩy tốt {end}",
        "dí tốt {end}",
        "lên tốt {end}",
        "tốt {end}",
        "dâng tốt {end}",
        "thúc tốt lên {end}",
    ],
    chess.KNIGHT: [
        "nhảy mã {end}",
        "di chuyển mã lên {end}",
        "lùi mã về {end}",
    ],
    chess.BISHOP: ["phi tượng {end}", "lùi tượng {end}", "đưa tượng lên {end}"],
    chess.ROOK: ["qua xe {end}", "di chuyển xe qua {end}", "đưa xe qua {end}"],
    chess.QUEEN: ["ăn hậu vào {end}"],
    chess.KING: ["vào vua {end}", "lên vua {end}"],
}


def gen_move(board: chess.Board, context: GameContext) -> str:
    moving_piece = board.piece_at(context.move.from_square)
    if moving_piece is None:
        raise ValueError("Bruh wtf")
    if board.piece_at(context.move.to_square) is not None:
        return security.safe_format(
            random.choice(
                [
                    "ăn {piece} vào {end}",
                    "ăn {piece} lên {end}",
                    "đổi {piece} vào {end}",
                ]
            ),
            piece=utils.name(moving_piece),
            end=chess.square_name(context.move.to_square),
        )

    return security.safe_format(
        random.choice(TEXT[moving_piece.piece_type]),
        piece=utils.name(moving_piece),
        end=chess.square_name(context.move.to_square),
    )
