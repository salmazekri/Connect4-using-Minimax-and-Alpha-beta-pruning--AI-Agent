# Connect4-using-Minimax-and-Alpha-beta-pruning-AI-Agent
## Assumptions made in this project:
The code assumes a fixed game board size of 6 rows and 7 columns, as indicated by the rows and cols variables.
The game assumes a two-player setup, with the player and AI taking turns.
The AI is assumed to make optimal moves based on the selected algorithm, aiming to win the game or prevent the player from winning.
The game is assumed to terminate when the board is completely filled.
The code assumes the availability of the Pygame library for the graphical user interface and visual representation of the game.

## Data Structures used:
board: The game board is represented as a 2D numpy array, which provides a convenient way to manipulate and access elements. The complexity of accessing an element is O(1), and updating an element is also O(1).
visited_states: This is a dictionary used to store visited board states as keys and their corresponding best move and score as values. The complexity of accessing and updating an element in a dictionary is on average O(1), assuming a well-distributed hash function.

## Strategies Comparison
COMPARING the three algorithms in terms of time taken and the number of expanded nodes:
# minimax_without_alpha_beta: 
This algorithm applies the basic minimax strategy without alpha-beta pruning. It explores all possible game states up to a specified depth. The time complexity for this algorithm is O(b^d), where b is the average branching factor (number of available moves) and d is the depth. As it explores all possible game states, the number of expanded nodes can be high, especially for larger boards and deeper depths.
# minimax_alpha_beta: 
This algorithm enhances the minimax algorithm by using alpha-beta pruning. It prunes branches of the search tree that are guaranteed to be suboptimal. This leads to fewer nodes being expanded, resulting in improved time complexity compared to the basic minimax algorithm. The time complexity is typically lower than O(b^d), but it can still vary based on the game state and the efficiency of the pruning.
# expected_minimax: 
This algorithm introduces probabilistic evaluation by considering potential moves of the opponent players. It assigns weights to different outcomes based on their probabilities and combines them with the minimax approach. The time complexity and the number of expanded nodes for this algorithm are similar to those of the minimax algorithm, as it explores similar game states. However, the weights and probabilistic evaluations introduce additional complexity in determining the best move.

## Conclusion:
The algorithm with the smallest tree would typically be minimax_without_alpha_beta since it explores all possible game states without pruning any branches. This results in the maximum number of expanded nodes, but it ensures that every possible outcome is evaluated.
As depth increases, it becomes harder to beat the AI and response time of the game increases.
ORDER of increasing tree size:
1)Min max with pruning
2) Expecti min max
3) min max without pruning

## Response time for 10 games:
1)3.5 seconds/10/2 - second longest
2) 3 seconds/10/2 - fastest
3) 4 seconds/10/2 - longest response time
