"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""

import arcade
import random
import math
from abc import abstractmethod
from abc import ABC

"""
- Global variables that'll be used through out the program
"""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_INTRO = 0
GAME_RUN = 1
GAME_DEATH = 2
GAME_WIN = 3

BULLET_RADIUS = 11
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_THRUST_AMOUNT = 3
SHIP_RADIUS = 18
SHIP_HEALTH = 15

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 23

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 15

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 9


# Create the Point class that will "__init__" the point object
# This will be used by the Ship, Bullet & Asteroids classes
class Point:

    def __init__(self):
        # this will be generating the center for the object.
        self.x = 0
        self.y = 0

    """
    - The object will pass  in random start number
    - This function will return the y point.
    """
    def generate_asteroid_x(self, start):
        # left side
        if start == 1:
            return 0
        # right side
        elif start == 2:
            return 800
        # bottom
        elif start == 3:
            return random.randint(50, 750)
        # top
        else:
            return random.randint(50, 750)
        
        
    """
    - The object will pass  in random start number
    - This function will return the y point.
    """
    def generate_asteroid_y(self, start):

        # left side
        if start == 1:
            return random.randint(50, 550)
        # right side
        elif start == 2:
            return random.randint(50, 550)
        # bottom
        elif start == 3:
            return 0
        # top
        else:
            return 600

"""
# Create the Velocity class that will "__init__" the point object
# This will be used by the Ship, Bullet & Asteroids classes
"""
class Velocity:

    def __init__(self):
        # this will create a velocity attribute for the object
        self.dx = 0
        self.dy = 0

"""
# flying object class which will utilize the Point & Velocity classes
"""
class flying_object:
    """
    This is a base class for all flying objects (bullets and ship and astroids)
    """

    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        # always start being alive
        self.alive = True
        self.height = 0
        self.width = 0
        # import ship texture
        self.texture = arcade.load_texture("images/playerShip1_orange.png")
        self.rotation = 0
        self.alpha = 255 
        self.radius = 0

    def draw(self):
        # display the figure
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.rotation, self.alpha)


    def check_offscreen(self):
        """
        Every flying object will wrap.
        meaning that if goes off the screen it will move to another side of the screen
        """
        if self.center.y > SCREEN_HEIGHT:
            # move it to the bottom
            self.center.y = 0

        if self.center.y < 0:
            # move it the top
            self.center.y = SCREEN_HEIGHT

        if self.center.x > SCREEN_WIDTH:
            # move it to the left
            self.center.x = 0

        if self.center.x < 0:
            # move it to the right
            self.center.x = SCREEN_WIDTH
    
    # change the position by adding velocity
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
  
"""
# Ship class which will utilize the flying object class
"""
class Ship(flying_object):

    def __init__(self):
        super().__init__()
        self.center.x = 400
        self.center.y = 300
        self.thrust = SHIP_THRUST_AMOUNT
        self.rotation = 0
        # import the ship texture
        self.texture1 = arcade.load_texture("images/playerShip1_orange.png")
        self.width = 40
        self.height = 35
        self.radius = SHIP_RADIUS
        self._health = SHIP_HEALTH

    def ignite_thrusters(self):
        self.velocity.dx += math.cos(math.radians(self.rotation + 90)) * self.thrust
        self.velocity.dy += math.sin(math.radians(self.rotation + 90)) * self.thrust

    def check_state(self, frame):
        # if health at 0 then kill it
        if self.health == 0:
            self.alive = False

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        if health < 0:
            self._health = 0
        else:
            self._health = health

"""
# The ship thruster class will be effective the Ship starts moving
"""
class Ship_Thrusters(Ship):

    def __init__(self):
        super().__init__()
        # Exact same ship, but with a different texture that has thrusters
        self.texture = arcade.load_texture("images/playerShip1_Thruster.png")


