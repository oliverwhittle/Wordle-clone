import pygame
from pygame.locals import *
import random

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Wordle Clone")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (108,169,101)
YELLOW = (200,182,83)
GREY = (120,124,127)
DARK_GREY = (18,18,19)

BACKGROUND_COLOUR = WHITE
TEXT_COLOUR = BLACK
GRID_COLOUR = BLACK

font = pygame.font.Font(None, 36)

clock.tick(60)

screen.fill(BACKGROUND_COLOUR)

cell_width = 75
cell_height = 75
grid_width = 5
grid_height = 6

border_width = 2

def get_random_word(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip().lower()

todays_word = get_random_word('words.txt').upper()

def compare_words(word1, word2):
    comparison_array = []

    remaining_letters = list(word2)

    for i, (letter1, letter2) in enumerate(zip(word1, word2)):
        if letter1 == letter2:
            comparison_array.append('Green')
            remaining_letters.remove(letter1)
        else:
            comparison_array.append(None)

    for i, letter1 in enumerate(word1):
        if comparison_array[i] is None and letter1 in remaining_letters:
            comparison_array[i] = "Yellow"
            remaining_letters.remove(letter1)

    for i, letter1 in enumerate(word1):
        if comparison_array[i] is None:
            comparison_array[i] = "Grey"

    return comparison_array

grid_start_x = (screen.get_width() - (grid_width * cell_width)) // 2
grid_start_y = (screen.get_height() - (grid_height * cell_height)) // 2 - 150

for row in range(grid_height):
    for col in range(grid_width):
        x = grid_start_x + col * cell_width
        y = grid_start_y + row * cell_height
        pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)

qwerty_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

keyboard_width = len(qwerty_layout[0]) * cell_width
keyboard_height = len(qwerty_layout) * cell_height

keyboard_start_x = (screen.get_width() - keyboard_width) // 2
keyboard_start_y = (screen.get_height() - keyboard_height) // 2 + 250

