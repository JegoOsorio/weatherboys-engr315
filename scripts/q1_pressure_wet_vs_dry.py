"""Q1: Is average station pressure lower on wet days than on dry days?  (Welch two-sample t-test)
Run from the main repo folder:  python scripts/q1_pressure_wet_vs_dry.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from daily_data import build_daily, MIN_READINGS

daily = build_daily()
d = daily[daily["n_press"] >= MIN_READINGS]          # days with enough pressure readings
wet = d.loc[d["wet"], "press_avg"]
dry = d.loc[~d["wet"], "press_avg"]

# ----- metrics -----
diff = wet.mean() - dry.mean()
t, p = stats.ttest_ind(wet, dry, equal_var=False)    # Welch t-test
v1, v2 = wet.var(ddof=1) / len(wet), dry.var(ddof=1) / len(dry)
dof = (v1 + v2) ** 2 / (v1 ** 2 / (len(wet) - 1) + v2 ** 2 / (len(dry) - 1))
margin = stats.t.ppf(0.975, dof) * np.sqrt(v1 + v2)
pooled_sd = np.sqrt((wet.var(ddof=1) + dry.var(ddof=1)) / 2)

print("Q1: Average station pressure, wet days vs dry days (Luray Caverns Airport, 2015-2025)")
print("-" * 70)
print(f"Days used:               {len(d)}  (wet = {len(wet)}, dry = {len(dry)})")
print(f"Wet days mean pressure:  {wet.mean():.2f} hPa  (std dev {wet.std():.2f})")
print(f"Dry days mean pressure:  {dry.mean():.2f} hPa  (std dev {dry.std():.2f})")
print(f"Difference (wet - dry):  {diff:.2f} hPa")
print(f"95% CI of difference:    [{diff - margin:.2f}, {diff + margin:.2f}] hPa")
print(f"Welch t-statistic:       {t:.2f}   (df = {dof:.0f})")
print(f"p-value:                 {p:.3g}")
print(f"Effect size (Cohen's d): {diff / pooled_sd:.2f}")
print("Conclusion:", "wet days have significantly lower pressure (p < 0.05)" if p < 0.05 and diff < 0
      else "no significant difference at the 5% level")

# ----- plot -----
fig, ax = plt.subplots(figsize=(5, 4))
means = [dry.mean(), wet.mean()]
ci = [stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x)) for x in (dry, wet)]
ax.bar(["Dry days", "Wet days"], means, yerr=ci, capsize=6, color=["#d9a441", "#4a7fb5"], width=0.5)
for i, m in enumerate(means):
    ax.text(i, m + ci[i] + 0.3, f"{m:.1f}", ha="center")
ax.set_ylim(970, 990)
ax.set_ylabel("Average station pressure (hPa)")
ax.set_title("Q1: Average pressure on dry vs wet days\n(Luray Caverns Airport, 2015-2025; error bars = 95% CI)", fontsize=10)
ax.text(0.5, -0.14, "Note: y-axis starts at 970 hPa, not 0", transform=ax.transAxes, ha="center", fontsize=8)
fig.tight_layout()
fig.savefig("results/q1_plot.png", dpi=200)
print("Saved results/q1_plot.png")