"""
# This class inherits from flying_object.
# This is the base class for all other asteroids.
"""
class Asteroid(flying_object, ABC):
    def __init__(self):
        super().__init__()
        # this decides which side of the screen to spawn at.
        self.start = random.randint(1, 4)

        # uses the function from point to find the x and y
        self.center.x = self.center.generate_asteroid_x(self.start)
        self.center.y = self.center.generate_asteroid_y(self.start)

        # uses angle object and its methods to find the direction it should go
        angle = Angle()
        self.direction = angle.generate_angle(self.start)

        # uses the direction to get the correct speed
        self.velocity.dx = math.cos(math.radians(self.direction)) * BIG_ROCK_SPEED
        self.velocity.dy = math.sin(math.radians(self.direction)) * BIG_ROCK_SPEED

        self.radius = BIG_ROCK_RADIUS

        # starts at 0, but this will increase as the astroids advance
        self.rotation = 0

        self.dr = 1

        self.texture = arcade.load_texture("images/meteorGrey_big1.png")
        self.width = 50
        self.height = 50

    def spin(self):
        self.rotation += self.dr

    @abstractmethod
    def split(self):
        # this will be implemented in the child classes
        pass

    @abstractmethod
    def hit_ship(self):
        # this will be implemented in the child classes
        pass

"""
# Big Asteroid class
"""
class BigAsteroid(Asteroid):

    def __init__(self):
        super().__init__()
        # takes two hits to kill
        self.health = 2
        self.dr = BIG_ROCK_SPIN

    def split(self):
        # takes one away from health
        self.health -= 1

        # checks if the astorid is dead
        if self.health == 0:
            # when the bullet hits the astroid, it will split and
            # produce two medium and 1 small astroid.
            # velocity is changed from the orginal astroid
            list = [MediumAsteroid(self.center.x, self.center.y, self.velocity.dx, self.velocity.dy + 2),
                    MediumAsteroid(self.center.x, self.center.y, self.velocity.dx, self.velocity.dy - 2),
                    SmallAsteroid(self.center.x, self.center.y, self.velocity.dx + 5, self.velocity.dy)]
            # kills it
            self.alive = False

        else:
            list = []

        # either returns the new astroids or an empty list
        return list

    def hit_ship(self):
        # does 8 damage to the ship
        return 6


"""
# Medium Asteroid class
"""
class MediumAsteroid(Asteroid):

    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.velocity.dx = dx
        self.velocity.dy = dy
        self.radius = MEDIUM_ROCK_RADIUS
        self.texture = arcade.load_texture("images/meteorGrey_med1.png")
        self.width = 35
        self.height = 35
        self.dr = MEDIUM_ROCK_SPIN

    def split(self):
        list = [SmallAsteroid(self.center.x, self.center.y, self.velocity.dx + 1.5, self.velocity.dy + 1.5),
                SmallAsteroid(self.center.x, self.center.y, self.velocity.dx - 1.5, self.velocity.dy - 1.5), ]
        
        # destroy it
        self.alive = False

        # returns a list of two small asteroids
        # when it is hit by a laser
        return list

    def hit_ship(self):
        # does 5 damage to the ship
        return 5

"""
# Small Asteroid class
"""
class SmallAsteroid(Asteroid):

    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.center.x = x
        self.center.y = y
        self.velocity.dx = dx
        self.velocity.dy = dy
        self.radius = SMALL_ROCK_RADIUS
        self.texture = arcade.load_texture("images/meteorGrey_small1.png")
        self.width = 22
        self.height = 22
        self.dr = SMALL_ROCK_SPIN

    def split(self):
        # asteroid is done splitting
        list = []

        # destroy it
        self.alive = False

        # returns an empty list
        return list

    def hit_ship(self):
        # does only damage of 2 to ship
        return 3
 
