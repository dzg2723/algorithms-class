# Darren Good
# 08-Apr-2019
# Python 3.6.3
# Algorithms
# Chapter 7 Exercise 26

import math, copy, sys, time, random
from xlrd import open_workbook
from xlutils.copy import copy as CP

def buildGraph(phones, towers, range_param):
    """
    Given a list of phones and towers with a range parameter,
    returns a matrix of edges that connect the phones and towers
    """

    # Include source and sink nodes
    total_nodes = len(phones) + len(towers) + 2

    # Indices 0 through (len(phones)-1) will be phone nodes
    # Indices (len(phones)) through (len(phones)+len(towers)-1) will be tower nodes
    # Last two indices will be source and sink, respectively
    graph = []
    num_of_phones = len(phones)
    num_of_towers = len(towers)
    
    # Fill in the graph
    for i in range(total_nodes):
        graph.append([])
        for j in range(total_nodes):

            # Source -> Phones
            if (i == total_nodes-2 and j < num_of_phones):
                graph[i].append([0,1]) # flow,capacity

            # Tower -> Sink
            elif (num_of_phones <= i < (num_of_phones+num_of_towers) and j == total_nodes-1):
                graph[i].append([0,1]) # flow,capacity

            # Phone -> Tower
            elif(i < num_of_phones and num_of_phones <= j < (num_of_phones+num_of_towers)):
                dist = math.sqrt( (phones[i][0]-towers[j-num_of_phones][0])**2 + (phones[i][1]-towers[j-len(phones)][1])**2 )

                # If within distance, add edge between nodes
                if (dist <= range_param):
                    graph[i].append([0,1])
                else:
                    graph[i].append([0,0])

            # No edge between nodes
            else:
                graph[i].append([0,0]) # flow,capacity

    return graph


def findSTPath(graph, start, goal):
    """
    A basic Depth First Search altered from some code Charles supplied
    Returns the first simple path found from the start to goal
    """
    visited = []
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            for i in range(len(graph[vertex])):
                if (graph[vertex][i][1] - graph[vertex][i][0] > 0):
                    if not i in path:
                        if i == goal:
                            return path + [i]
                        else:
                            stack.append((i, path + [i]))
    return None

def bottleneck(graph, path):
    """
    Returns the minimum capacity of the edges in the given path
    """
    capacities = []
    for i in range(len(path)-1):
        start = path[i]
        dest = path[i+1]
        capacities.append(graph[start][dest][1])
    return min(capacities)

def FordFulkerson(graph):
    """
    Uses the Ford Fulkerson algorithm on the given graph to find
    the max flow from the source to sink.
    """
    
    # Keep track of the maximum flow
    max_flow = 0
    
    # Prep a copy to use for the residual graph
    residual = copy.deepcopy(graph)
    
    # Find a starting path through the graph
    path = findSTPath(graph, len(graph)-2, len(graph)-1)

    # More flow can be achieved if there exists a path from the source to sink
    while (path != None):
        flow = bottleneck(residual, path)
        max_flow += flow

        # Update the flow through the graph
        for i in range(len(path)-1):

            # If capacity of edge is zero, then its a backward edge
            if (graph[path[i]][path[i+1]][1] == 0):     
                graph[path[i+1]][path[i]][0] -= flow
                
            # Else it is a forward edge
            else:
                graph[path[i]][path[i+1]][0] += flow
            
        # Update residual graph
        for i in range(len(path)-1):
            residual[path[i]][path[i+1]][1] -= flow # remove flow from available capacity
            
        for i in range(len(path)-1, 0, -1):
            residual[path[i]][path[i-1]][1] += flow # add available capacity on backward edges        


        # Look for another s-t path
        path = findSTPath(residual, len(graph)-2, len(graph)-1)
        
    return [max_flow,graph]

