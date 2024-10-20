from Basic_functionallity import Display, Board, Bot
import pygame, sys, pyperclip
# creating class instances
board = Board(True)
display = Display(screen_size=(800, 800), allow_moves_as_opposite_colored_player=True)
bot = Bot(3)
# defining variables
clock = pygame.time.Clock()
flip_each_time = False
color_to_move = "white"
play_vs_bot = True # for if playing against the bot
full_bot_game = False # for a bot vs bot game
bot_playing_vs_white = False # for the color you play if you play against the bot (True is bot = black)
max_fps = 60
running = True
# board.legal_moves(['g1f3', 'g8f6', 'b1a3', 'b8c6', 'f3h4', 'c6b4', 'c2c3', 'b4d5', 'c3c4', 'd5c3', 'd2c3', 'e7e5', 'a3b5', 'c7c6', 'b5d6', 'f8d6', 'd1d6', 'd8e7', 'd6c7', 'e7c5', 'b2b3', 'h7h6', 'c1b2', 'g7g6', 'h4f3', 'd7d6', 'h2h3', 'f6e4', 'e2e3', 'e4g5', 'b3b4', 'g5f3', 'g2f3', 'c5b6', 'c4c5', 'b6c7', 'c3c4', 'c8d7', 'e3e4', 'd7e6', 'f1e2', 'a8b8', 'b2c3', 'd6d5', 'e4d5', 'c6d5', 'c4d5', 'e6d5', 'e2c4', 'd5e6', 'c4d3', 'b7b6', 'f3f4', 'c7c6', 'f2f3', 'a7a6', 'b4b5', 'b6c5', 'b5c6', 'f7f6', 'h3h4', 'g6g5', 'h4g5', 'f6g5', 'c6c7', 'h8g8'])
while running:
    display.update_screen(board, True)
    pyperclip.copy(board.player_moves)
    clock.tick(max_fps)
    for event in pygame.event.get():
        # checking if debugging keycodes is enabled, if any key is down, and if the key is d (to enable all debugging you need to hold d)
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_d]:
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
        # checking if the application is being closed
        if event.type == pygame.QUIT:
            # quitting and stopping all game loop code
            pygame.quit()
            running = False
    # logic for flipping the board (if enabled)
    color_to_move = 0
    if board.who_to_move() != color_to_move:
        color_to_move = board.who_to_move()
        if flip_each_time:
            display.flip_viewing_angle()
        if play_vs_bot:
            if board.who_to_move() == "black" and bot_playing_vs_white:
                board.legal_move(bot.minimax(3, board, board.who_to_move())[1][0])
            elif board.who_to_move() == "white" and not bot_playing_vs_white:
                board.legal_move(bot.minimax(3, board, board.who_to_move())[1][0])
        elif full_bot_game:
            board.legal_move(bot.minimax(3, board, board.who_to_move())[1][0])
