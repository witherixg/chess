import os


class Player:
    def __init__(self, symbol):
        self.symbol = symbol


class Box:
    def __init__(self, x, y):
        self.player = None
        self.x = x
        self.y = y

    def __str__(self):
        if not self.player:
            return ' '
        else:
            return self.player.symbol


class SubBoard:
    def __init__(self, x, y):
        self.boxes = []
        self.x = x
        self.y = y
        self.state = None
        for i in range(0, 3):
            self.boxes.append([Box(i, j) for j in range(0, 3)])

    def print_self(self):
        print("*-0--1--2-X")
        for x in range(0 + 3 * self.x, 3 + 3 * self.x):
            print(x - 3 * self.x, end="")
            for y in range(0 + 3 * self.y, 3 + 3 * self.y):
                print(' ' + get_box_by_pos(x, y).__str__() + ' ', end="")
            print('|')
        print('Y' + '-' * 10)

    def check_win(self):
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
        for combo in win_combinations:
            x1, x2, x3 = map(lambda x: x % 3, combo)
            y1, y2, y3 = map(lambda x: x // 3, combo)
            b1, b2, b3 = self.boxes[x1][y1], self.boxes[x2][y2], self.boxes[x3][y3]
            if b1.__str__() == b2.__str__() == b3.__str__() == p1.symbol:
                self.state = p1
                break
            if b1.__str__() == b2.__str__() == b3.__str__() == p2.symbol:
                self.state = p2
                break
        list_ = []
        flag = False
        for i in range(0, 3):
            list_.extend(self.boxes[i])

        for i in list_:
            if i.__str__() == ' ':
                flag = True
                break
        print(flag)
        if not flag:
            self.state = ghost_player
        if self.state:
            print(self.state.symbol)


class Board:
    def __init__(self):
        self.s_boxes = []
        self.state = None
        for i in range(0, 3):
            self.s_boxes.append([SubBoard(i, j) for j in range(0, 3)])
        self.chosen_x = -1
        self.chosen_y = -1

    @staticmethod
    def print_self():
        print("* 0  1  2   3  4  5   6  7  8  X")
        for x in range(0, 9):
            print(x, end="")
            for y in range(0, 9):
                print(' ' + get_box_by_pos(x, y).__str__() + ' ', end="")
                if y == 2 or y == 5:
                    if (y + 1) // 3 == g_board.chosen_x and x // 3 == g_board.chosen_y:
                        print('>', end="")
                    elif (y - 1) // 3 == g_board.chosen_x and x // 3 == g_board.chosen_y:
                        print('<', end="")
                    else:
                        print('|', end="")
            print()
            if x == 2 or x == 5:
                print(' ' + '-' * 29)

        print('Y')


def pos_parse(s: str):
    list_ = []
    temp = s.replace('(', "").replace(')', "")
    if len(temp.split(',')) == 2:
        list_ = temp.replace(' ', "").split(',')
    if len(temp.split(' ')) == 2:
        list_ = temp.split(' ')
    if not (len(list_) == 2):
        return
    for i in list_:
        if not i.isdigit():
            return
    y, x = map(int, list_)
    return x, y


def command_parse(s: str):
    for player_index in (1, 2):
        if s.replace(' ', "").startswith(f"#p{player_index}"):
            list_ = s.replace('#', "").replace(f"p{player_index}", "").split(' ')
            if len(list_) < 0:
                continue

            for i in list_:
                if pos_parse(i) is not None:
                    x, y = pos_parse(i)
                else:
                    continue
                if player_index == 1:
                    next_all_allowed(p1, x, y)
                    os.system("cls")
                    print("Changed sucessfully!")
                    g_board.print_self()

                elif player_index == 2:
                    next_all_allowed(p2, x, y)
                    os.system("cls")
                    print("Changed sucessfully!")
                    g_board.print_self()


def input_pos(range_):
    s = ""
    x = 0
    y = 0
    while not s:
        s = input(">>> ")
        command_parse(s)
        if pos_parse(s) is not None:
            x, y = pos_parse(s)
        else:
            s = ""
        if not (0 <= x <= range_ and 0 <= y <= range_):
            s = ""
    return x, y


g_board = Board()
p1 = Player('x')
p2 = Player('o')
ghost_player = Player('?')


def next_all_allowed(player, x, y):
    return next_movement(player, x // 3, y // 3, x % 3, y % 3)


def next_movement(player, x, y, in_x, in_y):
    if g_board.s_boxes[x][y].state:
        return ' '
    if g_board.s_boxes[x][y].boxes[in_x][in_y].player:
        return ' '
    g_board.s_boxes[x][y].boxes[in_x][in_y].player = player
    g_board.s_boxes[x][y].check_win()


def get_box_by_pos(x, y) -> Box:
    s_x = x // 3
    in_x = x % 3
    s_y = y // 3
    in_y = y % 3
    s_b = g_board.s_boxes[s_x][s_y]
    return s_b.boxes[in_x][in_y]


def check_same(list_: list):
    return len(set(list_)) == 1


def main():
    won_player = None
    global g_board
    current_player = p1
    print("Input positions as:\n(1)x,y\n(2)(x,y)\n(3)x y")

    while True:  # Steps
        ept_num = 0
        p1_num = 0
        p2_num = 0
        g_board.print_self()
        res = ' '
        while res == ' ':
            if (not (0 <= g_board.chosen_x <= 8 and 0 <= g_board.chosen_y <= 8)):
                print("Free Step...")
                x, y = input_pos(8)
                res = next_all_allowed(current_player, x, y)
                if res == ' ':
                    continue
                g_board.chosen_x = x % 3
                g_board.chosen_y = y % 3
            else:
                print("Limited Step...")
                g_board.s_boxes[g_board.chosen_x][g_board.chosen_y].print_self()
                ix, iy = input_pos(2)
                res = next_movement(current_player, g_board.chosen_x, g_board.chosen_y, ix, iy)
                g_board.chosen_x, g_board.chosen_y = ix, iy
            if not g_board.s_boxes[g_board.chosen_x][g_board.chosen_y]:
                g_board.chosen_x = g_board.chosen_y = -1
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1
        os.system("cls")
        list_ = []
        for i in range(0, 3):
            list_.extend(g_board.s_boxes[i])
        for sb in list_:
            if sb.state == p1:
                p1_num += 1
            if sb.state == p2:
                p2_num += 1
            if sb.state is None:
                ept_num += 1
        if p1_num == 5:
            print(f"Player 1({p1.symbol}) won!")
            return
        if p2_num == 5:
            print(f"Player 2({p2.symbol}) won!")
            return
        if ept_num == 0:
            print("Draw...")
            return


if __name__ == "__main__":
    main()
