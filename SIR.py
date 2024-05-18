import pygame
import random
import matplotlib.pyplot as plt
import io
from math import sqrt, exp
import csv

def run(AVG_POP, AVG_SIZE, MAX_PATIENTS_ZERO, NEIGHBOURHOOD_SIZE, N_CITIES, TRAVEL_RATE, INFECTION_RATE, INFECTION_TIME, DAYS):
    pygame.init()

    SCREEN_WIDTH = 1800
    SCREEN_HEIGHT = 1000
    BACKGROUND_COLOR = (0, 0, 0)
    DOT_RADIUS = 1
    ZOOM_RATIO = 1.2


    # ________________________________________________________________________

    S0 = [random.randint(AVG_POP - AVG_POP//2, AVG_POP + AVG_POP//2) for _ in range(N_CITIES)]
    I0 = [random.randint(0, MAX_PATIENTS_ZERO) for _ in range(N_CITIES)]
    TOTAL_POP = sum(S0) + sum(I0)
    SQUARE_SIZES = [random.randint(AVG_SIZE - AVG_SIZE//2, AVG_SIZE + AVG_SIZE//2) for _ in range(N_CITIES)]

    # ________________________________________________________________________


    St, It, Rt = [0 for _ in range(DAYS)], [0 for _ in range(DAYS)], [0 for _ in range(DAYS)]
    St[0] = sum(S0)
    It[0] = sum(I0)
    Rt[0] = 0

    def save_stats():
        with open('stats.csv', 'w', newline='') as csvfile:
            fieldnames = ['Day', 'S', 'I', 'R']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for day in range(DAYS):
                writer.writerow({'Day': day, 'Susceptible': St[day], 'Infected': It[day], 'Recovered': Rt[day]})
    
    def generate_square_positions(sizes, start_pos=(50, 50), margin=50):
        positions = []
        current_x, current_y = start_pos
        max_row_height = 0

        for size in sizes:
            if current_x + size > 1.2 * AVG_SIZE * (sqrt(N_CITIES) + 1):
                current_x = start_pos[0]
                current_y += max_row_height + margin
                max_row_height = 0

            positions.append((current_x, current_y))
            current_x += size + margin
            max_row_height = max(max_row_height, size)

        return positions


    def calculate_zoom_level():
        max_extent = 0
        for pos, size in zip(SQUARE_POSITIONS, SQUARE_SIZES):
            extent_x = pos[0] + size
            extent_y = pos[1] + size
            max_extent = max(max_extent, extent_x, extent_y)
        zoom_level = 950 / max_extent
        return zoom_level


    def generate_adjacency_list(positions, sizes, margin=50):
        def is_adjacent(pos1, size1, pos2, size2):
            horizontal_adj = (pos1[0] + size1 + margin >= pos2[0] and pos1[0] <= pos2[0] + size2 + margin)
            vertical_adj = (pos1[1] + size1 + margin >= pos2[1] and pos1[1] <= pos2[1] + size2 + margin)
            return horizontal_adj and vertical_adj

        adjacency_list = [[] for _ in range(len(positions))]

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if is_adjacent(positions[i], sizes[i], positions[j], sizes[j]):
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)

        return adjacency_list

    COLORS = [
        (0, 255, 0),  # S
        (255, 0, 0),  # I
        (0, 0, 255)   # R
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

    SQUARE_POSITIONS = generate_square_positions(SQUARE_SIZES)
    ZOOM_LEVEL = calculate_zoom_level()
    CONNECTIONS_GRAPH = generate_adjacency_list(SQUARE_POSITIONS, SQUARE_SIZES)

    class Person:
        """Class representing a singular person"""

        def __init__(self, pos, current_square):
            self.pos = pos
            self.current_square = current_square
            self.status = "S"
            self.color = COLORS[0]
            self.infected_time = -1
            self.has_travelled = False

        def move_inside_new(self):
            distance = random.randint(10, 25)
            direction = random.choice([DIRECTIONS[i] for i in range(8)
                                    if (self.pos[0] + DIRECTIONS[i][0] * distance < SQUARE_SIZES[self.current_square] and self.pos[1] + DIRECTIONS[i][1] * distance < SQUARE_SIZES[self.current_square]
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
            self.has_travelled = True

        def infect(self):
            if self.status == "I":
                for other in self.get_neighbors():
                    if other.status == "S":
                        distance = sqrt((self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2)
                        infection_prob = exp(-3/2 * distance)
                        if random.random() <= infection_prob * INFECTION_RATE:
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
            self.s_count = S0[id]
            self.i_count = I0[id]
            self.r_count = 0

        def calc_people(self):
            ppl = [val for val in self.map.values() if val != []]
            self.people = flatten(ppl)

        def create_map(self):
            city_map = {}
            for x in range(self.size + 1):
                for y in range(self.size + 1):
                    city_map[(x, y)] = []
            return city_map

        def populate(self, S0i):
            for _ in range(S0i):
                person_pos = (random.randint(0, self.size), random.randint(0, self.size))
                self.map[person_pos].append(Person(person_pos, self.id))

        def update_counts(self):
            self.s_count = len([p for p in self.people if p.status == 'S'])
            self.i_count = len([p for p in self.people if p.status == 'I'])
            self.r_count = len([p for p in self.people if p.status == 'R'])


    def create_cities():
        for id, pos in enumerate(SQUARE_POSITIONS):
            cities.append(City(id, pos, S0[id] + I0[id], SQUARE_SIZES[id]))
            cities[id].populate(S0[id] + I0[id])
            cities[id].calc_people()


    def draw_cities(screen, ZOOM_LEVEL, offset_x, offset_y):
        screen.fill(BACKGROUND_COLOR)
        for city in cities:
            city.update_counts()
            total = city.s_count + city.i_count + city.r_count
            infected_ratio = city.i_count / total
            color = get_color(infected_ratio)
            scaled_pos = (city.pos[0] * ZOOM_LEVEL + offset_x, city.pos[1] * ZOOM_LEVEL + offset_y)
            scaled_size = city.size * ZOOM_LEVEL
            pygame.draw.rect(screen, color, pygame.Rect(scaled_pos[0] - 10, scaled_pos[1] - 10, scaled_size + 20, scaled_size + 20))
            pygame.draw.rect(screen, 'black', pygame.Rect(scaled_pos[0], scaled_pos[1], scaled_size, scaled_size))
            draw_text(screen, f"miasto {city.id + 1}", scaled_pos[0] + scaled_size // 2, scaled_pos[1] + scaled_size + 10, size=int(108 * ZOOM_LEVEL/2))

    def draw_text(screen, text, x, y, size, color=(255, 255, 255)):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)



    def get_color(infected_ratio):
        cmap = plt.get_cmap("RdYlGn_r")
        return [int(255 * c) for c in cmap(infected_ratio)[:3]]


    def draw_people(screen, ZOOM_LEVEL, offset_x, offset_y):
        if DOT_RADIUS * ZOOM_LEVEL >= 1:
            for city in cities:
                for person in city.people:
                    scaled_pos = (city.pos[0] * ZOOM_LEVEL + person.pos[0] * ZOOM_LEVEL + offset_x,
                                city.pos[1] * ZOOM_LEVEL + person.pos[1] * ZOOM_LEVEL + offset_y)
                    pygame.draw.circle(screen, person.color, scaled_pos, int(DOT_RADIUS * ZOOM_LEVEL))


    def update_people(t):
        travel()
        for city in cities:
            for person in city.people:
                person.infect()
                person.remove_check()
                person.move_inside_new()
                if person.status == "S":
                    St[t] += 1
                elif person.status == "I":
                    It[t] += 1
                    person.infected_time += 1
                else:
                    Rt[t] += 1
                person.has_travelled = False
                
        for city in cities:
            city.calc_people()
        



    def travel():
        for city in cities:
            if CONNECTIONS_GRAPH[city.id] != []:
                people_to_move = int(city.pop * TRAVEL_RATE)

                for _ in range(people_to_move):
                    person = random.choice(city.people)
                    while person.has_travelled:
                        person = random.choice(city.people)
                    destination = cities[random.choice(CONNECTIONS_GRAPH[city.id])]
                    person.travel(destination)
                    replacement = random.choice(destination.people)
                    while replacement.has_travelled:
                        replacement = random.choice(destination.people)
                    replacement.travel(city)
                    city.people.remove(person)
                    destination.people.remove(replacement)
                    destination.people.append(person)
                    city.people.append(replacement)


    def flatten(xss):
        return [x for xs in xss for x in xs]


    def draw_city_list(screen):
        screen.fill(BACKGROUND_COLOR)
        city_list = ""
        for city in cities:
            city.update_counts()
            total = city.s_count + city.i_count + city.r_count
            infected_ratio = city.i_count / total
            color = get_color(infected_ratio)
            city_info = f"miasto {city.id + 1} - S: {city.s_count} || I: {city.i_count} || R: {city.r_count}"
            city_list += city_info + '\n'
            draw_text(screen, city_info, 500 + offset_x, 50 + (city.id * 50) + offset_y, 50, color)

        return city_list


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SIR Model")
    cities = []
    create_cities()
    for i, I0i in enumerate(I0):
        if I0i > 0:
            inf = random.sample(cities[i].people, I0i)
            for person in inf:
                person.status = "I"
                person.infected_time = 0
                person.color = COLORS[1]

    fig, axes = plt.subplots()

    running = True
    paused = False
    day = 1
    show_cities = True
    show_stats = False
    city_list = ""
    offset_x = 0
    offset_y = 0
    dragging = False
    last_mouse_pos = None

    while running and day < DAYS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_v:
                    show_cities = not show_cities
                    offset_x = 0
                    offset_y = 0
                elif event.key == pygame.K_s:
                    show_stats = not show_stats
            if show_cities:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        dragging = True
                        last_mouse_pos = pygame.mouse.get_pos()
                    elif event.button == 4:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        ZOOM_LEVEL *= ZOOM_RATIO
                        offset_x = (offset_x - mouse_x) * ZOOM_RATIO + mouse_x
                        offset_y = (offset_y - mouse_y) * ZOOM_RATIO + mouse_y
                    elif event.button == 5:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        ZOOM_LEVEL /= ZOOM_RATIO
                        offset_x = (offset_x - mouse_x) / ZOOM_RATIO + mouse_x
                        offset_y = (offset_y - mouse_y) / ZOOM_RATIO + mouse_y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        offset_x += mouse_pos[0] - last_mouse_pos[0]
                        offset_y += mouse_pos[1] - last_mouse_pos[1]
                        last_mouse_pos = mouse_pos
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        offset_y += 100
                    elif event.button == 5:
                        offset_y -= 100

        if not paused:
            update_people(day)
            day += 1

        if show_cities:
            draw_cities(screen, ZOOM_LEVEL, offset_x, offset_y)
            draw_people(screen, ZOOM_LEVEL, offset_x, offset_y)
        else:
            city_list = draw_city_list(screen)

        
        axes.clear()
        fig.patch.set_facecolor('black')
        axes.set_facecolor('black')
        axes.set_ylim(bottom=0, top=sum(S0)+1)
        axes.plot([i for i in range(day)], St[:day], c='g', label='Susceptible')
        axes.plot([i for i in range(day)], It[:day], c='r', label='Infected')
        axes.plot([i for i in range(day)], Rt[:day], c='b', label='Recovered')
        axes.tick_params(axis='x', colors='white')
        axes.tick_params(axis='y', colors='white')
        axes.spines['bottom'].set_color('white')
        axes.spines['top'].set_color('white')
        axes.spines['left'].set_color('white')
        axes.spines['right'].set_color('white')
        axes.yaxis.label.set_color('white')
        axes.xaxis.label.set_color('white')
        axes.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = pygame.image.load(buf)
        screen.blit(image, (1000, 250))

        if show_stats:
            draw_text(screen, f"S: {(100.0 * St[day-1] / TOTAL_POP):.2f}%, I: {(100.0 * It[day-1] / TOTAL_POP):.2f}%, R: {(100.0 * Rt[day-1] / TOTAL_POP):.2f}%", 1100, 100, 90)
        pygame.display.flip()

            

    save_stats()
    plt.savefig("wykres.png")
    pygame.quit()