import os
import numpy as np

import matplotlib.pyplot as plt
# import mpc_utils
# import pin_utils
# import example_robot_data
# import pinocchio as pin
from read_plot_utils import read_jsid_bag
from matplotlib.collections import LineCollection
import matplotlib
from matplotlib import cm
CONTROLLER_NAME = "ctrl_mpc_linearized"
dt_ocp = 1e-1
T = 10
nq = 7


bag_name = "ctrl_mpc_linearized_expe"
bag_path = "/home/arthur/Desktop/Code/Ros/bag-analysys/ctrl_mpc_linearized_expe.bag"
data = read_jsid_bag(bag_path=bag_path, controller_name=CONTROLLER_NAME, T=T)
q = data["xu_solution"]
q = q["q,v,u"]

N_h = len(q)

def get_q0(q_time_step):
    return(q_time_step[0:nq])

def plot_q0i(i):
    q0 = np.zeros((len(q), nq))
    for time_step, q_time_step in enumerate(q):
        q0[time_step, :] = get_q0(q_time_step)
    plt.plot(q0[:,i], "-o", label = "q0")

def get_qi(q_time_step, i):
    return q_time_step[i * nq: (i+1) * nq] 

# plot_q0i(1)

# Prepare data for scatter plot of predicted states
pred_time_steps = []
pred_values = []
pred_colors = []


for t in range(len(q)):
    colors = np.linspace(0, 0.8, T)
    q_time_step = q[t]
    time_start = t * dt_ocp * T
    time_span = np.linspace(time_start, time_start + T * dt_ocp, T)
    for i in range(T):
        qi = get_qi(q_time_step, i)
        pred_time_steps.append(time_span[i])
        pred_values.append(qi[1])
        pred_colors.append(colors[i])

# Create color map
my_colors = cm.Greys(pred_colors)

# Scatter plot of predicted states
plt.scatter(pred_time_steps, pred_values, s=10, zorder=1, c=my_colors)
plt.xlabel('Time Step')
plt.ylabel('State Value')
plt.title('MPC Predictions and Actual States Over Time')
plt.legend()
plt.grid(True)
plt.show()

#  Plot state data
plt.show()
