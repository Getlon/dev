import random


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Выстрел за доску.'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Уже стреляли в эту клетку'


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bot, l, direction):
        self.bot = bot
        self.lives = l
        self.direction = direction
        self.l = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            current_x = self.bot.x
            current_y = self.bot.y
            if self.direction == 0:
                current_x += i
            elif self.direction == 1:
                current_y += i
            ship_dots.append(Dot(current_x, current_y))
        return ship_dots


class Board:
    def __init__(self, hid=False):
        self.hid = hid
        self.count = 0
        self.field = [["O"] * 6 for i in range(6)]
        self.ships = []
        self.busy = []

    def add_ship(self, ship):

        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
        for d in ship.dots:
            for dx, dy in near:
                current = Dot(d.x + dx, d.y + dy)
                if not (self.out(current)) and current not in self.busy:
                    if verb:
                        self.field[current.x][current.y] = "."
                    self.busy.append(current)

    def __str__(self):
        result = ""
        result += "  | 1 | 2 | 3 | 4 | 5 | 6 |\n"
        for i, row in enumerate(self.field):
            result += f'{i + 1} | ' + ' | '.join(row) + ' |\n'

        if self.hid:
            result = result.replace("■", "O")
        return result

    def out(self, dot):
        return not ((0 <= dot.x < 6) and (0 <= dot.y < 6))

    def shot(self, dot):
        if dot in self.busy:
            raise BoardUsedException()

        if self.out(dot):
            raise BoardOutException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль поврежден!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise Exception()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as error:
                print(error)


class AI(Player):
    def ask(self):
        dot = Dot(random.randint(0, 5), random.randint(0, 5))
        print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
        return dot


class User(Player):
    def ask(self):
        while True:
            cords = input('Введите координаты: ').split()
            if len(cords) != 2:
                print('Нужно ввести 2 координаты.')
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print('Это должны быть числа. (1 - 6)')
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.user = User(pl, co)

    def random_place(self):
        lens_ship = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        try1 = 0
        for l in lens_ship:
            while True:
                try1 += 1
                if try1 > 1000:
                    return None
                ship = Ship(Dot(random.randint(0, 6), random.randint(0, 6)), l, random.randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def greet(self):
        print('-----------------')
        print('   морской бой   ')
        print('-----------------')
        print('формат ввода: x y')
        print('x - номер строки ')
        print('y - номер столбца')

    def loop(self):
        num = 0
        while True:
            print("-" * 27)
            print("Доска игрока:")
            print(self.user.board)
            print("-" * 27)
            print("Доска компьютера:")
            print(self.ai.board)

            if num % 2 == 0:
                print("-" * 27)
                print("Ходит игрок.")
                repeat = self.user.move()
            else:
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.user.board.count == 7:
                print("-" * 27)
                print("Компьютер выиграл!")
                input()
                break
            num += 1

            if self.ai.board.count == 7:
                print("-" * 27)
                print("Игрок выиграл!")
                input()
                break

    def start(self):
        self.greet()
        self.loop()


sea_battle = Game()
sea_battle.start()
