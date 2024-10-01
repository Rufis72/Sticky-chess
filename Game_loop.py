from Basic_functionallity import Display, Board
import pygame, sys
board = Board()
board.legal_moves(["e2e4", "e7e5", "f1c4", "f8c5", "g1f3", "g8f6"])
display = Display(allow_moves_as_opposite_colored_player=True)
clock = pygame.time.Clock()
flip_each_time = True
color_to_move = "white"
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if flip_each_time:
        if board.who_to_move() != color_to_move:
            display.flip_viewing_angle()
            color_to_move = board.who_to_move()
    display.update_screen(board, True)
