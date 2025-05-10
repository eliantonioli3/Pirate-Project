import pygame
from path_finding import PathFinding
from ASTAR import AStar as ASTARPathFinder
from DFS import DFS as DFSPathFinder
from BFS import BFS as BFSPathFinder
from GREEDY import Greedy as GREEDYPathFinder
from UCS import UCS as UCSPathFinder
from WEBEX import WebEX as WebEXpansionPathFinder
import heuristics
from world import World
clock = pygame.time.Clock()
import click
import time
import json

WIDTH = 1000
UI_WIDTH = 300  
WIN = win = pygame.display.set_mode((WIDTH + UI_WIDTH, WIDTH), pygame.HWSURFACE | pygame.DOUBLEBUF)                      
pygame.display.set_caption("Search Algorithm")
pygame.init()

def load_raw_images():
    images = {
        "start": pygame.image.load("img/pirata.png"),
        "end": pygame.image.load("img/tesoro.png"),
        "crab": pygame.image.load("img/crab.png"),
        "barrier": pygame.image.load("img/water.png"),
        "cactus": pygame.image.load("img/cactus.png"),
        "impronte": pygame.image.load("img/impronte.png"),
        "current_E": pygame.image.load("img/current_E.png"),
        "current_S": pygame.image.load("img/current_S.png"),
        "current_N": pygame.image.load("img/current_N.png"),
        "current_W": pygame.image.load("img/current_W.png"),

    }

    images["crab_large"] = pygame.transform.scale(images["crab"], (30, 30))
    images["cactus_large"] = pygame.transform.scale(images["cactus"], (30, 30))
    images["end_large"] = pygame.transform.scale(images["end"], (30, 30))

    return images

def resize_images(images, cell_width):
    scaled_images = {}
    for key, img in images.items():
        if "_large" in key:
            scaled_images[key] = img  
        else:
            scaled_images[key] = pygame.transform.smoothscale(img, (cell_width, cell_width))
    return scaled_images

def draw_border(win):
    
    wood_texture = pygame.image.load("img/wood_texture.jpg").convert()
    wood_texture = pygame.transform.scale(wood_texture, (120, 40))  # Ridimensiona la texture per adattarla ai bordi

    GOLD_COLOR = (212, 175, 55)  
    DARK_GOLD = (162, 130, 33) 
    LIGHT_GOLD = (255, 221, 85)  
    border_thickness = 20 

    for idx, y in enumerate(range(0, WIDTH, 40)):  
        win.blit(wood_texture, (0, y))  
        win.blit(wood_texture, (WIDTH - 120, y))  

    pygame.draw.rect(win, DARK_GOLD, (50, 0, border_thickness, WIDTH))  
    pygame.draw.rect(win, DARK_GOLD, (WIDTH - 70, 0, border_thickness, WIDTH))  

    pygame.draw.rect(win, GOLD_COLOR, (52, 0, border_thickness - 4, WIDTH))  
    pygame.draw.rect(win, GOLD_COLOR, (WIDTH - 68, 0, border_thickness - 4, WIDTH))  

    pygame.draw.rect(win, LIGHT_GOLD, (54, 0, border_thickness - 8, WIDTH))  
    pygame.draw.rect(win, LIGHT_GOLD, (WIDTH - 66, 0, border_thickness - 8, WIDTH))  

    pygame.draw.rect(win, (0, 0, 0), (50, 0, border_thickness, 5))  
    pygame.draw.rect(win, (0, 0, 0), (WIDTH - 70, 0, border_thickness, 5))   

     

    


 
BROWN    = (165, 42, 42)
SAND_COLOR = (255, 255, 102)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
LIME = (50, 205, 50)
NAVY     = (0, 0, 128)
LIGHT_BLUE = (173, 216, 230)

