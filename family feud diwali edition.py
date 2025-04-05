"""
KEYBINDS:
    - SPACE: Show X
    - Z: Play intro sound
    - X: Play clapping sound
    - RIGHT: Next question
    - LEFT: Previous question
    - M: Move flying crocodillo
    -BACKSPACE: Start/Pause timer

GROUP 1:
    - I: Increase Group 1 score
    - U: Decrease Group 1 score
GROUP 2:
    - P: Increase Group 2 score
    - O: Decrease Group 2 score
"""

import pygame
import time

pygame.init()
pygame.display.init()  
running = True
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mega super level 9999 level diwali quiz")

# Load background pattern
flower_pattern = pygame.image.load("bg1.jpg")
flower_pattern = pygame.transform.scale(flower_pattern, (WIDTH, HEIGHT))
bg2 = pygame.image.load('bg2.jpg')
bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT))
bg3 = pygame.image.load('bg3.jpg')
bg3 = pygame.transform.scale(bg3, (WIDTH, HEIGHT))
bg4 = pygame.image.load('bg4.jpg')
bg4 = pygame.transform.scale(bg4, (WIDTH, HEIGHT))
bg5 = pygame.image.load('bg5.jpg')
bg5 = pygame.transform.scale(bg5, (WIDTH, HEIGHT))
bg6 = pygame.image.load('bg6.png')
bg6 = pygame.transform.scale(bg6, (WIDTH, HEIGHT))
bg7 = pygame.image.load('bg7.png')
bg7 = pygame.transform.scale(bg7, (WIDTH, HEIGHT))
bg8 = pygame.image.load('bg8.png')
bg8 = pygame.transform.scale(bg8, (WIDTH, HEIGHT))

backgrounds = [flower_pattern, bg2, bg3, bg4, bg5, bg6, bg7, bg8]
current_background = 0

# Load flying image
flying_image = pygame.image.load("tiny_crocodillo.png")
flying_image = pygame.transform.scale(flying_image, (150, 100))

class Logo:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (500, 200))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
stop_button = pygame.image.load('stop.png').convert_alpha()
stop_img = Logo(WIDTH//2 - 400, HEIGHT//2 - 250, stop_button)
stop_img.draw(screen)

YELLOW = (255, 255, 0)
GOLD = (184, 134, 11)
DARK_YELLOW = (200, 200, 0)
DARK_PURPLE = (75, 0, 130)
PURPLE = (128, 0, 128)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE =   (0, 0, 100)
ORANGE =  (255, 165, 0)
BLACK =  (0, 0, 0)
GREEN =  (0, 255, 0)

button_width, button_height = 300, 150

buttons = [
    pygame.Rect(WIDTH // 2 - 350, HEIGHT // 2 - 200, button_width, button_height),
    pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 - 200, button_width, button_height),
    pygame.Rect(WIDTH // 2 - 350, HEIGHT // 2 + 50, button_width, button_height),
    pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 50, button_width, button_height)
]

button_states = [False, False, False, False]

questions = [
    {"question": "Quel nourriture est manger pendant Diwali?",  #Food
     "answers": ["Samosa", "Guulab", "Poori", "Barfi"]},
    {"question": "Quels religions sont associes avec Diwali?", #Religions
     "answers": ["Hinduism", "Buddhism", "Jainisme", "Sikhisme"]}, 
    {"question": "Quel vetements sont porter pendant Diwali?",  #Clothings
     "answers": ["Saris", "Lehnga-Coli", "Veshti", "Kurta"]},
    {"question": "Quel pays celebre Diwali?",  #Countries
     "answers": ["L'Inde", "Canada", "Sri Lanka", "Malasie"]},
    {"question": "Quel activites sont font pendant Diwali?",  #Activities
     "answers": ["Allumage Diyas", "Feu d'artifice", "Nettoyage du maison", "Cadaux"]},
    {"question": "Signifiance du nourriture?",  #Significance of food
     "answers": ["Joie", "Triomphe", "Paix", "N/A"]},
    {"question": "Quel dieux principaux qui sont celebre pendant Diwali?",  #Gods
     "answers": ["Parvati", "Shiva", "Lakshimi", "Ganesha"]},
    {"question": "Quels sont les valeurs du Diwali?",  #Values
     "answers": ["L'egalite", "Loyaute", "L'Humilite", "Patience"]},
]

current_section = 0 

group1_score = 0
group2_score = 0

font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 48)
score_font = pygame.font.Font(None, 72)

show_x = False
x_timer = 0

total_seconds = 90
start_time = None
paused = True
paused_time = 0
timer_active = False
timer_color = BLACK  # Default color when not started

flying = False
fly_x, fly_y = 0, HEIGHT // 2
fly_speed = 2 #crocodillo speeeed
direction_x = 1
direction_y = 1
pygame.mixer.init()
sound_effect = pygame.mixer.Sound("x_sound.mp3")
flip_sound_effect = pygame.mixer.Sound("flip_sound.mp3")
intro_sound_effect = pygame.mixer.Sound("intro_sound.mp3")
clapping_sound_effect = pygame.mixer.Sound("clap_sound.mp3")
ding_sound = pygame.mixer.Sound("ding_sound.mp3")
ack_sound = pygame.mixer.Sound("ack_sound.mp3")

