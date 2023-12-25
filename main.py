import numpy as np
import math
import pygame
import random
import sys
rows = 6
cols = 7

PLAYER = 0
AI = 1

EMPTY = 0
player_val = 1
ai_val = 2

PINK = (255,192,203)
PURPLE = (128, 0, 128)
L_GREEN = (144, 238, 144)
L_BLUE = (173,216,230)
L_PINK = (255, 182, 193)
L_YELLOW =(255,255,204)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
block = 4

def initialize_board():
    board = np.zeros((rows, cols), dtype=int)
    return board

def is_terminal(board):
	if(av_cols(board) == []):
		return True
	return False

def evaluate_window(window, piece):
	score = 0
	opp_piece = player_val
	if piece == player_val:
		opp_piece = ai_val

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 80

	return score


def heuristic(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, cols//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(rows):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(cols-3):
			window = row_array[c:c+block]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(cols):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(rows-3):
			window = col_array[r:r+block]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(rows-3):
		for c in range(cols-3):
			window = [board[r+i][c+i] for i in range(block)]
			score += evaluate_window(window, piece)

	for r in range(rows-3):
		for c in range(cols-3):
			window = [board[r+3-i][c+i] for i in range(block)]
			score += evaluate_window(window, piece)

	return score

def check_winner(board):
	p_count = 0
	ai_count = 0
	moves =[[1,0],[0,1],[1,1],[1,-1]] #[col,row] 1. checks horizontal 2. vertical  3. diagonal +ve  4. diagonal -ve
	for m in moves:
		col_move = m[0]
		row_move = m[1]
		for c in range(cols):
			for r in range(rows):
				max_c = c + 3*col_move
				max_r = r + 3*row_move
				if (0 <= max_c and max_c < cols and 0 <= max_r and max_r < rows):
					if(board[r][c] != 0):
						winner = board[r][c]
						if((board[r+row_move][c+col_move] == winner) and (board[r+2*row_move][c+2*col_move] == winner) and (board[r+3*row_move][c+3*col_move] == winner)):
							if winner == player_val:
								p_count+=1
							else:
								ai_count +=1
	print( ai_count)
	print(p_count)
	if (p_count> ai_count):
		return player_val
	elif(p_count<ai_count):
		return ai_val
	return 0

def av_cols(board):
	columns = []
	for col in range(cols):
		if(board[rows-1][col] == 0):
			columns.append(col)
	return columns

def av_row(board, c):
	for r in range(rows):
		if board[r][c] == 0:
			return r
def minimax_without_alpha_beta(board, depth, min_max, prefix="", visited_states=None):
    if visited_states is None:
        visited_states = {}

    board_hash = hash(tuple(map(tuple, board)))  # Generate a unique hash for the board state

    if depth == 0:
        return (None, heuristic(board, ai_val))
    if is_terminal(board):
        return (None, heuristic(board, ai_val))

    if board_hash in visited_states:  # Check if the board state has already been visited
        return visited_states[board_hash]

    if min_max:
        best_score = -math.inf
        best_column = None

        for col in av_cols(board):
            r = av_row(board, col)
            child = board.copy()
            child[r][col] = ai_val
            _, score = minimax_without_alpha_beta(child, depth - 1, False, prefix + "    |", visited_states)
            if score > best_score:
                best_score = score
                best_column = col
            print(f"{prefix}├── (Depth: {depth}, Col: {col}, Score: {score})")

        visited_states[board_hash] = best_column, best_score  # Store the best move and score for the current state
        return best_column, best_score

    else:
        best_score = math.inf
        best_column = None

        for col in av_cols(board):
            row = av_row(board, col)
            child = board.copy()
            child[row][col] = player_val
            _, score = minimax_without_alpha_beta(child, depth - 1, True, prefix + "    |", visited_states)
            if score < best_score:
                best_score = score
                best_column = col
            print(f"{prefix}├── (Depth: {depth}, Col: {col}, Score: {score})")

 

        visited_states[board_hash] = best_column, best_score  # Store the best move and score for the current state
        return best_column, best_score


def minimax_alpha_beta(board, depth, alpha, beta, min_max, prefix="", visited_states=None):
    if visited_states is None:
        visited_states = {}

    available_cols = av_cols(board)
    board_hash = hash(tuple(map(tuple, board)))  # Generate a unique hash for the board state

    if depth == 0:
        return (None, heuristic(board, ai_val))
    if is_terminal(board):
        return (None, heuristic(board, ai_val))

    if board_hash in visited_states:  # Check if the board state has already been visited
        return visited_states[board_hash]

    if min_max:  # max
        best_move = None
        best_score = -math.inf

        for col in available_cols:
            r = av_row(board, col)
            child = board.copy()
            child[r][col] = ai_val
            _, score = minimax_alpha_beta(child, depth - 1, alpha, beta, False, prefix + "    |", visited_states)
            if score > best_score:
                best_score = score
                best_move = col

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
            print(f"{prefix}├── (Depth: {depth}, Col: {col}, Score: {score})")

        visited_states[board_hash] = best_move, best_score  # Store the best move and score for the current state
        return best_move, best_score

    else:
        best_score = math.inf
        best_move = None

        for col in available_cols:
            r = av_row(board, col)
            child = board.copy()
            child[r][col] = player_val
            _, score = minimax_alpha_beta(child, depth - 1, alpha, beta, True, prefix + "    |", visited_states)
            if score < best_score:
                best_score = score

 

                best_move = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break
            print(f"{prefix}├── (Depth: {depth}, Col: {col}, Score: {score})")

        visited_states[board_hash] = best_move, best_score  # Store the best move and score for the current state
        return best_move, best_score


def expected_minimax(board, depth, min_max, prefix="", visited_states=None):
    if visited_states is None:
        visited_states = {}

    board_hash = hash(tuple(map(tuple, board)))  # Generate a unique hash for the board state

    if depth == 0:
        return (None, heuristic(board, ai_val))
    if is_terminal(board):
        return (None, heuristic(board, ai_val))

    if board_hash in visited_states:  # Check if the board state has already been visited
        return visited_states[board_hash]

    if min_max:
        best_score = -math.inf
        best_column = None

        for col in av_cols(board):
            row = av_row(board, col)
            child = board.copy()
            child[row][col] = ai_val
            prob_score = 0.6 * heuristic(child, ai_val)
            if col > 0:
                b_copy_left = board.copy()
                b_copy_left[row][col - 1] = ai_val
                prob_score += 0.4 * heuristic(b_copy_left, ai_val)
            if col < cols - 1:
                b_copy_right = board.copy()
                b_copy_right[row][col + 1] = ai_val
                prob_score += 0.4 * heuristic(b_copy_right, ai_val)

            _, score = expected_minimax(child, depth - 1, False, prefix + "    |", visited_states)
            score += prob_score
            if score > best_score:
                best_score = score
                best_column = col
            print(f"{prefix}├── (Depth: {depth}, Col: {col}, Score: {score})")

 

        visited_states[board_hash] = best_column, best_score  # Store the best move and score for the current state
        return best_column, best_score

    else:
        best_score = math.inf
        best_column = None

        for col in av_cols(board):
            row = av_row(board, col)
            child = board.copy()
            child[row][col] = player_val
            prob_score = 0.6 * heuristic(child, player_val)
            if col > 0:
                b_copy_left = board.copy()
                b_copy_left[row][col - 1] = player_val
                prob_score += 0.4 * heuristic(b_copy_left, player_val)
            if col < cols - 1:
                b_copy_right = board.copy()
                b_copy_right[row][col + 1] = player_val
                prob_score += 0.4 * heuristic(b_copy_right, player_val)

            _, score = expected_minimax(child, depth - 1, True, prefix + "    |", visited_states)
            score += prob_score

            if score < best_score:
                best_score = score
                best_column = col
            print(f"{prefix}├── (Depth: {depth}, Col: {col}, Score: {score})")

        visited_states[board_hash] = best_column, best_score  # Store the best move and score for the current state
        return best_column, best_score

board = initialize_board()
#print(np.flip(board, 0))
game_over = False

pygame.init()

play_pos_size = 100

width = cols * play_pos_size
height = (rows+1) * play_pos_size

size = (width, height)

RADIUS = int(play_pos_size/2 - 5)



def draw_board(board):
	for c in range(cols):
		for r in range(rows):
			pygame.draw.rect(screen, BLUE, (c*play_pos_size, r*play_pos_size+play_pos_size, play_pos_size, play_pos_size))
			pygame.draw.circle(screen, L_YELLOW, (int(c*play_pos_size+play_pos_size/2), int(r*play_pos_size+play_pos_size+play_pos_size/2)), RADIUS)
	
	for c in range(cols):
		for r in range(rows):		
			if board[r][c] == player_val:
				pygame.draw.circle(screen, PINK, (int(c*play_pos_size+play_pos_size/2), height-int(r*play_pos_size+play_pos_size/2)), RADIUS)
			elif board[r][c] == ai_val: 
				pygame.draw.circle(screen, PURPLE, (int(c*play_pos_size+play_pos_size/2), height-int(r*play_pos_size+play_pos_size/2)), RADIUS)
	pygame.display.update()


# Function to handle algorithm selection screen
def algorithm_selection_screen(size):
	window = pygame.display.set_mode(size)
	selected_algorithm = None
	button_width = 400
	button_height = 50
	base_font = pygame.font.Font(None, 32) 
	global user_text 
	user_text = ''
	input_rect = pygame.Rect(100, 100, 140, 32)
	color_passive = pygame.Color('WHITE') 
	color = color_passive 
	active = False
	color_active = pygame.Color('GREY')
	while not selected_algorithm:
		window.fill(L_YELLOW)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				
				if 100 <= mouse_pos[0] <= 100 + button_width and 200 <= mouse_pos[1] <= 200 + button_height:
					selected_algorithm = minimax_without_alpha_beta
				elif 100 <= mouse_pos[0] <= 100 + button_width and 300 <= mouse_pos[1] <= 300 + button_height:
					selected_algorithm = minimax_alpha_beta
				elif 100 <= mouse_pos[0] <= 100 + button_width and 400 <= mouse_pos[1] <= 400 + button_height:
					selected_algorithm = expected_minimax

			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if input_rect.collidepoint(event.pos): 
					active = True
				else: 
					active = False
			if event.type == pygame.KEYDOWN: 
  
            	# Check for backspace 
				if event.key == pygame.K_BACKSPACE: 
					user_text = user_text[:-1] 
				else: 
					user_text += event.unicode
		if active: 
			color = color_active 
		else: 
			color = color_passive 
		pygame.draw.rect(window, color, input_rect)
		pygame.draw.rect(window, BLACK, (100, 100, 100, 32), 1)
		text_surface = base_font.render(user_text, True, (255, 255, 255)) 
		window.blit(text_surface, (input_rect.x+5, input_rect.y+5))
		# set width of textfield so that text cannot get outside of user's text input 
		input_rect.w = max(100, text_surface.get_width()+10) 
		# display.flip() will update only a portion of the screen to updated, not full area 
		#pygame.display.flip() 
			  
		# Draw buttons
	
      
  
        		
		pygame.draw.rect(window, L_PINK, (100, 200, button_width, button_height))
		pygame.draw.rect(window, L_PINK, (100, 300, button_width, button_height))
		pygame.draw.rect(window, L_PINK, (100, 400, button_width, button_height))
		pygame.draw.rect(window, BLACK, (100, 200, button_width, button_height), 1)
		pygame.draw.rect(window, BLACK, (100, 300, button_width, button_height), 1)
		pygame.draw.rect(window, BLACK, (100, 400, button_width, button_height), 1)
		
        # Button labels
		font = pygame.font.Font(None, 30)
		label = font.render("DEPTH", 1, BLACK)
		window.blit(label, (100,70))
		
		minimax_text = font.render("Minimax", True, BLACK)
		minimax_alpha_beta_text = font.render("Minimax with Alpha-Beta", True, BLACK)
		expected_minimax_text = font.render("Expected Minimax", True, BLACK)
		window.blit(minimax_text, (125, 215))
		window.blit(minimax_alpha_beta_text, (125, 315))
		window.blit(expected_minimax_text, (125, 415))
		
		pygame.display.update()
	return selected_algorithm

screen = pygame.display.set_mode(size)
algorithm = algorithm_selection_screen(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("arial", 70)

turn = random.randint(PLAYER, AI)
k = int(user_text)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, L_YELLOW, (0,0, width, play_pos_size))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, PINK, (posx, int(play_pos_size/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, L_YELLOW, (0,0, width, play_pos_size))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/play_pos_size))
				if board[rows-1][col] == 0:
					row = av_row(board, col)
					board[row][col] = player_val


					if is_terminal(board):
						#print("TERMINAL")
						
						if(check_winner(board) == ai_val):
							label = myfont.render("AI wins", 1, RED)
						elif(check_winner(board) ==0):
							label = myfont.render("TIE", 1, RED)
						else:
							label = myfont.render("PLAYER WINS", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					#print(np.flip(board, 0))
					draw_board(board)
					
	if turn == AI and not game_over:
		if(algorithm == minimax_without_alpha_beta):
			#print("algo1")
			col, score = algorithm(board, k, True)
		elif(algorithm == minimax_alpha_beta):
			col, score = algorithm(board, k, -math.inf, math.inf, True)
		else:
			col, score = algorithm(board, k, True)
        
		
		if (board[rows-1][col] == 0):
			row = av_row(board, col)
			board[row][col] = ai_val
			#print("henaa")
			if is_terminal(board):
				#print("TERMINAL")
				if(check_winner(board) == ai_val):
					label = myfont.render("AI wins", 1, PURPLE)
				elif(check_winner(board) ==0):
					label = myfont.render("TIE", 1, PURPLE)
				else:
					label = myfont.render("PLAYER WINS", 1, PURPLE)
				screen.blit(label, (40,10))
				game_over = True

			#print(np.flip(board, 0))
			draw_board(board)

			turn += 1
			turn = turn % 2
			
	if game_over:
		pygame.time.wait(5000)
		print("Thank you for playing Connect Four!")
		pygame.quit()
		sys.exit()
	