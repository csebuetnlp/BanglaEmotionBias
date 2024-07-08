import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.mixture import GaussianMixture
import matplotlib.patches as patches
import pickle


def draw_ellipse(position, covariance, ax, color, alpha=1.0):
    """
    Draw an ellipse with a given position and covariance.

    Parameters:
    - position: The center of the ellipse.
    - covariance: The covariance matrix.
    - ax: The matplotlib axes to draw on.
    - color: The color of the ellipse.
    - alpha: The alpha blending value for transparency.
    """
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)

    for nsig in range(1, 4):
        ellipse = patches.Ellipse(
            position,
            nsig * width,
            nsig * height,
            angle=angle,
            edgecolor=color,
            facecolor="none",
            lw=2,
            alpha=alpha,
        )
        ax.add_patch(ellipse)


def tsne_and_scatterplot(
    male_embeddings,
    female_embeddings,
    perplexity=30,
    n_iter=1000,
    random_state=42,
    n_clusters=3,
):
    """
    Perform t-SNE on word embeddings and create a scatterplot with clustering ellipses.

    Parameters:
    - male_embeddings: List of numpy arrays for male word embeddings.
    - female_embeddings: List of numpy arrays for female word embeddings.
    - perplexity: t-SNE perplexity parameter.
    - n_iter: Number of iterations for t-SNE.
    - random_state: Random state for reproducibility.
    - n_clusters: Number of clusters for GMM.
    """
    # Combine male and female embeddings
    embeddings = np.vstack([male_embeddings, female_embeddings])

    # Perform t-SNE
    tsne = TSNE(perplexity=perplexity, n_iter=n_iter, random_state=random_state)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Fit GMM to find clusters
    gmm = GaussianMixture(
        n_components=n_clusters, covariance_type="full", random_state=random_state
    )
    gmm.fit(embeddings_2d)
    labels = gmm.predict(embeddings_2d)
    cluster_centers = gmm.means_
    covariances = gmm.covariances_

    # Split the transformed embeddings back into male and female
    male_embeddings_2d = embeddings_2d[: len(male_embeddings)]
    female_embeddings_2d = embeddings_2d[len(male_embeddings) :]

    # Create scatterplot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(
        male_embeddings_2d[:, 0],
        male_embeddings_2d[:, 1],
        c="green",
        label="Male Words",
    )
    ax.scatter(
        female_embeddings_2d[:, 0],
        female_embeddings_2d[:, 1],
        c="red",
        label="Female Words",
    )

    # Draw ellipses for clusters
    colors = ["blue", "cyan", "magenta", "yellow", "black"]
    for i, (pos, covar) in enumerate(zip(cluster_centers, covariances)):
        draw_ellipse(pos, covar, ax, color=colors[i % len(colors)])

    # Customize plot
    ax.set_title("t-SNE of Word Embeddings with Clustering Ellipses")
    ax.set_xlabel("t-SNE 1")
    ax.set_ylabel("t-SNE 2")
    ax.legend()
    plt.show()


with open("embeddings.pkl", "rb") as file:
    embeddings = pickle.load(file)

male_embeddings = embeddings["male"]
female_embeddings = embeddings["female"]

tsne_and_scatterplot(
    male_embeddings=male_embeddings, female_embeddings=female_embeddings, n_clusters=5
)
