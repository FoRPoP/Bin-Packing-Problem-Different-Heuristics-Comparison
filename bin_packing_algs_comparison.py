import random
import time
from typing import Generator, Union
from matplotlib import ticker
import matplotlib.pyplot as plt
from functools import partial
import seaborn as sns
import math

from bin_packing_algs import *

def generate_objects(num_objects: int, min_size: int = 0, max_size: int = 1.0) -> Generator:

    for _ in range(num_objects):
        yield random.uniform(min_size, max_size)


def sort_lists(generated_lists: dict[int, list[list[float]]]) -> tuple[dict, dict]:

    sorting_times = {}
    sorted_lists = {size: [] for size in generated_lists.keys()}

    for size, lists_by_size in generated_lists.items():
        print(f'Sorting lists with size: {size}.')

        total_sort_time = 0
        sorted_lists[size] = []

        for objects_list in lists_by_size:
            sorted_objects, sort_time = timed_sort(objects_list)
            sorted_lists[size].append(sorted_objects)
            total_sort_time += sort_time

            print(f'Sorted list {len(sorted_lists[size])}/{len(lists_by_size)}.')

        sorting_times[size] = total_sort_time / len(lists_by_size)

        print(f'Successfully finished sorting the lists with size: {size} with average sorting time of: {sorting_times[size]}.')
    
    return sorted_lists, sorting_times


def timed_sort(objects_list: list[float]) -> tuple[list[float], float]:

    start_time = time.time()
    sorted_objects = sorted(objects_list, reverse=True)
    end_time = time.time()
    return sorted_objects, ((end_time - start_time) * 1000)


def analyze_results(results: list[int]) -> tuple[int, int, int]:

    best_result = min(results)
    worst_result = max(results)
    average_result = sum(results) / len(results)
    return best_result, average_result, worst_result


def run_algs(algs: dict[str, any], lists_by_sizes: dict[list[float]]) -> dict:

    results = {'best': {}, 'avg': {}, 'worst': {}, 'time': {'best': {}, 'avg': {}, 'worst': {}}}

    for alg_name, alg in algs.items():

        print(f'Running algorithm: {alg_name}.')

        results['best'][alg_name] = []
        results['avg'][alg_name] = []
        results['worst'][alg_name] = []
        results['time']['best'][alg_name] = []
        results['time']['avg'][alg_name] = []
        results['time']['worst'][alg_name] = []

        for size, lists_by_size in lists_by_sizes.items():

            print(f'Running for lists with size: {size}.')

            trial_results = []
            trial_times = []
            for objects_list in lists_by_size:
                start_time = time.time()
                result = alg(objects_list)
                end_time = time.time()
                trial_times.append((end_time - start_time) * 1000)
                trial_results.append(result)

                print(f'Finished running {len(trial_times)}/{len(lists_by_size)} lists.')
            
            best, avg, worst = analyze_results(trial_results)
            results['best'][alg_name].append(best)
            results['avg'][alg_name].append(avg)
            results['worst'][alg_name].append(worst)
    
            time_best, time_avg, time_worst = analyze_results(trial_times)
            results['time']['best'][alg_name].append(time_best)
            results['time']['avg'][alg_name].append(time_avg)
            results['time']['worst'][alg_name].append(time_worst)

        print(f'Successfully ran algorithm: {alg_name}')

    return results


def adjust_offline_results(offline_results: dict, sorting_times: dict, input_sizes: list[int]) -> None:

    for alg_name in offline_results['time']['avg']:
        for i, size in enumerate(input_sizes):
            offline_results['time']['best'][alg_name][i] += sorting_times[size]
            offline_results['time']['avg'][alg_name][i] += sorting_times[size]
            offline_results['time']['worst'][alg_name][i] += sorting_times[size]


