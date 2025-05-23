# import the pygame module, so you can use it
import pygame

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
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load image (it is in same directory)
    image = pygame.image.load("Python/img/01_image.png")
    # set the colorkey, so the pink border is not visible anymore
    image.set_colorkey((255, 0, 255))
    # set the alpha value to 128 (0 fully transparent, 255 opaque)
    image.set_alpha(128)
    bgd_image = pygame.image.load("Python/img/background.png")

    # define the position of the smlly
    xpos = 50
    ypos = 50
    # how many pixels we move our smlly each frame
    step_x = 10
    step_y = 10

    # a clock for controlling the fps later
    clock = pygame.time.Clock()

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # check if the smlly is still on screen, if not change direction
        if xpos > screen_width - 64 or xpos < 0:
            step_x = -step_x
        if ypos > screen_height - 64 or ypos < 0:
            step_y = -step_y
        
        # update the position of the smlly
        xpos += step_x  # move it to the right
        ypos += step_y  # move it down

        # first erase the screen (just blit the background over anything on screen)
        screen.blit(bgd_image, (0, 0))
        # now blit the smlly on screen
        screen.blit(image, (xpos, ypos))
        # and update the screen (don't forget that!)
        pygame.display.flip()

        # this will slow it down to 10 fps, so you can watch it,
        # otherwise it would run too fast
        clock.tick(16)

# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    main()