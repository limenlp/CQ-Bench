from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
from transformers import pipeline
import os
from openai import OpenAI
from tqdm import tqdm
import jsonlines
import random
import re
import json
import argparse
from vllm import LLM, SamplingParams
from prompts_exps import *
import sys

api_key = " Your API_KEY"
api_key_ds = "Your API_KEY"
client = OpenAI(api_key = api_key)

client_ds = OpenAI(api_key = api_key_ds,base_url="https://api.deepseek.com")

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


def generate_prompts(dataset,setting,category,reasoning, prompt_type):
    prompts_all = []
    for data in dataset:
        story = data['story']
        if setting=='1':
          
            for question in data['questions']:
                value = question['value']
                
                options = question['options']
               
                if not reasoning:
                    if category == 'multiple':
                        name = question['name']
                        prompt = instruction_prompt_text_setting_1_multiple.format(story=story,statement=value,options=options, name=name)
                    else:
                        prompt = instruction_prompt_text_setting_1.format(story=story,statement=value,options=options)
                else:
                    if category == 'multiple':
                        name = question['name']
                        #TODO: add step by step
                        prompt = instruction_prompt_reasoning_setting_1_multiple.format(story=story,statement=value,options=options, name=name)
                    else:
                        if prompt_type == 'zero':
                            prompt = instruction_prompt_reasoning_setting_1_step_by_step_zero_shot.format(story=story,statement=value,options=options)
                        else:
                            prompt = instruction_prompt_reasoning_setting_1_step_by_step_one_shot.format(story=story,statement=value,options=options,demonstration=demonstration_t1)

                messages = [
                    {"role": "system", "content": "You are an American who has basic common sense"},
                    {"role": "user", "content": prompt}
                    ]
                prompts_all.append(messages)


        elif setting=='2':
            true_values = data['values']
            options_provided = '\n'.join(data['options'])
            option_prompt = "\nHere are 15 options:\n" + options_provided
            if not reasoning:
                prompt = instruction_prompt_text.format(number=len(true_values))+ story + option_prompt + format_prompt_text
    
            else:
                if prompt_type == 'zero':
                    prompt = instruction_prompt_text_setting2_decompose_zero_shot.format(number=len(true_values),story=story,options=option_prompt)
                else:
                    prompt = instruction_prompt_text_setting2_decompose_one_shot.format(number=len(true_values),story=story,options=option_prompt,demonstrations=demonstration)

            messages = [
                {"role": "system", "content": "You are an American who has basic common sense"},
                {"role": "user", "content": prompt}
                ]
            prompts_all.append(messages)
        elif setting == '3':
            raise NotImplementedError
          
    return prompts_all
            
           
if __name__ =='__main__':
    parser = argparse.ArgumentParser(
                    prog='Culture',
                    )
    parser.add_argument('-m', '--model',default= 'o3-mini',choices=[
        'Qwen/Qwen2.5-7B-Instruct',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_7b_lora_sft_5',
        '/home/ziyi/LLaMA-Factory/output/llama3.2_3b_lora_sft',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_14b_lora_sft_5',
        '/home/ziyi/LLaMA-Factory/output/llama3.2_3b_lora_sft_attitude',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_7b_lora_sft_5_attitude',
        '/home/ziyi/LLaMA-Factory/output/qwen2.5_14b_lora_sft_5_attitude',
        'Qwen/Qwen2.5-14B-Instruct',
        'Qwen/Qwen2.5-32B-Instruct',
        'gemini-2.0',
        'deepseek-v3',
        'deepseek-r1',#only on 25 stories for now 
        'o3-mini',#only on 25 stories for now
        'o1',
        'gpt-4o-mini',
        'Llama-3.1-8B-Instruct',
        'meta-llama/Llama-3.1-70B-Instruct',
        'meta-llama/Llama-3.3-70B-Instruct',
        'meta-llama/Llama-3.2-3B-Instruct',
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
    ])     

    parser.add_argument('-g', '--setting',default='1') #setting 1 attitude detection, setting 2 value detection(multi-select)
    parser.add_argument('-r','--reasoning',action='store_true')
    parser.add_argument('-o','--output_folder',default='results')
    parser.add_argument('-p','--prompt',default='zero', choices=['zero','one'])
    
    parser.add_argument('-c','--category',default='social',choices=['random','politic','social','ethical','religious','multiple','human'])
    args = parser.parse_args()
 
    model_name = args.model

    setting = args.setting
    category = args.category
    reasoning = args.reasoning
    prompt_type = args.prompt
    data_file = f'dataset_setting{setting}_{category}.json'
    dataset = json.load(open(os.path.join('datasets',data_file)))
    folder = os.path.join(args.output_folder, args.model)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    result_column = []
    # options_column = []

    if args.reasoning:
        if 'sft' not in model_name:
            if prompt_type == 'one':
                output_file = f'results_{setting}_{category}_reasoning_one_shot.json'
            else:
                output_file = f'results_{setting}_{category}_reasoning.json'
        else:
            output_file = f'results_{setting}_{category}_reasoning_sft.json'
    else:
        output_file = f'results_{setting}_{category}.json'
    print(output_file)
    if os.path.exists(os.path.join(folder,output_file)):
        print('exist')
        sys.exit()
    all_prompts = generate_prompts(dataset,setting,category,reasoning,prompt_type)
    if model_name in open_source_models:
        if model_name in ['meta-llama/Llama-3.3-70B-Instruct']:

            llm = LLM(model=model_name,trust_remote_code=True,tensor_parallel_size=4)
        elif model_name in ['Qwen/Qwen2.5-32B-Instruct']:
            llm = LLM(model=model_name,trust_remote_code=True,tensor_parallel_size=2)
        else:
            llm = LLM(model=model_name,trust_remote_code=True)
        sampling_params = SamplingParams(temperature=0.8,max_tokens=4096)
        outputs = llm.chat(messages=all_prompts,
                   sampling_params=sampling_params,
                   use_tqdm=True)
        for output in outputs:
            generated_text = output.outputs[0].text
            result_column.append(generated_text)
        json.dump(result_column,open((os.path.join(folder,output_file)),'w'),indent=4)
  
    elif model_name in api_models:
        if model_name in ['deepseek-reasoner','deepseek-chat']:
            for message in tqdm(all_prompts):
                response = client_ds.chat.completions.create(
                    model=model_name,
                    messages=message,
                    stream=False
                )

                result = response.choices[0].message.content
                result_column.append(result)
                json.dump(result_column,open((os.path.join(folder,output_file)),'w'),indent=4)

        if model_name in ['gpt-4o-mini','gpt-4o','o3-mini','o1']:
            print(len(all_prompts))
            for message in tqdm(all_prompts):
                completion = client.chat.completions.create(
                model=model_name,
                messages=message
                )         
                result = completion.choices[0].message.content
                result_column.append(result)
                json.dump(result_column,open((os.path.join(folder,output_file)),'w'),indent=4)
        else:
            raise NotImplementedError
        
    
   
       
