from Basic_functionallity import Display, Board
import pygame, sys
board = Board()
display = Display()
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    display.update_screen(board)
