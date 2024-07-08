import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Example data
data = {
    "Event": ["Event1", "Event2", "Event3", "Event4"],
    "Anger (Male)": [5, 2, 4, 3],
    "Sadness (Female)": [7, 8, 6, 5],
    "Joy (Female)": [2, 3, 1, 4],
    "Fear (Female)": [4, 6, 3, 2],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Set Event as index
df.set_index("Event", inplace=True)

# Create a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df, annot=True, cmap="coolwarm", linewidths=0.5)

# Add title and labels
plt.title("Emotion Attribution by Gender and Event")
plt.xlabel("Emotion (Gender)")
plt.ylabel("Event")

# Show plot
plt.show()
