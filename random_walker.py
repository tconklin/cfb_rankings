import numpy as np
import matplotlib.pyplot as plt
def random_walk(t_exp,n_walkers):
    xy_pos = np.zeros((t_exp,n_walkers,2)) #initialize the array of x and y positions for each walker and time step
    for j in range(n_walkers): #in the range of all walkers
        t = 0 #reset time to 0 for the new walker
        t_min = 0 #reset minimum value of the array
        while t<t_exp: #while the time is less than the experiment time
            rv = np.random.rand(1)*2*np.pi #select a random variable on the range [0,2pi]
            t += -np.log(np.random.rand(1)) #drawing from an exponential distribution
            t_max = int(np.ceil(t)) #set the maximum value for the array indices you'll be setting (this time step)
            xy_pos[t_min+1:t_max,j,0] = xy_pos[t_min,j,0]+np.sin(rv) #move the random walker in the x direction
            xy_pos[t_min+1:t_max,j,1] = xy_pos[t_min,j,1]+np.cos(rv) #move the random walker in the y direction
            t_min = int(np.floor(t)) #set the minimum value for the array indices you'll be setting (next time step)
    plt.plot(xy_pos[:,:,0],xy_pos[:,:,1]) #plots all the walkers
