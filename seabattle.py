from random import randint


class GUI:
    def __init__(self, location):
        self.location = location


class Counter:
    def __init__(self, count):
        self.count = count


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'You are trying to shoot off the board!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'You already shot in that cage'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:

    def __init__(self, head, length, direction):
        self.head = head
        self.length = length
        self.direction = direction
        self.hitpoint = length  # -1 при попадании

    @property
    def dots(self):

        dot_list = []

        for i in range(self.length):
            dothead_x = self.head.x
            dothead_y = self.head.y
            if self.direction:
                dothead_x += i
            else:
                dothead_y += i
            dot_list.append(Dot(dothead_x, dothead_y))

        return dot_list

    def hit(self, shot):
        return shot in self.dots


class Board:
    # размещение кораблей
    # какая-то проверка на расположение
    # хранить всех КЛЕТОК (не точек ?)
    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size

        self.counter = 0  # число сбитых кораблей
        self.shiplist = []  # список кораблей
        self.busy = []  # занятые или стреляные точки
        self.field = [['O'] * size for i in range(size)]

    def __str__(self):
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            res = res.replace("O", "■")
        return res

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = '■'
            self.busy.append(dot)

        self.shiplist.append(ship)
        self.contour(ship)

    def contour(self, ship, placing=False):
        near = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for dot in ship.dots:
            for dx, dy in near:
                pt = Dot(dot.x + dx, dot.y + dy)
                if not self.out(pt) and pt not in self.busy:
                    if placing:
                        self.field[pt.x][pt.y] = '.'
                    self.busy.append(pt)

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()
        else:
            self.busy.append(dot)

        for ship in self.shiplist:
            if ship.hit(dot):
                ship.hitpoint -= 1
                self.field[dot.x][dot.y] = 'X'
                if ship.hitpoint == 0:
                    self.counter += 1
                    self.contour(ship, placing=True)
                    print('Ship destroyed!')
                    return True
                else:
                    print('Ship hit!')
                    return True

        self.field[dot.x][dot.y] = '.'
        print('Miss!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as message:
                print(message)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0, 5), randint(0, 5))
        print(f'AI turn: {dot.x + 1} {dot.y + 1}')
        return dot


class User(Player):
    def ask(self):
        while True:
            dot = input('Your turn: ').split()

            if len(dot) != 2:
                print(' Enter 2 coordinates! ')
                continue

            x, y = dot

            if not x.isdigit() or not y.isdigit():
                print(' Enter numbers! ')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    user = User
    user_board = User.own_board
    ai = AI
    ai_board = AI.own_board

    def random_board(self):
        return None

    @staticmethod
    def greet():
        print('============================')
        print('||       Sea Battle       ||')
        print('============================')

    def loop(self):
        return None

    def start(self):
        self.greet()


#   | 1 | 2 | 3 | 4 | 5 | 6 |
#
# 1 | О | О | О | О | О | О |
#
# 2 | О | О | О | О | О | О |
#
# 3 | О | О | О | О | О | О |
#
# 4 | О | О | О | О | О | О |
#
# 5 | О | О | О | О | О | О |
#
# 6 | О | О | О | О | О | О |

# 1 корабль на 3 клетки
# 2 корабля на 2 клетки
# 4 корабля на 1 клетку

begin = Game()
begin.start()
