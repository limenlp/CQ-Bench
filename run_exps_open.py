# open ended experiments
import pandas as pd
import os
from openai import OpenAI
import json
import argparse
from pydantic import BaseModel 
from tqdm import tqdm
from prompts_exps import * 
from vllm import LLM, SamplingParams
class Response(BaseModel):
    theme1: str
    theme2: str 
    theme3: str 
    theme4: str 
    theme5: str  

class Value(BaseModel):
    val: str 

api_key = os.environ.get("API_KEY")
api_key_ds = os.environ.get("API_KEY")
MODEL_generation = 'o3-mini'
MODEL_evaluation = 'gpt-4o'
client = OpenAI(api_key = api_key)
client_ds = OpenAI(api_key = api_key_ds,base_url="https://api.deepseek.com")

def call_model(prompt, model):
    if model.startswith('DeekSeek'):
       
        completion_model = client_ds.chat.completions.create(
        model = model,
        stream = False,
        messages=[
            {"role": "system", "content": f"You are an expert at understanding cultural values."}, 
            {"role": "user", "content": prompt}  
        ]
        )
    else:
        completion_model = client_ds.chat.completions.create(
        model = model,
        stream = False,
        messages=[
            {"role": "system", "content": f"You are an expert at understanding cultural values."}, 
            {"role": "user", "content": prompt}  
        ]
        )
    result = completion_model.choices[0].message.content
    
    return result

def parse_response(resp, type='response'):
    start = resp.index('{')
    end = resp.index('}')
    resp = resp[start:end+1]
    if type == 'response': 
        resp = Response(**json.loads(resp))  
    else: 
        # value 
        resp = Value(**json.loads(resp))
    return [resp.theme1, resp.theme2, resp.theme3, resp.theme4, resp.theme5]

def rephrase_values(values, topic):
    values_rephrased = [] 
    values = values.split("\n")
    for v in values:
        v_prompt = rephrase_prompt.format(value=v) 
        response = call_model(v_prompt, MODEL_generation) 
        val = parse_response(response, 'value')
        values_rephrased.append(val)

    return values_rephrased

def main():
    parser = argparse.ArgumentParser(
                    prog='Openended-CI')   
    
    parser.add_argument('-c', '--category', default='human',choices = ['random','ethical','political','religious','social','human'])
    parser.add_argument('-v', '--valueType', default='ethics, social, religion, politics, security, migration and science') 
    parser.add_argument('-m','--model',default='o1',choices=['gpt-4o-mini','o3-mini','o1','deepseek-chat','deepseek-reasoner','Qwen/Qwen2.5-32B-Instruct'])
    # parser.add_argument('-out', '--outFile', default="results/o3-mini/results_open_random.csv")
    args = parser.parse_args()
    category = args.category
    model = args.model
    outfile = os.path.join('results',args.model,f'results_open_{category}_fixed.csv')
    # read data 

    file = f'datasets/dataset_{category}_original.json'
    data = json.load(open(file))

    results_file = pd.DataFrame()

    scores = []
    total_values = []
    original_values = []
    final_judges = [] 
    summary_judges = []
    gt_resolved = []
    predictions = [] 
    
    if model!='Qwen/Qwen2.5-32B-Instruct':
        for i, _ in tqdm(enumerate(data)):       
            story = _['story']
            p1 = multi_step_prompt_p1.format(story=story, topic=args.valueType)
            response = call_model(p1, args.model)

            summary = response 
            if category not in ["random","human"] :
                valueType = category
            else:
                valueType = args.valueType
            p2 = multi_step_prompt_p2.format(story=story, topic=valueType, summary=summary)
            preds = call_model(p2, args.model) 

            gt_values = _['values']
            original_values.append(gt_values)
        
            predictions.append(preds)
    else:
        llm = LLM(model=model,trust_remote_code=True)
        sampling_params = SamplingParams(temperature=0.8,max_tokens=4096)
        all_multi_step_prompt_p1=[]
        for i, _ in enumerate(data): 
        # print(len(data))
            story = _['story']
            if category!="random":
                valueType = category
            else:
                valueType = args.valueType
            p1 = multi_step_prompt_p1.format(story=story, topic=args.valueType)
            all_multi_step_prompt_p1.append([
            {"role": "system", "content": f"You are an expert at understanding cultural values."}, 
            {"role": "user", "content": p1}  
        ])
        all_summary_response = llm.chat(messages=all_multi_step_prompt_p1,
                        sampling_params=sampling_params,
                        use_tqdm=True)
        all_summary = [output.outputs[0].text for output in all_summary_response]
        
        all_multi_step_prompt_p2=[]
        for d,summary in tqdm(zip(data,all_summary)):
        
            story = d['story']
            p2 = multi_step_prompt_p2.format(story=story, topic=args.valueType, summary=summary)
            all_multi_step_prompt_p2.append([
            {"role": "system", "content": f"You are an expert at understanding cultural values."}, 
            {"role": "user", "content": p2}  
        ])
        all_results_response = llm.chat(messages=all_multi_step_prompt_p2,
                        sampling_params=sampling_params,
                        use_tqdm=True)
        all_results = [output.outputs[0].text for output in all_results_response]

        for _,pred in tqdm(zip(data,all_results)):

            gt_values = _['values']
            original_values.append(len(gt_values)) 
            predictions.append(pred)
            gt_resolved.append(gt_values)

    results_file['predictions'] = predictions
    results_file['ground truth values'] = original_values
    results_file.to_csv(outfile, index=False)

if __name__=='__main__':

    main()