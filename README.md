# efficient-AI-hardware-generator
Repository to investigate whether AI can generate hardware for inference which could surpass typical hardware in standard metrics.

# structure


# research goal
Investigating whether AI can be used to analyse neural networks and other models to significantly reduce hardware generation time.
The hardware should be evaluated based on the inference latency or throughput, energy consumption and hardwawre consumption.

# background
AI is becoming larger and requires more processing power. Traditional GPU's can provide high performance but the impact of reducing the power consumption further is dramastic considering the use of AI. To further improve AI this repository will investigate the use of AI for optimizing hardware.
However creating more efficient hardware is a labour intensive process with several hardware designers working several years before achieving better performance. Therefore, this repository investigates whether with the support of AI we can create optimized hardware in a significantly reduced time period. 

The AI should be able to:
1. Analyse the software model
2. Determine the required operations and the total operation count.
3. Express the operation count in terms of hardware units. E.g. multiply accumaltes, bias additions, floating point operations and other conversions. 
4. Analyse the bottlenecks in terms of latency and throughput. 
5. Provide a clear method to evaluate the hardware design in the given constraints and optimization criteria.
6. Explore the design space and provide performance over itterations.  

Software model optimizations can take place after the proof of concept has been established. Optimization can be quantization, model adaptations, pruning. 

# method
The first proof of concept will be to investigate a simple neural network like a fully connected network and ask design space exploration.
The evaluation can take place through Vitis HLS in which Vitis HLS is used to create building blocks for Vivado.
The Vivado suite can be used to create the eventual hardware and program an FPGA.
The FPGA can be evaluated as a proof of concept. It is most likely not more efficient 

Vitis High Level Synthesis can be used to create building blocks in Vivado. 
These two suits can be used to evaluate designs.
The AI should be aware of standard building blocks like multiply accumalate blocks and hardware devices like the DRAM and BRAM 

# Results



