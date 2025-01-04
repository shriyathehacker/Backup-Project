from random import choice

global size

class Node:
    def __init__(self, initialValue, id):
        self.id = id #Assign a unique identifier for each node
        self.value = initialValue #Assign a value whether its a node or an edge
        self.neighbours = [] #Create a neighbour list
        exists(id[0] + 2, id[1], self.neighbours) #Add the neighbours to the list
        exists(id[0] - 2, id[1], self.neighbours)
        exists(id[0], id[1] + 2, self.neighbours)
        exists(id[0], id[1] - 2, self.neighbours)
        self.visited = False

    def visit(self):
        self.value = 0 #Visit the node
        self.visited = True

    def __str__(self):
        if self.value == 1: #if its a wall or edge then we assign it a unique colour
            return "\033[1;36m" + str(self.value) + "\033[0m"
        else:
            return "\033[1;35m" + str(self.value) + "\033[0m" #assign the colour
    
class Manager:
    def __init__(self):
        self.graph = [] #Initalize a graph

    def getNode(self, id):
        for node in self.graph: #Iterate through the graph
            if node.id == id: #If the id of node is the one I am trying to finding
                return node #Return the node
            
        return None #return nothing

    def addNode(self, node): #Add node
        self.graph.append(node) #Append node

    def pickRandomNode(self): #Pick a random node
        return choice(self.graph)

    def length(self): #Returns the length of the list
        return len(self.graph)

def exists(x, y, list):
    global size #Grab the size of the node
    if 0 <= x <= 2 * size: #If x and y is in the map
        if 0 <= y <= 2 * size:
            list.append((x, y)) #add it to the list if it exists

def createMaze(mySize): #Size must be odd
    global size
    size = mySize
    map = []

    nodeManager = Manager()
    edgeManager = Manager() #Create the managers

    for row in range((2 * size) + 1): #Create the map, the size is the number of 0's
        tList = [] #create a temporary list
        for column in range((2 * size) + 1):
            if row % 2 == 0 or column % 2 == 0: #If either x or y is even then its an edge else its a node
                edge = Node(1, (row, column)) #Create the Edge
                tList.append(edge) #Add it to the tList
                edgeManager.addNode(edge) #Add the edge to the edge manager
            else:
                node = Node(0, (row, column)) #Create the node
                tList.append(node) #Add it to the tList
                nodeManager.addNode(node) #Add the node to the node manager

        map.append(tList) #Add the tList to the map

    currentNode = nodeManager.getNode((size, size)) #Pick a starting node
    queue = [currentNode] #Add the starting node to the queue
    currentNode.visit() #Visit the starting node

    while len(queue) > 0: #While the queue is empty
        if len(currentNode.neighbours) == 0: #If their are no more neighbours
            currentNode = queue.pop(0) #Backtrack to an earlier node
        else:
            neighbour = choice(currentNode.neighbours) #Pick a random neighbour
            currentNode.neighbours.remove(neighbour) #Remove the current neighbour
            neighbourNode = nodeManager.getNode(neighbour) #Get the neighbour object
            if not(neighbourNode.visited): #If we haven't already visited the neighbour
                currentNodeID = currentNode.id
                edgeID = ((currentNodeID[0] + neighbour[0]) // 2, (currentNodeID[1] + neighbour[1]) // 2) #Compute the midpoint which would be the connecting edge
                edgeManager.getNode(edgeID).visit() #Convert the midpoint into a path 
                neighbourNode.visit() #Visit the neighbour node to prevent cycles
                queue.append(neighbourNode) #Add the neighbour to the queue

    nodeManager.getNode((size, size)).value = 2 #Set the player starting positino
    
    tileMap = []
    for row in map:
        tList = []
        for column in row:
            tList.append(column.value)
        tileMap.append(tList)
    return tileMap