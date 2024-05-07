import numpy as np
import matplotlib.pyplot as plt


minlatitude = 51
maxlatitude = 60
minlongitude = -164
maxlongitude = -146
maxdepth = 240000
minmag = 0.5
maxmag = 6.5


tiled_labels = np.load('tiled_labels.npy')
print(tiled_labels.shape)
scaled_labels = tiled_labels[0, :, :]
print(scaled_labels.shape)
scaled_all_results = np.load("results_ref.npy")

results_ref = scaled_all_results

err_all = np.abs(results_ref - tiled_labels)

scaled_results = np.mean(results_ref, axis=0)
results_std = np.std(results_ref, axis=0)

fig, axes = plt.subplots(nrows=2, ncols=2)
plt.subplots_adjust(top=0.922,
bottom=0.123,
left=0.119,
right=0.947,
hspace=0.524,
wspace=0.46)
axes = axes.ravel()

titles = (r"Latitude / $^{\circ}$", r"Longitude / $^{\circ}$", "Depth / km", "Magnitude")
ticks = (
    np.linspace(minlatitude, maxlatitude, 7),
    np.linspace(minlongitude, maxlongitude, 7),
    np.linspace(0, maxdepth * 1e-3, 7),
    np.linspace(minmag, maxmag, 7),
)
ranges = ((minlatitude, maxlatitude), (minlongitude, maxlongitude), (0, maxdepth * 1e-3), (minmag, maxmag))
units = (r"$^{\circ}$", r"$^{\circ}$", " km", "")
letters = "abcd"

r2 = 1 - sum((scaled_labels - scaled_results) ** 2) / sum((scaled_labels - scaled_labels.mean()) ** 2)
print(r2)

for i in range(4):
    ax = axes[i]
    ax.set_title(titles[i])
    ax.text(
        x=0.0, y=1.11, transform=ax.transAxes, s='(%s)' % letters[i], fontsize=14, 
        verticalalignment="top", #bbox={"edgecolor": "k", "linewidth": 1, "facecolor": "w",}
    )
    ax.plot(ranges[i], ranges[i], "k--")
    ax.errorbar(
        scaled_labels[:, i], scaled_results[:, i], yerr=results_std[:, i], 
        fmt='none', ms=5, alpha=0.3, mfc="k", ecolor="blue", mec="k", mew=0.8, capsize=2,
    )  
    ax.text(
        x=0.1, y=0.93, transform=ax.transAxes, c="black",
        s=r"mean absolute error: %.2f%s" % (err_all[:, :, i].mean(), units[i])
    )

    ax.text(
        x=0.1, y=0.86, transform=ax.transAxes, c="black",
        s=r"standard deviation: %.2f%s" % (err_all[:, :, i].std(), units[i])
    )
    ax.set_xlabel("Ground truth value", fontsize=12)
    ax.set_ylabel("Predicted value", fontsize=12)
    ax.set_xlim(ranges[i])
    ax.set_ylim(ranges[i])
    ax.set_xticks(ticks[i])
    ax.set_yticks(ticks[i])
    ax.grid()

plt.tight_layout()
plt.savefig("fig_S1.png")
plt.show()