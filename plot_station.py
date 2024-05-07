# Import modules

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

fig, axes = plt.subplots(nrows=2, ncols=2)#, figsize=(9, 9))

axes = axes.ravel()

titles = (r"Latitude / $^{\circ}$", r"Longitude / $^{\circ}$", "Depth / km", "Magnitude")
ticksx = (
    np.linspace(0, 50, 6),
    np.linspace(0, 50, 6),
    np.linspace(0, 50, 6),
    np.linspace(0, 50, 6),
)
ticksy = (
    np.linspace(0, 4, 5),
    np.linspace(0, 8, 5),
    np.linspace(0, 50, 6),
    np.linspace(0, 0.4, 6),
)
rangesx = ((0, 55), (0, 55), (0, 55), (0, 55))
rangesy = ((0, 4), (0, 8), (0, 50), (0, 0.4))
units = (r"$^{\circ}$", r"$^{\circ}$", " km", "")
letters = "abcd"

x = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5]
y = [[0.16, 0.22, 0.33, 0.40, 0.57, 0.97, 1.75, 2.32, 2.53, 3.46], 
     [0.37, 0.49, 0.68, 1.03, 1.32, 2.45, 3.76, 4.54, 5.38, 6.91], 
     [7.83, 9.52, 11.26, 14.31, 17.58, 19.69, 23.42, 28.51, 31.35, 46.43], 
     [0.151, 0.163, 0.187, 0.193, 0.203, 0.227, 0.257, 0.278, 0.293, 0.319]]
r2 = 1 - sum((scaled_labels - scaled_results) ** 2) / sum((scaled_labels - scaled_labels.mean()) ** 2)
print(r2)

for i in range(4):
    ax = axes[i]
    ax.set_title(titles[i])
    ax.text(
        x=0.0, y=1.1, transform=ax.transAxes, s='(%s)' % letters[i], fontsize=14, 
        verticalalignment="top",
    )
    ax.plot(x, y[i], c='red')
    ax.scatter(x, y[i], c='red')
    ax.set_xlabel("Maximum number of stations", fontsize=12)
    ax.set_ylabel("Mean absolute error", fontsize=12)
    ax.set_xlim(rangesx[i])
    ax.set_ylim(rangesy[i])
    ax.set_xticks(ticksx[i])
    ax.set_yticks(ticksy[i])
    ax.grid()
plt.subplots_adjust(top=0.921,
bottom=0.123,
left=0.085,
right=0.977,
hspace=0.2,
wspace=0.572)
plt.tight_layout()
plt.savefig("fig_S1.png")
plt.show()