def shiftPhone(fordGraph, phones, towers, moving_phone, final_loc, range_param):
    """
    Moves the moving_phone as far east as possible while keeping it within
    range of its paired tower.

    fordGraph:  The ergonomic flow network (each phone is paired with its own tower)
    phones:  The list of (x,y) coordinates for each phone
    towers:  The list of (x,y) coordinates for each tower
    moving_phone: Index of the moving phone in phones list (will be 0 for given problem)
    final_loc:  The x location of the moving phone once it reaches its destination moving east
    range_param:  The range in which a phone can connect to a tower
    """
    
    num_of_phones = len(phones)
    num_of_towers = len(towers)
    
    # Get coords of moving phone
    phone_x = phones[moving_phone][0]
    phone_y = phones[moving_phone][1]

    # Get the tower that the moving phone is currently connected to
    curr_tower = findConnectedTower(fordGraph, num_of_phones, num_of_towers, moving_phone)

    # Get coords of tower
    tower_x = towers[curr_tower][0]
    tower_y = towers[curr_tower][1]
        
    # Find the point in which the moving phone leaves its tower's connectivity
    # (Intersection between y=phone_y and right half of tower's connectivity range)
    x_intersect = tower_x + math.sqrt((range_param**2) - ((phone_y - tower_y)**2))

    # Moving phone will leave tower's connection range
    if (final_loc > x_intersect):

        # Set the moving phone's coordinates to the edge of tower range
        phones[moving_phone] = (x_intersect, phone_y)

    # Moving phone will reach its destination before reaching intersection point
    else:

        # Set the moving phone's coordinates to its destination
        phones[moving_phone] = (final_loc, phone_y)

    # Return updated coordinates of phones
    return phones

def adjustGraph(baseGraph, fordGraph, phones, towers, moving_phone, range_param):
    """
    Updates network flow graph after a phone has been moved by removing any edges to
    towers out of range and adding edges to towers within range.

    fordGraph:  The ergonomic flow network (each phone is paired with its own tower)
    phones:  The list of (x,y) coordinates for each phone
    towers:  The list of (x,y) coordinates for each tower
    moving_phone: Index of the moving phone in phones list (will be 0 for given problem)
    range_param:  The range in which a phone can connect to a tower
    """
    # Get coords of the moved phone
    phone_x = phones[moving_phone][0]
    phone_y = phones[moving_phone][1]

    # Get the tower that the moving phone is currently connected to
    curr_tower = findConnectedTower(fordGraph, len(phones), len(towers), moving_phone)
    DELTA_X = 0.00001

    for i in range(len(towers)):
        dist = math.sqrt( ( (phone_x + DELTA_X)-towers[i][0])**2 + (phone_y-towers[i][1])**2 )
        curr_tower_x = towers[curr_tower][0]

        # Find all new towers within connecting distance and make sure phone connects to tower that allows it to move further east
##        if (dist <= range_param and towers[i][0] > curr_tower_x): # TODO this is not entirely correct
##            baseGraph[moving_phone][i+len(phones)] = [0,1] # flow,capacity

        if (dist <= range_param):
            baseGraph[moving_phone][i+len(phones)] = [0,1] # flow,capacity
            
        # Remove any existing edges to towers outside of range
        else:
            baseGraph[moving_phone][i+len(phones)] = [0,0] # flow,capacity

    return baseGraph


def findConnectedTower(fordGraph, num_of_phones, num_of_towers, target_phone):
    """
    Returns index of tower that the target phone is currently connected to.
    
    fordGraph:  The ergonomic flow network (each phone is paired with its own tower)
    num_of_phones:  The number of phones in the graph
    num_of_towers:  The number of towers in the graph
    target_phone:  Index in the phones list of the phone of interest.
    """
    
    # Find the target phone's current tower
    curr_tower = -1
    for i in range(num_of_phones, (num_of_phones + num_of_towers)):
        if (fordGraph[target_phone][i][0] == 1):
            curr_tower = i
            break
    
    # Make sure the phone has a current tower
    if (curr_tower < 0):
        print("Error:  Tried to find connected tower, but the graph is not ergonomic. Exiting...")
        raise sys.exit()

    # Return index for tower adjusted to match index in towers list
    return curr_tower - num_of_phones

def buildCertificate(graph, phones, towers, phone_tower_assignments):
    #TODO comment this section
    
    connections = []
    for i in range(len(phones)):
        tower = findConnectedTower(graph, len(phones), len(towers), i)
        connections.append((i,tower))
    phone_tower_assignments.append(connections)
    return phone_tower_assignments
        

