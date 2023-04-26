############################ Experimental Data Collection ########################################################

import sys
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('_mpl-gallery')
plt.rcParams.update({'font.size': 12})
plt.rcParams["figure.autolayout"] = True

dataset = 'testing'
df = pd.read_csv(f'low_level_scores_{dataset}_set.csv')

# Full dataframe of heuristics and results the whole dataset
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

# Number of times each heuristic was the best
best_heuristics = df['Best heuristic'].value_counts()
best_heuristics.to_csv(f'low_level_best_heuristics_{dataset}.csv')

# Summary of heuristic performances, mean, quartiles etc...
results_df.describe().to_csv(f'low_level_scores_{dataset}_summary.csv')

# Initial Hyper heuristic scores on the testing set
hh_scores = pd.read_csv('hyper_heuristic_testing_archive data_(popsize=20,num_iterations=500)_fitness_df_400.csv')
hh_scores = hh_scores[['0','1','2','3','4']]
hh_scores.columns = ['HH0','HH1','HH2','HH3','HH4']

# Secondary hyper heuristic scores
hh2_scores = pd.read_csv('hyper_heuristic_testing_archive data_popsize=40,num_iterations=200_fitness_df_150.csv.csv')
hh2_scores = hh2_scores[['0','1','2','3','4']]
hh2_scores.columns = ['HH0','HH1','HH2','HH3','HH4']


# Dataframe of time taken by heuristics
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

# Summary of time data
times_df.describe().to_csv(f'low_level_times_{dataset}_summary.csv')

ff_df = pd.DataFrame({'Fitness': df['First Fit Score'],
                      'Heuristic': 'First Fit'})
ffd_df = pd.DataFrame({'Fitness': df['First Fit Decreasing Score'],
                      'Heuristic': 'First Fit Decreasing'})
nf_df = pd.DataFrame({'Fitness': df['Next Fit Score'],
                      'Heuristic': 'Next Fit'})
nfd_df = pd.DataFrame({'Fitness': df['Next Fit Decreasing Score'],
                      'Heuristic': 'Next Fit Decreasing'})
bf_df = pd.DataFrame({'Fitness': df['Best Fit Score'],
                      'Heuristic': 'Best Fit'})
bfd_df = pd.DataFrame({'Fitness': df['Best Fit Decreasing Score'],
                      'Heuristic': 'Best Fit Decreasing'})
djd_df = pd.DataFrame({'Fitness': df['Djang-Fitch Score'],
                      'Heuristic': 'Djang and Fitch'})
djd2_df = pd.DataFrame({'Fitness': df['Djang-Fitch 2 Score'],
                      'Heuristic': 'Djang and Fitch 2'})
hh0_df = pd.DataFrame({'Fitness': hh_scores['HH0'],
                       'Heuristic': 'Converged HH'})
# hh1_df = pd.DataFrame({'Fitness': hh_scores['HH1'],
#                        'Heuristic': 'HH1'})
# hh2_df = pd.DataFrame({'Fitness': hh_scores['HH2'],
#                        'Heuristic': 'HH2'})
# hh3_df = pd.DataFrame({'Fitness': hh_scores['HH3'],
#                        'Heuristic': 'HH3'})
# hh4_df = pd.DataFrame({'Fitness': hh_scores['HH4'],
#                        'Heuristic': 'HH4'})
hh2_scores_df = pd.DataFrame({'Fitness': hh2_scores['HH0'],
                       'Heuristic': 'Broad HH'})

concat_df = pd.concat([ff_df, ffd_df, nf_df, nfd_df, bf_df, bfd_df, djd_df, djd2_df, hh0_df, hh2_scores_df])
concat_df.to_csv('concat_df.csv')

results_df = pd.merge(results_df, hh_scores['HH0'], left_index=True, right_index=True)
results_df = pd.merge(results_df, hh2_scores['HH0'], left_index=True, right_index=True)
# Plotting
plot_scatter = False
plot_box = True
quartile_plot = False


if plot_scatter:
    plt.rcParams["figure.figsize"] = [8, 6]
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
    plt.xlabel(f'Mean fitness across {dataset} set')
    plt.legend(loc='upper right')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.savefig('low_level_performance')
    plt.show()

if plot_box:  
    plt.rcParams["figure.autolayout"] = True
    positions = range(len(results_df.columns))
    plt.boxplot([results_df[col] for col in results_df.columns],
                positions=positions, showfliers=False,
                boxprops={'facecolor': 'none'}, medianprops={'color': 'black'}, patch_artist=True)
    means = [np.mean(results_df[col]) for col in results_df.columns]
    sns.violinplot('Heuristic', 'Fitness', data=concat_df)
    plt.show()


if quartile_plot:
    mean_series = results_df.mean(axis=1)
    quartile_df = results_df.quantile(q=[0.25, 0.5, 0.75], axis=1, numeric_only=True).transpose()
    quartile_df.columns = ['Lower Quartile', 'Median', 'Upper Quartile']
    quartile_df['Mean'] = mean_series

    quartile_df = quartile_df[:100]

    quartile_df['Mean'].plot.line()
    quartile_df['Lower Quartile'].plot.line()
    quartile_df['Median'].plot.line()
    quartile_df['Upper Quartile'].plot.line()
    leg = plt.legend(loc='upper right', frameon=False)

    plt.show()
