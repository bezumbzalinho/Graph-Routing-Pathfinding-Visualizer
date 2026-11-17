from queue import PriorityQueue

# This class represent a graph
class My_Map:
    # Initialize the class
    def __init__(self):
        self.__graph = {}
    # Add a link from A and B of given distance, and also add the inverse link
    def connect(self, A, B, distance=1):
        self.__graph.setdefault(A, {})[B] = distance
        self.__graph.setdefault(B, {})[A] = distance
    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.__graph.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    def __repr__(self):
        return ('{}'.format(self.__graph))
    def __len__(self):
        return len(self.__graph.keys())

# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name:str, parent:str, to_faro=None):
        self.name = name
        self.parent = parent
        if to_faro is not None: # if to_faro is not None, it means that we working with Greedy Search or A* algorithms
            self.f = 0 # Distance to start node
            self.g = to_faro # Distance to start node or [Faro] node
        else:
            self.g = 0 # Distance to start node or [Faro] node
    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name
    def __repr__(self):
        return ('{}'.format(self.name))
    # Sort nodes
    def __lt__(self, other):
         return self.g < other.g

class Algorithms:
    def __init__(self, graph, to_faro):
        self.__graph = graph
        self.__to_faro = to_faro
    def depth_first_search(self, start, end):
        # Create lists for open nodes and closed nodes
        open = []
        closed = []
        # Create a start node and an goal node
        start_node = Node(start, None)
        goal_node = Node(end, None)
        # Add the start node
        open.append(start_node)

        levels_dict = {0 : [start]}

        iterations = {0: [start + ': 0']}

        number_of_iterations = 1
        
        # Loop until the open list is empty
        while len(open) > 0:
            # Get the last node (LIFO)
            current_node = open.pop(-1)
            # Add the current node to the closed list
            closed.append(current_node)
            
            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path_with_distances = []
                path = []
                distance = current_node.g
                while current_node != start_node:
                    path.append(current_node.name)
                    path_with_distances.append(current_node.name + ': ' + str(current_node.g))
                    current_node = current_node.parent
                path_with_distances.append(start_node.name + ': ' + str(start_node.g))
                path.append(start_node.name)
                # Return the results
                for key in levels_dict:
                    levels_dict[key] = list(set(levels_dict[key]))
                return { 'path': path[::-1], 'path_with_distances': path_with_distances[::-1], 'distance': distance, 'levels': levels_dict, 'iteractions': iterations }
            # Get neighbours
            neighbors = self.__graph.get(current_node.name)
            # Loop neighbors
            for key, value in neighbors.items():
                # Create a neighbor node
                neighbor = Node(key, current_node)
                level = 0
                level_neighbor = neighbor
                # iterate while not reaching the start node to get the level number we are working on
                while level_neighbor != start_node:
                    level+=1
                    level_neighbor = level_neighbor.parent
                levels_dict.setdefault(level, []).append(key)
                # update iteractions dict
                iterations.setdefault(number_of_iterations, []).append(key + ": " + str(current_node.g + self.__graph.get(current_node.name, neighbor.name)))
                # Check if the neighbor is in the closed list
                if neighbor in closed:
                    continue
                # Check if neighbor is in open list and if it has a lower f value
                if neighbor in open:
                    continue
                # Calculate cost so far
                neighbor.g = current_node.g + self.__graph.get(current_node.name, neighbor.name)
                # Everything is green, add neighbor to open list
                open.append(neighbor)
            number_of_iterations+=1
        # Return None, no path is found
        return None
    def uniform_cost(self, start, end):
        # Create lists for open nodes and closed nodes
        open = PriorityQueue()
        closed = []
        # Create a start node and an goal node
        start_node = Node(start, None)
        goal_node = Node(end, None)
        # Add the start node
        open.put(start_node)

        levels_dict = {0 : [start]}

        iterations = {0: [start + ': 0']}

        number_of_iterations = 1
        
        # Loop until the open list is empty
        while not open.empty():
            # Get the node
            current_node = open.get()
            # Add the current node to the closed list
            closed.append(current_node)
            
            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path_with_distances = []
                path = []
                distance = current_node.g
                while current_node != start_node:
                    path.append(current_node.name)
                    path_with_distances.append(current_node.name + ': ' + str(current_node.g))
                    current_node = current_node.parent
                path_with_distances.append(start_node.name + ': ' + str(start_node.g))
                path.append(start_node.name)
                # Return the results
                for key in levels_dict:
                    levels_dict[key] = list(set(levels_dict[key]))
                return { 'path': path[::-1], 'path_with_distances': path_with_distances[::-1], 'distance': distance, 'levels': levels_dict, 'iteractions': iterations }
            # Get neighbours
            neighbors = self.__graph.get(current_node.name)
            # Loop neighbors
            for key, value in neighbors.items():
                # Create a neighbor node
                neighbor = Node(key, current_node)
                level = 0
                level_neighbor = neighbor
                # iterate while not reaching the start node to get the level number we are working on
                while level_neighbor != start_node:
                    level+=1
                    level_neighbor = level_neighbor.parent
                levels_dict.setdefault(level, []).append(key)
                # Check if the neighbor is in the closed list
                if(neighbor in closed):
                    continue
                # Calculate cost so far
                neighbor.g = current_node.g + self.__graph.get(current_node.name, neighbor.name)
                # Everything is green, add neighbor to open list
                open.put(neighbor)
            pq_list = list(open.queue)
            # update iteractions dict
            for node in pq_list:
                iterations.setdefault(number_of_iterations, []).append(node.name + ": " + str(node.g))
            number_of_iterations+=1
        # Return None, no path is found
        return None
    def greedy_search(self, start, pure:bool = False):
        open = PriorityQueue()
        if not pure: closed = []
        # Create a start node and an goal node
        start_node = Node(start, None, to_faro=self.__to_faro.get(start))
        goal_node = Node('Faro', None)
        # Add the start node
        open.put(start_node)

        levels_dict = {0 : [start]}

        iterations = {0: [start + ': 0']}

        number_of_iterations = 1

        while not open.empty():
            # Get the node
            current_node = open.get()
            # Add the current node to the closed list
            if not pure: closed.append(current_node)

            if current_node == goal_node:
                path_with_distances = []
                path = []
                distance = current_node.f
                while current_node != start_node:
                    path.append(current_node.name)
                    path_with_distances.append(current_node.name + ': ' + str(current_node.f))
                    current_node = current_node.parent
                path_with_distances.append(start_node.name + ': ' + str(start_node.f))
                path.append(start_node.name)
                # Return the results
                for key in levels_dict:
                    levels_dict[key] = list(set(levels_dict[key]))
                return { 'path': path[::-1], 'path_with_distances': path_with_distances[::-1], 'distance': distance, 'levels': levels_dict, 'iteractions': iterations }
            # Get neighbours
            neighbors = self.__graph.get(current_node.name)
            # Loop neighbors
            for key, value in neighbors.items():
                # Create a neighbor node
                neighbor = Node(key, current_node)
                level = 0
                level_neighbor = neighbor
                # iterate while not reaching the start node to get the level number we are working on
                while level_neighbor != start_node:
                    level+=1
                    level_neighbor = level_neighbor.parent
                levels_dict.setdefault(level, []).append(key)
                # Check if the neighbor is in the closed list
                if not pure and neighbor in closed:
                    continue
                # Calculate cost so far
                neighbor.f = current_node.f + self.__graph.get(current_node.name, neighbor.name)
                # get the cost to [Faro]
                neighbor.g = self.__to_faro.get(key)
                # Everything is green, add neighbor to open list
                open.put(neighbor)
            pq_list = list(open.queue)
            # update iteractions dict
            for node in pq_list:
                iterations.setdefault(number_of_iterations, []).append(node.name + ": " + str(node.g))
            number_of_iterations+=1
        # Return None, no path is found
        return None
    def a_star(self, start):
        open = PriorityQueue()
        closed = []
        # Create a start node and an goal node
        start_node = Node(start, None, to_faro=self.__to_faro.get(start))
        goal_node = Node('Faro', None)
        # Add the start node
        open.put(start_node)

        levels_dict = {0 : [start]}

        iterations = {0: [start + ': 0']}

        number_of_iterations = 1

        while not open.empty():
            # Get the node
            current_node = open.get()
            # Add the current node to the closed list
            closed.append(current_node)

            if current_node == goal_node:
                path_with_distances = []
                path = []
                distance = current_node.f
                while current_node != start_node:
                    path.append(current_node.name)
                    path_with_distances.append(current_node.name + ': ' + str(current_node.f))
                    current_node = current_node.parent
                path_with_distances.append(start_node.name + ': ' + str(start_node.f))
                path.append(start_node.name)
                # Return the results
                for key in levels_dict:
                    levels_dict[key] = list(set(levels_dict[key]))
                return { 'path': path[::-1], 'path_with_distances': path_with_distances[::-1], 'distance': distance, 'levels': levels_dict, 'iteractions': iterations }
            # Get neighbours
            neighbors = self.__graph.get(current_node.name)
            # Loop neighbors
            for key, value in neighbors.items():
                # Create a neighbor node
                neighbor = Node(key, current_node)
                level = 0
                level_neighbor = neighbor
                # iterate while not reaching the start node to get the level number we are working on
                while level_neighbor != start_node:
                    level+=1
                    level_neighbor = level_neighbor.parent
                levels_dict.setdefault(level, []).append(key)
                # Check if the neighbor is in the closed list
                if neighbor in closed:
                    continue
                # Calculate cost so far
                neighbor.f = current_node.f + self.__graph.get(current_node.name, neighbor.name)
                # get the cost to [Faro] + so far
                neighbor.g = current_node.f + self.__graph.get(current_node.name, neighbor.name) + self.__to_faro.get(key)
                # Everything is green, add neighbor to open list
                open.put(neighbor)
            pq_list = list(open.queue)
            # update iteractions dict
            for node in pq_list:
                iterations.setdefault(number_of_iterations, []).append(node.name + ": " + str(node.g))
            number_of_iterations+=1
        # Return None, no path is found
        return None