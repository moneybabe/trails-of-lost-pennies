from functions import *
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from tqdm import tqdm
import pandas as pd

def process_interval_chunk(interval_chunk, l, k):
    results = []
    for interval in tqdm(interval_chunk):
        a, b = interval
        output = M_lk_down(a, b, l, k)
        results.append((output.a, output.b, a, b))
    return results

def main():
    interval = iv.linspace('1/3', '3', int(1e7))
    workers = 8
    interval_chunks = np.array_split(np.array(list(zip(interval[:-1], interval[1:]))), workers)

    l, k = 5, 4
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(process_interval_chunk, interval_chunks, [l] * workers, [k] * workers)

    # Flatten the results
    results = [item for sublist in results for item in sublist]

    error_lower_bounds, error_upper_bounds, a, b = zip(*results)
    error_lower_bounds = [float(x) for x in error_lower_bounds]
    error_upper_bounds = [float(x) for x in error_upper_bounds]
    a = [float(x) for x in a]
    b = [float(x) for x in b]
    results_df = pd.DataFrame({
        'a': a, 
        'b': b, 
        'error_lower_bound': error_lower_bounds, 
        'error_upper_bound': error_upper_bounds
    })
    results_df.to_csv('results.csv', index=False)

if __name__ == '__main__':
    main()
    