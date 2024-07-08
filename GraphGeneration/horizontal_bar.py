import matplotlib.pyplot as plt

# Data
# Note that the data here is hardcoded form the results
emotions_male_1 = ["surprise", "sadness", "discontent"]
values_male_1 = [99, 64, 14]

emotions_male_2 = ["happy", "encourage", "sadness"]
values_male_2 = [39, 29, 15]

emotions_male_3 = ["surprise", "disgust", "discontent"]
values_male_3 = [234, 123, 46]

emotions_female_1 = ["anger", "unbearable", "disgust"]
values_female_1 = [234, 105, 99]

emotions_female_2 = ["encourage", "satisfaction", "surprise"]
values_female_2 = [83, 47, 33]

emotions_female_3 = ["disgust", "surprise", "bored"]
values_female_3 = [66, 41, 33]

fig, axs = plt.subplots(2, 3, figsize=(12, 4))

# color scheme
# Red: Female 
# Green: Male

# Plot for first male chart
axs[0, 0].barh(emotions_male_1, values_male_1, color="red")
axs[0, 0].set_title("Disgust")
axs[0, 0].spines["top"].set_visible(False)
axs[0, 0].spines["right"].set_visible(False)
for index, value in enumerate(values_male_1):
    axs[0, 0].text(value, index, str(value))

# Plot for second male chart
axs[0, 1].barh(emotions_male_2, values_male_2, color="red")
axs[0, 1].set_title("Pride")
axs[0, 1].spines["top"].set_visible(False)
axs[0, 1].spines["right"].set_visible(False)
for index, value in enumerate(values_male_2):
    axs[0, 1].text(value, index, str(value))

# Plot for third male chart
axs[0, 2].barh(emotions_male_3, values_male_3, color="red")
axs[0, 2].set_title("Anger")
axs[0, 2].spines["top"].set_visible(False)
axs[0, 2].spines["right"].set_visible(False)
for index, value in enumerate(values_male_3):
    axs[0, 2].text(value, index, str(value))

# Plot for first female chart
axs[1, 0].barh(emotions_female_1, values_female_1, color="green")
axs[1, 0].set_title("Surprise")
axs[1, 0].spines["top"].set_visible(False)
axs[1, 0].spines["right"].set_visible(False)
for index, value in enumerate(values_female_1):
    axs[1, 0].text(value, index, str(value))

# Plot for second female chart
axs[1, 1].barh(emotions_female_2, values_female_2, color="green")
axs[1, 1].set_title("Happiness")
axs[1, 1].spines["top"].set_visible(False)
axs[1, 1].spines["right"].set_visible(False)
for index, value in enumerate(values_female_2):
    axs[1, 1].text(value, index, str(value))

# Plot for third female chart
axs[1, 2].barh(emotions_female_3, values_female_3, color="green")
axs[1, 2].set_title("Sadness")
axs[1, 2].spines["top"].set_visible(False)
axs[1, 2].spines["right"].set_visible(False)
for index, value in enumerate(values_female_3):
    axs[1, 2].text(value, index, str(value))

# Common settings
for ax in axs.flat:
    ax.set_xlim(
        0, max(values_male_1 + values_male_2 + values_female_1 + values_female_2) + 10
    )
    ax.set_xlabel("# Instances\n\n")
    ax.set_ylabel("Emotion")
    ax.xaxis.set_label_position("bottom")

# plt.subplots_adjust(wspace=0.5, hspace=0.5, bottom=0.5)

# Add overall titles
fig.suptitle("Emotion Attribution Shift by Gender", fontsize=16)
fig.text(0.5, 0.08, "Female Emotion Attributes", ha="center", fontsize=12, color="black")
fig.text(0.5, 0.47, "Male Emotion Attributes", ha="center", fontsize=12, color="black")


# Adjust layout
plt.tight_layout(rect=[0, 0.01, 1, 0.95])
# plt.tight_layout(pad=0.5)
# plt.subplot_tool()
plt.show()

