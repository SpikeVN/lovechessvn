import chess

import lovechessvn

b = chess.Board()

PEN = "1. e4 e5 2. Bc4 Nf6 3. Nf3 Nc6 4. d3 Bc5 5. Nc3"
HISTORY = []


def mv(san: str) -> None:
    move = b.parse_san(san)
    t = lovechessvn.gen_prompt(
        b,
        lovechessvn.GameContext(
            lovechessvn.player_color(b.turn),
            lovechessvn.player_color(not b.turn),
            b.turn,
            move,
        ),
    )
    if len(HISTORY) >= 3:
        while t[1] in (HISTORY[-1][1], HISTORY[-2][1], HISTORY[-3][1]):
            t = lovechessvn.gen_prompt(
                b,
                lovechessvn.GameContext(
                    lovechessvn.player_color(b.turn),
                    lovechessvn.player_color(not b.turn),
                    b.turn,
                    move,
                ),
            )
    elif len(HISTORY) > 0:
        while t[1] == HISTORY[-1][1]:
            t = lovechessvn.gen_prompt(
                b,
                lovechessvn.GameContext(
                    lovechessvn.player_color(b.turn),
                    lovechessvn.player_color(not b.turn),
                    b.turn,
                    move,
                ),
            )
    HISTORY.append(t)
    print(t[0])
    b.push(move)


for m in PEN.split():
    if "." in m:
        continue
    mv(m)

lovechessvn.ENGINE.quit()
