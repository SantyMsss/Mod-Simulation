import pygame
import random
import queue

pygame.init()

# Colores
yellow = (255, 255, 102)
black  = (0,   0,   0)
green  = (0, 255,   0)
blue   = (50, 153, 213)
pink   = (255,   0,   255)

# Dimensiones y velocidad
dis_width   = 800
dis_height  = 600
block_size  = 20
snakespeed  = 8

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake con Balón')

# Carga de imágenes
snake_image = pygame.image.load("img/escbarca.png")
snake_image = pygame.transform.scale(snake_image, (block_size, block_size))
snake_image.set_colorkey(pink)

background_image = pygame.image.load("img/cancha.jpg")
background_image = pygame.transform.scale(background_image, (dis_width, dis_height))

# Imagen del balón como comida
ball_image = pygame.image.load("img/balonfut.jpg")
ball_image = pygame.transform.scale(ball_image, (block_size, block_size))
ball_image.set_colorkey(pink)

# Mapa de direcciones
compass = {
    "up":    (0, -block_size),
    "down":  (0,  block_size),
    "left":  (-block_size, 0),
    "right": ( block_size, 0)
}

clock      = pygame.time.Clock()
Q          = queue.Queue()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render(f"Score: {score}", True, yellow)
    dis.blit(value, [0, 0])

def our_snake(snake_list):
    for x in snake_list:
        dis.blit(snake_image, (x[0], x[1]))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over  = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List       = []
    Length_of_snake  = 1
    direction        = "right"

    foodx = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, dis_height - block_size) / block_size) * block_size

    while not game_over:

        while game_close:
            dis.blit(background_image, (0, 0))
            message("Perdiste! C=continuar  Q=salir", yellow)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over  = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over  = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Q.put("left")
                elif event.key == pygame.K_RIGHT:
                    Q.put("right")
                elif event.key == pygame.K_UP:
                    Q.put("up")
                elif event.key == pygame.K_DOWN:
                    Q.put("down")

        if not Q.empty():
            move = Q.get()
            if (move == "left"  and direction != "right") or \
               (move == "right" and direction != "left")  or \
               (move == "up"    and direction != "down")  or \
               (move == "down"  and direction != "up"):
                direction = move
                x1_change, y1_change = compass[direction]

        x1 += x1_change
        y1 += y1_change

        if x1 < 0 or x1 >= dis_width or y1 < 0 or y1 >= dis_height:
            game_close = True

        dis.blit(background_image, (0, 0))
        dis.blit(ball_image, (foodx, foody))

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        our_snake(snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, dis_height - block_size) / block_size) * block_size
            Length_of_snake += 1

        clock.tick(snakespeed)

    pygame.quit()
    quit()

gameLoop()
