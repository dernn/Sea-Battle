from random import randint


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
        self.hitpoint = length

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

    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size

        self.counter = 0  # число сбитых кораблей
        self.shiplist = []  # список кораблей
        self.busy = []  # занятые или стреляные точки
        self.field = [['O'] * size for i in range(size)]

    def __str__(self):
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            res = res.replace("■", "0")
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

    def defeat(self):
        return self.counter == len(self.shiplist)

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

    def __init__(self, size=9):  # board scaling
        self.size = size
        self.units = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # масштабирование

        player = self.random_board()
        computer = self.random_board()
        computer.hide = True

        self.ai = AI(computer, player)
        self.user = User(player, computer)

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        for lgth in self.units:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), lgth, randint(0, 1))
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
            board = self.try_board()
        return board

    @staticmethod
    def greet():
        print('============================')
        print('||       Sea Battle       ||')
        print('============================')
        print('|| input format: x y      ||')
        print('|| x  -  string #         ||')
        print('|| y  -  column #         ||')
        print('============================')
        print()
        input('Press Enter to begin...')

    def show_boards(self):
        print('-' * 30)
        print("User's board:")
        print(self.user.board)
        print('-' * 30)
        print('AI board:')
        print(self.ai.board)
        print('-' * 30)

    def loop(self):
        num = 0
        while True:
            self.show_boards()
            if num % 2 == 0:
                print("User's turn!")
                repeat = self.user.move()
            else:
                print("AI turn!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.show_boards()
                print('-' * 30)
                print("User wins!")
                break

            if self.user.board.defeat():
                self.show_boards()
                print('-' * 30)
                print("AI wins!")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
