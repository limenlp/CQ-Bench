import json
import jsonlines
import random
import argparse
from generate_story_pipeline import get_value_options

def main():
    parser = argparse.ArgumentParser(
                    prog='Culture',
                    )
    parser.add_argument('-c','--category',default='random')
    parser.add_argument('-s','--task',default='1')
    parser.add_argument('-v','--value_file',default='WVQ_simple.jsonl')           # positional argument
    args = parser.parse_args()
    category = args.category
    setting = args.task
    # Load the value set
    value_file = args.value_file
    values, value_options = get_value_options(value_file)

    options_all = []
    for value in value_options:
        for option in value_options[value]:
            value_option = value+'--'+option.strip()
            options_all.append(value_option)
    # Load the dataset
    f = open(f'dataset_{category}_original.json')
    dataset = json.load(f)
    results = []
    if setting=='1':
        for index,data in enumerate(dataset):
     
            story = data['story']
            values = data['values']
            if category!='multiple':
                final_values = []
                contradiction = data['contradiction']
                for v in value:
                    if v not in contradiction:
                        final_values.append(v)
            else:
                final_values = values
            questions = []
            for v in final_values:
                name = v.split(':')[0]
                v_raw = ':'.join(v.split(':')[1:])

                question = {"name":name,'value':v_raw.split('--')[0],'options':value_options[v_raw.split('--')[0]],'gold label':v_raw.split('--')[1]}
                questions.append(question)
            data_point = {'story':story,'questions':questions}
            results.append(data_point)

    elif setting=='2':
       
        for index,data in enumerate(dataset):
         
            story = data['story']
            values = data['values']
            original_values = data['original_values']
            left_values = list(set(options_all)-set(original_values))  
            contradiction = data['contradiction']
            for value in contradiction:
                v, gold_option = value.split('--')
                options = value_options[v]
                for op in options:
                    new_v = v+'--'+op.strip()
                    if new_v in left_values:
                        left_values.remove(new_v)
            
            random_values = random.sample(left_values,15-len(values))
            options_provided = values+random_values
            random.shuffle(options_provided)
            data_point = {'story':story,'options':options_provided,'values':values}
            results.append(data_point)

        with open(f'dataset_setting{setting}_{category}.json','w') as f:
            json.dump(results,f,indent=4)


if __name__=='__main__':
    main()