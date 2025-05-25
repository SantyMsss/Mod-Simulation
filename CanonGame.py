import pygame
import random
import math

# --------------------
# Constants
# --------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
METAL_GRAY = (105, 105, 105)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Cannon settings
CANNON_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
CANNON_LENGTH = 60
CANNON_WIDTH = 12
CANNON_BASE_RADIUS = 25
CANNON_MIN_ANGLE = 10   # degrees
CANNON_MAX_ANGLE = 160  # degrees
ANGLE_STEP = 2

# Projectile settings
PROJECTILE_SPEED = 25
GRAVITY = 0.3
PROJECTILE_WIDTH = 8
PROJECTILE_HEIGHT = 8
TRAIL_LENGTH = 5

# Target settings
SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_INTERVAL = 2000
TARGET_RADIUS = 30
TARGET_SPEED_RANGE = (2, 5)

# --------------------
# Classes
# --------------------
class Cannon:
    def __init__(self, position):
        self.x, self.y = position
        self.angle = 90
        self.power = 1.0  # Power multiplier for shots

    def rotate(self, delta):
        self.angle = max(CANNON_MIN_ANGLE, min(CANNON_MAX_ANGLE, self.angle + delta))

    def fire(self):
        rad = math.radians(self.angle)
        vx = PROJECTILE_SPEED * math.cos(rad) * self.power
        vy = -PROJECTILE_SPEED * math.sin(rad) * self.power
        start_x = self.x + CANNON_LENGTH * math.cos(rad)
        start_y = self.y - CANNON_LENGTH * math.sin(rad)
        return Projectile(start_x, start_y, vx, vy)

    def draw(self, surface):
        # Draw cannon base (circular platform)
        pygame.draw.circle(surface, BROWN, (int(self.x), int(self.y)), CANNON_BASE_RADIUS)
        pygame.draw.circle(surface, DARK_GRAY, (int(self.x), int(self.y)), CANNON_BASE_RADIUS, 3)
        
        # Draw cannon pivot point
        pygame.draw.circle(surface, METAL_GRAY, (int(self.x), int(self.y)), 8)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 8, 2)
        
        # Calculate cannon barrel end position
        rad = math.radians(self.angle)
        end_x = self.x + CANNON_LENGTH * math.cos(rad)
        end_y = self.y - CANNON_LENGTH * math.sin(rad)
        
        # Draw cannon barrel (with gradient effect using multiple lines)
        for i in range(CANNON_WIDTH):
            offset = i - CANNON_WIDTH // 2
            start_x = self.x + offset * math.sin(rad) * 0.3
            start_y = self.y + offset * math.cos(rad) * 0.3
            barrel_end_x = end_x + offset * math.sin(rad) * 0.3
            barrel_end_y = end_y + offset * math.cos(rad) * 0.3
            
            # Create gradient effect
            if abs(offset) < 2:
                color = LIGHT_GRAY
            else:
                color = DARK_GRAY
                
            pygame.draw.line(surface, color, (start_x, start_y), (barrel_end_x, barrel_end_y), 2)
        
        # Draw main cannon barrel outline
        pygame.draw.line(surface, BLACK, (self.x, self.y), (end_x, end_y), CANNON_WIDTH)
        pygame.draw.line(surface, METAL_GRAY, (self.x, self.y), (end_x, end_y), CANNON_WIDTH - 4)
        
        # Draw cannon muzzle
        pygame.draw.circle(surface, BLACK, (int(end_x), int(end_y)), 6)
        pygame.draw.circle(surface, DARK_GRAY, (int(end_x), int(end_y)), 4)
        
        # Draw angle indicator
        self._draw_angle_indicator(surface)

    def _draw_angle_indicator(self, surface):
        # Draw angle arc
        font = pygame.font.SysFont(None, 24)
        angle_text = font.render(f"{int(self.angle)}°", True, BLACK)
        text_rect = angle_text.get_rect()
        text_rect.center = (self.x - 40, self.y - 40)
        surface.blit(angle_text, text_rect)
        
        # Draw small arc to show angle
        arc_radius = 35
        start_angle = math.radians(0)
        end_angle = math.radians(self.angle)
        
        # Draw angle arc (simplified)
        arc_points = []
        for i in range(int(self.angle)):
            rad = math.radians(i)
            arc_x = self.x + arc_radius * math.cos(rad)
            arc_y = self.y - arc_radius * math.sin(rad)
            arc_points.append((arc_x, arc_y))
        
        if len(arc_points) > 1:
            pygame.draw.lines(surface, RED, False, arc_points, 2)

