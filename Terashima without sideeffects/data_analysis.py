import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('_mpl-gallery')

df = pd.read_csv('low_level.csv')

results_df = df.loc[:, [
         'First Fit Score',
         'First Fit Decreasing Score',
         'Next Fit Score',
         'Next Fit Decreasing Score',
         'Best Fit Score',
         'Best Fit Decreasing Score',
         'Djang-Fitch Score']]

# Mean fitness
print(results_df.mean())
# print(results_df.describe())

# Best heuristic
maxValueIndex = results_df.idxmax(axis=1)
best_heuristics = maxValueIndex.value_counts().to_frame()
# print(best_heuristics.head())
plt.rcParams["figure.figsize"] = [8, 4]
plt.rcParams["figure.autolayout"] = True

plt.scatter(results_df.mean()[0], 0.5, label='FF')
plt.scatter(results_df.mean()[1], 0.5, label='FFD')
plt.scatter(results_df.mean()[2], 0.5, label='NF')
plt.scatter(results_df.mean()[3], 0.5, label='NFD')
plt.scatter(results_df.mean()[4], 0.5, label='BF')
plt.scatter(results_df.mean()[5], 0.5, label='BFD')
plt.scatter(results_df.mean()[6], 0.5, label='DJD')

print(results_df.describe())

plt.errorbar(results_df.mean()[0], 0.5, xerr=results_df.std()[0], fmt="o")
ax = plt.gca()
ax.get_yaxis().set_visible(False)
plt.xlabel('Plot Number')
plt.legend(loc='upper right')
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()