import example_robot_data
import pinocchio as pin
import yaml
import numpy as np


def get_croco_reaching():
    with open("/home/arthur/Desktop/Code/Ros/bag-analysys/controller_configs.yaml", "r") as file:
        params = yaml.safe_load(file)
        params = params["ctrl_mpc_linearized"]

    return params