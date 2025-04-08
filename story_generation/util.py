import pandas as pd
import re
from bert_score import score
from tqdm import tqdm
from generate_story_pipeline import longest_common_substrings
# Find unmatched questions in llama outputs and the closest match from options 
def find_unmatched_with_progress(row):
    llama_lines = set(line.strip() for line in row['prediction'].split('\n') if '--' in line)
    option_lines = set(line.strip() for line in row['options'].split('\n') if '--' in line)
    
    # Split each line into questions and answers
    llama_questions_answers = [line.split('--', 1) for line in llama_lines]
    option_questions_answers = [line.split('--', 1) for line in option_lines]
    
    # Extract only the questions from both sets
    llama_questions = {qa[0].strip() for qa in llama_questions_answers}
    option_questions = {qa[0].strip() for qa in option_questions_answers}
    
    # Find unmatched questions in 'llama' that are not in 'options'
    unmatched_questions = llama_questions.difference(option_questions)
    
    # If no unmatched questions, return empty strings
    if not unmatched_questions:
        return pd.Series(["", ""], index=['unmatched', 'closest_match'])
    
    # Reconstruct unmatched questions with their answers
    unmatched_question_list = []
    closest_match_list = []
    
    for unmatched_question in unmatched_questions:
        unmatched_qa = next(qa for qa in llama_questions_answers if qa[0].strip() == unmatched_question)
        unmatched_question_full = ' -- '.join(unmatched_qa)
        unmatched_question_list.append(unmatched_question_full)
    
    # Calculate BERTScore to find closest match
    for unmatched_question_full in unmatched_question_list:
        unmatched_question = unmatched_question_full.split(' -- ')[0]
        best_match = None
        best_score = -1
        
        for option_qa in option_questions_answers:
            option_question = option_qa[0].strip()
            _, _, F1 = score([unmatched_question], [option_question], lang="en", verbose=False)
            similarity_score = F1[0].item()
            
            if similarity_score > best_score:
                best_score = similarity_score
                best_match = ' -- '.join(option_qa)
        
        if best_score >= 0.85:
            closest_match_list.append(best_match)
        else:
            closest_match_list.append(unmatched_question_full)

    unmatched_str = '\n'.join(unmatched_question_list)
    closest_match_str = '\n'.join(closest_match_list)
    
    return pd.Series([unmatched_str, closest_match_str], index=['unmatched', 'closest_match'])


def normalize_line(line):
    return re.sub(r'\s*--\s*', ' -- ', line.strip())

# function to replace unmatched lines with closest match
def replace_unmatched_with_closest(row):
    # Normalize and split 'llama3.1' into lines
    llama_lines = [normalize_line(line) for line in row['prediction'].split('\n') if '--' in line]
    
    # Split unmatched and closest_match into lines
    unmatched_lines = [normalize_line(line) for line in row['unmatched'].split('\n') if line.strip()] if row['unmatched'] else []
    closest_lines = [normalize_line(line) for line in row['closest_match'].split('\n') if line.strip()] if row['closest_match'] else []
    
    # Create a mapping from unmatched lines to closest matches
    unmatched_to_closest = dict(zip(unmatched_lines, closest_lines))
    
    # Replace unmatched lines in llama_lines with closest match
    updated_llama = [unmatched_to_closest.get(line, line) for line in llama_lines]
    
    return '\n'.join(updated_llama)

# def compare_strings(s1,s2):
#     embedding1 = model.encode(s1, convert_to_tensor=True)
#     embedding2 = model.encode(s2, convert_to_tensor=True)
#     similarity = util.cos_sim(embedding1, embedding2)
#     if similarity >0.5:
#         return 1
#     else:
#         return 0
def match_value(value,ground_truth):
    max_len=0
    return_result = ''
    # ground_truth=ground_truth.split('\n')
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
def process_reflect_check(result,ground_truth):
    result_check_reflect_list = result.split('Values not reflected:')
    to_add_values = result_check_reflect_list[-1]
    values=[]
    if len(to_add_values)<20:
        return []
    if to_add_values.strip()=='':
        return []
    if 'None' in to_add_values:
        return []
    else:
        to_add_values =  to_add_values.split('\n')
        # print(to_add_values)
        for v in to_add_values:
            if v.strip()=='' or 'NO' in v:
                continue
            else:
                v = match_value(v, ground_truth)
                if v!='':
                    values.append(match_value(v,ground_truth))
    values = list(set(values))
    if '**' in values:
        values.remove('**')
    return values

def combine_missing_values(missing_values_list,ground_truth,method='all'):
    combined_missing_values=[]
    if method=='all':
        for missing_values in missing_values_list:
            for value in missing_values:
                if value not in combined_missing_values:
                    combined_missing_values.append(value)
    elif method=='majority':
        for value in ground_truth:
            count=0
            for missing_values in missing_values_list:
                if value in missing_values:
                    count+=1
            if count>=2:
                combine_missing_values.append(value)
    return combined_missing_values

def process_consistency(consistent_check,ground_truth):
    consistent_checks = consistent_check.split('\separator')
    contradictions={}
    for comment in consistent_checks:
        try:
            comment = comment.split('[Contradictions]:')[1]
        except:
            continue
        comment = comment.strip('*')
        comment = comment.strip('\n')
        comment_singles = comment.split('\n')
        # sentences = story.split('\n\n')
        # rewrite_results=[]
        
        for contradiction in comment_singles:
            if contradiction.strip()=='':
                continue
            if 'NO' in contradiction:
                continue
            if len(contradiction.split(':'))<3:
                continue
            name = contradiction.split(":")[-2].strip()
            value_list = contradiction.split(":")[:-2]
            value = ':'.join(value_list)
            value = match_value(value,ground_truth)
            name = name.strip().strip('[')
            name = name.strip('*')
            if value in contradictions:
                if name not in contradictions[value]:
                    contradictions[value].append(name)
            else:
                contradictions[value]=[name]
            

    return contradictions