for row_index, row in enumerate(qwerty_layout):
    for col_index, char in enumerate(row):
        if row_index == 1:
            key_x = keyboard_start_x + col_index * cell_width + cell_width // 2
        elif row_index == 2:
            key_x = keyboard_start_x + col_index * cell_width + cell_width
        else:
            key_x = keyboard_start_x + col_index * cell_width
        key_y = keyboard_start_y + row_index * cell_height
        pygame.draw.rect(screen, GRID_COLOUR, (key_x, key_y, cell_width, cell_height), border_width)
        text = font.render(char, True, TEXT_COLOUR)
        text_rect = text.get_rect(center=(key_x + cell_width // 2, key_y + cell_height // 2))
        screen.blit(text, text_rect)

row = 0
col = 0

key_log = [None] * grid_width

guessed_letters = {}

game_won = False
game_lost = False

pygame.display.update()

running = True

word_entered = False  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.unicode.isalpha() and (game_won == False and game_lost == False) and event.key != pygame.K_RETURN:
            key = pygame.key.name(event.key).upper()
            key_log[col] = str(key)

            text = font.render(str(key), True, TEXT_COLOUR)

            x = grid_start_x + col * cell_width
            y = grid_start_y + row * cell_height

            pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
            screen.blit(text, (x + cell_width // 2 - text.get_width() // 2, y + cell_height // 2 - text.get_height() // 2))

            col += 1

            pygame.display.update()

            if col >= grid_width:
                word_entered = True
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            if col > 0:
                col -= 1
                key_log[col] = None
                x = grid_start_x + col * cell_width
                y = grid_start_y + row * cell_height
                pygame.draw.rect(screen, BACKGROUND_COLOUR, (x, y, cell_width, cell_height))
                pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                pygame.display.update()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if word_entered:
                if "".join(key_log) not in open('words.txt').read().upper():
                    for i in range(grid_width):
                        if key_log[i] is not None:
                            key_log[i] = None          

                    for col in range(grid_width):
                        x = grid_start_x + col * cell_width
                        y = grid_start_y + row * cell_height
                        pygame.draw.rect(screen, BACKGROUND_COLOUR, (x, y, cell_width, cell_height))
                        pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                    
                    col = 0

                else:
                    position_array = compare_words("".join(key_log), todays_word)
                    if all(position_array[i] == "Green" for i in range(len(position_array))):
                        winning_row = row
                        for col in range(grid_width):
                            x = grid_start_x + col * cell_width
                            y = grid_start_y + winning_row * cell_height
                            text = font.render(key_log[col], True, TEXT_COLOUR)
                            pygame.draw.rect(screen, GREEN, (x, y, cell_width, cell_height))
                            pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                            screen.blit(text, (x + cell_width // 2 - text.get_width() // 2, y + cell_height // 2 - text.get_height() // 2))
                        game_won = True
                    else:
                        for col in range(grid_width):
                            x = grid_start_x + col * cell_width
                            y = grid_start_y + row * cell_height
                            text = font.render(key_log[col], True, TEXT_COLOUR)
                            if position_array[col] == "Green":
                                pygame.draw.rect(screen, GREEN, (x, y, cell_width, cell_height))
                            elif position_array[col] == "Yellow":
                                pygame.draw.rect(screen, YELLOW, (x, y, cell_width, cell_height))
                            elif position_array[col] == "Grey":
                                pygame.draw.rect(screen, GREY, (x, y, cell_width, cell_height))
                            pygame.draw.rect(screen, GRID_COLOUR, (x, y, cell_width, cell_height), border_width)
                            screen.blit(text, (x + cell_width // 2 - text.get_width() // 2, y + cell_height // 2 - text.get_height() // 2))
                    
                    for i, letter in enumerate(key_log):
                        if letter not in guessed_letters:
                            guessed_letters[letter] = position_array[i]
                        elif letter in guessed_letters:
                            if guessed_letters[letter] == "Grey" and position_array[i] != "Grey":
                                guessed_letters[letter] = position_array[i]
                            elif guessed_letters[letter] == "Yellow" and position_array[i] == "Green":
                                guessed_letters[letter] = position_array[i]
                    
                    for row_index, keyboard_row in enumerate(qwerty_layout):
                        for col_index, char in enumerate(keyboard_row):
                            if row_index == 1:
                                key_x = keyboard_start_x + col_index * cell_width + cell_width // 2
                            elif row_index == 2:
                                key_x = keyboard_start_x + col_index * cell_width + cell_width
                            else:
                                key_x = keyboard_start_x + col_index * cell_width
                            key_y = keyboard_start_y + row_index * cell_height
                            if char in guessed_letters:
                                if guessed_letters[char] == "Green":
                                    colour = GREEN
                                elif guessed_letters[char] == "Yellow":
                                    colour = YELLOW
                                elif guessed_letters[char] == "Grey":   
                                    colour = GREY
                            else:
                                colour = BACKGROUND_COLOUR
                            pygame.draw.rect(screen, colour, (key_x, key_y, cell_width, cell_height))
                            pygame.draw.rect(screen, GRID_COLOUR, (key_x, key_y, cell_width, cell_height), border_width)
                            text = font.render(char, True, TEXT_COLOUR)
                            text_rect = text.get_rect(center=(key_x + cell_width // 2, key_y + cell_height // 2))
                            screen.blit(text, text_rect)

                    col = 0
                    row += 1
                    if row >= grid_height and game_won == False:
                        game_lost = True
                        screen.fill(BACKGROUND_COLOUR)
                        text = font.render("You lost! The word was: " + todays_word, True, TEXT_COLOUR)
                        text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        break
                    elif game_won == True:
                        screen.fill(BACKGROUND_COLOUR)
                        text = font.render("You won! The word was: " + todays_word, True, TEXT_COLOUR)
                        text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        break

            pygame.display.update()

pygame.quit()

