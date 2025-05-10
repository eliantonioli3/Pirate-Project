class World(object):
    def __init__(self, x_lim : int, y_lim : int, walls : set, crabs : set, cactus : set,currents: dict, ends : set):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.walls = walls
        self.crabs = crabs
        self.cactus = cactus
        self.currents = currents
        self.ends = ends
        World._instance = self

    def __str__(self):
        ret = ""
        for x in range(0,self.x_lim):                          
            for y in range(0,self.y_lim):
                if (x,y) in self.walls:
                    ret+="%"
                elif (x, y) in self.crabs:
                    ret += "CR" 
                elif (x, y) in self.cactus:
                    ret += "CA"
                elif (x, y) in self.currents:
                    ret += "CU"
                elif (x, y) in self.ends:
                    ret += "EN" 
                else:
                    ret+=" "
            ret+="\n"
        return ret
    
    @classmethod
    def get_instance(c):
    
        return c._instance