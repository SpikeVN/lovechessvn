import random

import chess
import chess.engine

from . import config, move, utils, purpose
from .context import GameContext
from .stockfish import ENGINE


def gen_prompt(board: chess.Board, context: GameContext) -> tuple[str, int]:
    mem_board = chess.Board(board.fen())
    moving_piece = mem_board.piece_at(context.move.from_square)
    if moving_piece is None:
        raise ValueError("Bruh wtf")
    move_text = move.gen_move(board, context)

    if len(board.move_stack) == 0:
        return (
            f"{utils.capitalize(context.player)} sử dụng tuyệt chiêu {move_text} để khởi đầu ván cờ",
            0,
        )

    if mem_board.is_castling(context.move):
        return random.choice(
            [
                (
                    f"{utils.capitalize(context.player)} nhập thành, đưa vua vào vị trí an toàn, chuẩn bị cho các trận đánh lớn",
                    1,
                ),
                (
                    f"Không dám để vua ở giữa bàn cờ thêm, nên {context.player} vội vã nhập thành, đưa vua vào góc bàn cờ",
                    2,
                ),
            ]
        )

    analysis = ENGINE.analyse(
        mem_board,
        limit=chess.engine.Limit(
            time=config.get_config("max_time"), depth=config.get_config("max_depth")
        ),
    )
    if "score" in analysis and analysis["score"].turn == (not context.player_color):
        return random.choice(
            [
                (f"Thừa thế xông lên, {context.player} {move_text}", 3),
                (
                    f"Trước sự ngông nghênh của đối thủ, {context.player} nghiến răng {move_text}, quyết dạy cho đối thủ một bài học",
                    4,
                ),
            ]
        )

    former_attackers = mem_board.attackers(
        utils.reverse(context.player_color), context.move.from_square
    )

    mem_board.push(context.move)

    if len(mem_board.checkers()) != 0:
        return f"Thấy vua đối phương vừa nhô lên, {context.player} liền {move_text}", 5

    contemporary_attackers = mem_board.attackers(
        utils.reverse(context.player_color), context.move.to_square
    )
    for attacker in former_attackers:
        attacker_piece = mem_board.piece_at(attacker)

        if attacker_piece is None:
            continue
        print(attacker_piece, chess.square_name(attacker))
        if utils.value_of(attacker_piece) >= utils.value_of(moving_piece):
            if attacker not in contemporary_attackers:
                if attacker_piece.symbol in ("r", "R"):
                    return (
                        f"{utils.capitalize(context.player)} chạy {moving_piece} sang {chess.square_name(context.move.to_square)}",
                        6,
                    )
                else:
                    return (
                        f"{utils.capitalize(context.player)} chạy {moving_piece} lên {chess.square_name(context.move.to_square)}",
                        7,
                    )
            else:
                return (
                    f"{utils.capitalize(context.player)} bất ngờ bỏ {moving_piece} {move_text}",
                    8,
                )

    rand = [
        (
            f"{utils.capitalize(context.player)} {move_text}",
            17,
        ),
        (
            f"{utils.capitalize(context.player)} {move_text}",
            18,
        ),
        (
            f"{utils.capitalize(context.player)} {move_text}",
            19,
        ),
        (
            f"{utils.capitalize(context.player)} {move_text}",
            20,
        ),
        (
            f"{utils.capitalize(context.player)} {move_text}",
            21,
        ),
    ]

    center_contenders = (
        list(mem_board.attackers(context.player_color, chess.E4))
        + list(mem_board.attackers(context.player_color, chess.E5))
        + list(mem_board.attackers(context.player_color, chess.D4))
        + list(mem_board.attackers(context.player_color, chess.D5))
    )

    if context.move.to_square in center_contenders:
        if moving_piece.symbol().lower() in ("b", "n", "q"):
            rand += [
                (
                    f"{utils.capitalize(context.player)} {move_text} chĩa về phía trung tâm, sẵn sàng khai hỏa",
                    9,
                )
            ]
        rand += [
            (
                f"{utils.capitalize(context.player)} phát triển {utils.name(moving_piece)} lên {chess.square_name(context.move.to_square)}, đưa quân ra củng cố trung tâm",
                10,
            )
        ]

    if context.move.to_square in (chess.E4, chess.E5, chess.D4, chess.D5):
        rand += [
            (
                f"{utils.capitalize(context.player)} quyết tâm dành thế chủ động trên chiến trường nên mạnh mẽ {move_text}",
                11,
            )
        ] * config.get_config("response_weight")

    if len(mem_board.move_stack) >= 1:
        rand += [
            (
                f"{utils.capitalize(context.player)} nhanh chóng đáp trả bằng nước {move_text}",
                12,
            ),
            (
                f"{utils.capitalize(context.player)} cũng không phải tay vừa, nên {move_text}",
                13,
            ),
            (f"Không chậm trễ, {utils.capitalize(context.player)} {move_text}", 14),
            (
                f"Không để {utils.player_color(utils.reverse(context.player_color))} phải chờ lâu, {utils.capitalize(context.player)} nhanh chóng {move_text}",
                15,
            ),
            (
                f"Sau một hồi suy nghĩ, {utils.capitalize(context.player)} đáp trả bằng {move_text}",
                16,
            ),
        ]

    root = random.choice(rand)
    p = purpose.gen_purpose(board, context)
    if p == "":
        return root[0] + ".", root[1]
    else:
        return root[0] + ", " + p + ".", root[1]
