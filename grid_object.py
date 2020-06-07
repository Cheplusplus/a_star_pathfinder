class Node:
    # -------------------New Node object-----------------------
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.neighbours = []


class Grid:
    """
    This class creates a new grid of Node objects
    :param rows: Int
    :param cols: Int
    :return Grid object
    """
    def __init__(self, rows=65, cols=65):
        self.rows = rows
        self.cols = cols
        self.grid = None
        self.new_grid(rows, cols)

    # ---------------------Get the nodes next to this node-----------------------------
    def search_neighbouring_nodes(self, node):
        new_node_coordinates = [(node.coordinates[0] + 1, node.coordinates[1] + 1),
                                (node.coordinates[0] - 1, node.coordinates[1] - 1),
                                (node.coordinates[0], node.coordinates[1] + 1),
                                (node.coordinates[0], node.coordinates[1] - 1),
                                (node.coordinates[0] + 1, node.coordinates[1]),
                                (node.coordinates[0] - 1, node.coordinates[1]),
                                (node.coordinates[0] + 1, node.coordinates[1] - 1),
                                (node.coordinates[0] - 1, node.coordinates[1] + 1)]
        for new_node in new_node_coordinates:
            if self.rows < new_node[0] or new_node[0] < 0 or self.cols < new_node[1] or new_node[1] < 0:
                continue
            else:
                this_node = self.grid[int(new_node[0])][int(new_node[1])]
                node.neighbours.append(this_node)
    # ---------------------------------------------------------------------------------

    def get_neighbours(self, rows, cols):
        for row in range(rows - 1):
            for col in range(cols - 1):
                self.search_neighbouring_nodes(self.grid[row][col])

    # ------------------Create new grid----------------------
    def new_grid(self, rows, cols):
        new_grid = []
        rows = rows
        cols = cols

        for i in range(cols):
            new_grid.append([0 for j in range(rows)])

        for row in range(rows):
            for col in range(cols):
                new_grid[row][col] = Node((row, col))

        self.grid = new_grid

        self.get_neighbours(rows, cols)
    # ---------------------------------------------------------
