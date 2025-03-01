import numpy as np

from pathlib import Path
from rosbags.dataframe import get_dataframe
from rosbags.highlevel import AnyReader


def trim_dfs(df_lst):
    min_size = len(min([df.index for df in df_lst], key=lambda idx: len(idx)))
    for i in range(len(df_lst)):
        df_lst[i] = df_lst[i][:min_size]
    return df_lst


def index_2_tarr(index):
    # Compute time indices
    idx_arr = index.to_numpy()
    t_delta_arr = idx_arr - idx_arr[0]
    ns2sec = np.vectorize(lambda x: float(x) / 1e9)
    return ns2sec(t_delta_arr)


def index_2_tarr_for_pose_ref(index, start_time):
    # Compute time indices
    idx_arr = index.to_numpy()
    t_delta_arr = idx_arr - start_time
    ns2sec = np.vectorize(lambda x: float(x) / 1e9)
    return ns2sec(t_delta_arr)


def df_col_vec_asarr(df, col_name):
    return np.asarray([l for l in df[col_name]])


def df_col_pose_asarr(df, col_name):
    return np.asarray(
        [
            [
                msg.position.x,
                msg.position.y,
                msg.position.z,
                msg.orientation.x,
                msg.orientation.y,
                msg.orientation.z,
                msg.orientation.w,
            ]
            for msg in df[col_name]
        ]
    )


def df_col_twist_asarr(df, col_name):
    return np.asarray(
        [
            [
                msg.linear.x,
                msg.linear.y,
                msg.linear.z,
                msg.angular.x,
                msg.angular.y,
                msg.angular.z,
            ]
            for msg in df[col_name]
        ]
    )

def read_jsid_bag(bag_path, controller_name):

    topics = [
        f"/{controller_name}/joint_configurations_comparison",
        f"/{controller_name}/joint_velocities_comparison",
        f"/{controller_name}/joint_torques_comparison",
        f"/{controller_name}/absolute_pose_ref",
    ]

    fields = ["commanded", "measured", "error"]

    with AnyReader([Path(bag_path)]) as reader:
        df_q = get_dataframe(reader, topics[0], fields)
        df_dq = get_dataframe(reader, topics[1], fields)
        df_tau = get_dataframe(reader, topics[2], fields)
        df_pose_ref = get_dataframe(reader, topics[3], ["pose"])

    # there might be a one msg difference between the different topics in a same bag -> trim that
    min_size = len(
        min([df_q.index, df_dq.index, df_tau.index], key=lambda idx: len(idx))
    )
    df_q = df_q[:min_size]
    df_dq = df_dq[:min_size]
    df_tau = df_tau[:min_size]
    start_time = df_q.index.to_numpy()[0]
    d_res = {
        "t": index_2_tarr(df_q.index),
        "q": {
            "commanded": df_col_vec_asarr(df_q, "commanded"),
            "measured": df_col_vec_asarr(df_q, "measured"),
            "error": df_col_vec_asarr(df_q, "error"),
        },
        "dq": {
            "commanded": df_col_vec_asarr(df_dq, "commanded"),
            "measured": df_col_vec_asarr(df_dq, "measured"),
            "error": df_col_vec_asarr(df_dq, "error"),
        },
        "tau": {
            "commanded": df_col_vec_asarr(df_tau, "commanded"),
            "measured": df_col_vec_asarr(df_tau, "measured"),
            "error": df_col_vec_asarr(df_tau, "error"),
        },
        "pose_ref": {
            "pose": df_col_pose_asarr(df_pose_ref, "pose"),
            "time": index_2_tarr_for_pose_ref(df_pose_ref.index, start_time),
        },
    }

    return d_res


def read_tsid_bag(bag_path, controller_name):

    topics = [
        f"/{controller_name}/task_pose_comparison",
        f"/{controller_name}/task_twist_comparison",
        f"/{controller_name}/joint_torques_comparison",
    ]

    fields = ["commanded", "measured", "error"]

    with AnyReader([Path(bag_path)]) as reader:
        df_x = get_dataframe(reader, topics[0], fields)
        df_dx = get_dataframe(reader, topics[1], fields)
        df_tau = get_dataframe(reader, topics[2], fields)

    # there might be a one msg difference between the different topics in a same bag -> trim that
    df_x, df_dx, df_tau = trim_dfs([df_x, df_dx, df_tau])

    d_res = {
        "t": index_2_tarr(df_x.index),
        "x": {
            "commanded": df_col_pose_asarr(df_x, "commanded"),
            "measured": df_col_pose_asarr(df_x, "measured"),
            "error": df_col_pose_asarr(df_x, "error"),
        },
        "dx": {
            "commanded": df_col_twist_asarr(df_dx, "commanded"),
            "measured": df_col_twist_asarr(df_dx, "measured"),
            "error": df_col_twist_asarr(df_dx, "error"),
        },
        "tau": {
            "commanded": df_col_vec_asarr(df_tau, "commanded"),
            "measured": df_col_vec_asarr(df_tau, "measured"),
            "error": df_col_vec_asarr(df_tau, "error"),
        },
    }

    return d_res

