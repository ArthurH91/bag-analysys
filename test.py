import matplotlib.pyplot as plt
import numpy as np

# Example data
time = np.linspace(0, 10, 100)
longevity = np.sin(time)

# Calculate the alpha values for fading effect
alpha_values = np.linspace(1, 0, len(time))

# Plot each segment with varying alpha values
plt.figure(figsize=(10, 6))
for i in range(len(time) - 1):
    plt.plot(time[i:i+2], longevity[i:i+2], color='blue', alpha=alpha_values[i])

# Set axis labels
plt.xlabel('Time')
plt.ylabel('Longevity')
plt.title('Line Plot with Fading Transparency')

plt.show()