"""
# Angle class to determine angles of objects
"""
class Angle:

    def __init__(self):
        pass

    def generate_angle(self, start):
        """
        The object will pass  in random start number
        This number will decide which side of the screen the
        astroid will spawn at.
        This function will return an appropriate angle
        that the astroid should start will with.
        """

        # left side
        if start == 1:
            return random.randint(-30, 30)
        # right side
        elif start == 2:
            return random.randint(150, 210)
        # bottom
        elif start == 3:
            return random.randint(60, 120)
        # top
        else:
            return random.randint(240, 300)


"""
This is the bullet class, to be fired from the ship.
Inherited most attibutes and methods from flying_object
"""
class Bullet(flying_object):

    def __init__(self, angle, x, y, dx, dy):
        # angle: same angle as the ship's
        # x, y: same position as the ship's

        super().__init__()
        self.center.x = x
        self.center.y = y
        # receives angle (to be used for speed)
        self.rotation = angle
        self.ship_dx = dx
        self.ship_dy = dy
        # bullet speed
        self.velocity.dx = math.cos(math.radians(self.rotation)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(self.rotation)) * BULLET_SPEED
        # import the bullet picture
        self.texture = arcade.load_texture("images/laserBlue01.png")
        self.width = 25
        self.height = 6
        # used to keep track how long bullet has been alive
        self.time_alive = 0.0
        self.radius = BULLET_RADIUS

    def check_alive(self):
        # this function is called every frame it will add one.
        self.time_alive += 1

        # bullets will only last for the 60 frames.
        if self.time_alive > BULLET_LIFE:
            self.alive = False

    def hit_ship(self):
        # does 7 damage to the ship
        return 7


