import pygame
import random
import math
from get_colors import get_color
 
class Player_vert(pygame.sprite.Sprite):
    """ This class represents the paddles on either side of the screen
        It derives from the "Sprite" class in Pygame """
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, x, y, joystick_no, color):
        # Call the parent class (Sprite) constructor
        # super().__init__()
        super(self.__class__, self).__init__()

        # Variables to hold the height and width of the block
        self.width = 10
        self.height = 75
        self.my_joystick = None
        self.color = color
 
        # Create an image of the ball, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
 
        # Set initial position of sprite
        self.rect.center = (x,y)
 
        # Count the joysticks the computer has
        joystick_count = pygame.joystick.get_count()
        if joystick_count < joystick_no+1:
            # No joysticks!
            print("Error, not enough joysticks. Found ", joystick_count)
        else:
            # Use joystick #0 and initialize it
            self.my_joystick = pygame.joystick.Joystick(joystick_no)
            self.my_joystick.init()
 
    def update(self):
        """ Update the player's position. """

        # As long as there is a joystick
        if self.my_joystick != None:

            # This gets the position of the axis on the game controller
            # It returns a number between -1.0 and +1.0
            vert_axis_pos = self.my_joystick.get_axis(1)
            
            # Move y according to the axis.
            # We multiply by 20 to speed up the movement.
            self.rect.y = self.rect.y+vert_axis_pos*20 
 
            # If the user moves past the top/bottom of the screen, set the
            # position to the edge.
            if self.rect.y < 0:
                self.rect.y = 0
            if self.rect.y > screen_height - self.height:
                self.rect.y = screen_height - self.height

class Player_hor(pygame.sprite.Sprite):
    """ This class represents the paddles on either side of the screen
        It derives from the "Sprite" class in Pygame """
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, x, y, joystick_no, color):
        # Call the parent class (Sprite) constructor
        # super().__init__()
        super(self.__class__, self).__init__()
 
        self.width = 75
        self.height = 10 ##75   
        self.my_joystick = None
        self.color = color
 
        # Create an image of the ball, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
 
        # Set initial position of sprite
        self.rect.center = (x,y)
 
        # Count the joysticks the computer has
        joystick_count = pygame.joystick.get_count()
        if joystick_count < joystick_no+1:
            # No joysticks!
            print("Error, not enough joysticks. Found ", joystick_count)
        else:
            # Use joystick #0 and initialize it
            self.my_joystick = pygame.joystick.Joystick(joystick_no)
            self.my_joystick.init()

    def update(self):
        """ Update the player's position. """

        # As long as there is a joystick
        if self.my_joystick != None:

            hor_axis_pos = self.my_joystick.get_axis(0)
            self.rect.x = self.rect.x+hor_axis_pos*20

            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x > screen_width - self.width:
                self.rect.x = screen_width - self.width
 
class Wall(pygame.sprite.Sprite):
    """ This class represents the wall at the top and bottom of the
        screen. """
 
    # Constructor function
    def __init__(self, x, y, width, height):
        # Call the parent's constructor
        # super().__init__()
        super(self.__class__, self).__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill((get_color("blue")))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
class Ball(pygame.sprite.Sprite):
    """ This class represents the ball that bounces around. """
 
    # Set speed vector
    change_x = 0
    change_y = 0
    walls = None
 
    # Constructor function
    def __init__(self, x, y, walls, color):
        # Call the parent's constructor
        # super().__init__()
        super(self.__class__, self).__init__()

        self.color = color
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) 
        self.walls = walls
 
    def update(self):
        """ Update the ball's position. """

        # Get the old position, in case we need to go back to it
        old_x = self.rect.x
        new_x = old_x + self.change_x
        self.rect.x = new_x
 
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, self.walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.x = old_x
            self.change_x *= -1
            self.image.fill(collide[0].color)
 
        old_y = self.rect.y
        new_y = old_y + self.change_y
        self.rect.y = new_y 
 
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, self.walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.y = old_y
            self.change_y *= -1
            self.image.fill(collide[0].color)
 
        if self.rect.x < -10 or self.rect.x > screen_width + 10:
            self.change_x = 0
            self.change_y = 0
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen_width = 500
screen_height = 500
 
screen = pygame.display.set_mode([screen_width, screen_height])
 
# Set the title of the window
pygame.display.set_caption('Johnsenfrs Pong Game')
 
# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
 
