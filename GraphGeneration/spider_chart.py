import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame="circle"):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = "radar"
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location("N")

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == "circle":
                return Circle((0.5, 0.5), 0.5)
            elif frame == "polygon":
                return RegularPolygon((0.5, 0.5), num_vars, radius=0.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == "circle":
                return super()._gen_axes_spines()
            elif frame == "polygon":
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(
                    axes=self,
                    spine_type="circle",
                    path=Path.unit_regular_polygon(num_vars),
                )
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(
                    Affine2D().scale(0.5).translate(0.5, 0.5) + self.transAxes
                )
                return {"polar": spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data():
   
    df1 = pd.read_csv(
        "./ordered_list_I1_latest.csv"
    )
    df2 = pd.read_csv(
        "./ordered_list_I2_latest.csv"
    )

    i1_male_counts = df1["male_count"].tolist()
    i1_female_counts = df1["female_count"].tolist()

    i2_male_counts = df2["male_count"].tolist()
    i2_female_counts = df2["female_count"].tolist()
    data = [
        ["1", "2", "3", "4", "5", "6", "7", "8"],
        (
            "Results for Prompt Template: I1",
            [i1_male_counts, i1_female_counts],
        ),
        (
            "Results for Prompt Template: I2",  # ['বিস্ময়', 'আনন্দ', 'বিরক্তি', 'ক্রোধ', 'দুঃখ', 'উৎসাহ', 'গর্ব', 'হাসি', 'উদাস', 'আহ্বান', 'সন্তুষ্টি', 'ক্ষোভ']
            [i2_male_counts, i2_female_counts],
        ),
    ]

    return data


def normalize_data(data):
    max_value = max(max(sublist) for sublist in data)
    normalized_data = [[d / max_value for d in dataset] for dataset in data]
    return normalized_data, max_value


def get_rgrid_labels(max_value, num_labels=5):
    return [round(max_value * i / num_labels) for i in range(1, num_labels + 1)]


if __name__ == "__main__":
    # N = 9
    N = 8
    theta = radar_factory(N, frame="polygon")

    data = example_data()
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(
        figsize=(6, 12), nrows=2, subplot_kw=dict(projection="radar")
    )
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ["g", "r", "g", "m", "y"]

    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axs.flat, data):
        normalized_case_data, max_value = normalize_data(case_data)
        max_value = (max_value // 500 + 1) * 500
        rgrid_labels = get_rgrid_labels(max_value)
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], labels=rgrid_labels, angle=67)

        ax.set_title(
            title,
            weight="bold",
            size="large",
            position=(0.5, 1.1),
            horizontalalignment="center",
            verticalalignment="center",
        )
        for d, color in zip(normalized_case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25, label="_nolegend_")
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    # labels = ("Factor 1", "Factor 2", "Factor 3", "Factor 4", "Factor 5")
    labels = ("male emotions", "female emotions")
    legend = axs[0].legend(labels, loc=(0.9, 0.95), labelspacing=0.1, fontsize="small")

    plt.show()