class Spot:
    images = None
    
    def __init__(self, row, col, width, offset_x=0, offset_y=0,images=None):
        self.img_path = None
        self.row = row
        self.col = col
        self.x = row * width + offset_x  
        self.y = col * width + offset_y 
        self.color = SAND_COLOR
        self.width = width

        if Spot.images is None and images is not None:
            Spot.images = images 
        
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLUE
    
    def is_crab(self):
        return self.color == GREY
    
    
    def is_current(self):
        return self.color == NAVY
    
    def is_cactus(self):
        return self.color == LIME

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLUE
    
    def make_crab(self):
        self.color = GREY
    
    def make_cactus(self):
        self.color = LIME

    def make_end(self):
        self.color = TURQUOISE
       

    def make_path(self):
        self.color = PURPLE
    
    def make_current(self,direction):
        self.color = NAVY
        self.current_direction = direction
    
    def make_treasure_collected(self):
        self.img_path = Spot.images["end"]        

    

    def draw(self, win):
        if self.is_start():
            win.blit(Spot.images["start"], (self.x, self.y))
        elif self.is_end():
            win.blit(Spot.images["end"], (self.x, self.y))
        elif self.is_barrier():
            win.blit(Spot.images["barrier"], (self.x, self.y))
        elif self.is_crab():
            win.blit(Spot.images["crab"], (self.x, self.y))
        elif self.is_cactus():
            win.blit(Spot.images["cactus"], (self.x, self.y))
        elif self.img_path:
            win.blit(self.img_path, (self.x, self.y))
        elif self.is_current():
            win.blit(Spot.images[f"current_{self.current_direction}"], (self.x, self.y))
        else :
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __str__(self):
        return "({},{})".format(self.row, self.col)

def make_grid(rows, width, raw_images):
    grid = []
    gap = width// rows
    grid_size = rows * gap 
    images = resize_images(raw_images, gap) 

    offset_x = (WIDTH - grid_size) // 2  
    offset_y = (WIDTH - grid_size) // 2  
    for i in range(rows):
        grid.append([])
        for j in range(width):
            spot = Spot(i, j, gap, offset_x, offset_y,images)
            grid[i].append(spot)

    return grid, offset_x, offset_y

def make_grid_from_file(filename, width, raw_images):
    f = open(filename)

    data = json.load(f)

    rows = data['rows']
    grid = []
    gap = width // rows
    images = resize_images(raw_images, gap)
    grid_size = rows * gap

    offset_x = (WIDTH - grid_size) // 2
    offset_y = (WIDTH - grid_size) // 2

    global SAND_COLOR
    if "currents" in filename.lower():
        SAND_COLOR = LIGHT_BLUE
    else:
        SAND_COLOR = (255, 255, 102)  
    
    start = (data['start'][0],data['start'][1])
    if isinstance(data['end'][0], list):            
        ends = {tuple(ele) for ele in data['end']}
    else:                                           
        ends = {tuple(data['end'])}  
    
    barrier = {(ele[0],ele[1]) for ele in data['barrier']}
    crab = {(ele[0],ele[1]) for ele in data['crab']}
    cactus = {(ele[0],ele[1]) for ele in data['cactus']}
    currents = {tuple(ele[:2]): ele[2] for ele in data['currents']}  
    

    end_spots = []
    
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, offset_x, offset_y,images)
            if (i,j) in barrier:
                spot.make_barrier()
            if (i,j) in crab:
                spot.make_crab()
            if (i,j) in cactus:
                spot.make_cactus()
            if (i,j) in currents:
                spot.make_current(currents[(i, j)])
            elif (i, j) in ends:
                spot.make_end()
                end_spots.append((i,j))
            elif (i,j) == start:
                spot.make_start()
                start = spot
            grid[i].append(spot)

    return grid, start, end_spots, rows, barrier,crab,cactus,currents, offset_x, offset_y


def draw_grid(win, rows, width, offset_x, offset_y):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (offset_x, offset_y + i * gap), (offset_x + width, offset_y + i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (offset_x + i * gap, offset_y), (offset_x + i * gap, offset_y + width))


def draw(win, grid, rows, width,offset_x, offset_y):
    window_width, window_height = win.get_size()
    
    grid_width = window_width - UI_WIDTH  
    grid_height = window_height  
    
    win.fill(WHITE, rect=(0, 0, grid_width, grid_height))

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width, offset_x, offset_y)
    draw_border(win) 
    pygame.display.update()


def mark_spots(start, grid, plan,p):
    
    x = start.row
    y = start.col
    for a in plan:
        if a == 'N':
            y+=1
        elif a == 'S':
            y-=1
        elif a == 'E':
            x+=1
        elif a == 'W':
            x-=1
        elif a == 'NE':
            x += 1
            y += 1
        elif a == 'NW':
            x -= 1
            y += 1
        elif a == 'SE':
            x += 1
            y -= 1
        elif a == 'SW':
            x -= 1
            y -= 1

        grid[x][y].img_path = None
        terrain = p.terrainType((x, y)) 
        if terrain == "end": 
            grid[x][y].make_treasure_collected()  
        else :
            grid[x][y].make_path()      

        

