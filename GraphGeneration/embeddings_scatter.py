import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pickle
from scipy.spatial import ConvexHull


def draw_convex_hull(points, ax, color):
    """
    Draw a convex hull around a set of points.

    Parameters:
    - points: The points to draw the hull around.
    - ax: The matplotlib axes to draw on.
    - color: The color of the hull.
    """
    hull = ConvexHull(points)
    for simplex in hull.simplices:
        ax.plot(points[simplex, 0], points[simplex, 1], color=color)


def tsne_and_scatterplot(
    male_embeddings, female_embeddings, perplexity=30, n_iter=1000, random_state=42
):
    """
    Perform t-SNE on word embeddings and create a scatterplot with clustering visuals.

    Parameters:
    - male_embeddings: List of numpy arrays for male word embeddings.
    - female_embeddings: List of numpy arrays for female word embeddings.
    - perplexity: t-SNE perplexity parameter.
    - n_iter: Number of iterations for t-SNE.
    - random_state: Random state for reproducibility.
    """
    # Combine male and female embeddings
    embeddings = np.vstack([male_embeddings, female_embeddings])

    # Perform t-SNE
    tsne = TSNE(perplexity=perplexity, n_iter=n_iter, random_state=random_state)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Split the transformed embeddings back into male and female
    male_embeddings_2d = embeddings_2d[: len(male_embeddings)]
    female_embeddings_2d = embeddings_2d[len(male_embeddings) :]

    # Create scatterplot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(
        male_embeddings_2d[:, 0],
        male_embeddings_2d[:, 1],
        c="green",
        label="Male Emotion Words",
    )
    ax.scatter(
        female_embeddings_2d[:, 0],
        female_embeddings_2d[:, 1],
        c="red",
        label="Female Emotion Words",
    )

    # Draw convex hulls
    # draw_convex_hull(male_embeddings_2d, ax, "green")
    # draw_convex_hull(female_embeddings_2d, ax, "red")

    # Annotate points with their indices
    for i in range(len(male_embeddings_2d)):
        ax.annotate(
            str(i),
            (male_embeddings_2d[i, 0], male_embeddings_2d[i, 1]),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
            fontsize=8,
            color="black",
        )
    for i in range(len(female_embeddings_2d)):
        ax.annotate(
            str(i + len(male_embeddings_2d)),
            (female_embeddings_2d[i, 0], female_embeddings_2d[i, 1]),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
            fontsize=8,
            color="black",
        )

    # Customize plot
    ax.set_title("Embedding plot of Unique Male and Female Attributed Emotions")
    ax.set_xlabel("t-SNE dimension 1")
    ax.set_ylabel("t-SNE dimension 2")
    ax.legend()
    plt.show()

with open("./embeddings.pkl", "rb") as file:
    embeddings = pickle.load(file)

male_embeddings = embeddings["male"]
female_embeddings = embeddings["female"]

tsne_and_scatterplot(
    male_embeddings=male_embeddings, female_embeddings=female_embeddings
)

# The 