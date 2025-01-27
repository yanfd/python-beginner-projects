import random

dice_drawing = {
    1: (
        " __________",
        "|          |",
        "|    1     |",
        "|     ●    |",
        "|          |",
        "|__________|",
    ),
    2: (
        " __________",
        "|          |",
        "|       ●  |",
        "|    2     |",
        "|  ●       |",
        "|__________|",
    ),
    3: (
        " __________",
        "|          |",
        "|   3  ●   |",
        "|    ●     |",
        "|  ●       |",
        "|__________|",
    ),
    4: (
        " __________",
        "|          |",
        "|  ●    ●  |",
        "|    4     |",
        "|  ●    ●  |",
        "|__________|",
    ),
    5: (
        " __________",
        "|          |",
        "|  ● 5  ●  |",
        "|    ●     |",
        "|  ●    ●  |",
        "|__________|",
    ),
    6: (
        " __________",
        "|          |",
        "|  ●    ●  |",
        "|  ●  6 ●  |",
        "|  ●    ●  |",
        "|__________|",
    ),
}
def roll_dice():
    num = input("roll the dice?(y/n)")
    while num.lower() == 'y':
        rand1 = random.randint(1,6)
        rand2 = random.randint(1,6)
        print(f'You rolled {rand1} and {rand2}')
        print("\n".join(dice_drawing[rand1]))
        print("\n".join(dice_drawing[rand2]))

        num = input("\nRoll again? (y/n): ")


roll_dice()