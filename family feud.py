import pygame
import sys
import subprocess
import os
import time
from PIL import Image, ImageSequence

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")


WHITE = (255, 255, 255)
GOLD = (184, 134, 11)
DARK_BLUE = (0, 0, 50)

font = pygame.font.Font(None, 60)

start_button_img = pygame.image.load('play.png').convert_alpha()
credit_button_img = pygame.image.load('credits.png').convert_alpha()
exit_button_img = pygame.image.load('quit.png').convert_alpha()
logo_button_img = pygame.image.load('Logo.png').convert_alpha()
diwali_button_img = pygame.image.load('Diwali.png').convert_alpha()
x_button_img = pygame.image.load('x.png').convert_alpha()
credit_bg_img = pygame.image.load('credit_bg.png').convert_alpha()
bg = pygame.image.load('background.png')


class Button:
    def __init__(self, x, y, image, is_small=False):
        if is_small: 
            self.image = pygame.transform.scale(image, (50, 50))
        else:
            self.image = pygame.transform.scale(image, (280, 110))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            return True
        return False

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Logo:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (1200, 500))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
class Diwali:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (700, 300))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


start_button = Button(WIDTH//13 - 140, HEIGHT//2 + 115, start_button_img)
credits_button = Button(WIDTH//13 - 140, HEIGHT//2 + 250, credit_button_img)
quit_button = Button(WIDTH//13 - 140, HEIGHT//2 + 400, exit_button_img)
logo_img = Logo(WIDTH//2 - 575, HEIGHT//2 - 600, logo_button_img)
diwali_img = Diwali(WIDTH//2 + 100, HEIGHT//2 - 350, diwali_button_img)

def draw_menu():
    screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))
    start_button.draw(screen)
    credits_button.draw(screen)
    quit_button.draw(screen)
    logo_img.draw(screen)
    diwali_img.draw(screen)

def credits_screen():
    popup_width, popup_height = 900, 700
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2

    close_button = Button(popup_x + popup_width - 210, popup_y + 110, x_button_img, is_small=True)

    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    
    credit_bg = pygame.transform.scale(credit_bg_img, (popup_width, popup_height))
    popup_surface.blit(credit_bg, (0, 0))

    title_font = pygame.font.Font(None, 60)
    text_font = pygame.font.Font(None, 40)

    title_text = "Credits"
    title = title_font.render(title_text, True, DARK_BLUE)
    title_rect = title.get_rect(center=(popup_width // 2, 135))
    
    underline_thickness = 5
    underline_rect = pygame.Rect(title_rect.left, title_rect.bottom + 5, title_rect.width, underline_thickness)

    popup_surface.blit(title, title_rect)
    pygame.draw.rect(popup_surface, DARK_BLUE, underline_rect)

    names = ["Kyle Pat", "Pranushan Piruthviraj", "Derek Lai", "Johnny Ren"]
    for i, name in enumerate(names):
        text = text_font.render(name, True, DARK_BLUE)
        text_rect = text.get_rect(center=(popup_width // 2, 235 + i * 100))
        popup_surface.blit(text, text_rect)

    running = True
    while running:
        draw_menu()
        
        screen.blit(popup_surface, (popup_x, popup_y))
        
        close_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if close_button.is_clicked(event.pos):
                    running = False 

        pygame.display.update()
        pygame.time.delay(30)

class SimpleLoadingScreen:
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.display_size = pygame.display.Info().current_w, pygame.display.Info().current_h - 50
        self.screen = pygame.display.set_mode(self.display_size)
        
        # Set scale factor to 1.0 to keep original size
        self.scale_factor = 1.5
        
        # Load GIF frames
        self.gif_frames = self.load_gif_frames("run.gif")
        self.current_frame = 0
        self.frame_delay = 50  # Keep this faster animation speed
        self.last_update = pygame.time.get_ticks()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Font setup
        self.font = pygame.font.Font(None, 50)  # Default font, size 50

    def load_gif_frames(self, filename):
        """Loads frames from a GIF and converts them to Pygame surfaces."""
        pil_image = Image.open(filename)
        frames = []
        
        for frame in ImageSequence.Iterator(pil_image):
            frame = frame.convert("RGBA")  # Ensure compatibility
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            pygame_image = pygame.image.fromstring(data, size, mode)
            frames.append(pygame_image)
        
        # Only scale if scale_factor is not 1.0
        if self.scale_factor != 1.5:
            scaled_frames = []
            for frame in frames:
                original_size = frame.get_size()
                new_size = (int(original_size[0] * self.scale_factor), 
                          int(original_size[1] * self.scale_factor))
                scaled_frames.append(pygame.transform.scale(frame, new_size))
            return scaled_frames
        else:
            return frames

    def draw_loading_text(self):
        """Draws 'Loading...' text on the screen."""
        loading_text = self.font.render("Loading...", True, self.WHITE)
        text_x = (self.display_size[0] - loading_text.get_width()) / 2
        text_y = self.display_size[1] - 100  # Position near the bottom
        self.screen.blit(loading_text, (text_x, text_y))

    def run(self):
        """Run the loading screen with GIF animation and text."""
        running = True
        start_time = time.time()
        duration = 3  # Show for 3 seconds
        
        while running and time.time() - start_time < duration:
            self.screen.fill(self.BLACK)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update and draw GIF animation
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
                self.last_update = current_time
            
            # Center the GIF
            gif_x = (self.display_size[0] - self.gif_frames[self.current_frame].get_width()) / 2
            gif_y = (self.display_size[1] - self.gif_frames[self.current_frame].get_height()) / 2
            self.screen.blit(self.gif_frames[self.current_frame], (gif_x, gif_y))
            
            # Draw the "Loading..." text
            self.draw_loading_text()
            
            # Update display
            pygame.display.flip()
            pygame.time.delay(16)  # Keep the smoother frame rate
        
        # After the animation completes, run the game
        self.run_family_feud()

    def run_family_feud(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "family feud diwali edition.py")
        print(f"Attempting to run Family Feud from: {script_path}")
        
        import sys
        python_exe = sys.executable
        print(f"Using Python interpreter: {python_exe}")
        
        try:
            subprocess.run([python_exe, script_path], check=True)
            pygame.quit()
            sys.exit()
        except subprocess.CalledProcessError as e:
            print(f"Error running the Family Feud script: {e}")
        except FileNotFoundError:
            print(f"Error: The script was not found at {script_path}")

def start_game():
    loading_screen = SimpleLoadingScreen()
    loading_screen.run() 

def play_background_music():
    pygame.mixer.music.load('cafe_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0) 

running = True
play_background_music()  

while running:
    draw_menu()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event.pos):
                print("Start Game")
                start_game() 
                pygame.quit() 
                sys.exit()
            elif credits_button.is_clicked(event.pos):
                credits_screen()
            elif quit_button.is_clicked(event.pos):
                pygame.quit()
                sys.exit()
                
    pygame.time.delay(30)

# Run the loading screen
if __name__ == "__main__":
    SimpleLoadingScreen().run()

pygame.quit()
