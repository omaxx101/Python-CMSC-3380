import pygame
import sys
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)

player_size = 20
player_speed = 20
score = 0
best=0
name=""

UP = (0, -player_speed)
DOWN = (0, player_speed)
LEFT = (-player_speed, 0)
RIGHT = (player_speed, 0)

def main():

    global best_score,name

    best_score_file = open('/Users/oumerhassen/Desktop/codes/python/best_score_2.txt', 'r+')
    name_file = open('/Users/oumerhassen/Desktop/codes/python/best_name.txt', 'r')
    best_score = int(best_score_file.read())
    name = name_file.read()
    
    best_score_file.close()
    name_file.close()

    pygame.init()
    window = view()
    gameplay(window)

def view():
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(' Snake Game')
    return window

def gameplay(window):
    global score,best
    
    segments = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
    direction = (player_speed, 0)
    target_x, target_y = spawn_apple(segments)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT]  or keys[pygame.K_a] )and direction != (player_speed, 0):
            direction = (-player_speed, 0)
        if (keys[pygame.K_RIGHT]or keys[pygame.K_d]) and direction != (-player_speed, 0):
            direction = (player_speed, 0)
        if (keys[pygame.K_UP]or keys[pygame.K_w])and direction != (0, player_speed):
            direction = (0, -player_speed)
        if (keys[pygame.K_DOWN]or keys[pygame.K_s]) and direction != (0, -player_speed):
            direction = (0, player_speed)

        head = (segments[0][0] + direction[0], segments[0][1] + direction[1])

    # if statemnts to checks for various instances 
        if head[0] == target_x and head[1] == target_y:
            segments.append(segments[-1])
            target_x, target_y = spawn_apple(segments)
            score += 1

        
        if head[0] < 0 or head[0] >= WINDOW_WIDTH or head[1] < 0 or head[1] >= WINDOW_HEIGHT:
            update_best_score(window)
            game_over(window)  # Call game over function
            return

        if head in segments[1:]:
            update_best_score(window)
            game_over(window)  # Call game over function
            return

        segments = [head] + segments[:-1]

        window.fill(BLACK)
        draw_snake(window, segments)
        draw_apple(window, target_x, target_y)
        game_screen(window)

       # Display the score and best score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, WHITE)
        best_score_text = font.render("Best Score by " + name + ": " +str(best_score), True, WHITE)
        window.blit(score_text, (10, 10))
        window.blit(best_score_text, (10, 50))


        pygame.display.update()
        clock.tick(15)  # Adjust FPS for smooth gameplay

def draw_snake(window, segments):
    for segment in segments:
        pygame.draw.rect(window, GREEN, (segment[0], segment[1], player_size, player_size))

def draw_apple(window, x, y):
    pygame.draw.rect(window, RED, (x, y, player_size, player_size))

def spawn_apple(segments):
    while True:
        x = random.randint(10, (WINDOW_WIDTH - player_size) // player_size) * player_size
        y = random.randint(10, (WINDOW_HEIGHT - player_size) // player_size) * player_size
        if (x, y) not in segments:
            return x, y

def game_screen(window):
    pygame.draw.line(window, WHITE, (0, 0), (WINDOW_WIDTH, 0), 15)
    pygame.draw.line(window, WHITE, (0, 0), (0, WINDOW_HEIGHT), 10)
    pygame.draw.line(window, WHITE, (WINDOW_WIDTH - 2, 0), (WINDOW_WIDTH - 2, WINDOW_HEIGHT), 10)
    pygame.draw.line(window, WHITE, (0, WINDOW_HEIGHT - 2), (WINDOW_WIDTH, WINDOW_HEIGHT - 2), 15)

def update_best_score(window):
    global score, best_score, name
    if score > best_score:
        best_score = score
        best_score_file = open('/Users/oumerhassen/Desktop/codes/python/best_score_2.txt', 'w')
        name_file = open('/Users/oumerhassen/Desktop/codes/python/best_name.txt', 'w')
        best_score_file.write(str(best_score))
        
        # Prompt the user to enter their name
        name = input_name(window)
        name_file.write(name)
        
        best_score_file.close()
        name_file.close()

def input_name(window):
    # Create a Pygame input box for entering the name
    window.fill(BLACK)
    font = pygame.font.Font(None, 54)
    text = font.render("Enter Your Name ", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
    window.blit(text, text_rect)

    font = pygame.font.Font(None, 32)
    input_box_width = 200
    input_box_height = 40
    input_box_x = (WINDOW_WIDTH - input_box_width) // 2
    input_box_y = (WINDOW_HEIGHT - input_box_height) // 2
    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
    color_inactive = pygame.Color('gray')
    color_active = pygame.Color('green')
    color = color_inactive
    active = False
    name = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle the active variable if the user clicks inside the input box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Change the color of the input box
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                # If the input box is active and the user presses Enter, return the entered name
                if active:
                    if event.key == pygame.K_RETURN:
                        return name
                    # If the user presses backspace, remove the last character from the name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    # Otherwise, add the pressed character to the name
                    else:
                        name += event.unicode

        # Render the input box and the entered name
        txt_surface = font.render(name, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        window.blit(txt_surface, (input_box.x +5, input_box.y+ 5))
        pygame.draw.rect(window, color, input_box, 2)

        pygame.display.flip()

def game_over(window):

    global score,best
    window.fill(BLACK)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
    window.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2  , WINDOW_HEIGHT // 2 + 50))
    window.blit(score_text, score_rect)

    font = pygame.font.Font(None, 36)
    best_score_text = font.render("Best Score by " + name + ": " + str(best_score), True, WHITE)
    best_score_rect = best_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
    window.blit(best_score_text, best_score_rect)

    font = pygame.font.Font(None, 54)
    retry_text = font.render("Retry", True, GREEN)
    retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 ))
    window.blit(retry_text, retry_rect)

    pygame.display.update()

    # Reset score for retry
    score = 0

    # Wait for user input (retry or quit)
    while True:
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if retry_rect.collidepoint(mouse_x, mouse_y):
                # Restart the game
                gameplay(window)
                return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Restart the game if Enter key is pressed
                gameplay(window)
                return


main()