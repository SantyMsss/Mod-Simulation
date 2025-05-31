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
CANNON_MIN_ANGLE = 10  # degrees
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
level = 0


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
                Projectile.image = pygame.transform.scale(Projectile.image,
                                                          (PROJECTILE_WIDTH * 2, PROJECTILE_HEIGHT * 2))
            except:
                # If image fails to load, create a custom projectile
                Projectile.image = self._create_custom_projectile()

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alive = True
        self.trail = []  # For trail effect
        self.age = 0  # For effects over time

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
    global level

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
        self.vy = random.choice([-1, 1]) * random.uniform(*TARGET_SPEED_RANGE) if level >= 2 else 0
        self.alive = True
        self.hit_effect = 0  # For explosion effect
        self.level = level
        self.hits_required = 2 if level >= 3 else 1
        self.hits_taken = 0

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
        pygame.draw.circle(surface, RED, (size // 2, size // 2), TARGET_RADIUS)
        pygame.draw.circle(surface, WHITE, (size // 2, size // 2), TARGET_RADIUS - 5)
        pygame.draw.circle(surface, RED, (size // 2, size // 2), TARGET_RADIUS - 10)
        pygame.draw.circle(surface, WHITE, (size // 2, size // 2), 5)

        return surface

    def update(self):
        self.x += self.vx
        if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
            self.vx *= -1
        if level >= 2:
            self.y += self.vy
            if self.y < self.radius or self.y > SCREEN_HEIGHT // 2 - self.radius:
                self.vy *= -1

        if self.hit_effect > 0:
            self.hit_effect -= 1

    def hit(self):
        """Called when target is hit"""
        self.hits_taken += 1
        if self.hits_taken >= self.hits_required:
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

                if self.level >= 3:
                    bar_width = 40
                    bar_height = 6
                    bar_x = self.x - bar_width // 2
                    bar_y = self.y - self.radius - 10

                    # Calculate health ratio
                    health_ratio = (self.hits_required - self.hits_taken) / self.hits_required

                    # Background (gray)
                    pygame.draw.rect(surface, LIGHT_GRAY, (bar_x, bar_y, bar_width, bar_height))
                    # Foreground (green)
                    pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
                    # Border
                    pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)


# --------------------
# menu Game
# --------------------
def main_menu(screen, background):
    font_title = pygame.font.SysFont(None, 60)
    font_instruction = pygame.font.SysFont(None, 36)

    title_text = font_title.render("Juego de Disparos con Cañón", True, BLACK)
    instruction_text = font_instruction.render("Presiona ENTER para comenzar", True, DARK_GRAY)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

    while True:
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # Sal del menú y comienza el juego


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

    main_menu(screen, background)
    LEVEL_TIME = 50_000  # 40 segundos en milisegundos
    level_start_time = pygame.time.get_ticks()  # Momento en que empezó el nivel
    pause_start_time = 0
    game_over = False

    cannon = Cannon(CANNON_POS)
    projectiles = []
    targets = []
    explosions = []  # For hit effects
    score = 0
    game_over = False
    game_won = False
    global level
    level = 1  # nivel inicial
    spawn_interval = SPAWN_INTERVAL
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT:
                targets.append(Target())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not paused:
                    projectiles.append(cannon.fire())
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SPAWN_EVENT, 0)  # Detener timer
                        pause_start_time = pygame.time.get_ticks()

                    else:
                        pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)  # Reactivar timer
                        pause_end_time = pygame.time.get_ticks()
                        time_paused = pause_end_time - pause_start_time

                        # Ajustamos el tiempo de inicio para que ignore el tiempo pausado
                        level_start_time += time_paused

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if not paused and not game_over:
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

                            if score >= 80:
                                game_over = True
                                game_won = True

            # Cambiar nivel al llegar a 20 puntos
            if score >= 20 and level == 1:
                level = 2
                level_start_time = pygame.time.get_ticks()
                # Cambiar intervalo de aparición para nivel 2 (más rápido)
                spawn_interval = 1000  # 1 segundo en lugar de 2
                pygame.time.set_timer(SPAWN_EVENT, spawn_interval)
                # Opcional: Aumentar velocidad de los objetivos
                TARGET_SPEED_RANGE = (4, 8)  # Velocidad mayor

            # Cambiar nivel al llegar a 20 puntos
            if score >= 40 and level == 2:
                level = 3
                level_start_time = pygame.time.get_ticks()

        # Clean up dead objects
        projectiles = [p for p in projectiles if p.alive]
        targets = [t for t in targets if t.alive or t.hit_effect > 0]

        if not game_over and not paused:
            elapsed = pygame.time.get_ticks() - level_start_time
            remaining_time = max(0, LEVEL_TIME - elapsed)

            if remaining_time == 0:
                game_over = True

        # Draw win
        if game_over and game_won:
            font = pygame.font.SysFont(None, 72)
            win_text = font.render("¡GANASTE! Puntaje: 60", True, YELLOW)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(win_text, win_rect)
            pygame.display.flip()
            # Pausa para que el usuario vea el mensaje antes de salir o reiniciar
            pygame.time.wait(5000)
            running = False

        # Draw everything
        screen.blit(background, (0, 0))

        # Draw game objects
        if not game_over and not paused:
            cannon.draw(screen)
            for p in projectiles:
                p.draw(screen)
            for t in targets:
                t.draw(screen)

        if paused:
            font = pygame.font.SysFont(None, 72)
            pause_text = font.render("PAUSA", True, RED)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_text, text_rect)

        # Draw UI
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surf, (10, 10))

        # Draw level
        font_level = pygame.font.SysFont(None, 36)
        level_surf = font_level.render(f"Nivel: {level}", True, BLACK)
        screen.blit(level_surf, (10, 40))

        # draw time
        # Mostrar tiempo restante (si no game over)
        font = pygame.font.SysFont(None, 30)
        if not game_over:
            time_text = font.render(f"Tiempo: {remaining_time // 1000}s", True, BLACK)
            screen.blit(time_text, (10, 70))

        # Draw instructions

        font_small = pygame.font.SysFont(None, 24)
        instructions = [
            "<- -> : Rotar cañón",
            "ESPACIO: Disparar"
        ]
        for i, instruction in enumerate(instructions):
            inst_surf = font_small.render(instruction, True, BLACK)
            screen.blit(inst_surf, (10, SCREEN_HEIGHT - 60 + i * 25))

        if game_over:
            # Fondo semi-transparente para destacar el mensaje
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # negro semi-transparente
            screen.blit(overlay, (0, 0))

            game_over_font = pygame.font.SysFont(None, 80)
            restart_font = pygame.font.SysFont(None, 40)

            game_over_text = game_over_font.render("GAME OVER", True, RED)
            restart_text = restart_font.render("Presiona R para volver a jugar", True, WHITE)

            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)

            # Detectar si presionan R para reiniciar
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reiniciar todo para volver a jugar
                score = 0
                level = 1
                projectiles.clear()
                targets.clear()
                level_start_time = pygame.time.get_ticks()
                game_over = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()