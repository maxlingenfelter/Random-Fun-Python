import random

print('Let the game begin.')
play = 'true'
cs = 0
ps = 0
ag = 'GO'

while play == 'true':
    rpc = input('rock, paper, scissors? >')
    posiblle = ['rock', 'paper', 'scissors']
    if rpc in posiblle:
        posiblle_results = ['rock', 'paper', 'scissors']
        result = random.choice(posiblle_results)
        print("I chose > " + str(result))

        if rpc == result:
            print('  ')
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('Tie. Press Enter To Play Again! Or Type EXIT >')

        elif rpc == 'rock' and result == 'paper':
            print('  ')
            cs = cs + 1
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('You Lose! Press Enter To Play Again! Or Type EXIT >')

        elif rpc == 'rock' and result == 'scissors':
            print('  ')
            ps = ps + 1
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('You Win! Press Enter To Play Again! Or Type EXIT >')

        # 1

        elif rpc == 'paper' and result == 'rock':
            print('  ')
            ps = ps + 1
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('You Win! Press Enter To Play Again! Or Type EXIT >')

        elif rpc == 'paper' and result == 'scissors':
            print('  ')
            cs = cs + 1
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('You Lose! Press Enter To Play Again! Or Type EXIT >')

        # 2

        elif rpc == 'scissors' and result == 'rock':
            print('  ')
            cs = cs + 1
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('You Lose! Press Enter To Play Again! Or Type EXIT >')

        elif rpc == 'scissors' and result == 'paper':
            print('  ')
            ps = ps + 1
            print('Score: ' + str(ps) + '-' + str(cs))
            ag = input('You Win! Press Enter To Play Again! Or Type EXIT >')

        # 3

        # EXIT
        if ag == 'EXIT':
            play = 'false'
            break

    else:
        print('Not a valid choice')
        print('Try Again!')
        print(' ')
