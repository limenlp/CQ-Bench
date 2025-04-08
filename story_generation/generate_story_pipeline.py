from prompts import *
import random
import pandas as pd
import re
import jsonlines
import re
import os
import json
from openai import OpenAI
import argparse
from tqdm import tqdm
api_key = os.environ.get("OPENAI_API_KEY")

MODEL_generation="gpt-4o-mini"
MODEL_validation='gpt-4o'
client = OpenAI(api_key = api_key)

def get_value_options(file):
    values_option={}
    values = []
    reader = jsonlines.open(file)
    for line in reader:
        value = line['q_content']
        option = line['option']
        option = re.sub(r'\d+', '', option)
        options = option.split('.')
        values.append(value)
        
        if "" in options:
                options.remove('')
        if " " in options:
                options.remove(' ')
        
        values_option[value]=options
    return values, values_option

def call_gpt(prompt,model):
    
    completion_same = client.chat.completions.create(
    model = model,
    stream = False,
    messages=[
        {"role": "system", "content": "You are an expert in story generation and culture."}, 
        {"role": "user", "content": prompt}  
    ]
    )

    
    result = completion_same.choices[0].message.content
    return result

predefined_scene = ['company', 'school','neighborhood','national park','restaurant','amusement park','airplane']

def longest_common_substrings(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    longest, substrings = 0, set()

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longest:
                    longest = dp[i][j]
                    substrings = {s1[i - longest:i]}
                elif dp[i][j] == longest:
                    substrings.add(s1[i - longest:i])

    return list(substrings)

def match_value(value,ground_truth):
    max_len=0
    return_result = ''
    ground_truth=ground_truth.split('\n')
    for gt in ground_truth:
        match_result = longest_common_substrings(value.lower(),gt.lower())
        if len(match_result)==0:
            continue
        if len(match_result[0])>max_len:
            max_len = len(match_result[0])
            return_result=gt
    if return_result!='':
        return return_result
    else:
        return value
def parse_sentence(sentences,story,comment,ground_truth):
    try:
        comment_speech = longest_common_substrings(story,comment)[0]
    except:
        print(comment)
        return "","","",""
    # print(comment_speech)
    to_replace_sentence = ''
    for i, sentence in enumerate(sentences):
        if comment_speech in sentence:
            to_replace_sentence = sentence
            last_speech = sentences[i-1]
            break
    if len(comment.split(":"))<3:
        return "","","",""
    name = comment.split(":")[-2].strip()
    value = comment.split(":")[:-2]
    value = ':'.join(value) 
    value = match_value(value,ground_truth)
    if '*' in name:
        name = name.replace('*',"")
    if to_replace_sentence=="":
        return "","","",""
    return to_replace_sentence,last_speech,name,value
def _reflect_check(story,values):
    prompt_check_reflect = check_reflect_prompt.format(story = story,values = values)
    result_check_reflect = call_gpt(prompt_check_reflect,MODEL_validation)
    result_check_reflect_list = result_check_reflect.split('Values not reflected:')
    to_add_values = result_check_reflect_list[-1]
    return result_check_reflect,to_add_values

def _reflect_value(story,values_to_add):
    prompt_rewrite = refine_the_story_prompt.format(story = story, values = values_to_add)
    result = call_gpt(prompt_rewrite, MODEL_generation)
    return result

def _consistency_check(story,values):
    prompt_check_consistency = check_consistency_prompt.format(story=story,values = values)
    result_check_consistency = call_gpt(prompt_check_consistency,MODEL_validation)
    return result_check_consistency
      
def _consistency_rewrite(story,ground_truth_values,result):
    comment = result.split('[Contradictions]:')[1]
    comment = comment.strip('*')
    comment = comment.strip('\n')
    comment_singles = comment.split('\n\n')
    sentences = story.split('\n\n')
    rewrite_results=[]
    for contradiction in comment_singles:
        if contradiction.strip()=='':
            continue
        # rewrite_speech = call_gpt(resolve_consistency_prompt.format(story=story, values = values, contradiction = contradiction), MODEL_validation)
        # if "*" in contradiction:
        #     contradiction=contradiction.replace('*','')
        # common_string = longest_common_substrings(story,contradiction)[0]
        # story = story.replace(common_string,rewrite_speech)
        to_replace_speech, last_speech, name, value = parse_sentence(sentences,story,contradiction,ground_truth_values)
        if to_replace_speech=="":
            continue
        prompt = resolve_consistency_prompt_from_last.format(story=story, last_speech = last_speech, name=name, value=value)
        rewrite_speech = call_gpt(prompt,MODEL_validation)
        story = story.replace(to_replace_speech,rewrite_speech)
        rewrite_results.append(rewrite_speech)
    return story,'\n'.join(rewrite_results)

def process_text(text):
    text = text.strip('"')
    text = text.strip("'")
    text = text.strip("“")
    text = text.strip('”')
    return text
    
def modify_final_story(rewritten_speech,story):
    comments = rewritten_speech.split('\n\n')
    for comment in comments:
        if comment.startswith('Value'):
            
            comment=comment.strip()
            _,original_speech,refined_speech = comment.split('\n')
            original_speech = original_speech.strip('Original speech:')
            original_speech = process_text(original_speech)
         
            refined_speech = refined_speech.strip('Refined speech:')
            refined_speech = process_text(refined_speech)
            # print(original_speech,refined_speech)
            # print(bool(original_speech in story))
            story = story.replace(original_speech,refined_speech)
    return story
  
def _obvious_check_and_rewrite(story,values):
    result_check_obvious = call_gpt(check_obvious_speech_prompt.format(story = story, values=values), MODEL_validation)
    
    if 'NO' not in result_check_obvious and len(result_check_obvious.split('[Final answer]:'))>1:
            comments = result_check_obvious.split('[Final answer]:')[1]
            rewritten_speech = call_gpt(resolve_obvious_speech_prompt.format(story=story, values=values, comments = comments), MODEL_generation)
            story_final = modify_final_story(rewritten_speech, story)
    else:
        story_final = story
        comments=''
        rewritten_speech = ''
    return result_check_obvious,story_final, rewritten_speech

def load_combinations(file):
    df = pd.read_csv(file)
    existing_combinations=[]
    for index, row in df.iterrows():
        location=row['Location']
        values = row['values']
        existing_combinations.append([values,location])
    return existing_combinations


if __name__=='__main__':
    ground_truth_values=[]
    locations = []
    first_results=[]
    reflect_check_results = []
    reflected_story_results=[]
    rewritten_speeches = []
    consistent_check_results=[]
    consistent_story_results = []
    obvious_check_results=[]
    final_story_results = []
    obvious_rewrite_results=[]
    
    parser = argparse.ArgumentParser(
                    prog='Culture',
                    )
    parser.add_argument('-o','--output_file',default='generated_story_random_296.csv')           # positional argument
    parser.add_argument('-n','--number',default=296)
    parser.add_argument('-v', '--value_file',default='values/WVQ_simple.jsonl')
    parser.add_argument('-f','--previous_file',default="generated_story_random_400.csv")
    args = parser.parse_args()
    values, values_option = get_value_options(args.value_file)
    if args.previous_file=='':
        existing_combinations = []
    else:
        existing_combinations = load_combinations(args.previous_file)
    
    for i in tqdm(range(args.number)):
        question_prompts=[]
        selected_values = random.sample(values,5)
        for value in selected_values:       
            choice = random.choice(values_option[value])
            question_prompt = value + "--" + choice.strip() 

            question_prompts.append(question_prompt)
        question_prompt = '\n'.join(question_prompts)
        location = random.choice(predefined_scene)
        combination = [question_prompt,location]
        if combination in existing_combinations:
            continue
        else:
            existing_combinations.append(combination)
        prompt_first = first_generation_prompt  + '\n'.join(question_prompts) + "\nHere is the pre-defined location of the scene: "+location+'\nNow using the culture values to generate a story.'
        story_first = call_gpt(prompt_first, MODEL_generation)
        reflect_check,values_to_add = _reflect_check(story_first,question_prompt)
        if values_to_add.strip()!='':
            reflect_story = _reflect_value(story_first,values_to_add)
        else:
            reflect_story = story_first
        consistent_check= _consistency_check(reflect_story,question_prompt)
        if 'NO' not in consistent_check:
            consistent_story, rewritten_speech = _consistency_rewrite(reflect_story,question_prompt, consistent_check)
        else:
            consistent_story = reflect_story
        obvious_check, obvious_story, obvious_rewrite = _obvious_check_and_rewrite(consistent_story,question_prompt)
        locations.append(location)
        ground_truth_values.append(question_prompt)
        first_results.append(story_first)
        reflect_check_results.append(reflect_check)
        reflected_story_results.append(reflect_story)
        consistent_check_results.append(consistent_check)
        rewritten_speeches.append(rewritten_speech)
        consistent_story_results.append(consistent_story)
        obvious_check_results.append(obvious_check)
        final_story_results.append(obvious_story)
        obvious_rewrite_results.append(obvious_rewrite)
        dataframe = pd.DataFrame({"Location":locations,
                                  "values":ground_truth_values,
                        "First story":first_results,
                         
                         "Reflect check": reflect_check_results,
                         "Reflected story":reflected_story_results,
                         "Consistent check": consistent_check_results,
                         "Consistent story": consistent_story_results,
                         "rewritten speech": rewritten_speeches,
                         "Obvious check": obvious_check_results,
                         "Obvious rewrite":obvious_rewrite_results,
                         "Final story":final_story_results})

        dataframe.to_csv(args.output_file, index=False)
