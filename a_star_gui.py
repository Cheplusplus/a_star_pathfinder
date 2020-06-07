import pygame as pg
import a_star_pathfinding


# ----------------Init / Fonts----------------
pg.init()
pg.font.init()
sans = pg.font.SysFont('Comic Sans MS', 38)

# -----------------Screen---------------------
screen = pg.display.Info()
scr_w = screen.current_w
scr_h = screen.current_h - 105
screen = pg.display.set_mode((scr_h, scr_h))
pg.display.set_caption("A Star path finding algorithm")

# -----------------Clock---------------------
clock = pg.time.Clock()
clock_time = 60


# ----------------Globals--------------------
obstacles = [(3, 3)]
running = True
block_size = 15
draw_nodes = True
red = (150, 0, 0)
green = (0, 150, 0)
blue = (0, 0, 150)
black = (0, 0, 0)
white = (155, 155, 155)


# -----------------Returns the mouse position-----------------------------
def get_mouse_pos():
    mouse_pos = pg.mouse.get_pos()
    mouse_pos = (int(mouse_pos[0] / block_size), int(mouse_pos[1] / block_size))
    return mouse_pos


def get_mouse_click():
    clicked = [False, False]
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            clicked[0] = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            clicked[0] = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            clicked[1] = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
            clicked[1] = False
    return clicked


class Menu:

    def __init__(self, name, text):
        self.name = name
        self.pos = (0, 0)
        self.text = text
        self.text_surface = sans.render(self.text, False, white)
        self.text_surface_size = self.text_surface.get_size()

    def on_click(self):
        event = get_mouse_pos()
        if self.pos[0] < event[0] < self.text_surface_size[0] / block_size:
            if self.pos[1] < event[1] < self.text_surface_size[1]/ block_size:
                return True

    def draw(self):
        screen.blit(self.text_surface, self.pos)


class Game:

    def __init__(self, width, height):
        self.size = (width, height)
        self.screen = pg.display.set_mode(self.size)

    def run(self):
        run = True

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            pass

    def reset(self):
        pass


# ----------------------draw a node----Takes a colour and fill value-------------------------
def draw_node(node, colour, fill):
    if not isinstance(node, pg.Vector2):
        node = pg.Vector2(node[0], node[1])
    draw_coordinates = node * block_size
    pg.draw.rect(screen, colour, [draw_coordinates[0], draw_coordinates[1], block_size, block_size], fill)


# -----------------------------Draw a map----------------------------
def create_map():
    # -----------------Variables------------------
    global running
    global obstacles
    creating_map = True

    # -----------------Blank screen and draw obstacles in the list including start and end nodes-----------------------
    screen.fill(black)
    for obstacle in obstacles:
        draw_node(obstacle * block_size, blue, 0)
    # draw_node(a_star_pathfinding.start_node, green, 0)
    # draw_node(a_star_pathfinding.end_node, red, 0)
    pg.display.update()

    # ------------------start creating the map -------------------------------------
    while creating_map:
        # -------------------Go through events---------------------------
        clicked = get_mouse_click()
        # -----------------------Left mouse button pressed-------------------------
        if clicked[0]:
            mouse_pos = get_mouse_pos()
            obstacles.append(mouse_pos)
            draw_node(mouse_pos, blue, 0)
            pg.display.update()

        # ----------------------Right mouse button pressed-------------------------
        elif clicked[1]:
            mouse_pos = get_mouse_pos()
            if mouse_pos in obstacles:
                obstacles = list(set(obstacles))
                obstacles.remove(mouse_pos)
            draw_node(mouse_pos, black, 0)
            pg.display.update()

    # ----------------Returns the list of obstacles uncleaned-------------------
    return obstacles


# ------------------------What to do at the end of the loop?------------------
def reset():
    # ----------------Variables------------------
    global running
    global obstacles
    global draw_nodes

    # ------------------Get events---------------------------
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            return False

        elif event.type == pg.KEYDOWN:

            # ----------------Set the draw search----------------
            if event.key == pg.K_a:
                draw_nodes = not draw_nodes

            # -------------------Clear the map-----------------------
            elif event.key == pg.K_d:
                obstacles.clear()

            # ----------------Reset-----------------
            elif event.key == pg.K_e:
                return False
    return True


# -----------------------Main()---------------------
def main():
    # ---------Variables------------
    global running
    global obstacles

    # ------------------Main loop------------------
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            # ------------------Get Key pressed------------------
            elif event.type == pg.KEYDOWN:

                # ----------------Create New map----------------
                if event.key == pg.K_a:
                    obstacles = list(set(create_map()))

                # -------------------Clear the map-----------------------
                elif event.key == pg.K_d:
                    pass

        # ---------------------Send cleaned obstacles list to path finder-------------------

        a_star_pathfinding.obstacles = obstacles

        # --------------------Create a new grid with obstacles list------------------------
        a_star_pathfinding.setup()
        pg.display.update()

        # -----------------Return the path and check it---------------------
        path = a_star_pathfinding.find_shortest_path((1, 1), (50, 50))
        if path:
            for node in path:
                draw_node(node, red, 0)
                if draw_nodes:
                    clock.tick(clock_time)
                    pg.display.update()
            pg.display.update()

        while reset():
            pass
        screen.fill(black)
        pg.display.update()


if __name__ == '__main__':
    main()
