from Basic_functionallity import Display, Board
import pygame, sys
board = Board()
display = Display()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    display.update_screen(board)
