import pandas as pd
from openai import OpenAI
import argparse
import os
import json
from tqdm import tqdm
from run_exps_open_api import call_gpt
from prompts_exps import llm_judge, llm_judge_topic_mentioned
api_key = os.getenv('YOU_API_KEY')
MODEL_evaluation = 'gpt-4o'

categories = ["ethics", "social", "religion", "politics", "security", "migration", "science"]
def parse_pred(pred):
    if '[Final answer]:' not in pred:
        return 
    answers = pred.split('[Final answer]:')[1]
    # all_values = []
    # for category in answers:
    #     all_values.extend(answers[category])
    
    # return all_values
    return answers

def parse_judgement(judgement):
   
    if '[Final answer]:' not in judgement:
        return
    final = judgement.split('[Final answer]:')[1]
    score_list = final.split('\n')
    scores=[]
    for score in score_list:
        if score.strip()=="":
            continue
        score = score.split(':')[-1].strip()
        if score=="":
            continue
        try:
            scores.append(float(score))
        except:
            continue
    if len(scores)==0:
            return
    return scores

def get_remove_indexes(dataset):
    remove_indexes=[]
    for data in dataset:
        value = data['values']
        contradiction = data['contradiction']
        remove_index=[]
        for contra in contradiction:
            try:
                remove_index.append(value.index(contra))
            except:
                continue
        remove_indexes.append(remove_index)
    return remove_indexes
            
    

if __name__ =='__main__':
    parser = argparse.ArgumentParser(
                    prog='Culture',
                    )
    parser.add_argument('-c','--category',default='social',choices=['random','political','social','ethical','religious','multiple','human'])
    parser.add_argument('-m', '--model',default= 'o3-mini',choices=['gpt-4o-mini','gpt-4o','o3-mini','o1','Qwen/Qwen2.5-32B-Instruct'])
    args = parser.parse_args()
    category = args.category
    data_file = f'datasets/dataset_{category}_original.json'
    result_file =  os.path.join('results',args.model,f'results_open_{category}_fixed.csv')
    evaluation_file = os.path.join('results',args.model,f'evaluation_results_open_{category}_fixed.csv')
    result_df = pd.read_csv(result_file)
    ground_truths = result_df['ground truth values'].to_list()
    predictions = result_df['predictions'].to_list()
    df_evaluation = pd.DataFrame()
    judgements=[]
    scores_all = []
    i = 0
    predictions_all=[]
    ground_truths_all=[]
    dataset = json.load(open(data_file))
    remove_indexes = get_remove_indexes(dataset)
    for pred, gt, index in tqdm(zip(predictions, ground_truths[:100], remove_indexes[:100])):
        
        final_answer = parse_pred(pred)
        judge_prompt = llm_judge.format(gt=gt, pred=final_answer)
        final_judge = call_gpt(judge_prompt, MODEL_evaluation)
        judgements.append(final_judge)
        predictions_all.append(pred)
        ground_truths_all.append(gt)
        scores = parse_judgement(final_judge)
        
        # if not scores:
        #     continue
        # if index!=[]:
        #     index=sorted(index)
        #     index.reverse()
        #     for id in index:
        #         scores.pop(id)
        # scores_all.extend(scores)
        # i+=1
        
    df_evaluation['judgement'] = judgements
    df_evaluation['prediction'] = predictions_all
    df_evaluation['ground truth'] = ground_truths_all
    df_evaluation.to_csv(evaluation_file,index=False)
    # print(sum(scores_all)/len(scores_all))
    





    
