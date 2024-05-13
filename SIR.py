import pygame
import random
import matplotlib.pyplot as plt

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = (0, 0, 0)
SQUARE_SIZE = 300
DOT_RADIUS = 1
DOT_COLOR = (0, 0, 0)
SQUARE_COLOR = (255, 255, 255)
NEIGHBOURHOOD_SIZE = 2

# -------------------SIMULATION PARAMETERS------------------
"""
WOLNA CHOROBA
---------------
TRAVEL_RATE = 0.1
INFECTION_RATE = 0.2
INFECTION_TIME = 7
S0 = [1500, 1500, 1500, 4000, 1500]
I0 = [0, 0, 0, 1, 0]
DAYS = 200
"""

"""
SREDNIA CHOROBA
---------------
TRAVEL_RATE = 0.1
INFECTION_RATE = 0.7
INFECTION_TIME = 4
S0 = [1500, 1500, 1500, 4000, 1500]
I0 = [0, 0, 0, 1, 0]
DAYS = 50
"""

"""
BARDZO SZYBKA CHOROBA
---------------
TRAVEL_RATE = 0.1
INFECTION_RATE = 1
INFECTION_TIME = 7
S0 = [1500, 1500, 1500, 4000, 1500]
I0 = [0, 0, 0, 1, 0]
DAYS = 50
"""

TRAVEL_RATE = 0.1
INFECTION_RATE = 1
INFECTION_TIME = 7
S0 = [1500, 1500, 1500, 4000, 1500]
I0 = [0, 0, 0, 1, 0]
DAYS = 50

# ----------------------------------------------------------

St, It, Rt = [0 for _ in range(DAYS)], [0 for _ in range(DAYS)], [0 for _ in range(DAYS)]
St[0] = sum(S0) - sum(I0)
It[0] = sum(I0)
Rt[0] = 0

SQUARE_POSITIONS = [
    (50, 50),
    (350, 350),
    (650, 650),
    (50, 650),
    (650, 50)
]

COLORS = [
    (0, 255, 0), # S
    (255, 0, 0), # I
    (0, 0, 255)  # R
]

DIRECTIONS = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1)
]

# ----------------------------------------------------------

class Person:
    """Class representing a singular person"""
    def __init__(self, pos, current_square):
        self.pos = pos
        self.current_square = current_square
        self.status = "S"
        self.color = COLORS[0]
        self.infected_time = -1

    def move_inside(self):
        distance = random.randint(10, 50)
        direction = random.choice([DIRECTIONS[i] for i in range(8) 
                                   if (self.pos[0] + DIRECTIONS[i][0] * distance < SQUARE_SIZE and self.pos[1] + DIRECTIONS[i][1] * distance < SQUARE_SIZE 
                                       and self.pos[0] + DIRECTIONS[i][0] * distance > 0 and self.pos[1] + DIRECTIONS[i][1] * distance > 0)])
        new_x = self.pos[0] + direction[0] * distance
        new_y = self.pos[1] + direction[1] * distance
        self.pos = (new_x, new_y)

    def move_inside_new(self):
        distance = random.randint(10, 50)
        direction = random.choice([DIRECTIONS[i] for i in range(8) 
                                   if (self.pos[0] + DIRECTIONS[i][0] * distance < SQUARE_SIZE and self.pos[1] + DIRECTIONS[i][1] * distance < SQUARE_SIZE 
                                       and self.pos[0] + DIRECTIONS[i][0] * distance > 0 and self.pos[1] + DIRECTIONS[i][1] * distance > 0)])
        new_x = self.pos[0] + direction[0] * distance
        new_y = self.pos[1] + direction[1] * distance
        cities[self.current_square].map[self.pos].remove(self)
        self.pos = (new_x, new_y)
        cities[self.current_square].map[self.pos].append(self)

    def travel(self, destination):
        cities[self.current_square].map[self.pos].remove(self)
        self.pos = (random.randint(0, destination.size), random.randint(0, destination.size))
        self.current_square = destination.id
        cities[self.current_square].map[self.pos].append(self)

    def infect(self):
        if self.status == "I":
            for other in self.get_neighbors():
                if other.status == "S" and random.random() <= INFECTION_RATE:
                    other.status = "I"
                    other.infected_time = 0
                    other.color = COLORS[1]

    def remove_check(self):
        if self.status == "I" and self.infected_time > INFECTION_TIME:
            self.status = "R"
            self.color = COLORS[2]

    def get_neighbors(self):
        neighbors = []
        neigh_cells = [(x, y) for x in range(self.pos[0] - NEIGHBOURHOOD_SIZE, self.pos[0] + NEIGHBOURHOOD_SIZE + 1) 
                       for y in range(self.pos[1] - NEIGHBOURHOOD_SIZE, self.pos[1] + NEIGHBOURHOOD_SIZE + 1) 
                       if x <= cities[self.current_square].size and x >= 0
                       and y <= cities[self.current_square].size and y >= 0]
        for cell in neigh_cells:
            if cities[self.current_square].map[cell] != []:
                neighbors.extend(cities[self.current_square].map[cell])
                
        return neighbors

