import numpy as  np
import random
T = 100         # How many days to simulate

class Burglar:
    def __init__(self,x,y):
        self.s = (x,y) 
        self.active = True

class Discrete_Model:
    l = 1               # Grid spacing
    omega = 1/15        # Dynamic attractiveness decay rate
    Ata = 0.2             # Measures neighborhood effects (ranging from0 to 1)
    theta = 0.56        # Increase in attractiveness due to one burglary event
    A0 = 1/30           # ???
    Gamma = 0.019       # Rate of burglar generation at each site
    dt = 1/100          # Time step
    grid_num = 128

    def __init__(self):
        self.A = np.empty((self.grid_num,self.grid_num))
        self.B = np.ones((self.grid_num,self.grid_num))
        self.n = np.empty((self.grid_num,self.grid_num))
        self.p = np.empty((self.grid_num,self.grid_num))
        self.As0 = np.ones((self.grid_num,self.grid_num))
        self.B_bar = (self.theta * self.Gamma / self.omega)
        self.N_bar = (self.Gamma * self.dt) / (1 - np.e**( -self.A0 * self.dt ))

        self.burglar_list = []
        for x in range(self.grid_num):
            for y in range (self.grid_num):
                for _ in range( int(self.N_bar) ):
                    self.burglar_list.append( Burglar(x,y) )

        self.B *= self.B_bar
        self.As0 *= self.A0
    
    def go_burgle(self,s):
        p = 1 - np.e ** ( -self.A[s] * self.dt )
        if random.random() < p : return True
        else: return False

    def create_burglar(self):
        'return True or False by randomly'
        if random.random() < self.Gamma: return True
        else: return True

    def move_to(self,s):
        x,y = s
        total = 0
        four_dir = ((-1,0), (1,0), (0,1), (0,-1))
        can_go = []
        for dir in four_dir:
            if 0 <= x+dir[0] < self.grid_num and 0 <= y+dir[1] < self.grid_num :
                now = ( dir, self.A[ x+dir[0],y+dir[1] ])
                total += now[1]
                can_go.append(now)
        chose =  random.random() * total
        cnt = 0
        for (dir,attractiveness) in can_go:
            cnt += attractiveness
            if chose < cnt:
                return (x+dir[0], y+dir[1])        

    def simulate(self,t): # Now is time t.
        #step 0: update attractiveness by last state
        self.A = self.As0 + self.B

        #step 1: cirminal loop -> the burglar run
        E = np.zeros((self.grid_num,self.grid_num))
        B_tmp = np.zeros((self.grid_num,self.grid_num))
        four_dir = ((-1,0), (1,0), (0,1), (0,-1))
        
        for burglar in self.burglar_list:
            if self.go_burgle(burglar.s):
                burglar.active = False
                E[ burglar.s ] += 1
            else: 
                burglar.s = self.move_to(burglar.s)
        
        tmp_list = []
        for burglar in self.burglar_list:
            if burglar.active:
                tmp_list.append(burglar)
        self.burglar_list = tmp_list

        #step 2: state update
        for x in range(self.grid_num):
            for y in range(self.grid_num):
                z,sigma = 0,0
                for dir in four_dir:
                    if 0 <= x+dir[0] < self.grid_num and 0 <= y+dir[1] < self.grid_num :
                        sigma += self.B[x+dir[0],y+dir[1]]
                        z += 1

                B_tmp[x,y] = ((1-self.Ata) * self.B[x,y] + self.Ata* (sigma / z)) * (1 - self.omega * self.dt ) + self.theta * E[x,y]
            
        self.B = B_tmp
        
        #step 3: New burglar create
        for x in range(self.grid_num):
            for y in range(self.grid_num):
                if self.create_burglar():
                    self.burglar_list.append( Burglar(x,y) )

if __name__ == "__main__":
    model = Discrete_Model()    
    t = 0
    c = 0
    while t < T:
        model.simulate(t)
        t += model.dt
        if t >= c:
            c += 1
            print(c)
            print(model.A)
        