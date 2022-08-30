from components import Board


def main():
    print('Input the size of the board N:')
    n = int(input())
    print('Input the number of black holes K:')
    k = int(input())
    print('Input 1 for debug mode or 0 for normal mode:')
    debug = int(input()) == 1

    print('Initializing the board...\n')
    board = Board(n, k, debug)
    print(board)

    revealed_cells = 0
    cells_total = n**2

    while True:
        print('Input the coordinates of the cell separated by a space or type -1 to quit:')
        try:
            coords = list(map(int, input().split()))
            if len(coords) == 1:
                if coords[-1] == -1:
                    print('Exiting...')
                    break
                raise ValueError

            x, y = coords
            state = board.reveal(x, y)

            if state == 0:
                print('\nCell already revealed!\n')
                continue
            elif state == -1:
                print('\nYou hit a black hole! Game over!\n')
                board.debug_mode()
                print(board)
                break
            elif state == -2:
                continue
            else:
                revealed_cells += state

            print(board)

            if cells_total - revealed_cells == k:
                board.debug_mode()
                print(board)
                print('\nYou won!\n')
                break

        except ValueError:
            print('\nInvalid input!\n')


if __name__ == '__main__':
    main()
