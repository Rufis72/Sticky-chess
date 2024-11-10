from Basic_functionallity import Display, Board, Bot
import pygame, pyperclip, random
# creating class instances
board = Board(False, True)
display = Display(screen_size=(800, 300), allow_moves_as_opposite_colored_player=True, if_view_from_whites_perspective=True)
bot = Bot(3)
# defining variables
clock = pygame.time.Clock()
flip_each_time = False
color_to_move = None
play_vs_bot = False # for if playing against the bot
full_bot_game = False # for a bot vs bot game
bot_playing_vs_white = False # for the color you play if you play against the bot (True is bot = black)
max_fps = 60
running = True #the black queen is stopping king movement
while running:
    display.update_screen(board, True)
    pyperclip.copy(board.player_moves)
    clock.tick(max_fps)
    for event in pygame.event.get():
        # checking if the application is being resized
        if event.type == pygame.VIDEORESIZE:
            # resizing and rescaling everything
            display.resize_display(*display.screen.get_size())
        # checking if debugging keycodes is enabled, if any key is down, and if the key is d (to enable all debugging you need to hold d)
        elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_d]:
            # debugging keycodes
            # copying moves to clipboard
            if event.key == pygame.K_m: # for moves
                pyperclip.copy(board.player_moves)
            # copying board to clipboard
            elif event.key == pygame.K_b: # b for board
                pyperclip.copy(board.board)
            # copying board colors to clipboard
            elif event.key == pygame.K_c: # c for color
                pyperclip.copy(board.board_color)
        # checking if the application is being closed
        elif event.type == pygame.QUIT:
            # quitting and stopping all game loop code
            pygame.quit()
            running = False
    # logic for anything that happens when there is a move
    if board.who_to_move() != color_to_move:
        # updating the color to move (to detect further moves)
        color_to_move = board.who_to_move()
        # checking if the board is flipped every move
        if flip_each_time:
            # flipping the board
            display.flip_viewing_angle()
        # logic for playing against a bot
        if play_vs_bot:
            # checking if the bot is playing as white or black, and checking if it's their turn to move
            if board.who_to_move() == "black" and bot_playing_vs_white:
                # updating the screen (so the move just played will display)
                display.update_screen(board, True)
                # getting and performing the move
                board.legal_move(bot.minimax(3, board, board.who_to_move())[1][0])
            elif board.who_to_move() == "white" and not bot_playing_vs_white:
                # updating the screen (so the move just played will display)
                display.update_screen(board, True)
                # getting and performing the move
                board.legal_move(bot.minimax(3, board, board.who_to_move())[1][0])
        # checking if the bot is playing itself
        elif full_bot_game:
            # getting and performing the move
            board.legal_move(bot.minimax(3, board, board.who_to_move())[1][0])
