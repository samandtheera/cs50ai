# Consider what it means if a sentence is spoken by a character. Under what conditions is that sentence true?
# Under what conditions is that sentence false? How can you express that as a logical sentence?

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
# Meaning if it is a knight, it is telling the truth
# Or it is a knave and it is lying.
knowledge0 = And(
    Implication(AKnight, AKnave),

    # If A is a Knight, A cannot be a Knave and vice versa.
    Biconditional(AKnight, Not(AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
# Meaning if A is a knave, it is lying -> A is a knave, B is a knight.
knowledge1 = And(
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(AKnight, And(AKnave, BKnave)),

    # If A is a Knave, A cannot Knight etc
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # If A says they are the same kind - both cases.
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, Not(And(AKnave, BKnave))),

    # If B says they are the diff kinds - both cases.
    Implication(BKnight, And(BKnight, AKnave)),
    Implication(BKnave, Not(And(BKnave, BKnight))),

    # If A is a Knave, A cannot be a Knight etc
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
    Or(AKnight, AKnave),

    # B says "A said 'I am a knave'."
    # Let's consider nested implications..
    # If B is a knight, it would not lie so consider AKnave. Either B is telling the truth or lying.
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    # B says "C is a knave."
    Implication(BKnight, And(BKnight, CKnave)),
    Implication(BKnave, Not(And(BKnave, CKnave))),

    # C says "A is a knight."
    Implication(CKnight, And(CKnight, AKnight)),
    Implication(CKnave, Not(And(CKnave, AKnight))),

    # # If A is a Knave, A cannot Knight etc
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnave, Not(CKnight))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
