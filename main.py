import pygame 
import time
import random
pygame.font.init()  # Initialize font module

# -------------------- Constants & Setup --------------------
WIDTH, HEIGHT = 800, 600  # Window dimensions
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space dog")  # Window title

# Load and scale background image
BG = pygame.transform.scale(pygame.image.load("img.jpeg"), (WIDTH, HEIGHT))

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_VEL = 5

# Falling star properties
STAR_WIDTH = 20
STAR_HEIGHT = 20
STAR_VEL = 5

# Font setup for displaying text
FONT = pygame.font.SysFont("comicsans", 30)

# -------------------- Draw Function --------------------
def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))  # Draw background
    
    # Display elapsed time at top-left
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    
    # Draw player (red square)
    pygame.draw.rect(WIN, "red", player)
    
    # Draw falling stars (white squares)
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    
    pygame.display.update()  # Update the display

# -------------------- Main Game Loop --------------------
def main():
    run = True
    
    # Create player rectangle
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    # Controls how often stars are added
    star_add_increament = 2000  # in milliseconds
    star_count = 0
    
    stars = []  # List to store falling stars
    hit = False  # True if player is hit by star
        
    while run:
        star_count += clock.tick(60)  # Limit FPS to 60 and increment star timer
        elapsed_time = time.time() - start_time  # Calculate time survived
        
        # Add new stars after certain time
        if star_count > star_add_increament:
            for _ in range(3):  # Add 3 stars at random x positions
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            
            # Speed up star spawns over time
            star_add_increament = max(200, star_add_increament - 50)
            star_count = 0    
        
        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL > 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL    
        
        # Move stars down and check for collisions
        for star in stars[:]:
            star.y += STAR_VEL
            
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True 
                break   
       
        # Game over if player is hit
        if hit:
            lost_text = FONT.render("You lost!", 1, "white")
            WIN.blit(lost_text, (
                WIDTH / 2 - lost_text.get_width() / 2,
                HEIGHT / 2 - lost_text.get_height() / 2
            ))
            pygame.display.update()
            pygame.time.delay(4000)  # Wait 4 seconds before closing
            break

        # Draw everything on screen
        draw(player, elapsed_time, stars) 
           
    pygame.quit()

# -------------------- Run the Game --------------------
if __name__ == "__main__":
    main()
  
