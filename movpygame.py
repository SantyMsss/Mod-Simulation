# ------------------------- actual code ------------------------------

# import the pygame module, so you can use it
import pygame
import numpy as np

# color values
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)
pink = (255, 0, 255)  # Fixed from original (was 255_0_255)

# basado en https://dr@id.bithucket.io/legacy/pygame_tutorial01.html

# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    
    # load and set the logo
    logo = pygame.image.load("Python/img/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("movement")
    
    # create a surface on screen that has the size of 240 x 180
    screen_width = 240
    screen_height = 180
    screen = pygame.display.set_mode((screen_width, screen_height))  # Fixed from original
    
    # load image (it is in same directory)
    image = pygame.image.load("Python/img/01_image.png")
    # set color key to pink, pink border is not visible anymore
    image.set_colorkey(pink)
    
    # background image
    bgd_image = pygame.image.load("Python/img/background.png")

    # blit image to screen
    screen.blit(bgd_image, (0, 0))  # first background
    # screen.fill(red)
    # screen.fill(blue)
    
    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()
    
    # define the position of the smily
    xpos = 50  # Fixed from original (was XP03)
    ypos = 50  # Fixed from original (was XP03)
    
    # how many pixels we move our smily each frame
    step_x = 10  # Fixed from original (was step.x)
    step_y = 10
    
    # and blit it on screen
    screen.blit(image, (xpos, ypos))
    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()
    
    # define a variable to control the main loop
    running = True
    
    # main Loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.KEYDOWN:
                screen.blit(bgd_image, (0, 0))
                if event.key == pygame.K_UP:
                    ypos -= step_y  # Fixed from original (was step_-y_#)
                if event.key == pygame.K_DOWN:
                    ypos += step_y  # Fixed from original (was step_-y_#)
                if event.key == pygame.K_LEFT:
                    xpos -= step_x  # Fixed from original (was step_-x)
                if event.key == pygame.K_RIGHT:
                    xpos += step_x  # Fixed from original (was step_-x)
            
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        # check smily position
        if xpos > screen_width - 64:
            xpos = 0  # Fixed from original (was XPOS)
        if xpos < 0:
            xpos = screen_width - 64  # Fixed from original (was XPOS)
        if ypos > screen_height - 64:
            ypos = 0  # Fixed from original (was YPOS)
        if ypos < 0:
            ypos = screen_height - 64  # Fixed from original (was YPOS)
        
        # now blit the smily on screen
        screen.blit(image, (xpos, ypos))
        # and update the screen (don't forget that!)
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()