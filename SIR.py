import pygame
import random
import math
import time
import matplotlib.pyplot as plt

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
SQUARE_SIZE = 200
DOT_RADIUS = 3
DOT_COLOR = (0, 0, 0)
SQUARE_COLOR = (255, 255, 255)

SQUARE_POSITIONS = [
    (50, 50),
    (260, 260),
    (470, 60)
]

COLORS = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255)
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

    def travel(self, destination):
        self.pos = (random.randint(0, destination.size), random.randint(0, destination.size))
        self.current_square = destination.id

    def infect(self):
        if self.status == "I":
            for other in self.get_neighbors():
                if other.status == "S" and random.random() <= infection_rate:
                    other.status = "I"
                    other.infected_time = 0
                    other.color = COLORS[1]

    def remove_check(self):
        if self.status == "I" and self.infected_time > infection_time:
            self.status = "R"
            self.color = COLORS[2]

    # UPDATE THIS IT'S BAD
    def get_neighbors(self):
        neighbors = []
        for dir in DIRECTIONS:
            for other in cities[self.current_square].people:
                for i in range(3):
                    if other.pos == (self.pos[0] + dir[0] * i, self.pos[1] + dir[1] * i):
                        neighbors.append(other)
        return neighbors

class City:
    """Class representing a singular city, with its id, position on screen, population, array of Person and size in pixels"""
    def __init__(self, id, pos, pop, size):
        self.id = id
        self.pos = pos
        self.pop = pop
        self.people = []
        self.size = size
        self.representation = pygame.Rect(pos[0], pos[1], size, size)
    
    def populate(self, S0i):
        for _ in range(S0i):
            person_pos = (random.randint(0, self.size), random.randint(0, self.size))
            self.people.append(Person(person_pos, self.id))

def create_citites():
    for id, pos in enumerate(SQUARE_POSITIONS):
        cities.append(City(id, pos, S0[id], SQUARE_SIZE))
        cities[id].populate(S0[id])

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
            person.move_inside()
            if person.infected_time >= 0:
                person.infected_time += 1
            if person.status == "S":
                St[t] += 1
            elif person.status == "I":
                It[t] += 1
            else:
                Rt[t] += 1

def travel():
    for city in cities:
        people_to_move = int(city.pop * travel_rate)
        
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


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIR Model")

cities = []
S0 = [50, 283, 300]
I0 = [5, 5, 5]
travel_rate = 0.1
infection_rate = 1
infection_time = 15
days = 150
St, It, Rt = [0 for i in range(days)], [0 for i in range(days)], [0 for i in range(days)]
St[0] = sum(S0) - sum(I0)
It[0] = sum(I0)
Rt[0] = 0

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
while running < days:
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