class Projectile:
    image = None

    def __init__(self, x, y, vx, vy):
        if Projectile.image is None:
            try:
                # Try to load the image first
                Projectile.image = pygame.image.load("img/bala.jpg").convert_alpha()
                # Remove white background more effectively
                Projectile.image = self._remove_white_background(Projectile.image)
                Projectile.image = pygame.transform.scale(Projectile.image, (PROJECTILE_WIDTH * 2, PROJECTILE_HEIGHT * 2))
            except:
                # If image fails to load, create a custom projectile
                Projectile.image = self._create_custom_projectile()
        
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alive = True
        self.trail = []  # For trail effect
        self.age = 0     # For effects over time

    @staticmethod
    def _remove_white_background(image):
        """Remove white background more effectively"""
        # Convert to per-pixel alpha
        image = image.convert_alpha()
        
        # Get the image data
        pixdata = pygame.PixelArray(image)
        
        # Replace white and near-white pixels with transparent
        white_color = image.map_rgb(WHITE)
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))
                # Check if pixel is white or very close to white
                if (pixel_color[0] > 240 and pixel_color[1] > 240 and pixel_color[2] > 240):
                    image.set_at((x, y), (0, 0, 0, 0))  # Transparent
        
        del pixdata
        return image

    @staticmethod
    def _create_custom_projectile():
        """Create a custom projectile if image loading fails"""
        size = PROJECTILE_WIDTH * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw a gradient projectile
        center = size // 2
        for radius in range(center, 0, -1):
            alpha = int(255 * (radius / center))
            color = (*ORANGE[:3], alpha)
            pygame.draw.circle(surface, color, (center, center), radius)
        
        # Add a bright center
        pygame.draw.circle(surface, YELLOW, (center, center), 2)
        
        return surface

    def update(self):
        # Store previous position for trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)
        
        # Update physics
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        
        # Bounce off walls
        if self.x < 0:
            self.x = 0
            self.vx *= -0.8  # Some energy loss on bounce
        elif self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
            self.vx *= -0.8
            
        # Bounce off ceiling
        if self.y < 0:
            self.y = 0
            self.vy *= -0.8
            
        # Remove when hitting ground
        if self.y > SCREEN_HEIGHT:
            self.alive = False

    def draw(self, surface):
        # Draw trail effect
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.3)
            trail_size = max(1, int(PROJECTILE_WIDTH * (i / len(self.trail))))
            
            # Create a temporary surface for the trail dot
            trail_surf = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
            trail_color = (*ORANGE[:3], alpha)
            pygame.draw.circle(trail_surf, trail_color, (trail_size, trail_size), trail_size)
            surface.blit(trail_surf, (trail_x - trail_size, trail_y - trail_size))
        
        # Draw main projectile
        rect = Projectile.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(Projectile.image, rect)
        
        # Add glow effect for young projectiles
        if self.age < 30:
            glow_surface = pygame.Surface((PROJECTILE_WIDTH * 4, PROJECTILE_HEIGHT * 4), pygame.SRCALPHA)
            glow_alpha = int(100 * (1 - self.age / 30))
            pygame.draw.circle(glow_surface, (*YELLOW[:3], glow_alpha), 
                             (PROJECTILE_WIDTH * 2, PROJECTILE_HEIGHT * 2), PROJECTILE_WIDTH * 2)
            glow_rect = glow_surface.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(glow_surface, glow_rect)