def mark_expanded(exp, grid):
    for e in exp:
        grid[e[0]][e[1]].make_closed()



FONT1 = pygame.font.SysFont("georgia", 21)
FONT2 = pygame.font.SysFont("comicsans", 24)
FONT3 = pygame.font.SysFont("consolas", 19)
FONT4 = pygame.font.SysFont("georgia", 18)


def draw_ui(win, total_cost, collected_objects, algorithm_name, elapsed_time, expanded_nodes,diagonal):

    pygame.draw.rect(win, (200, 200, 200), (WIDTH, 0, UI_WIDTH, WIDTH))  
    pygame.draw.rect(win, (50, 50, 50), (WIDTH + 5, 5, UI_WIDTH - 10, WIDTH - 10), 3) 
 
    title = FONT1.render("PIRATE'S GOLD RUSH", True, (0, 0, 0))
    win.blit(title, (WIDTH + 20, 150))

    algo_text = FONT2.render(f"Algoritmo: {algorithm_name}", True, (0, 0, 0))
    win.blit(algo_text, (WIDTH + 20, 250))

    cost_text = FONT2.render(f"Costo Totale: {total_cost}", True, (0, 0, 0))
    win.blit(cost_text, (WIDTH + 20, 300))

    nodes_text = FONT2.render(f"Nodi Espansi: {expanded_nodes}", True, (0, 0, 0))
    win.blit(nodes_text, (WIDTH + 20, 350))

    time_text = FONT2.render(f"Tempo: {elapsed_time:.0f}ms", True, (0, 0, 0))
    win.blit(time_text, (WIDTH + 20, 400))
    
    pygame.draw.line(win, (255, 215, 0), (WIDTH + 10, 440), (WIDTH + UI_WIDTH - 10, 440), 3)
    pygame.draw.line(win, (139, 69, 19), (WIDTH + 10, 443), (WIDTH + UI_WIDTH - 10, 443), 2)  
    y_offset = 447
    for obj, count in collected_objects.items():
        if obj == "Crabs":
         win.blit(Spot.images["crab_large"], (WIDTH + 20, y_offset))
        elif obj == "Cactus":
         win.blit(Spot.images["cactus_large"], (WIDTH + 20, y_offset))
        elif obj == "Treasure":
         win.blit(Spot.images["end_large"], (WIDTH + 20, y_offset))
        obj_text = FONT4.render(f"{obj}: {count}", True, (0, 0, 0))
        win.blit(obj_text, (WIDTH + 80, y_offset))
        y_offset += 25
    pygame.draw.line(win, (255, 215, 0), (WIDTH + 10, y_offset + 5), (WIDTH + UI_WIDTH - 10, y_offset + 5), 3)
    pygame.draw.line(win, (139, 69, 19), (WIDTH + 10, y_offset + 8), (WIDTH + UI_WIDTH - 10, y_offset + 8), 2)

    close_button_rect = pygame.Rect(WIDTH + UI_WIDTH - 50, 150, 25, 25)  
    pygame.draw.rect(win, (255, 0, 0), close_button_rect)  
    pygame.draw.rect(win, (255, 215, 0), close_button_rect, 2)  
    close_button_text = FONT2.render("X", True, (255, 255, 255))  

    text_width = close_button_text.get_width()
    text_height = close_button_text.get_height()
    text_x = WIDTH + UI_WIDTH - 50 + (25 - text_width) // 2
    text_y = 150 + (25 - text_height) // 2  
    win.blit(close_button_text, (text_x, text_y))

    diag_button_rect = pygame.Rect(WIDTH + 20, 195, 180, 40)
    pygame.draw.rect(win, (70, 130, 180), diag_button_rect, border_radius=8)  
    pygame.draw.rect(win, (255, 215, 0), diag_button_rect, 2, border_radius=8)   

    diag_text_str = "Diagonale: ON" if diagonal else "Diagonale: OFF"
    diag_text_color = (0, 255, 0) if diagonal else (255, 0, 0)
    diag_text = FONT3.render(diag_text_str, True, diag_text_color)
    win.blit(diag_text, (WIDTH + 30, 205))
    
    


