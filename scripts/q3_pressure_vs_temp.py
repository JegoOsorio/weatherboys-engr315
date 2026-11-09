"""Q3: How does average station pressure change with average temperature?  (linear fit + correlation)
Run from the main repo folder:  python scripts/q3_pressure_vs_temp.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from daily_data import build_daily, MIN_READINGS

daily = build_daily()
d = daily[(daily["n_press"] >= MIN_READINGS) & (daily["n_temp"] >= MIN_READINGS)]
x, y = d["temp_avg"], d["press_avg"]

fit = stats.linregress(x, y)
r_s, p_s = stats.spearmanr(x, y)
margin = stats.t.ppf(0.975, len(d) - 2) * fit.stderr

print("Q3: Average station pressure vs average temperature (Luray Caverns Airport, 2015-2025)")
print("-" * 70)
print(f"Days used:                 {len(d)}")
print(f"Fitted line:               pressure = {fit.slope:.3f} * temp + {fit.intercept:.1f}   (hPa, temp in deg C)")
print(f"Slope:                     {fit.slope:.3f} hPa per deg C   (95% CI [{fit.slope - margin:.3f}, {fit.slope + margin:.3f}])")
print(f"Correlation r:             {fit.rvalue:.3f}")
print(f"R-squared:                 {fit.rvalue ** 2:.3f}  (temperature explains {100 * fit.rvalue ** 2:.1f}% of the pressure changes)")
print(f"p-value (slope = 0):       {fit.pvalue:.3g}")
print(f"Spearman rank corr.:       {r_s:.3f}  (p = {p_s:.3g})")
print("Conclusion:", "weak but statistically significant negative trend" if fit.pvalue < 0.05 and fit.rvalue < 0
      else "no significant trend at the 5% level")

fig, ax = plt.subplots(figsize=(5.5, 4))
ax.scatter(x, y, s=4, alpha=0.3, color="#4a7fb5", label="Daily values")
xs = np.array([x.min(), x.max()])
ax.plot(xs, fit.intercept + fit.slope * xs, color="red", label=f"Fit: {fit.slope:.2f} hPa per deg C (r = {fit.rvalue:.2f})")
ax.set_xlabel("Average daily temperature (deg C)")
ax.set_ylabel("Average station pressure (hPa)")
ax.set_title("Q3: Pressure vs temperature\n(Luray Caverns Airport, 2015-2025)", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("results/q3_plot.png", dpi=200)
print("Saved results/q3_plot.png")
