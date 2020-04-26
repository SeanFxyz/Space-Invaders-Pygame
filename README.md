Space-Invaders-Pygame
=====================

This is a fork of the pygame example game attreyabhatt/Space-Invaders-Pygame
With a lot of alterations made to the design in an attempt to make it 
more extensible.

Design changes from the original game:

The GameObject class and subclasses:
------------------------------------

Player, Enemy, and Bullet are now implemented as subclasses of a
GameObject class. GameObjects can be added to the game by adding them to
the global game_objects list, while their behaviors are defined by their
own update() and on_collision() methods. Every GameObject has at least the
following attributes:

Properties:

enabled -- boolean that represents if the object should be updated

deleted -- boolean that represents if the object is to be deleted. If
true, the object will be removed from the global game_objects list.

x -- The object's x coordinate

y -- The object's y coordinate

sprite -- The object's sprite as a pygame Surface object

tags -- A list of strings (or whatever else you'd want to use) to
identify the object.

is_event_handler -- Indicates whether the pygame event list should be
passed as a parameter to the objects update() method.

Methods:

update(self, delta)
update(self, delta, events) -- During the game loop, all enabled
GameObjects in the game_objects list will have this method called. delta
should be the time that has passed since the last rendered frame, and
events, if the object is marked as an event handler by its
is_event_handler property, should be the current pygame event queue.

on_collision(self, collider) -- In the game loop, any object that is
detected to be colliding with another object will have this method
called. collider will be the object with which this GameObject is
colliding.

Collision checking
------------------

Every GameObject has its own hitbox described by a pygame.Rect object.
Each GameObject is responsible for moving and adjusting its own hitbox
in accordance with any of its movements or changes in size.

Input and movement
------------------
Although keyboard input is still acquired using pygame KEYDOWN and
KEYUP events, those events are now translated into key states by the
player object, which allowed for more reliable movement control to be
implemented. Each time the player computes its movement, it resets its
velocity to 0, then adds 1 if the right arrow key is pressed and subtracts
1 if the left arrow key is pressed, then sets its x value accordingly.

Velocity for Player and Enemy objects is actually implemented using 2D
vector objects from the pygame.math.Vector2() class, so changes to the
gameplay involving vertical/diagonal movement should be quite easy from
here.
