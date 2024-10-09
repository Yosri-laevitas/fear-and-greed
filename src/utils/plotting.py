import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pandas as pd


def plot_series_analysis(series: pd.Series) -> None:
    """
    Generates a 2x2 plot matrix for a pd.Series object with the following visualizations:
    1. Time series plot
    2. Distribution plot (Histogram and KDE)
    3. Boxplot
    4. QQ plot

    Parameters:
    series : pd.Series
        The input time series data to be analyzed.
    """

    # Set up the 2x2 subplot matrix
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Analysis of Series: {series.name}", fontsize=16)

    # 1. Time series plot (Top Left)
    axes[0, 0].plot(series.index, series.values, label="Time Series", color="b")
    axes[0, 0].set_title("Time Series Plot")
    axes[0, 0].set_xlabel("Time")
    axes[0, 0].set_ylabel("Values")
    axes[0, 0].grid(True)

    # 2. Distribution plot (Top Right: Histogram + KDE)
    sns.histplot(series, kde=True, ax=axes[0, 1], color="g", stat="density")
    axes[0, 1].set_title("Distribution (Histogram & KDE)")
    axes[0, 1].set_xlabel("Values")
    axes[0, 1].set_ylabel("Density")
    axes[0, 1].grid(True)

    # 3. Boxplot (Bottom Left)
    sns.boxplot(x=series, ax=axes[1, 0], color="orange")
    axes[1, 0].set_title("Boxplot")
    axes[1, 0].set_xlabel("Values")
    axes[1, 0].grid(True)

    # 4. QQ plot (Bottom Right)
    stats.probplot(series, dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title("QQ Plot")
    axes[1, 1].get_lines()[1].set_color("red")  # Set the color of the QQ line
    axes[1, 1].grid(True)

    # Adjust layout for better appearance
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def corr_heatmap(data, title):
    corr = data.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, square=True, cmap="coolwarm")
    plt.title(title)
    plt.show()