class Target:
    image = None

    def __init__(self):
        if Target.image is None:
            try:
                Target.image = pygame.image.load("img/avion.jpg").convert_alpha()
                # Remove white background
                Target.image = self._remove_white_background(Target.image)
                Target.image = pygame.transform.scale(Target.image, (TARGET_RADIUS * 2, TARGET_RADIUS * 2))
            except:
                # Create custom target if image fails
                Target.image = self._create_custom_target()
        
        self.radius = TARGET_RADIUS
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT // 2)
        self.vx = random.choice([-1, 1]) * random.uniform(*TARGET_SPEED_RANGE)
        self.alive = True
        self.hit_effect = 0  # For explosion effect

    @staticmethod
    def _remove_white_background(image):
        """Remove white background from target image"""
        image = image.convert_alpha()
        pixdata = pygame.PixelArray(image)
        
        white_color = image.map_rgb(WHITE)
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))
                if (pixel_color[0] > 240 and pixel_color[1] > 240 and pixel_color[2] > 240):
                    image.set_at((x, y), (0, 0, 0, 0))
        
        del pixdata
        return image

    @staticmethod
    def _create_custom_target():
        """Create a custom target if image loading fails"""
        size = TARGET_RADIUS * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw a red circular target
        pygame.draw.circle(surface, RED, (size//2, size//2), TARGET_RADIUS)
        pygame.draw.circle(surface, WHITE, (size//2, size//2), TARGET_RADIUS - 5)
        pygame.draw.circle(surface, RED, (size//2, size//2), TARGET_RADIUS - 10)
        pygame.draw.circle(surface, WHITE, (size//2, size//2), 5)
        
        return surface

    def update(self):
        self.x += self.vx
        if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
            self.vx *= -1
        
        if self.hit_effect > 0:
            self.hit_effect -= 1

    def hit(self):
        """Called when target is hit"""
        self.hit_effect = 20
        self.alive = False

    def draw(self, surface):
        if self.alive or self.hit_effect > 0:
            if self.hit_effect > 0:
                # Draw explosion effect
                explosion_radius = int(TARGET_RADIUS * (1 + (20 - self.hit_effect) / 10))
                explosion_alpha = int(255 * (self.hit_effect / 20))
                
                explosion_surf = pygame.Surface((explosion_radius * 2, explosion_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(explosion_surf, (*ORANGE[:3], explosion_alpha), 
                                 (explosion_radius, explosion_radius), explosion_radius)
                pygame.draw.circle(explosion_surf, (*YELLOW[:3], explosion_alpha // 2), 
                                 (explosion_radius, explosion_radius), explosion_radius // 2)
                
                explosion_rect = explosion_surf.get_rect(center=(int(self.x), int(self.y)))
                surface.blit(explosion_surf, explosion_rect)
            else:
                # Draw normal target
                rect = Target.image.get_rect(center=(int(self.x), int(self.y)))
                surface.blit(Target.image, rect)

# --------------------
# Main Game
# --------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Juego de Disparos con Cañón Mejorado")
    clock = pygame.time.Clock()

    # Load background
    try:
        background = pygame.image.load("img/cielo.jpg")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        # Create a gradient background if image fails
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(235 + (255 - 235) * color_ratio)
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    cannon = Cannon(CANNON_POS)
    projectiles = []
    targets = []
    explosions = []  # For hit effects
    score = 0

    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT:
                targets.append(Target())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectiles.append(cannon.fire())

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cannon.rotate(ANGLE_STEP)
        if keys[pygame.K_RIGHT]:
            cannon.rotate(-ANGLE_STEP)

        # Update game objects
        for p in projectiles:
            p.update()
        for t in targets:
            t.update()

        # Collision detection
        for p in projectiles:
            for t in targets:
                if t.alive and p.alive:
                    dist = math.hypot(p.x - t.x, p.y - t.y)
                    if dist < TARGET_RADIUS:
                        t.hit()  # Trigger hit effect
                        p.alive = False
                        score += 1

        # Clean up dead objects
        projectiles = [p for p in projectiles if p.alive]
        targets = [t for t in targets if t.alive or t.hit_effect > 0]

        # Draw everything
        screen.blit(background, (0, 0))
        
        # Draw game objects
        cannon.draw(screen)
        for p in projectiles:
            p.draw(screen)
        for t in targets:
            t.draw(screen)

        # Draw UI
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surf, (10, 10))
        
        # Draw instructions
        font_small = pygame.font.SysFont(None, 24)
        instructions = [
            "← → : Rotar cañón",
            "ESPACIO: Disparar"
        ]
        for i, instruction in enumerate(instructions):
            inst_surf = font_small.render(instruction, True, BLACK)
            screen.blit(inst_surf, (10, SCREEN_HEIGHT - 60 + i * 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()