class Game(arcade.Window):
    """
    This class handles all  the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
       
        self.held_keys = set()

        # create a ship
        self.ship = Ship()

        # create a ship that has thrusters
        self.ship_thrusters = Ship_Thrusters()

        # this will be used to determine when to draw the ship with thrusters
        self.draw_thrust = 0

        # list for all asteroids
        self.asteroids = []

        # start at with 5 asteroids incoming
        self.create_asteroids()

        # list for all bullets
        self.bullets = []

        # keeps track of frame count
        self.frame = 0

        # keeps track of delta time
        self.remember_time = 0

        # the state of the game
        # starts with the game intro
        self.current_state = GAME_INTRO

    
        
    def frame_count(self):
        """
        This function counts the frames
        """
        self.frame += 1

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        
        #arcade.background = arcade.load_texture("images/Space_background.jpg")
        #self.background = arcade.load_texture("images/Space_background.jpg")
        # if self.draw_thrust has a value of 1 or more then draw the
        # ship with thrusters
        if self.draw_thrust > 0 and self.current_state != GAME_DEATH:
            self.ship_thrusters.draw()

        # draws ship
        # will stop drawing the ship when the player loses the game
        if self.current_state != GAME_DEATH:
            self.ship.draw()

            # draw each bullet in bullet list
            for bullet in self.bullets:
                bullet.draw()

        # calls function to draw health on screen
        self.draw_health()

        # draw the intro to the game
        if self.current_state == GAME_INTRO:
            self.draw_warning()

        # move the asteroids when the game is the running state
        # or when the player dies.
        if self.current_state == GAME_RUN or self.current_state == GAME_DEATH:
            # goes through the asteroid list and draws them
            for asteroid in self.asteroids:
                asteroid.draw()

        # if current state of the game is death
        # then display the death screen
        if self.current_state == GAME_DEATH:
            self.draw_end()

        # if the player wins
        # then display the win screen
        if self.current_state == GAME_WIN:
            self.draw_win()
    
    
    # UPDATE function
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.remember_time += delta_time

        # count the frame
        self.frame_count()

        # calls the check offscreen function
        # dont wrap when the game ends.
        # Acts as if the ship "left the screen"
        if self.current_state != GAME_WIN:
            self.check_offscreen()

        # advance the bullets
        for bullet in self.bullets:
            bullet.advance()

        # advance the ship
        self.ship.advance()

        # now advance the ship with thrusters
        self.ship_thrusters.advance()

        if self.draw_thrust > 0:
            # if we should be drawing the thrusters
            # then add 1 each time the update function is called
            self.draw_thrust += 1
            if self.draw_thrust == 10:
                # now if it goes to 10 then set it to zero
                # so it doesn't draw again untill the space is pressed.
                self.draw_thrust = 0

        # switches from intro state to run state after 4 seconds
        if self.remember_time > 4 and self.current_state != GAME_WIN:
            self.current_state = GAME_RUN

        # only advance the asteroids and create asteroids
        # if the state is in run mode
        if self.current_state == GAME_RUN:

            # advance the asteroids
            for asteroid in self.asteroids:
                asteroid.advance()
                asteroid.spin()

            # see if a new asteroid should be added
            self.create_asteroid()

        # check collisions
        self.check_collisions()

        # update the current state of the ship
        self.ship.check_state(self.frame)

        # finally we clean up any dead objects
        self.clean_up_objects()


    # Creates 5 asteroids and adds it to the list. Game Start
    def create_asteroids(self):
        for i in range(1, 6):
            self.asteroids.append(BigAsteroid())

    # Creates a new big asteroid
    def create_asteroid(self):
        if random.randint(1, 1200) == 1:
            self.asteroids.append(BigAsteroid())
    
    
    # goes through every object and calls their check wrap function
    def check_offscreen(self):
        for asteroid in self.asteroids:
            asteroid.check_offscreen()

        for bullet in self.bullets:
            bullet.check_offscreen()

        self.ship.check_offscreen()
        self.ship_thrusters.check_offscreen()
    
    # Checks the collisions of objects (ship, asteroids, bullets)
    def check_collisions(self):

        for bullet in self.bullets:
            for asteroid in self.asteroids:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if ((bullet.center.x - asteroid.center.x) ** 2 + (
                            bullet.center.y - asteroid.center.y) ** 2) ** .5 < too_close:
                        # its a hit!
                        bullet.alive = False
                        list = asteroid.split()
                        self.asteroids += list

        for asteroid in self.asteroids:
            # Make sure they are both alive before checking for a collision
            if self.ship.alive and asteroid.alive:
                too_close = self.ship.radius + asteroid.radius
                if ((self.ship.center.x - asteroid.center.x) ** 2 + (
                        self.ship.center.y - asteroid.center.y) ** 2) ** .5 < too_close:
                    # its a hit!
                    if self.frame > 40:
                        hit_points = asteroid.hit_ship()
                        self.ship.health -= hit_points
                        self.frame = 0

        for bullet in self.bullets:
            # Make sure they are both alive before checking for a collision
            if self.ship.alive and bullet.alive and bullet.time_alive > 30:
                too_close = self.ship.radius + bullet.radius
                if ((self.ship.center.x - bullet.center.x) ** 2 + (
                        self.ship.center.y - bullet.center.y) ** 2) ** .5 < too_close:
                    # its a hit!
                    bullet.alive = False

                    # if the ship has not been hit in the
                    # past 30 frames then it can be hit
                    # INVICIBILITY!
                    if self.frame > 30:
                        hit_points = bullet.hit_ship()
                        self.ship.health -= hit_points
                        self.frame = 0


    def clean_up_objects(self):
        
        # Goes through every object within the list and checks if they are dead and need to be removed
        # Also checks to see if the player had died or won.
        for bullet in self.bullets:
            # checks to see if the bullet have passed their
            # 60 frames limit
            bullet.check_alive()
            if bullet.alive == False:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if asteroid.alive == False:
                self.asteroids.remove(asteroid)

        if self.ship.alive == False:
            self.current_state = GAME_DEATH
        elif not self.asteroids:
            self.current_state = GAME_WIN
    
    
    # import thruster ship when the ship is in motion
    def on_key_press(self, key, key_modifiers):
        # ignite thrusters when space is pressed
        if key == arcade.key.SPACE:
            self.ship.ignite_thrusters()
            self.ship_thrusters.ignite_thrusters()

            # set draw_thrust to 1 so that the draw function is
            # given the okay to draw. It will be turned off after 10 frames
            self.draw_thrust = 1

        # if player has died or won the game and the mouse is pressed then call the restart function
        if key == arcade.key.RETURN and (self.current_state == GAME_DEATH or self.current_state == GAME_WIN):
            self.restart()
    
    # The motion of the Ship
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # tracks mouse motion
        # set the ship and bullet angle in degrees
        self.ship.rotation = self.get_angle_degrees(x, y)
        self.ship_thrusters.rotation = self.get_angle_degrees(x, y)
    
    
    # When mouse button is pressed, the ship will fire
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!

        # grabs the current angle between the ship and mouse
        angle = self.get_angle_degrees(x, y) + 90

        # creates a bullet object using information from the ship
        bullet = Bullet(angle, self.ship.center.x, self.ship.center.y, self.ship.velocity.dx, self.ship.velocity.dy)

        # adds it to the list
        self.bullets.append(bullet)
    
    
    # Ship and Bullet degree angles
    def get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        """
        # get the angle in radians
        angle_radians = math.atan2(y - self.ship.center.y, x - self.ship.center.x)

        # convert to degrees
        # converted to degrees because the ship and bullet class needs degrees
        angle_degrees = math.degrees(angle_radians) - 90

        return angle_degrees
    
    
    # Restart the game function
    def restart(self):
        # clear asteroids
        self.asteroids.clear()

        # create a new ship
        self.ship = Ship()

        # create a new ship that has thrusters
        self.ship_thrusters = Ship_Thrusters()

        # reset to 0
        self.draw_thrust = 0

        # start at with 5 asteroids incoming
        self.create_asteroids()

        # clear list
        self.bullets.clear()

        # restart frame count
        self.frame = 0

        # restart time
        self.remember_time = 0

        # goes back to the game intro
        self.current_state = GAME_INTRO
    
    # Ship Heath status
    def draw_health(self):
        arcade.draw_rectangle_filled(400, 590, self.ship.health * 10, 10, arcade.color.FIREBRICK)
        arcade.draw_rectangle_outline(400, 590, 150, 10, arcade.color.WHITE)
        arcade.draw_text("Health Bar:", start_x=215, start_y=SCREEN_HEIGHT - 15, font_size=12,
                         color=arcade.color.WHITE)
    
    
    # Warning message at the start of the game
    def draw_warning(self):
        """
        draws the warning screen
        """
        output2 = "WARNING!"
        output3 = "Asteroids Incoming"
        output0 = "PROTECT YOUR SHIP!"

        arcade.draw_text(output2, 240, 450, arcade.color.FIREBRICK, 54)
        arcade.draw_text(output3, 160, 350, arcade.color.FIREBRICK, 40)
        arcade.draw_text(output0, 160, 250, arcade.color.ORANGE, 40)
    
    # Display message when the player dies
    def draw_end(self):
        """
        draws the death screen
        """
        output4 = "ERROR!"
        output5 = "SYSTEM FAILURE"
        output6 = "You Ship got distroyed"
        output10 = "Want To Again?\nPress Enter"

        arcade.draw_text(output4, 320, 400, arcade.color.FIREBRICK, 40)
        arcade.draw_text(output5, 310, 300, arcade.color.FIREBRICK, 20)
        arcade.draw_text(output6, 350, 200, arcade.color.FIREBRICK, 20)
        arcade.draw_text(output10, 340, 100, arcade.color.WHITE, 20)

    def draw_win(self):
        """
        draws the winning screen
        """
        output7 = "ASTEROIDS CLEARED!"
        output8 = "YOU PROTECTED YOUR SHIP!"
        output9 = "Want To Again?\nPress Enter"

        arcade.draw_text(output7, 180, 400, arcade.color.GREEN, 40)
        arcade.draw_text(output8, 175, 300, arcade.color.GREEN, 30)
        arcade.draw_text(output9, 340, 100, arcade.color.WHITE, 20)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()











