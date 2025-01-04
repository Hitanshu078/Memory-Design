import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class CacheLine:
    def __init__(self, tag=0):  # Cache line constructor with default tag
        self.tag = tag

class Cache:
    def __init__(self, cache_size_kb, block_size_bytes, associativity):
        self.block_size = block_size_bytes
        self.associativity = associativity
        self.hits = 0
        self.misses = 0

        cache_size_bytes = cache_size_kb * 1024
        self.num_sets = cache_size_bytes // (block_size_bytes * associativity)
        self.cache = [[None] * associativity for _ in range(self.num_sets)]

        self.index_bits = int(math.log2(self.num_sets))
        self.block_offset_bits = int(math.log2(block_size_bytes))

    def extract_tag(self, address):
        return address >> (self.index_bits + self.block_offset_bits)

    def extract_index(self, address):
        mask = (1 << self.index_bits) - 1
        return (address >> self.block_offset_bits) & mask

    def access(self, address):
        index = self.extract_index(address)
        tag = self.extract_tag(address)

        cache_set = self.cache[index]

        # Check for cache hit
        for i in range(self.associativity):
            if cache_set[i] is not None and cache_set[i].tag == tag:
                self.hits += 1
                return True  # Cache hit

        # Cache miss, insert the new line into the first available slot or replace an existing one
        self.misses += 1
        for i in range(self.associativity):
            if cache_set[i] is None:
                cache_set[i] = CacheLine(tag=tag)  # Place in an empty spot
                return False

        # Replace the first cache line (simple replacement policy)
        cache_set[0] = CacheLine(tag=tag)
        return False

    def clear_cache(self):
        self.cache = [[None] * self.associativity for _ in range(self.num_sets)]
        self.hits = 0
        self.misses = 0

    def run_trace_file(self, filename):
        try:
            with open(filename, 'r') as trace_file:
                for line in trace_file:
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    address = int(parts[1], 16)  # Convert hex address to integer
                    self.access(address)
        except FileNotFoundError:
            print(f"Error: Could not open the file {filename}")

    def get_miss_rate(self):
        total_accesses = self.hits + self.misses
        if total_accesses == 0:
            return 0.0
        return (self.misses / total_accesses) 

    def get_hit_rate(self):
        total_accesses = self.hits + self.misses
        if total_accesses == 0:
            return 0.0
        return (self.hits / total_accesses) 

def run_experiment(trace_files, cache_sizes, block_size, associativity):
    results = {trace: [] for trace in trace_files}
    hits = {trace: [] for trace in trace_files}
    misses = {trace: [] for trace in trace_files}

    for cache_size in cache_sizes:
        for trace_file in trace_files:
            cache = Cache(cache_size, block_size, associativity)
            cache.run_trace_file(trace_file)
            miss_rate = cache.get_miss_rate()
            results[trace_file].append(miss_rate)
            hits[trace_file].append(cache.hits)
            misses[trace_file].append(cache.misses)

    return results, hits, misses

def run_experiment_vary_block_size(trace_files, cache_size, block_sizes, associativity):
    results = {trace: [] for trace in trace_files}
    hits = {trace: [] for trace in trace_files}
    misses = {trace: [] for trace in trace_files}

    for block_size in block_sizes:
        for trace_file in trace_files:
            cache = Cache(cache_size, block_size, associativity)
            cache.run_trace_file(trace_file)
            miss_rate = cache.get_miss_rate()
            results[trace_file].append(miss_rate)
            hits[trace_file].append(cache.hits)
            misses[trace_file].append(cache.misses)

    return results, hits, misses

def run_experiment_vary_associativity(trace_files, cache_size, block_size, associativities):
    results = {trace: [] for trace in trace_files}
    hits = {trace: [] for trace in trace_files}
    misses = {trace: [] for trace in trace_files}

    for associativity in associativities:
        for trace_file in trace_files:
            cache = Cache(cache_size, block_size, associativity)
            cache.run_trace_file(trace_file)
            hit_rate = cache.get_hit_rate()
            results[trace_file].append(hit_rate)  # Store hit rates
            hits[trace_file].append(cache.hits)
            misses[trace_file].append(cache.misses)

    return results, hits, misses

def plot_results(results, x_values, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))

    # Plot each trace file's data
    for trace_file, values in results.items():
        plt.plot(x_values, values, marker='o', label=f'Trace: {trace_file}')

    # Set labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"{title} - {'; '.join(results.keys())}")  # Include file names in the title
    plt.legend()
    plt.grid(True)

    # Set x-axis to logarithmic scale with base 2
    plt.xscale('log', base=2)
    plt.xticks(x_values, [f'{size}' for size in x_values])

    # Customize y-axis to show four decimal places
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.4f}'))

    plt.show()


