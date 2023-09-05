import chess

VALUES = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 9999}

NAMES = {"P": "tốt", "N": "mã", "B": "tượng", "R": "xe", "Q": "hậu", "K": "vua"}


def capitalize(text: str) -> str:
    return text[0].upper() + text[1:]


def value_of(piece: chess.Piece) -> int:
    return VALUES[piece.symbol().upper()]


def name(piece: chess.Piece | int) -> str:
    if isinstance(piece, int):
        return NAMES[chess.PIECE_SYMBOLS[chess.PIECE_TYPES.index(piece)].upper()]
    return NAMES[piece.symbol().upper()]


def reverse(color: chess.Color) -> chess.Color:
    return chess.WHITE if color == chess.BLACK else chess.BLACK


def player_color(color: bool) -> str:
    return "trắng" if color else "đen"