class City:
    """Class representing a singular city, with its id, position on screen, population, array of Person and size in pixels"""
    def __init__(self, id, pos, pop, size):
        self.id = id
        self.pos = pos
        self.pop = pop
        self.size = size
        self.representation = pygame.Rect(pos[0], pos[1], size, size)
        self.map = self.create_map()
        self.people = []
    
    def calc_people(self):
        ppl = [val for val in self.map.values() if val != []]
        self.people = flatten(ppl)

    def create_map(self):
        city_map = {}
        for x in range(self.size+1):
            for y in range(self.size+1):
                city_map[(x, y)] = []
        return city_map

    def populate(self, S0i):
        for _ in range(S0i):
            person_pos = (random.randint(0, self.size), random.randint(0, self.size))
            self.map[person_pos].append(Person(person_pos, self.id))

def create_citites():
    for id, pos in enumerate(SQUARE_POSITIONS):
        cities.append(City(id, pos, S0[id], SQUARE_SIZE))
        cities[id].populate(S0[id])
        cities[id].calc_people()

def draw_cities(screen):
    screen.fill(BACKGROUND_COLOR)
    for city in cities:
        pygame.draw.rect(screen, SQUARE_COLOR, city.representation)

def draw_people(screen):
    for city in cities:
        for person in city.people:
            pygame.draw.circle(screen, person.color, (city.pos[0] + person.pos[0], city.pos[1] + person.pos[1]), DOT_RADIUS)

def update_people(t):
    travel()
    for city in cities:
        for person in city.people:
            person.infect()
            person.remove_check()
            person.move_inside_new()
            if person.infected_time >= 0:
                person.infected_time += 1
            if person.status == "S":
                St[t] += 1
            elif person.status == "I":
                It[t] += 1
            else:
                Rt[t] += 1
        city.calc_people()

def travel():
    for city in cities:
        people_to_move = int(city.pop * TRAVEL_RATE)
        
        # CHANGE THIS LATER IT'S BAD
        for _ in range(people_to_move):
            person = random.choice(city.people)
            destination = random.choice([c for c in cities if c != city])
            person.travel(destination)
            replacement = random.choice(destination.people)
            replacement.travel(city)
            city.people.remove(person)
            destination.people.remove(replacement)
            destination.people.append(person)
            city.people.append(replacement)

def flatten(xss):
    return [x for xs in xss for x in xs]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIR Model")
cities = []
create_citites()
for i, I0i in enumerate(I0):
    if I0i > 0:
        inf = random.sample(cities[i].people, I0i)
        for person in inf:
            person.status = "I"
            person.infected_time = 0
            person.color = COLORS[1]

draw_cities(screen)
draw_people(screen)
pygame.display.flip()

fig, axes = plt.subplots()

running = 1
while running < DAYS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_people(running)
    draw_cities(screen)
    draw_people(screen)
    pygame.display.flip()
    plt.pause(0.1)
    running += 1
    
    axes.set_ylim(bottom=0, top=sum(S0))
    axes.plot([i for i in range(running)], St[:running], c='g')
    axes.plot([i for i in range(running)], It[:running], c='r')
    axes.plot([i for i in range(running)], Rt[:running], c='b')
    axes.legend()
    plt.draw()

plt.savefig("wykres.png")