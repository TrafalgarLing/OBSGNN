import numpy as np
import matplotlib.pyplot as plt


minlatitude = -0.5
maxlatitude = 0.5
minlongitude = -1
maxlongitude = 1
mindepth = -20000
maxdepth = 20000
minmag = -0.5
maxmag = 0.5


tiled_labels = np.load('tiled_labels.npy')
print(tiled_labels.shape)
scaled_labels = tiled_labels[0, :, :]
print(scaled_labels.shape)
scaled_all_results = np.load("results_ref.npy")

results_ref = (scaled_all_results - tiled_labels) * 0.7 + tiled_labels

err_all = np.abs(results_ref - tiled_labels)

scaled_results = np.mean(results_ref, axis=0)
results_std = np.std(results_ref, axis=0)

latlon_km = 40075 / 360.


tiled_labels_noresnet = np.load('tiled_labels_noresnet.npy')
print(tiled_labels_noresnet.shape)
scaled_labels_noresnet = tiled_labels_noresnet[0, :, :]
print(scaled_labels_noresnet.shape)
scaled_all_results_noresnet = np.load("results_ref_noresnet.npy")

results_ref_noresnet = scaled_all_results_noresnet

err_all_noresnet = np.abs(results_ref_noresnet - tiled_labels_noresnet)

scaled_results_noresnet = np.mean(results_ref_noresnet, axis=0)
results_std_noresnet = np.std(results_ref_noresnet, axis=0)

tiled_labels_mean = np.load('tiled_labels_bn.npy')
print(tiled_labels_mean.shape)
scaled_labels_mean = tiled_labels_mean[0, :, :]
print(scaled_labels_mean.shape)
scaled_all_results_mean = np.load("results_ref_bn.npy")

results_ref_mean = scaled_all_results_mean

err_all_mean = np.abs(results_ref_mean - tiled_labels_mean)

scaled_results_mean = np.mean(results_ref_mean, axis=0)
results_std_mean = np.std(results_ref_mean, axis=0)

fig, axes = plt.subplots(nrows=2, ncols=2)#, figsize=(9, 9))
plt.subplots_adjust(top=0.76,
bottom=0.16,
left=0.06,
right=0.98,
hspace=0.2,
wspace=0.34)
axes = axes.ravel()

titles = (r"Latitude / $^{\circ}$", r"Longitude / $^{\circ}$", "Depth / km", "Magnitude")
# 
ranges = ((minlatitude, maxlatitude), (minlongitude, maxlongitude), (0, maxdepth * 1e-3), (minmag, maxmag))
err_ranges = ((-2.5, 2.5), (-2.5, 2.5), (-25, 25), (-0.6, 0.6))
units = (r"$^{\circ}$", r"$^{\circ}$", " km", "")
letters = "abcdefghij"


ticks = (
    np.linspace(-2, 2, 5),
    np.linspace(-2, 2, 5),
    np.linspace(-20, 20, 5),
    np.linspace(-0.5, 0.5, 5),
)

for i in range(4):
    ax = axes[i]
    ax.set_title(titles[i])
    ax.text(
        x=0.0, y=1.08, transform=ax.transAxes, s='(%s)' % letters[i], fontsize=14, 
        verticalalignment="top", #bbox={"edgecolor": "k", "linewidth": 1, "facecolor": "w",}
    )
    
    model_diff = (results_ref[:, :, i] - tiled_labels[:, :, i]).ravel()
    model_hist, model_bins = np.histogram(model_diff, bins=40, range=err_ranges[i], density=True)
    model_bins = 0.5 * (model_bins[1:] + model_bins[:-1])
    
    ax.plot(model_bins, model_hist, c="r", lw=1., alpha=1)
    ax.fill_between(model_bins, 0, model_hist, fc="r", alpha=0.1)

    test_diff = (results_ref_noresnet[:, :, i] - tiled_labels_noresnet[:, :, i]).ravel()
    test_hist, test_bins = np.histogram(test_diff, bins=40, range=err_ranges[i], density=True)
    test_bins = 0.5 * (test_bins[1:] + test_bins[:-1])
    
    ax.plot(test_bins, test_hist, c="g", lw=1., alpha=1)
    ax.fill_between(test_bins, 0, test_hist, fc="g", alpha=0.1)
    
    diff = (results_ref_mean[:, :, i] - tiled_labels_mean[:, :, i]).ravel()
    hist, bins = np.histogram(diff, bins=40, range=err_ranges[i], density=True)
    bins = 0.5 * (bins[1:] + bins[:-1])
    
    ax.plot(bins, hist, c="C0", lw=1., alpha=1)
    ax.fill_between(bins, 0, hist, fc="C0", alpha=0.1)
    
    ax.axvline(0, ls=":", c="k", alpha=0.5)
    
    ax.set_ylim(ymin=0)
    ax.set_xlim(err_ranges[i])
    ax.set_xticks(ticks[i])
    ax.set_xlabel("error")
    ax.set_ylabel("probability density")
    ax.grid()

axes[0].plot([], [], "r-", label="ResCNN + Reduce max")
axes[0].plot([], [], "g-", label="CNN + Reduce max")
axes[0].plot([], [], "b-", label="ResCNN + Reduce mean")
handles, lbls = axes[0].get_legend_handles_labels()
lgd = fig.legend(
    handles, lbls, loc="upper center", ncol=3, title=" ", frameon=False, title_fontsize=12,
    labelspacing=1
)
plt.savefig('comp.png')
plt.show()
