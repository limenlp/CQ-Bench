from openai import OpenAI
import pandas as pd
from tqdm import tqdm
from prompts import *
import argparse
import os
from generate_story_pipeline import _obvious_check_and_rewrite, _consistency_rewrite, _reflect_check,_consistency_check, call_gpt
api_key = os.environ.get("API_KEY")
client = OpenAI(api_key = api_key)



def main():
    # Load the dataset
    parser = argparse.ArgumentParser(
                    prog='Culture',
                    )
    parser.add_argument('-o','--output_file',default='generated_story_random_296.csv')           # positional argument

    parser.add_argument('-s','--story_file',default='')
    args = parser.parse_args()
    df = pd.read_csv(args.story_file)

    consistent_final=[]

    reflections_final=[]
    for index, row in tqdm(df.iterrows()):
        
       
        story = row['Final story']
    
        ground_truth = row['Values']
   
        consistent_validations=[]
        reflection_validations=[]
        for i in range(3):
            consistent_validation = _consistency_check(story,ground_truth)
            reflection_validation = _reflect_check(story,ground_truth)
            consistent_validations.append(consistent_validation)
            reflection_validations.append(reflection_validation)
        consistent_final.append('\separator\n'.join(consistent_validations))
        reflections_final.append('\separator\n'.join(reflection_validations))
       
    df['reflection multiple']=reflections_final
    df['consistency multiple']=consistent_final
    df.to_csv(args.output_file, index=False)
 
if __name__=='__main__':
    main()
