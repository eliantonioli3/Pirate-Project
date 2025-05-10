from search_problem import SearchProblem
from world import World


class PathFinding(SearchProblem):
    def __init__(self, init, goals, world: World, diagonal = True):

        self.diagonal = diagonal
        if diagonal:
            self.actions = ['N','S','W','E','NE', 'NW', 'SE', 'SW']
        else :
            self.actions = ['N','S','W','E']
        self.world = world
        self.goals = set(goals)
        
        self.costs = {
            
            "crab": 3,    
            "cactus":5   
        }
        
        print(f"Obiettivi inizializzati: {self.goals}")
        super().__init__(init, None, [(a,1) for a in self.actions])    

    def getSuccessors(self, state) -> set:           
        succ = set()   
                                     
        for a in self.actions:
            if a == 'S':
                next_state = (state[0], state[1]-1)    
            elif a == 'N':
                next_state = (state[0], state[1]+1)
            elif a == 'W':
                next_state = (state[0]-1, state[1])
            elif a == 'E':
                next_state = (state[0]+1, state[1])
            elif a == 'NE':
                next_state = (state[0] + 1, state[1] + 1)
            elif a == 'NW':
                next_state = (state[0] - 1, state[1] + 1)
            elif a == 'SE':
                next_state = (state[0] + 1, state[1] - 1)
            elif a == 'SW':
                next_state = (state[0] - 1, state[1] - 1)
            if self.is_walkable(next_state):    

                terreno = self.terrainType(next_state)                         
                cost = self.costs.get(terreno,1)                            
                if terreno == "current":
                    
                    current = self.world.currents[next_state]
                    cost = self.currentDirection(a,current,cost)
               
                succ.add((a, next_state,cost))
        
        return succ
    
    def isInTheLimits(self, state):
        return state[0] >=0 and state[0] <= self.world.x_lim and state[1] >=0 and state[1] <= self.world.y_lim
    
    
    def terrainType(self, state):

        if state in self.world.crabs :
            return "crab"
        if state in self.world.cactus :
            return "cactus"
        if state in self.world.currents :
            return "current"
        if state in self.world.ends :
            return "end"
        return "normal"
    
    def currentDirection(self, a,current, cost):

        if(current == 'N'):
          current = 'S'

        if(current == 'S'):
          current = 'N'

        if (a == 'E' and current == 'E') or (a == 'W' and current == 'W') or (a == 'N' and current == 'N') or (a == 'S' and current == 'S'):
             cost = 0
              
        elif (a == 'E' and current == 'W') or (a == 'W' and current == 'E') or (a == 'N' and current == 'S') or (a == 'S' and current == 'N'):
             cost =cost * 2 
             
        return cost
    
    def is_walkable(self, state):
        
        if not self.isInTheLimits(state):
            return False

        if state in self.world.walls:
            return False
        
        return True
   
        
    def isGoal(self, state):
        
        if state in self.goals :
            self.goals.remove(state)
            return True
    
    



