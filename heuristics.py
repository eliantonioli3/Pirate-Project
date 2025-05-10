from world import World 
import heapq
import math


def manhattan(start, goal) -> int:           
    x1,y1 = start
    x2,y2 = goal
    distanza = abs(y1-y2) + abs(x1-x2)
    return distanza

def manhattanMultiGoal(start,goals) : 

    return min(manhattan(start, goal) for goal in goals)

def euclidean(state, goal):
    x1, y1 = state
    x2,y2 = goal
    distanza = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distanza

def euclideanMultiGoal(start,goals) : 

    return min(euclidean(start, goal) for goal in goals)

def currentHeuristic(start,goals) :

    goal = list(goals)[0]  
    manhattan_distance = manhattan(start, goal)  
    world = World.get_instance()

    if start in world.currents:
        current_direction = world.currents[start]
        dx = goal[0] - start[0] #se dobbiamo muoverci a destra (+) o a sinistra (-)
        dy = goal[1] - start[1] #se dobbiamo muoverci in alto (+) o in basso (-)

        if (dx > 0 and current_direction == 'E') or (dx < 0 and current_direction == 'W') or \
           (dy > 0 and current_direction == 'N') or (dy < 0 and current_direction == 'S'):
            return manhattan_distance * 0  # Penalità ridotta se la corrente aiuta
        
        return manhattan_distance * 2  # Penalità aumentata se la corrente ostacola

    return manhattan_distance



import heapq

mst_cache = {}

def mst(start, goals, weight=2.0):
    
    if not goals:
        return 0

    goals = list(goals)
    goals_key = tuple(sorted(goals))  # Chiave cache:evitare di ricalcolare il MST se già fatto prima.

    # 1. Distanza minima dal punto corrente a un goal(il più vicino)
    min_start_to_goal = min(manhattan(start, g) for g in goals)

    # 2. Calcolo MST (usando cache se esiste):Se il costo MST tra questi goal è già stato calcolato, viene preso dalla cache
    if goals_key in mst_cache:
        mst_cost = mst_cache[goals_key] 
    else:                                 #altrimenti viene calcoalto mst
        visited = set()
        mst_cost = 0
        min_heap = []               #coda di priorità

        start_goal = goals[0]
        visited.add(start_goal)

        for goal in goals[1:]: #Scorre tutti i goal tranne il primo, che è già in visited.
                               #Si inseriscono tutti gli archi tra start_goal e gli altri goals nella heap.
            heapq.heappush(min_heap, (manhattan(start_goal, goal), start_goal, goal)) #tripla

        while min_heap and len(visited) < len(goals):#Si estrae l’arco più corto tra un nodo visitato e uno non visitato
            cost, u, v = heapq.heappop(min_heap)
            if v not in visited:
                visited.add(v)
                mst_cost += cost                 #aggiorno il costo
                for next_goal in goals: #Aggiunge tutti gli archi dal nuovo nodo v verso i restanti non visitati.
                    if next_goal not in visited:
                        heapq.heappush(min_heap, (manhattan(v, next_goal), v, next_goal))

        mst_cache[goals_key] = mst_cost

    # Ritorna euristica combinata
    return weight * min_start_to_goal + mst_cost