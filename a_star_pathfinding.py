from grid_object import Grid
from vector_math import distance_between


all_nodes = []
grid = None
path = []
obstacles = [(3, 3)]


def setup(rows=65, cols=65):
    global grid

    grid = Grid(rows, cols)
    for row in range(len(grid.grid)):
        for col in range(len(grid.grid[0])):
            node = grid.grid[row][col]
            node.origin = None
            node.g_cost = 0
            node.h_cost = 0
            node.f_cost = 0
            node.has_been = False
            node.searched = False


def find_lowest_f_cost():
    lowest_f_cost = 999 ** 99
    this_node = 0
    for node in all_nodes:
        if not node.has_been and node.f_cost < lowest_f_cost:
            this_node = node
            lowest_f_cost = node.f_cost
    this_node.has_been = True
    return this_node


# -----------------------Update the nodes costs----ll_node-------------------
def update_costs(node, origin, end):
    # set new origin to update from----------------------------
    node.origin = origin

    # ----------------Distance from starting node--------------------------
    g_cost = int(distance_between(origin.coordinates, node.coordinates) * 10)
    if not node == origin:
        g_cost += origin.g_cost
    node.g_cost = int(g_cost)

    # -----------------Distance from ending node-------------------------
    h_cost = int(distance_between(end.coordinates, node.coordinates) * 10)
    node.h_cost = int(h_cost)

    # ----------------Combination of g and h costs------------------
    f_cost = node.g_cost + node.h_cost
    node.f_cost = f_cost
# --------------------------------------------------------------------


def search_neighbours(node, end):
    global obstacles
    for new_node in node.neighbours:
        if not new_node.has_been and new_node.coordinates not in obstacles:
            if not new_node.searched:
                update_costs(new_node, node, end)
                new_node.searched = True
                all_nodes.append(new_node)
            elif node.g_cost < new_node.origin.g_cost:
                update_costs(new_node, node, end)


# -------------------Reset nodes for next search-----------------------
def reset_nodes():
    global all_nodes
    global path

    for node in all_nodes:
        node.origin = None
        node.g_cost = 0
        node. h_cost = 0
        node.f_cost = 0
        node.has_been = False
        node.searched = False
    all_nodes = []
    path = []
# ---------------------------------------------------------------------


# -------------------Set the shortest path as this objects path-------------------
def get_path(node, start):
    global path
    """
    This method runs recursively and sets the shortest path as this objects path
    :param node:
    """
    if node.coordinates != start.coordinates:
        path.append(node.origin.coordinates)
        get_path(node.origin, start)
# ---------------------------------------------------------------------------------


def find_shortest_path(start, end):
    try:
        start = grid.grid[start[0]][start[1]]
        end = grid.grid[end[0]][end[1]]
    except:
        print('Cannot move here')
        return
    all_nodes.append(start)
    update_costs(start, start, end)
    while end not in all_nodes:
        node = find_lowest_f_cost()
        search_neighbours(node, end)
    get_path(all_nodes[-1], start)
    new_path = list(reversed(path))
    reset_nodes()
    return new_path


# ----------------------------------------------------------------------------------------------


def main():
    setup()
    print(find_shortest_path((1, 1), (50, 50)))
    print(find_shortest_path((10, 10), (5, 50)))


if __name__ == '__main__':
    main()
