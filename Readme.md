# SERVERLESS CONFIGURATION METHOD EXPERIMENTES

This reposetory contains a set of tools to evalaute serverless configuration methods including functions, function-compostions data.

PR's for new functions or compostions wellcome.

# Sampling 

To sample you can define a workload file using the following syntax:
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

# Compositions

See the Readme in Compositions to generate abitray complex function compostions for AWS StepFunctions.

## Acknolagements

This work is part of a paper currenlty under review at UCC 2021.