def plot_hit_rate_vs_associativity(results, associativities, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))

    # Plot each trace file's data
    for trace_file, hit_rates in results.items():
        plt.plot(associativities, hit_rates, marker='o', label=f'{trace_file}')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Append trace file names to the title
    trace_files_str = "; ".join(results.keys())
    plt.title(f"{title} - {trace_files_str}")

    plt.legend()
    plt.grid(True)

    # Set x-axis to linear scale
    plt.xscale('linear')

    # Set x-axis ticks to integer values
    plt.xticks(associativities, [str(size) for size in associativities])

    # Customize y-axis to show integer values
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.show()

def print_table(results, x_values, label, hits, misses):
    print(f"{label} vs Miss Rate:")
    print("-" * 100)
    print(f"{label:<15} {'Trace File':<20} {'Miss Rate (%)':<15} {'Hits':<10} {'Misses':<10} {'Hit Rate (%)':<10}")
    print("-" * 100)

    for x_value in x_values:
        for trace_file, miss_rates in results.items():
            idx = x_values.index(x_value)
            miss_rate = miss_rates[idx]
            hit = hits[trace_file][idx]
            miss = misses[trace_file][idx]
            hit_rate = (hit / (hit + miss)) * 100 if (hit + miss) > 0 else 0
            print(f"{x_value:<15} {trace_file:<20} {miss_rate:<15.2f} {hit:<10} {miss:<10} {hit_rate:<10.2f}")
    print("-" * 100)
    
def explain_experiment(experiment):
    if experiment == 'a':
        explanation = """
        Instructions:
        - Design a 4-way set associative cache of size 1024 kilobytes. Block size: 4 bytes.
        - Cache size is 1024 KB, 4-byte block size, 4-way set associative.
        - Given the block size and associativity, there are 65,536 sets.
        - The cache uses 16 index bits and 2 block offset bits.
        - cache_size = 1024 kB
        - block_size = 4 bytes
        - associativity = 4
        """
    elif experiment == 'b':
        explanation = """
        Instructions: 
        - Vary the cache size from 128kB to 4096 kB and plot miss rate vs cache size.
        - cache_size = [128, 256, 512, 1024, 2048, 4096] kB
        - block_size = 4 bytes
        - associativity = 4
        """
    elif experiment == 'c':
        explanation = """
        Instructions:
        - Vary the block size from 1 byte to 128 bytes and observe the miss rate.
        - cache_size = 1024 kB
        - block_size = [1, 2, 4, 8, 16, 32] bytes
        - associativity = 4
        """
    elif experiment == 'd':
        explanation = """
        Instructions:
        - Vary the associativity from 1-way to 64-way and plot hit rate vs associativity.
        - cache_size = 1024 kB
        - block_size = 4 bytes
        - associativity = [1, 2, 4, 8, 16] ways
        """
    print(explanation)

def main():
    print("Select the experiment to run (a, b, c, d):")
    experiment = input("Enter experiment letter: ").lower()
    
    explain_experiment(experiment)

    trace_files = input("Enter trace files separated by space: ").split()

    output_type = input("Do you want to see the output as a 'graph' or 'table'? ").strip().lower()

    if experiment == 'a':
        cache_size = 1024  # Fixed cache size
        block_size = 4  # Fixed block size
        associativity = 4  # Fixed 4-way associativity

        results, hits, misses = run_experiment(trace_files, [cache_size], block_size, associativity)
        if output_type == 'graph':
            plot_results(results, [cache_size], "Cache Size (kB)", "Miss Rate", "Fixed Cache Size (1024kB) with 4-way associativity")
        else:
            print_table(results, [cache_size], "Cache Size", hits, misses)

    elif experiment == 'b':
        cache_sizes = [128, 256, 512, 1024, 2048, 4096]  # Cache sizes in kB
        block_size = 4  # Fixed block size
        associativity = 4  # Fixed 4-way associativity

        results, hits, misses = run_experiment(trace_files, cache_sizes, block_size, associativity)
        if output_type == 'graph':
            plot_results(results, cache_sizes, "Cache Size (kB)", "Miss Rate", "Miss Rate vs Cache Size")
        else:
            print_table(results, cache_sizes, "Cache Size", hits, misses)

    elif experiment == 'c':
        cache_size = 1024  # Fixed cache size
        block_sizes = [1, 2, 4, 8, 16, 32]  # Block sizes in bytes
        associativity = 4  # Fixed 4-way associativity

        results, hits, misses = run_experiment_vary_block_size(trace_files, cache_size, block_sizes, associativity)
        if output_type == 'graph':
            plot_results(results, block_sizes, "Block Size (Bytes)", "Miss Rate", "Miss Rate vs Block Size")
        else:
            print_table(results, block_sizes, "Block Size", hits, misses)

    elif experiment == 'd':
        cache_size = 1024  # Fixed cache size
        block_size = 4  # Fixed block size
        associativities = [1, 2, 4, 8, 16]  # Varying associativity

        results, hits, misses = run_experiment_vary_associativity(trace_files, cache_size, block_size, associativities)
        if output_type == 'graph':
            plot_hit_rate_vs_associativity(results, associativities, "Associativity", "Hit Rate", "Hit Rate vs Associativity")
        else:
            print_table(results, associativities, "Associativity", hits, misses)

if __name__ == "__main__":
    main()
