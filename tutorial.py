import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    
    AU = 149.6e6 * 1000 # Distance from earth to the sun in metres
    G = 6.67428e-11 #Gravitational constant
    SCALE = 250/ AU # 1AU = 250 pixels
    TIMESTEP = 3600*24 # 3600secs in an hour, 24hr in a day, 1 day at a time update. This is going to be delta t.
    #Interesting to note that this delta t should not be too large, else the simulation orbit wont even look like an elipse with a smooth curve. 
    #But too small a delta t will make the planets in the simulation move too slowly (despite it being a more accurate orbit) . 


    def __init__(self, x, y, radius, color, mass):
        self.x = x #SI units metres
        self.y = y #SI units metres
        self.radius = radius #SI units metres
        self.color = color
        self.mass = mass #SI units kg
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0 #SI units metres
        self.x_vel = 0 #SI units metres per second
        self.y_vel = 0 #SI units metres per second

    def draw(self, win): 
        x = self.x * self.SCALE + WIDTH / 2 
        y = self.y * self.SCALE + HEIGHT / 2
        #scale the metres down to the coordinate system of the window. + width/height /2 is so that the center of the window can be taken as (0,0) in our defined coord system.
        #originally (0,0) is at the top left of the window


        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2) #draws a bunch of lines 2 pixels thick between the points and doesnt enclose them because i put False    
        
        


        pygame.draw.circle(win, self.color, (x,y), self.radius)  #this circle is of course representing the planet in the window

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km", 1, WHITE) #Use font object to create a text object
            # win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
            win.blit(distance_text, (x - distance_text.get_width()/2, y + distance_text.get_height()/2))
            # just placement of textbox. originally is top left corner at the center of circle then extend down and right.


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2) #simple pythagorean theorem to find distance btw (x1,y1) and (x2,y2)
        
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / (distance**2) #Gravitational force = GMm / r^2 
        theta = math.atan2(distance_y, distance_x) #get angle to resolve the forces. tan inverse or arctan. sign of this theta matters!
        force_x = math.cos(theta) * force #horizontal component of Gravitational force
        force_y = math.sin(theta) * force #vertical component of Gravitational force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            # dont wanna calculate Gravitational force the planet exerts on itself
            if self == planet:
                continue
                

            fx, fy = self.attraction(planet) # get horizontal and vertical compenents of G force on self due to said planet in the list of planets
            total_fx += fx #add it to current vector sum of horizontal forces
            total_fy += fy #add it to current vector sum of vertical forces
        
        # F=ma, a=F/m. a= delta v/ delta t, delta v = a* delta t (timestep)
                     #(F        / m        ) * delta t
        self.x_vel += (total_fx / self.mass) * self.TIMESTEP #updated vector sum of the horizontal component of velocity
        self.y_vel += (total_fy / self.mass) * self.TIMESTEP #updated vector sum of the vertical component of velocity

        # v= delta s/ delta t, delta s = v * delta t
                 #v          * delta t
        self.x += self.x_vel * self.TIMESTEP #updated vector sum of the horizontal component of displacement
        self.y += self.y_vel * self.TIMESTEP #updated vector sum of the vertical component of displacement
        self.orbit.append((self.x, self.y)) #add the coord into the orbit list. this coord is in REAL metres.


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0,0,30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742 * 10**24) #new Instance of a Planet class
    earth.y_vel = 29.783 * 1000 # metres per second
    #all planets need this initial vertical velocity for it to move in an orbit (circular motion, kinda)
    #if not it will accelerate to the sun and past it, probably to infinity. 
    #To infinity??? but but conservation of energy
    #yeah, this simulation isnt perfect. rmb that the velocities and displacement are calculated in intervals. they do not vary continuously like proper calculus


    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]


    # event loop
    while run:
        
        clock.tick(60) # max 60 times per second. computer literally running this while loop 60 times per second
        WIN.fill((0,0,0)) #gonna fill whole background with black at the start of each display

        # How to fill screen with white
        # WIN.fill(WHITE)
        # pygame.display.update()

        # so that when you press x the simulation will stop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets) #all planets to their updated position
            planet.draw(WIN) #draw it all out
        pygame.display.update() 

    pygame.quit


main()