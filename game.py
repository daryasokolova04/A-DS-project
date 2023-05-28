import sys
import pygame
now_row, now_col = 0, 0

protect = {'0xxxx0': 70000, '0xxxx': 60000, 'xxxx0': 60000,
         '0x0xxx': 2000, 'xx0xx0': 2000, '0xx0xx': 2000, '0xxx0x': 2000, 'x0xxx0': 2000, 'xxx0x0': 2000,
         '0xxx0': 3000, '0xxx': 1500, 'xxx0': 1500, '0xxxo0': 1500,
         '0xx0x': 800, 'xx0x0': 800, 'x0xx0': 800, '0x0xx': 800, '0xx0': 200, '0x0': 100, 'x0': 10, '0x': 10, 'x': 1}

attack = {'0oooo0': 7700, '0oooo': 6600, 'oooo0': 6600,
         '0o0ooo': 2200, 'oo0oo0': 2200, '0oo0oo': 2200, '0ooo0o': 2200, 'o0ooo0': 2200, 'ooo0o0': 2200,
         '0ooo0': 3300, '0ooo': 1650, 'ooo0': 1650, '0ooox0': 1650,
         '0oo0o': 880, 'oo0o0': 880, 'o0oo0': 880, '0o0oo': 880, '0oo0': 220, '0o0': 110, 'o0': 11, '0o': 11, 'o': 2}


def check_win(mass, sign): #sign = крестик/нолик
    zeroes = 0
    for rows in mass:
        zeroes += rows.count(0)
    for rows in range(0, 20-4):
        for cols in range(20):
            if mass[rows][cols] == mass[rows+1][cols] == mass[rows+2][cols] == mass[rows+3][cols] \
                    == mass[rows+4][cols] == sign:
                return sign
    for rows in range(20):
        for cols in range(0, 20-4):
            if mass[rows][cols] == mass[rows][cols+1] == mass[rows][cols+2] == mass[rows][cols+3]\
                    == mass[rows][cols+4] == sign:
                return sign
    for rows in range(0, 20-4):
        for cols in range(0, 20-4):
            if mass[rows][cols] == mass[rows+1][cols+1] == mass[rows+2][cols+2] \
                    == mass[rows+3][cols+3] == mass[rows+4][cols+4] == sign:
                return sign
    for rows in range(0, 20-4):
        for cols in range(0, 20-4):
            if mass[rows][cols+4] == mass[rows+1][cols+3] == mass[rows+2][cols+2] ==\
                    mass[rows+3][cols+1] == mass[rows+4][cols] == sign:
                return sign
    if zeroes == 0:
        return "ничья"
    return False


def next_turn(mass, cost, pr_row, pr_col):
    global protect, attack
    cost[pr_row][pr_col] = -1
    for rows in range(max(0, pr_row - 2), min(20, pr_row + 3)):
        for cols in range(max(0, pr_col - 2), min(20, pr_col + 3)):
            if cost[rows][cols] != -1:
                lines = []
                for i in range(max(0, rows-5), min(15, rows+1)): #столбцы |
                    lines.append(str(mass[i][cols]) + str(mass[i+1][cols]) + str(mass[i+2][cols])
                                 + str(mass[i+3][cols]) + str(mass[i+4][cols]) + str(mass[i+5][cols]))

                for j in range(max(0, cols-5), min(15, cols+1)): #строки -
                    lines.append(str(mass[rows][j]) + str(mass[rows][j+1]) + str(mass[rows][j+2])
                                 + str(mass[rows][j+3]) + str(mass[rows][j+4]) + str(mass[rows][j+5]))

                up = min((min(rows, cols)), 5) #на сколько можно подняться по диагнонали
                down = min(19 - max(rows, cols), 5) #на сколько можно спуститься по диагонали
                for i in range(-up, down-5+1): #гл диагональ \
                    lines.append(str(mass[rows+i][cols+i]) + str(mass[rows+i+1][cols+i+1])
                                 + str(mass[rows+i+2][cols+i+2]) + str(mass[rows+i+3][cols+i+3])
                                 + str(mass[rows+i+4][cols+i+4]) + str(mass[rows+i+5][cols+i+5]))

                up = min(min(rows, 19 - cols), 5) #на сколько можно подняться по диагнонали
                down = min(min(cols, 19 - rows), 5) #на сколько можно спуститься по диагонали
                for i in range(-up, down-5+1): #побочная диагональ /
                    lines.append(str(mass[rows+i][cols-i]) + str(mass[rows+i+1][cols-i-1])
                                 + str(mass[rows+i+2][cols-i-2]) + str(mass[rows+i+3][cols-i-3])
                                 + str(mass[rows+i+4][cols-i-4]) + str(mass[rows+i+5][cols-i-5]))
                for line in lines:
                    for key in protect.keys():
                        if key in line:
                            cost[rows][cols] += protect[key]
                    for key in attack.keys():
                        if key in line:
                            cost[rows][cols] += attack[key]
    current = 0
    max_x, max_y = 0, 0
    for i in range(len(cost)):
        if current < max(cost[i]):
            current = max(cost[i])
            max_x = i
            max_y = cost[i].index(current)
    return max_x, max_y


pygame.init()
size_block = 22
margin = 1
width = height = size_block*20 + margin*21
screen = pygame.display.set_mode((width, height))#создание окна
pygame.display.set_caption("Пять в ряд")

red = (255, 102, 102)
green = (152, 230, 152)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
mass = [[0]*20 for i in range(20)]
cost = [[0]*20 for j in range(20)]
game_over = False
screen.fill(grey)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            mass = [[0]*20 for i in range(20)]
            cost = [[0]*20 for j in range(20)]
            screen.fill(grey)

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            now_col = x_mouse // (size_block + margin)
            now_row = y_mouse // (size_block + margin)
            if mass[now_row][now_col] == 0:
                mass[now_row][now_col] = 'x'
                new_row, new_col = next_turn(mass, cost, now_row, now_col)
                cost[new_row][new_col] = -1
                mass[new_row][new_col] = 'o'

    if not game_over:
        for row in range(20):
            for col in range(20):
                if mass[row][col] == 'x':
                    color = red
                elif mass[row][col] == 'o':
                    color = green
                else:
                    color = white
                x = col * size_block + (col + 1) * margin
                y = row * size_block + (row + 1) * margin
                pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                if color == red:
                    pygame.draw.line(screen, white, (x+5, y+5), (x+size_block-5, y+size_block-5), 2)
                    pygame.draw.line(screen, white, (x+size_block-5, y+5), (x+5, y + size_block-5), 2)
                elif color == green:
                    pygame.draw.circle(screen, white, (x+size_block//2, y+size_block//2), size_block//2-3, 2)

    game_over_x = check_win(mass, 'x')
    game_over_o = check_win(mass, 'o')

    if game_over_x is not False or game_over_o is not False:
        if game_over_o == 'o' and game_over_x is False:
            screen.fill(green)
            game_over = 'o'
        elif game_over_x == 'x' and game_over_o is False:
            screen.fill(red)
            game_over = 'x'
        else:
            screen.fill(white)
            game_over = 'ничья'
        font = pygame.font.SysFont("verdana", 32)
        text = font.render(game_over, True, white)
        text_rect = text.get_rect()
        text_x = screen.get_width() // 2 - text_rect.width // 2 - 5
        text_y = screen.get_height() // 2 - text_rect.height // 2 - 5
        screen.blit(text, (text_x, text_y))

    pygame.display.update()