def animate_path(start,world, grid, plan, p, win,rows,width, offset_x, offset_y, algorithm_name,elapsed_time, expanded_nodes,diagonal,raw_images):
    
    x, y = start.row, start.col
    total_cost = 0
    collected_objects = {"Crabs": 0, "Cactus": 0,"Treasure": 0}
    visited_treasures = set()  

    
    for state in plan:
        
        grid[x][y].reset()
        
        if state == 'N':
            y += 1
        elif state == 'S':
            y -= 1
        elif state == 'E':
            x += 1
        elif state == 'W':
            x -= 1
        elif state == 'NE':
            x += 1
            y += 1
        elif state == 'NW':
            x -= 1
            y += 1
        elif state == 'SE':
            x += 1
            y -= 1
        elif state == 'SW':
            x -= 1
            y -= 1

        grid[x][y].make_start()
        
        terrain = p.terrainType((x, y))
        
        cost = p.costs.get(terrain, 1)
        if terrain == "current" :
            current = world.currents[(x, y)]
            cost = p.currentDirection(state,current,cost)
            total_cost += cost

        else: 
            total_cost += cost 

        if terrain == "crab":
            collected_objects["Crabs"] += 1
        if terrain == "cactus":
            collected_objects["Cactus"] += 1
        if terrain == "end":
            if (x, y) not in visited_treasures:  
                collected_objects["Treasure"] += 1
                visited_treasures.add((x, y)) 

        draw(win, grid, rows, width, offset_x, offset_y)
        draw_ui(win, total_cost, collected_objects,algorithm_name,elapsed_time, expanded_nodes,diagonal)
        pygame.display.update()
        pygame.time.delay(50)
        grid[x][y].img_path = Spot.images["impronte"]
       

    print("Cost of the plan is: {}".format(total_cost))
    mark_spots(start,grid,plan,p)
    draw(win, grid, rows, width, offset_x, offset_y)
    draw_ui(win, total_cost, collected_objects,algorithm_name,elapsed_time, expanded_nodes,diagonal)
    pygame.display.update()
    return total_cost, collected_objects


ALGORITHMS_MAP = {
    "A*": lambda: ASTARPathFinder(heuristics.manhattanMultiGoal, True),
    "A* w=4": lambda: ASTARPathFinder(heuristics.manhattanMultiGoal, True, w=4),
    "GREEDY": lambda: GREEDYPathFinder(heuristics.manhattanMultiGoal, True),
    "UCS": lambda: UCSPathFinder(True),
    "BFS": lambda: BFSPathFinder(True),
    "DFS": lambda: DFSPathFinder(True),
    "WEBEX": lambda: WebEXpansionPathFinder(True),
    
    
}

HEURISTICS_MAP = {
    "Manhattan": heuristics.manhattanMultiGoal,
    "Euclidean": heuristics.euclideanMultiGoal,
    "Mst" : heuristics.mst,
    "Current" : heuristics.currentHeuristic
    
}

def draw_dropdown(surface, x, y, width, options, selected, open_dropdown):
    rect = pygame.Rect(x, y, width, 35)
    FONT = pygame.font.SysFont("impact", 18)
    
    pygame.draw.rect(surface, (139, 69, 19), rect, border_radius=8)  
    pygame.draw.rect(surface, (255, 215, 0), rect, 3, border_radius=8)  

    text = FONT.render(selected, True, (255, 255, 255))  
    surface.blit(text, (x + 10, y + 7))

    dropdown_rects = []
    if open_dropdown:
        for i, option in enumerate(options):
            opt_rect = pygame.Rect(x, y + (i + 1) * 35, width, 35)

            mouse_pos = pygame.mouse.get_pos()
            if opt_rect.collidepoint(mouse_pos):
                bg_color = (210, 105, 30)  
            else:
                bg_color = (160, 82, 45)  

            pygame.draw.rect(surface, bg_color, opt_rect, border_radius=6)
            pygame.draw.rect(surface, (255, 215, 0), opt_rect, 1, border_radius=6)  

            
            opt_text = FONT.render(option, True, (255, 255, 255))  
            surface.blit(opt_text, (x + 10, y + (i + 1) * 35 + 7))

            dropdown_rects.append((opt_rect, option))

    return rect, dropdown_rects


    
