from queue import PriorityQueue
from search_algorithm import SearchAlgorithm
from collections import deque
from search_algorithm import Node


class WebNode(Node):
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        super().__init__(state, parent, action, g)             
        self.h = h              

    def __lt__(self, other):
        
        return self.h < other.h
    

class WebEX(SearchAlgorithm):

    def solve(self, problem) -> list:
        start = problem.init
        goals = set(problem.goals)
        self.reset_expanded()

        # Espansione iniziale "web" da tutti i goal
        web_reach = {}  
        max_web_depth = 10  # profondità massima dell'espansione "web"

        for goal in goals:
            frontier = [(goal, 0)]
            visited = {goal}
            web_reach[goal] = goal
            self.update_expanded(goal)

            while frontier:
                state, depth = frontier.pop(0)
                if depth >= max_web_depth:
                    continue

                for action, succ, cost in problem.getSuccessors(state):
                    if succ not in visited:
                        visited.add(succ)
                        web_reach[succ] = goal
                        self.update_expanded(succ)
                        frontier.append((succ, depth + 1))

        total_path = []
        current_start = start
        remaining_goals = set(goals)

        def manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        while remaining_goals:
            # --- PRIMO STEP: arrivo fino a una web ---
            frontier = PriorityQueue()
            frontier.put((WebNode(current_start, None, None, 0, 0)))  
            visited = set()
            entry_node = None

            while not frontier.empty():
                node = frontier.get()  

                if node.state in web_reach and web_reach[node.state] in remaining_goals:
                    entry_node = node
                    break

                visited.add(node.state)

                for action, succ, cost in problem.getSuccessors(node.state):
                    if succ not in visited:
                        h = min(manhattan(succ, g) for g in remaining_goals)  # euristica greedy
                        child = WebNode(succ, node, action, node.g + cost, h)
                        self.update_expanded(succ)
                        frontier.put((child))  

            if entry_node is None:
                return None  # non sono riuscito a entrare in nessuna web

            # --- SECONDO STEP: dalla web arrivo DAVVERO al goal ---
            goal_target = web_reach[entry_node.state]
            path_to_goal = self.local_search(problem, entry_node.state, goal_target)

            if path_to_goal is None:
                return None  # non riesco a finire il collegamento

            total_path += self.extract_solution(entry_node) + path_to_goal
            current_start = goal_target
            remaining_goals.remove(goal_target)

        return total_path

    def local_search(self, problem, start, goal):
        """Mini-BFS dalla posizione start per raggiungere goal"""
        frontier = deque()
        frontier.append(WebNode(start, None, None, 0, 0))
        visited = {start}

        while frontier:
            node = frontier.popleft()
            if node.state == goal:
                return self.extract_solution(node)

            for action, succ, cost in problem.getSuccessors(node.state):
                if succ not in visited:
                    visited.add(succ)
                    child = WebNode(succ, node, action, node.g + cost, 0)  
                    frontier.append(child)
                    self.update_expanded(succ)

        return None  