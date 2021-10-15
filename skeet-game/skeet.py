"""
This program implements an awesome version of skeet.
It uses the python arcade library.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15

"""
Create Target() class along with its sub-classes (Point, Velocity, Bullet)
"""

class Point:
    # Initialize variables
    def __init__(self, co_x, co_y):
    
        self.x = co_x
        self.y = co_y

class Velocity:
    # Initialize variables
    def __init__(self, co_dx, co_dy):
        
        self.dx = co_dx
        self.dy = co_dy

"""
The flying object class will be used to create different objects in the game
"""
class flying_object:
    
    # Initialize flying objects that utilizes classes (Point and Velocity)
    def __init__(self):
        self.center = Point(0,0) 
        self.velocity = Velocity(0,0)
        
        
""" Bullet class and its functions """
class Bullet(flying_object):
    
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.alive = True
        
        # Initialize new bullet starting point to (20, 20)
        self.center.x = 20
        self.center.y = 20
        
        
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    
    def draw(self):
        
        # Draw Circle filled ball for shooting
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, BULLET_COLOR)
    
    # Check if bullet is in screen
    # return boolean to caller
    def is_off_screen(self, SWidth, SHeight):
        # Initalize boolean variable
        is_bullet_in_range = False
        if (self.center.x < SWidth) and (self.center.y < SHeight):
            is_bullet_in_range = False
        else:
            is_bullet_in_range = True
        return is_bullet_in_range
        
    # firing angle
    def fire(self, angle: float):
        
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        
class Target(flying_object):
    def __init__(self):
        super().__init__()
        self.radius = TARGET_RADIUS
        # Target bool
        self.alive = True
        # Initialize target type
        self.target_type = -1
        # Initialize target lifes
        self.impact = 1

             
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
     
     # draw target
    def draw(self):
        text_x = self.center.x - (self.radius * 1.2)
        text_y = self.center.y - (self.radius / 500)
        safe_square_length = TARGET_SAFE_RADIUS * 2
        
        if self.target_type == 0:
            
            arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_COLOR)
            
        elif self.target_type == 1:
            
            arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, TARGET_COLOR)
            
            arcade.draw_text(repr(self.impact), text_x, text_y, TARGET_COLOR, font_size = 15)
            
        elif self.target_type == 2:
            
            arcade.draw_rectangle_filled(self.center.x, self.center.y, safe_square_length, safe_square_length, TARGET_SAFE_COLOR)
        
        else:
            print("Target Error")
        
    def is_off_screen(self, SWidth, SHeight):
        # Initalize bool variable
        is_target_in_range = False
        
        if (self.center.x < SWidth) and (self.center.y < SHeight):
            is_target_in_range = False
            
        else:
            is_target_in_range = True
            
        return is_target_in_range
    
    def hit(self):
        # Standard Target
        if self.target_type == 0:  
            self.alive = False
            return 1
                    
        # Strong Target
        elif self.target_type == 1:
            if self.impact == 1:
                self.alive = False
                return 5
            else:
                self.impact -= 1
                return 1
        
        # Safe Target
        elif self.target_type == 2:
            self.alive = False
            return -10
             
        else:
            print("Target Deduction Error")

class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point(25, 25)
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, 360-self.angle)

   
    
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        target = Target()
        target.center.x = random.uniform(10, SCREEN_WIDTH / 2)
        target.center.y = random.uniform(SCREEN_HEIGHT / 2, SCREEN_HEIGHT) 
        random_target = random.randint(0, 2) # Random target chooser
        
        # Standard Target
        if random_target == 0:
            target.target_type = 0
            target.velocity.dx = random.randint(1, 5)
            target.velocity.dy = random.randint(-2, 5)
            
        # Strong Target
        elif random_target == 1:
            # Give strong target 3 lifes
            target.impact = 3
            target.target_type = 1
            target.velocity.dx = random.randint(1, 3)
            target.velocity.dy = random.randint(-2, 3)
            
        # Safe Target
        elif random_target == 2:
            target.target_type = 2
            target.velocity.dx = random.randint(1, 5)
            target.velocity.dy = random.randint(-2, 5)
            
        self.targets.append(target)
        
    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.

        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
