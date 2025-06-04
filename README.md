# Memory-Design

# Cache Memory Design and Analysis

This repository contains the implementation and analysis for Assignment 1 on Cache Memory Design, as part of the Computer Architecture coursework.

## Problem Statement

The goal is to design and analyze a 4-way set associative cache with various configurations and parameters. The experiments involve:

1. **Cache size variations**: Analyze hit/miss rates for cache sizes ranging from 128kB to 4096kB.
2. **Block size variations**: Observe how block sizes (1 byte to 128 bytes) affect cache performance for a fixed cache size of 1024kB.
3. **Associativity variations**: Examine the effect of associativity (1-way to 64-way) on hit rates for a fixed cache size of 1024kB.

The experiments are conducted using input memory trace files from the given [source](https://cseweb.ucsd.edu/classes/fa07/cse240a/proj1-traces.tar.gz).

---

## Features

- **Simulated Cache Design**: Implements a 4-way set associative cache.
- **Hit/Miss Rate Calculation**: Provides detailed statistics for input memory traces.
- **Parameter Exploration**: Analyzes the impact of cache size, block size, and associativity on performance.
- **Graphical Analysis**: Plots results for easier interpretation.

---

## Getting Started

### Prerequisites

- Programming Language: Python, C/C++, Java, or Verilog
- Memory trace files (download from the [provided link](https://cseweb.ucsd.edu/classes/fa07/cse240a/proj1-traces.tar.gz))

### Repository Structure

```
📂 CacheMemoryAssignment
├── 📂 src               # Source code
├── 📂 data              # Memory trace files
├── 📂 results           # Graphs and observation reports
├── README.md            # Project documentation
```

---

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/Hitanshu078/Memory-Design.git
   cd CacheMemoryAssignment
   ```

2. Execute the code for specific configurations:
   ```bash
   python src/cache_simulator.py --cache_size 1024 --block_size 4 --associativity 4
   ```

3. Analyze outputs in the `results` folder.

---

## Observations and Results

- **Cache Size Variation**: Miss rate trends across cache sizes (128kB to 4096kB).
- **Block Size Variation**: Performance trends based on block size changes.
- **Associativity Analysis**: Impact of different associativity levels on hit rates.

All results are presented in graphical form in the `results` directory.

---

## License

This project is licensed under the MIT License.
