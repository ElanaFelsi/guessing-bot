def guess():
    highest = 101
    lowest = 1
    while True:
        guess = int((highest+lowest)/2)
        print(f"Is your number {guess}?")
        if input() == 'y':
            break
        print("Is my guess higher than the secret number?")
        if input() == 'y':
            highest = guess
        else:
            lowest = guess

    print("YOU WIN!!!")
#import random
#
#num = input("whats ur number?")
#guess = random.randint(1, 101)
#print(f"Is your number {guess}?")
#res = input("y/n")
#highest = 101
#lowest = 1
#while res == 'n':
#    print("Is my guess higher than the secret number?")
#    higher = input("y/n")
#    if higher == 'y':
#        highest = guess
#        guess = random.randint(lowest, highest)
#    else:
#        lowest = guess
#        guess = random.randint(lowest, highest)
#
#    print(f"Is your number {guess}?")
#    res = input("y/n")

