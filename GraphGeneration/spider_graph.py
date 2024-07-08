import matplotlib.pyplot as plt
import numpy as np


def read_word_counts_from_file(file_name):
    word_counts = {}
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                word, count = line.strip().split(": ")
                word_counts[word.strip('"')] = int(count)
        return word_counts
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
        return None
    except ValueError:
        print(
            "Error reading data from the file. Please make sure the file contains words and their counts in the correct format."
        )
        return None


def select_top_attributes(word_counts1, word_counts2, num_attributes=12):
    common_attributes = set(word_counts1.keys()) & set(word_counts2.keys())
    if not common_attributes:
        print("There are no common attributes between the files.")
        return []

    # Select top 10-12 common attributes based on counts
    sorted_common_attributes = sorted(
        common_attributes, key=lambda w: word_counts1[w] + word_counts2[w], reverse=True
    )
    return sorted_common_attributes[
        : min(num_attributes, len(sorted_common_attributes))
    ]


def plot_spider_graph(words, counts, title):
    num_vars = len(words)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    words += words[:1]
    counts += counts[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], words)
    ax.plot(angles, counts, linewidth=2, linestyle="solid")
    ax.fill(angles, counts, "b", alpha=0.1)
    plt.title(title)
    plt.savefig(title + ".png")
    # plt.show()


def main():
    file1 = "top_20_common_woman_v2.txt"
    file2 = "top_20_common_man_v2.txt"

    word_counts_woman = read_word_counts_from_file(file1)
    word_counts_man = read_word_counts_from_file(file2)

    if word_counts_woman and word_counts_man:
        selected_attributes = select_top_attributes(word_counts_woman, word_counts_man)

        if selected_attributes:
            # Extract counts for selected attributes
            counts_woman = [word_counts_woman[attr] for attr in selected_attributes]
            counts_man = [word_counts_man[attr] for attr in selected_attributes]

            print("Selected Attributes:", selected_attributes)
            print(counts_man)
            print(counts_woman)

            # plot_spider_graph(selected_attributes, counts_woman, "Woman Attributes")
            # plot_spider_graph(selected_attributes, counts_man, "Man Attributes")
        else:
            print("Failed to select common attributes. Exiting.")
    else:
        print("Failed to read word counts from files. Exiting.")


if __name__ == "__main__":
    main()
