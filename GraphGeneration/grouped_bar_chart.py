import matplotlib.pyplot as plt
import numpy as np

# Example data
events = ['Event1', 'Event2', 'Event3', 'Event4']
anger_male = [5, 2, 4, 3]
sadness_female = [7, 8, 6, 5]
joy_female = [2, 3, 1, 4]
fear_female = [4, 6, 3, 2]

x = np.arange(len(events))  # label locations
width = 0.2  # width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plot data
bars1 = ax.bar(x - width, anger_male, width, label='Anger (Male)')
bars2 = ax.bar(x, sadness_female, width, label='Sadness (Female)')
bars3 = ax.bar(x + width, joy_female, width, label='Joy (Female)')
bars4 = ax.bar(x + 2*width, fear_female, width, label='Fear (Female)')

# Add labels, title, and custom x-axis tick labels
ax.set_xlabel('Events')
ax.set_ylabel('Frequency')
ax.set_title('Emotion Attribution by Gender and Event')
ax.set_xticks(x)
ax.set_xticklabels(events)
ax.legend()

# Show plot
plt.show()