@click.command()
@click.option('-s', '--search_algorithm', default = "ASTAR", help = "Search algorithm to be used")
@click.option('-h', '--heuristic', default = "Manhattan", help = "Heuristic function to be used")
@click.option('-f', '--filename', default = None, help = "Initialize map with data from file")
@click.option('-d', '--diagonal', type=bool, default=True, help="Enable diagonal movement (True/False)")
def main( search_algorithm,heuristic, filename = None,diagonal = True):
    global current_algorithm_name, current_heuristic_name
    win = WIN
    start = None
    width = WIDTH - 200
    rows = 50
    raw_images = load_raw_images()

    if filename is not None:                                                     
        grid, start, ends, rows, wall, crab, cactus,current, offset_x, offset_y = make_grid_from_file(filename,width,raw_images) 
    else:                                                                          
        grid, offset_x, offset_y = make_grid(rows, width,raw_images)
        wall = set()                                                           
    run = True

    total_cost = 0
    elapsed_time = 0
    expanded = 0
    collected_objects = {"Crabs": 0, "Cactus": 0,"Treasure": 0}
    current_algorithm_name = search_algorithm.upper() if search_algorithm.upper() in ALGORITHMS_MAP else "A*"
    current_heuristic_name = heuristic if heuristic in HEURISTICS_MAP else "Manhattan"

    search_algorithm = ALGORITHMS_MAP[current_algorithm_name]()
    show_algo_dropdown = False
    show_heuristic_dropdown = False
    
    search_algorithm = ALGORITHMS_MAP[current_algorithm_name]()
    algorithm_name = search_algorithm.__class__.__name__ 
    
    needs_redraw = True
    
    while run:
        if needs_redraw:
                
                draw(win, grid, rows, width, offset_x, offset_y)      
                draw_ui(win, total_cost, collected_objects, algorithm_name,elapsed_time, expanded,diagonal) 
                
                algo_rect, algo_dropdowns = draw_dropdown(win, WIDTH + 20, 535, 100, list(ALGORITHMS_MAP.keys()), current_algorithm_name, show_algo_dropdown)

                heuristic_rect = None
                heuristic_dropdowns = []
                if current_algorithm_name in ["A*", "A* w=4", "GREEDY"]:
                    heuristic_rect, heuristic_dropdowns = draw_dropdown(win, WIDTH + 150, 535, 100, list(HEURISTICS_MAP.keys()), current_heuristic_name, show_heuristic_dropdown)
                

                pygame.display.update()  
                needs_redraw = False
        
        clock.tick(30)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                diag_button_rect = pygame.Rect(WIDTH + 20, 195, 180, 40)
                if diag_button_rect.collidepoint(pos):
                    diagonal = not diagonal
                    needs_redraw = True

                close_button_rect = pygame.Rect(WIDTH + UI_WIDTH - 50, 150, 25, 25)
                if close_button_rect.collidepoint(pos):
                    run = False  

                if algo_rect.collidepoint(pos):
                    show_algo_dropdown = not show_algo_dropdown
                    needs_redraw = True
                else:
                    for rect, name in algo_dropdowns:
                        if rect.collidepoint(pos):
                            current_algorithm_name = name
                            show_algo_dropdown = False
                            search_algorithm = ALGORITHMS_MAP[name]()
                            algorithm_name = search_algorithm.__class__.__name__
                            needs_redraw = True

                if heuristic_rect and heuristic_rect.collidepoint(pos):
                    show_heuristic_dropdown = not show_heuristic_dropdown
                    needs_redraw = True
                else:
                    for rect, name in heuristic_dropdowns:
                        if rect.collidepoint(pos):
                            current_heuristic_name = name
                            show_heuristic_dropdown = False
                            needs_redraw = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and ends:

                    grid, start, ends, rows, wall, crab, cactus, current, offset_x, offset_y = make_grid_from_file(filename, width,raw_images)
                    heuristic_func = HEURISTICS_MAP.get(current_heuristic_name, None)

                    if hasattr(search_algorithm, 'heuristic') and heuristic_func:
                        search_algorithm.heuristic = heuristic_func
                    world = World(rows-1,rows-1,wall,crab,cactus,current,ends)          
                    p = PathFinding((start.row,start.col),ends,world,diagonal)
                    
                    start_time = time.time()
                    plan = search_algorithm.solve(p)
                    elapsed_time = (time.time() - start_time)*1000
                    expanded = search_algorithm.expanded
                    
                    print("Number of Expansions: {} in {:.0f} ms".format(search_algorithm.expanded, elapsed_time))
                    mark_expanded(search_algorithm.expanded_states, grid)

                    if plan is not None:
                        
                        total_cost, collected_objects = animate_path(start,world, grid, plan, p, win,rows,width,offset_x, offset_y,algorithm_name,elapsed_time,expanded,diagonal,raw_images)  
                    needs_redraw = True
                
                        
    pygame.quit()

if __name__ == '__main__':
    main()
