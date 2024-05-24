import numpy as np
import matplotlib.pyplot as plt

# Sample data for demonstration
# Assume each state has two dimensions for simplicity (e.g., position and velocity)
# Actual states (X0) over 10 time steps
X0 = np.array([[0, 0], [0.1, 0.2], [0.3, 0.4], [0.6, 0.5], [0.8, 0.7],
               [1.0, 0.9], [1.2, 1.0], [1.4, 1.2], [1.5, 1.3], [1.6, 1.4]])

# Predicted states (X) for each time step, prediction horizon = 5
X = np.array([[[0, 0], [0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5], [0.5, 0.6]],
              [[0.1, 0.2], [0.2, 0.4], [0.3, 0.5], [0.4, 0.6], [0.5, 0.7], [0.6, 0.8]],
              [[0.3, 0.4], [0.4, 0.5], [0.5, 0.6], [0.6, 0.7], [0.7, 0.8], [0.8, 0.9]],
              [[0.6, 0.5], [0.7, 0.6], [0.8, 0.7], [0.9, 0.8], [1.0, 0.9], [1.1, 1.0]],
              [[0.8, 0.7], [0.9, 0.8], [1.0, 0.9], [1.1, 1.0], [1.2, 1.1], [1.3, 1.2]],
              [[1.0, 0.9], [1.1, 1.0], [1.2, 1.1], [1.3, 1.2], [1.4, 1.3], [1.5, 1.4]],
              [[1.2, 1.0], [1.3, 1.1], [1.4, 1.2], [1.5, 1.3], [1.6, 1.4], [1.7, 1.5]],
              [[1.4, 1.2], [1.5, 1.3], [1.6, 1.4], [1.7, 1.5], [1.8, 1.6], [1.9, 1.7]],
              [[1.5, 1.3], [1.6, 1.4], [1.7, 1.5], [1.8, 1.6], [1.9, 1.7], [2.0, 1.8]],
              [[1.6, 1.4], [1.7, 1.5], [1.8, 1.6], [1.9, 1.7], [2.0, 1.8], [2.1, 1.9]]])

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the actual states using plt.scatter
plt.scatter(X0[:, 0], X0[:, 1], color='blue', label='Actual States (X0)')

# Plot the predicted states with varying transparency
for t in range(len(X0)):
    alpha = np.linspace(1.0, 0.2, X.shape[1])
    for k in range(X.shape[1]):
        plt.scatter(X[t, k, 0], X[t, k, 1], color='red', alpha=alpha[k])

plt.xlabel('State Dimension 1')
plt.ylabel('State Dimension 2')
plt.legend()
plt.title('MPC Predictions and Actual States')
plt.grid(True)
plt.show()