# Used for converting color maps and such
background = background.convert()
 
# Fill the screen with a black background
background.fill(get_color("black"))
 
# All sprite lists
wall_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
movingsprites = pygame.sprite.Group()
 
#Create the players
players = []
players_x = [20, screen_width-20, screen_width/2, screen_width/2]
players_y = [screen_height/2, screen_height/2, 20, screen_height -20]
players_color = [get_color("blue"), get_color("red"), get_color("pink"), get_color("green")]

for player in range(4):
    if player < 2:
        players.append(Player_vert(players_x[player], players_y[player], player, players_color[player]))
    else:
        players.append(Player_hor(players_x[player], players_y[player], player, players_color[player]))
         
    all_sprites.add(players[player])
    wall_list.add(players[player])
    movingsprites.add(players[player])

# Make the walls. (x_pos, y_pos, width, height)
# Top wall
#wall = Wall(0, 0, screen_width, 10)
#wall_list.add(wall)
#all_sprites.add(wall)
 
# Bottom wall
#wall = Wall(0, screen_height - 10, screen_width, screen_height)
#wall_list.add(wall)
#all_sprites.add(wall)
 
# Create the ball
ball = Ball(-50, -50, wall_list, get_color("white"))
movingsprites.add(ball)
all_sprites.add(ball)
 
clock = pygame.time.Clock()
 
# Game Menu loop
def game_menu():
    menu = True

    while menu:
        for event in pygame.event.get():
            print(event)

            largeText = pygame.font.Font('freesansbold.ttf',80)
            smallText = pygame.font.Font('freesansbold.ttf', 35)
            
            textHeading = largeText.render("Pong4Four", True, white)
            locationHeading = textHeading.get_rect()
            locationHeading.center = ((screen_width/2),(screen_height/4))

            textStart = smallText.render("Start Game", True, white)
            locationStart = textStart.get_rect()
            locationStart.center = ((screen_width/2),(2*screen_height/4))

            textSettings = smallText.render("Settings", True, white)
            locationSettings = textSettings.get_rect()
            locationSettings.center = ((screen_width/2),(2.75*screen_height/4))

            textQuit = smallText.render("Quit", True, white)
            locationQuit = textQuit.get_rect()
            locationQuit.center = ((screen_width/2),(3.5*screen_height/4))

            texts = [(textHeading, locationHeading), (textStart, locationStart), (textSettings, locationSettings), (textQuit, locationQuit)]

            screen.blits(texts)
            
            pygame.display.update()
            clock.tick(15)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False

# Main program loop
def game_loop():
    done = False

    while not done:

        ## Play music
        #pygame.mixer.music.load('foo.mp3')
        #pygame.mixer.music.play(0)
    
        # Loop through any window events
        for event in pygame.event.get():
            # The user clicked 'close' or hit Alt-F4
            if event.type == pygame.QUIT:
                done = True
    
            # The user clicked the mouse button
            # or pressed a key
            elif (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):## or player1.my_joystick.get_button(0) or player2.my_joystick.get_button(0) or player3.my_joystick.get_button(0) or player4.my_joystick.get_button(0): 
    
                # Is the ball not moving?
                if ball.change_y == 0:
    
                    # Start in the middle of the screen
                    ball.rect.x = screen_width / 2
                    ball.rect.y = screen_height / 2
                    ball.image.fill(white)
    
                    # Set a random vector
                    degree = random.randrange(0,360)
                    while degree == 0 or degree == 90 or degree == 180 or degree == 270 or degree == 360:
                        degree=random.randrange(0,360)
                    magnitude = 5 # determines the speed of the ball, may be subject to a random variable as well

                    ball.change_x = magnitude * math.cos(math.radians(degree))
                    ball.change_y = magnitude * math.sin(math.radians(degree))
            
                    #ball.change_y = random.randrange(-5, 6)
                    #ball.change_x = random.randrange(5, 10)
    
                    # Is the ball headed left or right? Select randomly
                    #if(random.randrange(2) == 0):
                        #ball.change_x *= -1
    
        # Update the ball position. Pass it the list of stuff it can bounce off of
        movingsprites.update()
    
        # Clear the screen
        screen.fill(black)
    
        # Draw the sprites
        all_sprites.draw(screen)
    
        # Display the screen
        pygame.display.flip()
    
        clock.tick(50)

game_menu()

game_loop()

pygame.quit() # All done, shut down Pygame