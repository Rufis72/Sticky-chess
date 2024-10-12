from Basic_functionallity import Display, Board, Bot
import pygame, sys
# creating class instances
board = Board()
display = Display(allow_moves_as_opposite_colored_player=True, screen_size=(800, 800))
bot = Bot(3)
# defining variables
clock = pygame.time.Clock()
flip_each_time = False
color_to_move = "white"
max_fps = 60
pressed = []
while True:
    clock.tick(max_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # checking if debugging keycodes is enabled, if any key is down, and if the key is d (to enable all debugging you need to hold d)
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_d]:
            import pyperclip
            # debugging keycodes
            # copying moves to clipboard
            if event.key == pygame.K_m: # for moves
                pyperclip.copy(board.player_moves)
            # copying board to clipboard
            if event.key == pygame.K_b: # b for board
                pyperclip.copy(board.board)
            # copying board colors to clipboard
            if event.key == pygame.K_c: # c for board
                pyperclip.copy(board.board_color)
    # logic for flipping the board (if enabled)
    if flip_each_time:
        if board.who_to_move() != color_to_move:
            display.flip_viewing_angle()
            color_to_move = board.who_to_move()
    display.update_screen(board, True)

