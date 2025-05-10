from search_algorithm import SearchAlgorithm
from queue import PriorityQueue
from search_algorithm import Node

class AstarNode(Node):
    def __init__(self, state, parent = None, action = None, g = 0, h = 0, w = 1) -> None:
        self.h = h
        self.w = w
        super().__init__(state, parent, action, g)
        
    def __lt__(self, other):
       return self.g + (self.w*self.h) < other.g + (self.w*other.h )      
    
    
class AStar(SearchAlgorithm):
    
    def __init__(self, heuristic = lambda x,y : 0, view = False, w = 1) -> None:
        self.heuristic = heuristic
        self.w = w                                         
        super().__init__(view)

    def solve(self, problem) -> list:

        current_start = problem.init
        goals = set(problem.goals) 
        total_path = []
        self.reset_expanded()

        while goals:
            
            node = AstarNode(current_start, None, None, 0, self.heuristic(current_start, goals), self.w)

            
            if problem.isGoal(node.state):
                path_segment = self.extract_solution(node)
                total_path += path_segment  
                goals.remove(node.state)  
                current_start = node.state  
                continue
        
            frontier = PriorityQueue()
            frontier.put(node)
            reached = set()
            reached.add(node.state)
            
            solution_found = False

            
            while not frontier.empty():
                n = frontier.get()

                
                if problem.isGoal(n.state):  
                    path_segment = self.extract_solution(n)
                    total_path += path_segment  
                    goals.remove(n.state)  
                    current_start = n.state  
                    solution_found = True
                    break

                for action, statoSucc, cost in problem.getSuccessors(n.state):
                    child = AstarNode(statoSucc, n, action, n.g + cost, self.heuristic(statoSucc, goals), self.w)
                    
                    if statoSucc not in reached:
                        self.update_expanded(statoSucc)
                        reached.add(statoSucc)
                        frontier.put(child)

            if not solution_found:
                return None  

        return total_path  
        

