# ■ МОРСКОЙ БОЙ ■
import random


class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, d, l, o):
        self.d = d
        self.l = l
        self.o = o
        self.lives = l

    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cx = self.d.x
            cy = self.d.y

            if self.o == 0:
                cx += i
            elif self.o == 1:
                cy += i

            ship_dots.append(Dot(cx, cy))

        return ship_dots


    def shooten(self, shot):
        return shot in self.dots


class Board:
    def out(self, dot, state=False):
        return not ((0 <= dot.x < 6) and (0 <= dot.y < 6))

    def begin(self):
        self.busy=[]
        self.shots=[]

    def __init__(self, size, state=False):
        self.state = state
        self.size = size
        self.score = 0
        self.field = [['0'] * size for i in range(size)]
        self.busy = []
        self.ships = []
        self.shots = []

    def __str__(self):
        f = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i in range((len(self.field))):
            f += f'\n{i + 1} | ' + ' | '.join(self.field[i]) + ' | '

        if self.state:
            f = f.replace('■', '0')

        return f

    def add_ship(self, ship):

        for dot in ship.dots():
            if self.out(dot) or (dot in self.busy):
                raise BoardWrongShipException()
        for dot in ship.dots():
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, state=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots():
            for cx, cy in near:
                cur_dot = Dot(dot.x + cx, dot.y + cy)
                if (not self.out(cur_dot)) and (cur_dot not in self.busy):
                    if state:
                        self.field[cur_dot.x][cur_dot.y] = "X"
                    self.busy.append(cur_dot)

    def shooting(self, dot):

        if self.out(dot):
            print('Стреляйте в доску!')
            raise BoardException()
        if dot in self.shots:
            print('Вы сюда уже стреяли!')
            raise BoardException()

        self.shots.append(dot)

        for ship in self.ships:
            if dot in ship.dots():
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"

                if ship.lives == 0:
                    self.contour(ship, state=True)
                    self.score += 1
                    print('Корабль уничтожен!')
                    return False

                else:
                    print('Корабль ранен!')
                    return True

        self.field[dot.x][dot.y] = 'T'
        print('Мимо!')
        return False


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                return self.enemy.shooting(self.ask())
            except BoardException as e:
                print(e)


class Computer(Player):
    def ask(self):
        dot = Dot(random.randint(0, 5), random.randint(0, 5))
        print(f"Ход компьютера: {dot.x+1} {dot.y+1}")
        return dot


class User(Player):
    def ask(self):
        while True:
            dots = input("Ваш ход: ").split()

            if len(dots) != 2:
                print("Введите 2 координаты!")
                continue

            x, y = dots

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:
    def __init__(self):
        field1 = self.random_board()
        field2 = self.random_board()
        #field2.state = True

        self.me = User(field1, field2)
        self.comp = Computer(field2, field1)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        attempts = 0
        cnt = 0
        board = Board(size=6)
        for i in lens:
            while cnt < 7:
                attempts += 1
                if attempts > 10000:
                    return None
                ship = Ship(Dot(random.randint(0, 5), random.randint(0, 5)), i, random.randint(0, 1))
                try:
                    board.add_ship(ship)
                    cnt += 1
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def play(self):
        print("Приветсвую вас в игре морской бой \n формат ввода: x y \n x - номер строки \n y - номер столбца")
        i = 0
        while True:
            print("Ваша доска:")
            print(self.me.board)
            print("Доска компьютера:")
            print(self.comp.board)
            if i % 2 == 0:
                print("Вы ходите!")
                f = self.me.move()
            else:
                print("Ходит компьютер!")
                f = self.comp.move()
            if f:
                i -= 1

            if self.comp.board.score == 7:
                print("Вы выиграли!")
                break

            if self.me.board.score == 7:
                print("Компьютер выиграл!")
                break
            i += 1


Game().play()
