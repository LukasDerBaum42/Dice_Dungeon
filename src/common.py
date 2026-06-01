import random
from random import Random, choice, randint

def p_chois(opption: dict[str, int]) -> str:
    changs1 = 0
    changs2 = 0
    rand_num = random.randint(1, 100)
    ops: list[str] = []
    out : str | None = None
    for j in opption:
        ops.append(j)
        p = opption[j]
        changs1 = changs2
        changs2 += p
        if (changs1 < rand_num) and (rand_num <= changs2):
            out = j
            break
    if out == None:
        out = str(Random.choice(ops))
    return out