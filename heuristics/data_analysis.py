import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('_mpl-gallery')

dataset = 'training'
df = pd.read_csv(f'low_level_scores_{dataset}_set.csv')

results_df = df.loc[:, [
         'First Fit Score',
         'First Fit Decreasing Score',
         'Next Fit Score',
         'Next Fit Decreasing Score',
         'Best Fit Score',
         'Best Fit Decreasing Score',
         'Djang-Fitch Score',
         'Djang-Fitch 2 Score',
         ]]


best_heuristics = df['Best heuristic'].value_counts()
best_heuristics.to_csv(f'low_level_best_heuristics_{dataset}.csv')

results_df.describe().to_csv(f'low_level_scores_{dataset}_summary.csv')

df2 = pd.read_csv(f'low_level_times_{dataset}_set.csv')
times_df = df2.loc[:, [
         'First Fit Times',
         'First Fit Decreasing Times',
         'Next Fit Times',
         'Next Fit Decreasing Times',
         'Best Fit Times',
         'Best Fit Decreasing Times',
         'Djang-Fitch Times',
         'Djang-Fitch 2 Times']]

times_df.describe().to_csv(f'low_level_times_{dataset}_summary.csv')

plot = False
if plot:
    plt.rcParams["figure.figsize"] = [8, 4]
    plt.rcParams["figure.autolayout"] = True

    plt.scatter(results_df.mean()[0], 0.5, label='FF')
    plt.scatter(results_df.mean()[1], 0.5, label='FFD')
    plt.scatter(results_df.mean()[2], 0.5, label='NF')
    plt.scatter(results_df.mean()[3], 0.5, label='NFD')
    plt.scatter(results_df.mean()[4], 0.5, label='BF')
    plt.scatter(results_df.mean()[5], 0.5, label='BFD')
    plt.scatter(results_df.mean()[6], 0.5, label='DJD')
    plt.scatter(results_df.mean()[7], 0.5, label='DJD2')

    ax = plt.gca()
    ax.get_yaxis().set_visible(False)
    plt.xlabel('Plot Number')
    plt.legend(loc='upper right')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()