def plot_results(input_sizes: list[int], results: dict[str, list[Union[int, float]]], title: str, ylabel: str, name: str) -> None:

    sns.set_style('whitegrid')
    palette = sns.color_palette('husl', len(results.items()))
    styles = ['solid', 'dashed', 'dashdot', 'dotted']

    for (alg_name, values), color, style in zip(results.items(), palette, styles * math.ceil((len(results.values()) / len(styles)))):
        plt.plot(input_sizes, values, label=alg_name, marker='o', markersize=4, color=color, linestyle=style, alpha=0.7)

    plt.xlabel('Number of Objects')
    plt.ylabel(ylabel)
    plt.xscale('log')
    plt.yscale('linear')
    plt.xticks(input_sizes)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.gca().ticklabel_format(style='plain', axis='y')
    plt.gca().ticklabel_format(style='plain', axis='x')

    plt.savefig(name)
    plt.show()


def main() -> None:

    input_sizes = [12, 25, 100, 500, 3000, 10000, 40000, 250000, 1000000]
    #input_sizes = [12, 25, 100, 500, 3000, 10000]
    num_trials = 100
    generated_lists = {size: [list(generate_objects(size)) for _ in range(num_trials)] for size in input_sizes}
    print("Successfully generated lists.")

    online_algorithms = {
        'Next Fit': next_fit,
        'Next 2 Fit': partial(next_k_fit, k=2),
        'Next 10 Fit': partial(next_k_fit, k=10),
        'Next 100 Fit': partial(next_k_fit, k=100),
        'First Fit': first_fit,
        'Best Fit': best_fit,
        'Worst Fit': worst_fit,
        'Almost Worst Fit': almost_worst_fit,
        'Refined First Fit': refined_first_fit,
        'Harmonic 20': partial(harmonic_k, k=20),
        'Refined Harmonic 20': partial(refined_harmonic, k=20)
    }

    offline_algorithms = {
        'Next Fit': next_fit,
        'Next 2 Fit': partial(next_k_fit, k=2),
        'Next 10 Fit': partial(next_k_fit, k=10),
        'Next 100 Fit': partial(next_k_fit, k=100),
        'First Fit': first_fit,
        'Best Fit': best_fit,
        'Worst Fit': worst_fit,
        'Almost Worst Fit': almost_worst_fit,
        'Refined First Fit': partial(refined_first_fit, offline=True),
        'Harmonic 20': partial(harmonic_k, k=20),
        'Refined Harmonic 20': partial(refined_harmonic, k=20),
    }

    sorted_lists, sorting_times = sort_lists(generated_lists)

    print('Successfully sorted lists.')

    online_results = run_algs(online_algorithms, generated_lists)
    offline_results = run_algs(offline_algorithms, sorted_lists)

    print('Successfully ran algorithms.')

    adjust_offline_results(offline_results, sorting_times, input_sizes)

    plot_results(input_sizes, online_results['avg'], 'Average Run of Online Algorithms', 'Bins Used', 'Average Run of Online Algorithms')
    #plot_results(input_sizes, online_results['best'], 'Best Run of Online Algorithms', 'Bins Used')
    #plot_results(input_sizes, online_results['worst'], 'Worst Run of Online Algorithms', 'Bins Used')
    
    plot_results(input_sizes, online_results['time']['avg'], 'Average Time of Online Algorithms', 'Time (ms)', 'Average Time of Online Algorithms')
    #plot_results(input_sizes, online_results['time']['best'], 'Best Time of Online Algorithms', 'Time (ms)')
    #plot_results(input_sizes, online_results['time']['worst'], 'Worst Time of Online Algorithms', 'Time (ms)')
    
    plot_results(input_sizes, offline_results['avg'], 'Average Run of Offline Algorithms', 'Bins Used', 'Average Run of Offline Algorithms')
    #plot_results(input_sizes, offline_results['best'], 'Best Run of Offline Algorithms', 'Bins Used')
    #plot_results(input_sizes, offline_results['worst'], 'Worst Run of Offline Algorithms', 'Bins Used')
    
    plot_results(input_sizes, offline_results['time']['avg'], 'Average Time of Offline Algorithms', 'Time (ms)', 'Average Time of Offline Algorithms')
    #plot_results(input_sizes, offline_results['time']['best'], 'Best Time of Offline Algorithms', 'Time (ms)')
    #plot_results(input_sizes, offline_results['time']['worst'], 'Worst Time of Offline Algorithms', 'Time (ms)')

    print('Successfully plotted the results.')


if __name__ == '__main__':
    main()