import random

import chess

from . import GameContext, utils, security


def gen_purpose(board: chess.Board, context: GameContext) -> str:
    moving_piece = board.piece_at(context.move.from_square)
    mem_board = chess.Board(board.fen())
    rand = [""] * 5 + ["móc lốp", "chơi nhây"]

    if moving_piece is None:
        raise ValueError("Bruh wtf")

    prev_atk = mem_board.attackers(
        utils.reverse(context.player_color), context.move.from_square
    )

    if mem_board.is_check() and mem_board.is_legal(context.move):
        rand += ["che chắn cho vua"] * 3
    mem_board.push(context.move)

    if context.move.to_square in (chess.E4, chess.E5, chess.D4, chess.D5):
        rand += ["đứng tấn ở trung tâm bao quát thế trận"] * 2

    con_atk = mem_board.attackers(
        utils.reverse(context.player_color), context.move.to_square
    )

    for atk in con_atk:
        if atk not in prev_atk and mem_board.piece_at(atk).symbol().upper() not in (
            "K",
            "P",
        ):
            rand += [
                "tránh khỏi tầm ngắm của quân {piece}",
                "tránh đòn",
            ]

    attacking = mem_board.attacks(context.move.to_square)

    for victim in attacking:
        victim_piece = mem_board.piece_at(victim)
        if victim_piece is None:
            continue
            # print(mem_board)
            # print(chess.square_name(victim))
            # raise ValueError("Bruh wtf")
        if victim_piece.color == moving_piece.color:
            continue

        threat = utils.NAMES[victim_piece.symbol().upper()]
        threat_move_end = chess.square_name(victim)
        if utils.value_of(victim_piece) > utils.value_of(moving_piece):
            if board.piece_at(victim).symbol().upper() in ("Q", "K", "R"):
                rand += [
                    f"truy sát {threat}",
                    f"bắt {threat}",
                ] * 2
            rand += [
                f"đuổi {threat}",
                f"tấn công {threat}",
                f"bắt lại con {threat} {threat_move_end}",
                "rình",
            ] * 2
            rand.append("tìm cách bắn tỉa các quân của {opponent}")
        elif utils.value_of(victim_piece) == utils.value_of(moving_piece):
            rand += [
                "gạ đổi",
                f"ép {utils.capitalize(context.player)} phải đổi {threat}",
                "đổi bớt quân cho nó thoáng cờ",
            ] * 2

    return security.safe_format(
        random.choice(rand),
        player=utils.capitalize(context.player),
        opponent=utils.capitalize(context.opponent),
    )
