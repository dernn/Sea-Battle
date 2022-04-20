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
        return "Вы пытаетесь выстрелить за доску"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


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

        self.shipcount = 0  # число сбитых кораблей
        self.shiplist = []  # список кораблей
        self.busy = []  # занятые или стреляные точки
        self.field = [['O'] * size for i in range(size)]

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            res = res.replace("O", "■")
        return res

    def add_ship(self, unit):
        if unit in self.field:
            return True
        else:
            return None  # Exception

    def contour(self):
        pass

    def out(self, dot):
        return not (0 <= dot.x < self.size) and (0 <= dot.y < self.size)

    def shot(self, mark):
        if mark in self.field:
            return True
        else:
            return None  # Exception: за пределы + повторно


class Player:
    own_board = Board
    enemy_board = Board

    def ask(self):
        return None

    def move(self):
        return Player.ask() in Board.shot(None)


class AI(Player):
    def ask(self):
        return None


class User(Player):
    def ask(self):
        return None


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
