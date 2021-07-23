import argparse
import numpy as  np
import os
import random

from plot_map import Plot2DArray


class Burglar(object):
    def __init__(self,x,y):
        self.s = (x,y) 
        self.active = True


class Discrete_Model(object):
    """
    This class impelements the discrete model proposed by Short et al. (2008), simulating 
    crime hotspots spatial development. 
    """

    def __init__(self, args, random_seed=6000):
        super().__init__()
        random.seed(random_seed)
        self.init_params(args)
        self.init_grid(args)
        self.init_burglar(args)

        print('args: {}'.format(args))
        

    @staticmethod
    def setup_paper_params(args):
        "the parameters proposed in the paper for the experiments of Fig.3"
        if args.expset == 'a':
            args.eta = 0.2
            args.theta = 0.56
            args.Gamma = 0.019
        if args.expset == 'b':
            args.eta = 0.2
            args.theta = 5.6
            args.Gamma = 0.002
        if args.expset == 'c':
            args.eta = 0.03
            args.theta = 0.56
            args.Gamma = 0.019
        if args.expset == 'd':
            args.eta = 0.03
            args.theta = 5.6
            args.Gamma = 0.002
        return args

    
    def init_params(self, args):
        self.l = args.l
        self.dt = args.dt
        self.omega = args.omega
        self.A0 = args.A0
        self.eta = args.eta
        self.theta = args.theta
        self.Gamma = args.Gamma
        self.grid_num = args.grid_num

        # initial value of B_s(0) of every lattice s 
        self.B_bar = (self.theta * self.Gamma / self.omega)

        # initial # of burglar in every lattice
        self.N_bar = (self.Gamma * self.dt) / (1 - np.e**( -self.A0 * self.dt ))


    def init_grid(self, args):
        grid_size = (self.grid_num, self.grid_num)
        self.A = np.empty(grid_size)
        self.As0 = np.ones((self.grid_num,self.grid_num)) * self.A0
        self.B = np.ones(grid_size) * self.B_bar
        

    def init_burglar(self, args):
        self.burglar_list = []
        for x in range(self.grid_num):
            for y in range (self.grid_num):
                for _ in range( int(self.N_bar) ):
                    self.burglar_list.append( Burglar(x,y) )


    def go_burgle(self,s):
        p = 1 - np.e ** ( -self.A[s] * self.dt )
        if random.random() < p : return True
        else: return False


    def create_burglar(self):
        "return True or False base on a constant rate Gamma"
        if random.random() < self.Gamma: return True
        else: return False


    def move_to(self,s):
        x,y = s
        total = self.neighbor_A[s]
        four_dir = ((-1,0), (1,0), (0,1), (0,-1))
        chosen =  random.random() * total
        cnt = 0
        for dir in four_dir:
            if 0 <= x+dir[0] < self.grid_num and 0 <= y+dir[1] < self.grid_num :
                cnt += self.A[ x+dir[0],y+dir[1] ]
                if chosen < cnt:
                    return (x+dir[0], y+dir[1])    
                


    def simulate(self, t):      # Now is time t.
        #step 0: update attractiveness by last state
        self.A = self.As0 + self.B
        # pre-calculate neigbor's attractive
        self.neighbor_A = np.zeros((self.grid_num, self.grid_num))
        self.neighbor_A[:-1,:] += self.A[ 1:,:]
        self.neighbor_A[ 1:,:] += self.A[:-1,:]
        self.neighbor_A[:,:-1] += self.A[:, 1:]
        self.neighbor_A[:, 1:] += self.A[:,:-1]

        #step 1: cirminal loop -> the burglar run
        E = np.zeros((self.grid_num,self.grid_num))
        B_tmp = np.zeros((self.grid_num,self.grid_num))
        
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
                z,sigma = 4,0
                if 0 == x or x == self.grid_num-1 : z -= 1
                if 0 == y or y == self.grid_num-1 : z -= 1 
                sigma = (self.neighbor_A[x,y])/z - self.A0
                B_tmp[x,y] = ((1-self.eta) * self.B[x,y] + self.eta* sigma ) * (1 - self.omega * self.dt ) + self.theta * E[x,y]  
        
        self.B = B_tmp
        
        #step 3: New burglar create
        for x in range(self.grid_num):
            for y in range(self.grid_num):
                if self.create_burglar():
                    self.burglar_list.append( Burglar(x,y) )



if __name__ == "__main__":

    # parameters
    parser = argparse.ArgumentParser()
    ## the param sets for experiment a~d of Fig.3 in the paper (Short, 2008)
    parser.add_argument('--expset', type=str, default='', help='valid input: a, b, c, d.')

    ## param for the model
    parser.add_argument('--T', type=int, default=200, help='How many days to simulate')
    parser.add_argument('--grid_num', type=int, default=128, help='')
    parser.add_argument('--l', type=float, default=1, help='Grid spacing')
    parser.add_argument('--dt', type=float, default=1/100, help='Time step')
    parser.add_argument('--omega', type=float, default=1/15, help='Dynamic attractiveness decay rate')
    parser.add_argument('--A0', type=float, default=1/30, help='???')
    parser.add_argument('--eta', type=float, default=0.03, help='Measures neighborhood effects (ranging from 0 to 1)')
    parser.add_argument('--theta', type=float, default=0.56, help='Increase in attractiveness due to one burglary event')
    parser.add_argument('--Gamma', type=float, default=0.002, help='Rate of burglar generation at each site')
    
    ## additional param
    parser.add_argument('--plot_rate', type=float, default=1., help='plot the fig every plot_rate days')
    args = parser.parse_args()

    # setup
    args = Discrete_Model.setup_paper_params(args)
    filename_prefix = "expset({})_eta_{}_theta_{}_Gamma_{}".format(args.expset, args.eta, args.theta, args.Gamma) if args.expset else ""

    model = Discrete_Model(args)
    plotter = Plot2DArray(filename_prefix=filename_prefix)

    
    # start simulation
    # t = 0
    # c = 0
    # while t < args.T:
    #     model.simulate(t)
    #     t += args.dt
    #     if t >= c:
    #         plotter.plot_map(model.A, t)
    #         c += args.plot_rate
    img_dir = os.path.join(os.getcwd(), 'imgfiles', filename_prefix)
    plotter.save_gif(img_dir=img_dir, args=args)
    plotter.save_mp4(img_dir=img_dir, args=args)