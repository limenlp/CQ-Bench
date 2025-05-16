# CQ-Bench


## Dataset
We have 7 categories: random, political, ethical, religious, social, multiple and human, where humans means the dataset we use for human evaluation. 
For each category, there is original dataset, Task 1 (Attitude detection), Task 2 (Value selection). The original dataset only includes story, ground truth values, filtered values and contradictory values. The task 1 and task 2 dataset includes questions and gold labels.

For value extraction, since there is no option, we simply use original dataset.

## Generating story
To generate story, run
```
cd story_generation
python generate_story_pipeline.py --output_file <output file name> --number <number of stories> --value_file <seed value values> --previous_file <if already generate stories>
```

To run validation, run:
```
python  validation.py --output_file <validation output> --story_file <generated story>
```

To generate dataset from story, run:
```
python organize_dataset.py --validation_file <validation file> --category <category>

python generate_dataset_from_original.py --category <category> --task <task> --value_file <value file>
```

## Run experiments
To run experiments on attitude detection and value selection

```
python run_exps.py --task <task> --category <category> --model <model name> --prompt <zero/few> --reasoning
```

To run experiments on value extraction

```
python run_exps_open.py 
```

To evaluate attitude detection and value selection

```
python evaluation.py --task <task> --category <category> --model <model name> --prompt <zero/few> --reasoning
```

To evaluate value extraction
```
python evaluate_open.py --category <category> --model <model name>
```


