"""Q2: Is the daily temperature range (max - min) smaller on wet days?  (Welch two-sample t-test)
Run from the main repo folder:  python scripts/q2_temp_range_wet_vs_dry.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from daily_data import build_daily, MIN_READINGS

daily = build_daily()
d = daily[daily["n_temp"] >= MIN_READINGS]
wet = d.loc[d["wet"], "temp_range"]
dry = d.loc[~d["wet"], "temp_range"]

diff = wet.mean() - dry.mean()
t, p = stats.ttest_ind(wet, dry, equal_var=False)
v1, v2 = wet.var(ddof=1) / len(wet), dry.var(ddof=1) / len(dry)
dof = (v1 + v2) ** 2 / (v1 ** 2 / (len(wet) - 1) + v2 ** 2 / (len(dry) - 1))
margin = stats.t.ppf(0.975, dof) * np.sqrt(v1 + v2)
pooled_sd = np.sqrt((wet.var(ddof=1) + dry.var(ddof=1)) / 2)

print("Q2: Daily temperature range (max - min), wet days vs dry days (Luray Caverns Airport, 2015-2025)")
print("-" * 70)
print(f"Days used:               {len(d)}  (wet = {len(wet)}, dry = {len(dry)})")
print(f"Wet days mean range:     {wet.mean():.2f} deg C  (std dev {wet.std():.2f})")
print(f"Dry days mean range:     {dry.mean():.2f} deg C  (std dev {dry.std():.2f})")
print(f"Difference (wet - dry):  {diff:.2f} deg C")
print(f"95% CI of difference:    [{diff - margin:.2f}, {diff + margin:.2f}] deg C")
print(f"Welch t-statistic:       {t:.2f}   (df = {dof:.0f})")
print(f"p-value:                 {p:.3g}")
print(f"Effect size (Cohen's d): {diff / pooled_sd:.2f}")
print("Conclusion:", "wet days have a significantly smaller range (p < 0.05)" if p < 0.05 and diff < 0
      else "no significant difference at the 5% level")

fig, ax = plt.subplots(figsize=(5, 4))
means = [dry.mean(), wet.mean()]
ci = [stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x)) for x in (dry, wet)]
ax.bar(["Dry days", "Wet days"], means, yerr=ci, capsize=6, color=["#d9a441", "#4a7fb5"], width=0.5)
for i, m in enumerate(means):
    ax.text(i, m + ci[i] + 0.3, f"{m:.1f}", ha="center")
ax.set_ylim(0, 16)
ax.set_ylabel("Daily temperature range, max - min (deg C)")
ax.set_title("Q2: Daily temperature range on dry vs wet days\n(Luray Caverns Airport, 2015-2025; error bars = 95% CI)", fontsize=10)
fig.tight_layout()
fig.savefig("results/q2_plot.png", dpi=200)
print("Saved results/q2_plot.png")
