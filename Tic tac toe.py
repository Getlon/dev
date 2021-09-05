def draw_playing_field(list1):
    print(f'''
  0 1 2
0 {list1[0][0]} {list1[0][1]} {list1[0][2]}
1 {list1[1][0]} {list1[1][1]} {list1[1][2]}
2 {list1[2][0]} {list1[2][1]} {list1[2][2]}''')


def check_win(list1):
    return list1[0][0] == list1[1][1] == list1[2][2] == '0' or\
           list1[2][0] == list1[1][1] == list1[0][2] == '0' or\
           list1[0][0] == list1[0][1] == list1[0][2] == '0' or\
           list1[0][0] == list1[1][0] == list1[2][0] == '0' or\
           list1[0][2] == list1[1][2] == list1[2][2] == '0' or\
           list1[2][0] == list1[2][1] == list1[2][2] == '0' or\
           list1[0][0] == list1[1][1] == list1[2][2] == 'x' or\
           list1[2][0] == list1[1][1] == list1[0][2] == 'x' or\
           list1[0][0] == list1[0][1] == list1[0][2] == 'x' or\
           list1[0][0] == list1[1][0] == list1[2][0] == 'x' or\
           list1[0][2] == list1[1][2] == list1[2][2] == 'x' or\
           list1[2][0] == list1[2][1] == list1[2][2] == 'x'


count = 0
playing_field = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
draw_playing_field(playing_field)
while True:
    while True:
        x1, x2 = map(int, list(input('Ход первого игрока (крестик) -> ').split(' ')))
        if playing_field[x1][x2] == 'x' or playing_field[x1][x2] == '0':
            print('Эта клетка занята.')
            continue
        playing_field[x1][x2] = 'x'
        break
    draw_playing_field(playing_field)
    if check_win(playing_field):
        print('Выйграл первый игрок (крестик).')
        break
    count += 1

    if count == 9:
        print('Ничья')
        break

    while True:
        x1, x2 = map(int, list(input('Ход второго игрока (нолик) -> ').split(' ')))
        if playing_field[x1][x2] == 'x' or playing_field[x1][x2] == '0':
            print('Эта клетка занята.')
            continue
        playing_field[x1][x2] = '0'
        break
    draw_playing_field(playing_field)

    if check_win(playing_field):
        print('Выйграл второй игрок (нолик).')
        break
    count += 1

    if count == 9:
        print('Ничья.')
        break
input()
