# open ended experiments
import pandas as pd
import os
from openai import OpenAI
import json
import argparse
from pydantic import BaseModel 
# from vllm import LLM, SamplingParams
from prompts_exps import * 
from tqdm import tqdm
open_source_models = ['Qwen/Qwen2.5-7B-Instruct',
        'Qwen/Qwen2.5-14B-Instruct',
        'Qwen/Qwen2.5-32B-Instruct',
        'Llama-3.1-8B-Instruct',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_7b_lora_sft_5',
        '/home/ziyi/LLaMA-Factory/output/llama3.2_3b_lora_sft',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_14b_lora_sft_5',
        '/home/ziyi/LLaMA-Factory/output/llama3.2_3b_lora_sft_attitude',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_7b_lora_sft_5_attitude',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_14b_lora_sft_5_attitude',
        'meta-llama/Llama-3.1-70B-Instruct',
        'meta-llama/Llama-3.2-3B-Instruct',
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"]
api_models = ['gemini-2.0',
        'deepseek-v3',
        'deepseek-r1',
        'o3-mini',
        'o1',
        'gpt-4o-mini',
]

class Response(BaseModel):
    theme1: str
    theme2: str 
    theme3: str 
    theme4: str 
    theme5: str  

class Value(BaseModel):
    val: str 

api_key = "Your API_KEY"
MODEL_generation = 'o3-mini'
MODEL_evaluation = 'gpt-4o'
client = OpenAI(api_key = api_key)

def call_gpt(prompt, model):
    
    completion_model = client.chat.completions.create(
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
        response = call_gpt(v_prompt, MODEL_generation) 
        val = parse_response(response, 'value')
        values_rephrased.append(val)

    return values_rephrased

if __name__=='__main__':

    parser = argparse.ArgumentParser(
                    prog='Openended-CI')   
    parser.add_argument('-s', '--stories', default='datasets/dataset_random_original.json')
    parser.add_argument('-v', '--valueType', default='ethics, social, religion, politics, security, migration and science') 
    parser.add_argument('-out', '--outFile', default="random_32b_updated_1.csv")
    parser.add_argument('-m','--model', default="Qwen/Qwen2.5-32B-Instruct")
    args = parser.parse_args()
    outfile = os.path.join('results',args.model,f'results_open_{category}.csv')
   
    # read data 
    file = open(args.stories)
    data = json.load(file)
    model_name = args.model
    results_file = pd.DataFrame()
    if model_name in open_source_models:
        if model_name in ['meta-llama/Llama-3.3-70B-Instruct']:

            llm = LLM(model=model_name,trust_remote_code=True,tensor_parallel_size=4)
        elif model_name in ['Qwen/Qwen2.5-32B-Instruct']:
            llm = LLM(model=model_name,trust_remote_code=True,tensor_parallel_size=2)
        else:
            llm = LLM(model=model_name,trust_remote_code=True)
        sampling_params = SamplingParams(temperature=0.8,max_tokens=4096)
        
    scores = []
    total_values = []
    original_values = []
    reasoning = [] 
    gt_resolved = []
    predictions = [] 
    final_judges = []
    all_multi_step_prompt_p1=[]
    for i, _ in enumerate(data): 
        # print(len(data))
        story = _['story']
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
        # response = call_gpt(p1, MODEL_generation)
        # we are going to get the summary 
        # summary = (response[response.index("\"summary\":")+11:-6]) 
        # summary = response 
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
        # preds = call_gpt(p2, MODEL_generation) 
        # print(preds)
    # use LLM as judge to decide how correct this is. 
    i=0
    for _,pred in tqdm(zip(data,all_results)):
        i+=1
        gt_values = _['values']
        original_values.append(len(gt_values)) 
        # contr = _['contradiction'] 
        # p3 = resolve_values.format(values=gt_values, contradiction=contr)
        # response = call_gpt(p3, MODEL_generation)
        # print(response)

        # finally judge 
        # p4 = llm_judge.format(gt=gt_values, pred=pred)
        # final_judge = call_gpt(p4, MODEL_generation)

        predictions.append(pred)
        gt_resolved.append(gt_values)
        # p4 = llm_judge.format(gt=gt_values, pred=pred)
        # final_judge = call_gpt(p4, MODEL_evaluation)
        # final_judges.append(final_judge)
        # predictions.append(pred)
        # gt_resolved.append(response)
        # print(final_judge)

        # try: 
        #     # parse final_judge 
        #     start = final_judge.index('{')
        #     end = final_judge.index('}')
        #     final_judge = final_judge[start:end+1]
        #     print(final_judge)
        #     final_judge = json.loads(final_judge)
        #     scores.append(final_judge['score'])
        #     reasoning.append(final_judge['reasoning'])
        #     total_values.append(final_judge['len_ground_truth'])

        # except: 
        #     scores.append(final_judge) 
        #     reasoning.append(final_judge)
        #     total_values.append(final_judge)

        # if i == 50: 
        #     break
    
    # results_file['reasoning'] = final_judges 
    # results_file['total values'] = total_values 
    # results_file['original total values'] = original_values
    results_file['predictions'] = predictions
    results_file['ground truth values'] = gt_resolved
    results_file.to_csv(outfile, index=False)