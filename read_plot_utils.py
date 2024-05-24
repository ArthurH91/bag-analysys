import numpy as np

from pathlib import Path
from rosbags.dataframe import get_dataframe
from rosbags.highlevel import AnyReader


def df_get_solution(df, T):
    # solution_data = df.data.to_numpy()
    # N_h = solution_data.shape[0] # Number of times the MPC generates a trajectory across the whole experiment
    # size_q = 7
    # size_v = 7
    # size_u = 7
    # T = int((solution_data[0].shape[0] + 7) / (size_q + size_u + size_v) )
    # q= np.zeros([N_h,T,size_q])
    # v= np.zeros([N_h,T,size_v])
    # u= np.zeros([N_h,T,size_u])
    # for mpc_iter in range(N_h):
    #     for idx in range (T):
    #         q[mpc_iter,idx,:] = solution_data[mpc_iter][idx*(size_q + size_u + size_v):idx*(size_q + size_u + size_v)+size_q]
    #         v[mpc_iter,idx,:] = solution_data[mpc_iter][idx*(size_q + size_u + size_v)+size_q:idx*(size_q + size_u + size_v)+size_q+size_v]
    #         u[mpc_iter,idx,:] = solution_data[mpc_iter][idx*(size_q + size_u + size_v)+size_q+size_v:(idx)*(size_q + size_u + size_v)]
    
    solution_data = df.data.to_numpy()
    N_h = len(solution_data)
    nq,nv,nu = 7,7,7
    
    q = np.zeros((N_h, nq*T))

    # Going through all the timesteps
    for timestep in range(N_h):
        # Going through all the nodes returned by the solver at a given timestep.
        q_timestep = np.zeros(nq * T)
        for n_node in range(T):
            q_timestep_n = solution_data[timestep][n_node * (nq+nv+nu) : n_node * (nq+nv+nu) + nq]
            q_timestep[nq * n_node: nq * n_node + nq] = q_timestep_n
        q[timestep, :] = q_timestep
    return q


def read_jsid_bag(bag_path, controller_name, T):

    topic = f"/{controller_name}/xu_solution",

    with AnyReader([Path(bag_path)]) as reader:
        df_xu_solution = get_dataframe(reader, topic[0], ["data"])
    d_res = {
        "xu_solution": {
            "q,v,u": df_get_solution(df_xu_solution, T),
        },
    }

    return d_res