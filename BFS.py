from search_algorithm import SearchAlgorithm
from queue import Queue
from search_algorithm import Node


class BFS(SearchAlgorithm):
    
    def solve(self, problem) -> list:                   
     
      current_start = problem.init  
      goals = set(problem.goals)  
      total_path = []  
      self.reset_expanded()

      while goals:  
          
          node = Node(current_start, None, None, 0)
          
          
          if problem.isGoal(node.state):
              path_segment = self.extract_solution(node)
              total_path += path_segment  
              goals.remove(node.state) 
              current_start = node.state 
              continue

          
          frontier = Queue()
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
                  child = Node(statoSucc, n, action, n.g + cost)  
                  
                  if statoSucc not in reached:  
                      self.update_expanded(statoSucc)  
                      reached.add(statoSucc)
                      frontier.put(child)

          
          if not solution_found:
              return None

      return total_path  
     