def main(phones, towers):

    MAX_DIST = 3    # Radius of connectivity around each tower
    Z = 4           # Distance to the east in which the first phone will travel
    TRAVELER = 0    # Index of phone in phones list that will be traveling east

    """
    ###TRIAL ONE###
    phones = [(2,1), (4,4), (6,1)]      # List of phone locations    
    towers = [(2,4), (4,1), (4,6)]      # List of tower locations

    MAX_DIST = 3    # Radius of connectivity around each tower
    Z = 4           # Distance to the east in which the first phone will travel
    TRAVELER = 0    # Index of phone in phones list that will be traveling east

    ###TRIAL TWO###
    phones = [(0,0), (2,1)]
    towers = [(1,1), (3,1)]

    MAX_DIST = 2    # Radius of connectivity around each tower
    Z = 4           # Distance to the east in which the first phone will travel
    TRAVELER = 0    # Index of phone in phones list that will be traveling east

    ###TRIAL THREE###
    phones = [(0,1), (1,3), (3,2), (5,4)]
    towers = [(1,1), (1,2), (3,4), (5,2)]

    MAX_DIST = 2    # Radius of connectivity around each tower
    Z = 4           # Distance to the east in which the first phone will travel
    TRAVELER = 1    # Index of phone in phones list that will be traveling east
    """

    final_loc = Z + phones[TRAVELER][0] # Final x-coordinate of moving phone

    # Make sure the lengths match, otherwise no matching can be made
    if (len(phones) != len(towers)):
        print("The graph cannot be ergonomic when the number of phones does not match the number of towers!")
        return

    # Keep track of each set of phone-tower connections for certificate
    phone_tower_assignments = []

    # Build the first graph
    baseGraph = buildGraph(phones, towers, MAX_DIST)
    graph = copy.deepcopy(baseGraph)

    while (True):
        # Attempt to find an ergonomic flow through graph
        max_flow, graph = FordFulkerson(graph)

        # Check if graph is ergonomic
        if (max_flow != len(phones)):
            print("Full connectivity could never be maintained or " +
                  "cannot be maintained when phone moves past (%f, %d)" % (phones[TRAVELER][0], phones[TRAVELER][1]))
            break

        # Update list of phone-tower matchings
        phone_tower_assignments = buildCertificate(graph, phones, towers, phone_tower_assignments)
        
        # Move traveling phone east        
        phones = shiftPhone(graph, phones, towers, TRAVELER, final_loc, MAX_DIST)

        # Check if phone reached its destination
        if (phones[TRAVELER][0] == final_loc):
            print(phone_tower_assignments)
            break

        # Update edges from moving phone to towers
        graphcopy = copy.deepcopy(baseGraph)
        graph = adjustGraph(graphcopy, graph, phones, towers, TRAVELER, MAX_DIST)



def constructTrial(num_of_sets):
    XRANGE = (0,5)
    YRANGE = (0,5)

    phones = []
    towers = []

    for i in range(num_of_sets):
        phones.append( (random.randint(XRANGE[0], XRANGE[1]), random.randint(YRANGE[0], YRANGE[1])) )
        towers.append( (random.randint(XRANGE[0], XRANGE[1]), random.randint(YRANGE[0], YRANGE[1])) )

        
##    print("Phones: ", phones)
##    print("Towers: ", towers)
    return (phones, towers)

def testRuns():

    #Path to excel sheet
    excel_path = r"trialData.xls"

    #Opens a book to read from and book to write to
    rbook = open_workbook(excel_path)
    wbook = CP(rbook)

    #Uses the first sheet of the Excel file
    sheet = wbook.get_sheet(0)

    #Track row to write in
    row = 1

    TRIALS = 20
    for trial_size in range(5, 100, 5):

        total_time = 0
        for i in range(TRIALS):
            phones, towers = constructTrial(trial_size)
            start = time.time()
            main(phones, towers)
            end = time.time()
            total_time += (end-start)
            
        average_time = total_time / TRIALS

        sheet.write(row, 0, str(trial_size))
        sheet.write(row, 1, str(average_time))
        row+=1

    wbook.save(excel_path)

        



testRuns()
print("DONE")
    
##phones = [(4, 4), (2, 1), (4, 3), (4, 0), (2, 5)]
##towers = [(5, 3), (2, 3), (0, 0), (2, 3), (5, 0)]

##phones = [(4, 2), (3, 0), (0, 5), (5, 4), (2, 2)]
##towers = [(3, 5), (1, 4), (5, 1), (2, 1), (2, 3)]

##phones = [(5, 1), (3, 4), (1, 0), (0, 4), (0, 4), (4, 2), (0, 5), (2, 2), (3, 2), (0, 0), (2, 0), (4, 0), (1, 2), (1, 4), (2, 3), (4, 2), (3, 1), (4, 2), (0, 3), (1, 1)]
##towers = [(4, 5), (3, 2), (5, 5), (1, 2), (2, 5), (1, 1), (4, 4), (1, 2), (2, 4), (0, 2), (4, 1), (5, 0), (1, 4), (2, 0), (1, 0), (4, 4), (2, 2), (4, 0), (3, 0), (0, 2)]
##main(phones, towers)    
    