def draw_text(question_text):
    pygame.draw.rect(screen, DARK_BLUE, (WIDTH//2 - 700, 90, 1400, 110))
    pygame.draw.rect(screen, ORANGE, (WIDTH//2 - 650, 100, 1300, 90))
    text_surface = font.render(question_text, True, DARK_BLUE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 150)) 
    screen.blit(text_surface, text_rect)

def draw_x():
    if show_x:
        x_font = pygame.font.Font(None, 500)
        x_surface = x_font.render("X", True, RED)
        x_rect = x_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 
        screen.blit(x_surface, x_rect)

def draw_score():
    pygame.draw.rect(screen, YELLOW, (200, 300, 300, 200))
    pygame.draw.rect(screen, PURPLE, (200, 300, 300, 200), 5)
    group1_label = font.render("Group 1", True, DARK_PURPLE)
    screen.blit(group1_label, (250, 320))
    score1_surface = score_font.render(str(group1_score), True, DARK_PURPLE)
    screen.blit(score1_surface, (350, 400))

    pygame.draw.rect(screen, YELLOW, (WIDTH - 500, 300, 300, 200))
    pygame.draw.rect(screen, PURPLE, (WIDTH - 500, 300, 300, 200), 5)
    group2_label = font.render("Group 2", True, DARK_PURPLE)
    screen.blit(group2_label, (WIDTH - 450, 320))
    score2_surface = score_font.render(str(group2_score), True, DARK_PURPLE)
    screen.blit(score2_surface, (WIDTH - 350, 400))

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

def draw_timer():
    global start_time, paused_time, timer_active, timer_color, paused  # <- Add paused here

    # Timer box background
    pygame.draw.rect(screen, WHITE, (WIDTH - 225, 50, 200, 100))
    pygame.draw.rect(screen, BLACK, (WIDTH - 225, 50, 200, 100), 5)

    # Calculate elapsed time
    if start_time is not None and not paused:
        elapsed = time.time() - start_time
        seconds_left = max(0, total_seconds - int(elapsed))
        if seconds_left <= 10:
            timer_color = RED
        else:
            timer_color = GREEN
    else:
        seconds_left = total_seconds - int(paused_time)
        timer_color = BLACK

    # Draw the time
    timer_text = font.render(format_time(seconds_left), True, timer_color)
    screen.blit(timer_text, (WIDTH - 185, 80))

    # If time runs out, trigger the effect just once
    if seconds_left == 0 and timer_active:
        sound_effect.set_volume(0.2)
        sound_effect.play()
        timer_active = False
        paused = True

def reset_buttons():
    global button_states
    button_states = [False, False, False, False]

running = True
while running:
    screen.blit(backgrounds[current_background], (0, 0))
    draw_text(questions[current_section]["question"])
    draw_timer()
    draw_score()
   
    if show_x and time.time() - x_timer > 1.3:
        show_x = False

    for i, button in enumerate(buttons):
        color = DARK_YELLOW if button_states[i] else YELLOW
        pygame.draw.rect(screen, color, button)
        pygame.draw.rect(screen, PURPLE, button, 5)

        if button_states[i]:
            text_surface = button_font.render(questions[current_section]["answers"][i], True, DARK_PURPLE)
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)
    
    draw_x()
    
    if flying:
        screen.blit(flying_image, (fly_x, fly_y))
        fly_x += direction_x * fly_speed
        fly_y += direction_y * fly_speed
        
        if fly_x >= WIDTH - 50 or fly_x <= 0:
            direction_x *= -1 
        if fly_y >= HEIGHT - 50 or fly_y <= 0:
            direction_y *= -1 
        if fly_x < 0 or fly_x > WIDTH or fly_y < 0 or fly_y > HEIGHT:
            flying = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    if not button_states[i]:
                        flip_sound_effect.set_volume(0.2)
                        flip_sound_effect.play()
                    button_states[i] = not button_states[i] 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if not timer_active:
                    # Start timer
                    start_time = time.time()
                    paused_time = 0
                    paused = False
                    timer_active = True
                elif not paused:
                    # Pause timer
                    paused_time = time.time() - start_time
                    paused = True
                else:
                    # Resume timer
                    start_time = time.time() - paused_time
                    paused = False
                    timer_active = True

            if event.key == pygame.K_SPACE:
                show_x = True 
                x_timer = time.time()
                sound_effect.set_volume(0.1)
                sound_effect.play()
            elif event.key == pygame.K_z:
                intro_sound_effect.set_volume(0.1)
                intro_sound_effect.play()
            elif event.key == pygame.K_x:
                clapping_sound_effect.set_volume(0.3)
                clapping_sound_effect.play()
            elif event.key == pygame.K_m:
                if flying:
                    flying = False 
                else:
                    flying = True  
                    fly_x = 0 
                    fly_y = HEIGHT // 2 
            elif event.key == pygame.K_i:
                group1_score += 1
                ding_sound.set_volume(0.3)
                ding_sound.play() 
            elif event.key == pygame.K_u:
                group1_score -= 1
                ack_sound.set_volume(0.2)
                ack_sound.play() 
            elif event.key == pygame.K_p:
                group2_score += 1
                ding_sound.set_volume(0.3)
                ding_sound.play() 
            elif event.key == pygame.K_o:
                group2_score -= 1
                ack_sound.set_volume(0.2)
                ack_sound.play() 
            elif event.key in [pygame.K_RIGHT, pygame.K_LEFT]:  # Reset timer on arrow key press
                start_time = time.time()
                paused_time = 0
                button_text = "Pause"
                paused = False
                if event.key == pygame.K_RIGHT and current_section < len(questions) - 1:
                    current_section += 1
                    reset_buttons()  
                    current_background = (current_background + 1) % len(backgrounds)
                elif event.key == pygame.K_LEFT and current_section > 0:
                    current_section -= 1
                    reset_buttons()  
                    current_background = (current_background - 1) % len(backgrounds)

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        
        # Handle timer visibility timeout
        if show_x and time.time() - x_timer > 1.3:
            show_x = False

    pygame.display.flip()  # <- this should be outside the event loop
    clock.tick(30)


pygame.quit()