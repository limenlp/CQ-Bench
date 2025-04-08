import pandas as pd
import json
import argparse
from util import combine_missing_values, process_reflect_check, process_consistency

def remove_missing_values(reflect_values,ground_truth:list):
    reflect_valid_final_multiple = reflect_values.split('\separator')
    missing_values_list = []
    new_values = []
    for reflection in reflect_valid_final_multiple:
        reflection = reflection.strip()
        missing_values = process_reflect_check(reflection,ground_truth)
        missing_values_list.append(missing_values)
    missing_values = combine_missing_values(missing_values_list,"majority")
    # print(missing_values)
    if missing_values ==[]:
        return ground_truth
    else:
        for value in ground_truth:
            if value not in missing_values:
                new_values.append(value)

       
        return new_values

def add_contradiction_label(contradiction,ground_truth):
    contradictions = process_consistency(contradiction, ground_truth)

    return contradictions

if __name__=='__main__':

    parser = argparse.ArgumentParser(
                    prog='Culture',
                    )
    parser.add_argument('-o','--validation_file')           
    parser.add_argument('-c','--category',default='random')           
    args = parser.parse_args()
    # Load the dataset
    df = pd.read_csv(args.validation_file)

    final_data = []
    for index, row in df.iterrows():
        values = row['values']
        values = values.split('\n')
        story = row['Final story']
        if len(story.split())<400:
            continue
        reflection = row['reflection validation multiple']
        consistency = row['consistency validation multiple']
        filtered_values = remove_missing_values(reflection,values)
        contradiction_labels = add_contradiction_label(consistency, values)
        datapoints = {"original_values":values,'values':filtered_values, 'story':story,'contradiction':contradiction_labels}
        final_data.append(datapoints)

    output_file = f'dataset_{args.category}_original.json'
    with open('dataset_multiple_original.json','w') as f:
        json.dump(final_data,f,indent=4)
 