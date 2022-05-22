import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

print("Chapter 5 :Transient Conduction")

size = ['length_X', 'length_Y']
surface = ['u_top' , 'u_right ',' u_bottom' , 'u_left' , 'u_inside']
value = ['k' , 'density' , 'specific_heat' ,'node_size ', 'Time']
value2cal = ['alpha ','delta_t ','max_iter_time' ,'gamma']


def Initial_condition():

    global size , surface
    
    u = np.empty((value2cal[2], size[0] ,size[1]))

    # Set the initial condition
    u.fill(surface[4])

    # Set the boundary conditions
    u[:, (size[0]-1):, :] = surface[0]
    u[:, :, :1] = surface[3]
    u[:, :1, 1:] = surface[2]
    u[:, :, (size[1]-1):] = surface[1]

    u[: , 0,                   0]     =  (surface[2]  + surface[3])/2
    u[: , 0,           (size[1]-1)]  =  (surface[2]  + surface[1])/2
    u[:, (size[0]-1), (size[1]-1)]  =  (surface[0]     + surface[1])/2
    u[:, (size[0]-1),            0]  =  (surface[0]     + surface[3])/2

    return u

def calculate(u):
    z = 0
    for k in range(0, value2cal[2]-1, 1):
        for i in range(1, size[0]-1, value[3]):
            for j in range(1, size[1]-1, value[3]):
                u[k + 1, i, j] = value2cal[3] * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
                
                print("계산중ㅠㅠㅠㅠ")
                print("계산중ㅜㅜㅜㅜㅜㅜㅜ")
                
    return u

def plotheatmap(u_k, k):
    # Clear the current plot figure

    t = time.time()
    plt.clf()
    plt.title(f"Temperature at t = {k*value2cal[1]:.3f} Time")              # 시간 = 반복횟수 * 시간
    plt.xlabel("x")
    plt.ylabel("y")
    plt.pcolormesh(u_k, cmap=plt.cm.jet)
    plt.colorbar()

    return plt

def Animate_heatmap():

    u = calculate(Initial_condition())

    def animate(k):
        plotheatmap(u[k], k)

    anim = animation.FuncAnimation(plt.figure(), animate, interval=10, frames = value2cal[2], repeat=False)
    anim.save("Result Animation.gif")

    plt.pcolormesh(u[value2cal[2]-1], cmap=plt.cm.jet)
    plt.savefig('Result picture.png')
    print("Done!")
