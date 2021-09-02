# SERVERLESS CONFIGURATION METHOD EXPERIMENTS

This repository contains a set of tools to evaluate serverless configuration methods, including functions, function-compositions data.

PR's for new functions and composition generators are welcome.


# Sampling 

The sampling can collect input data to train sizing methods or generate a validation set using exhaustive search. 
The sampling generator is configurable to allow for the collection of both.


To sample, you can define a workload file using the following syntax:
```
{
  "name": "EXPERIMENT_NAME",
  "url": "FUNCTION_WEB_TRIGGER_URL",
  "input":[ <ANY INPUT will be run to json.dumps()>],
  "itterations": NUM_OF_ITTERNATIOS_PER_MEMORY_AND_INPUT,
  "memory":[LIST_OF_MEMORY_SIZE_TO_SAMPLE]
}
``` 
Using `python bench.py <workload-file> <vendor> <function>` you can start collecting samples for each deployment. 
All data is collected in `data/EXPERIMENT_NAME_<DATE>.csv`

# Functions
In the `functions` folder, we collect a set of functions that can be used to evaluate sizing methods. These functions are also used by the composition generator to create complex, composed serverless functions. See the Readme in the folder for more information.

# Compositions

In the `compositions` folder, we collect composition templates and generators. See the Readme in `compositions/` for more details on generating arbitrary complex function compositions for AWS StepFunctions.

## Acknolagements

This work is part of a paper currently under review at UCC 2021.
