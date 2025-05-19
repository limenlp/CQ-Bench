import jsonlines
import re
import random
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
from prompts import *
from generate_story_pipeline import _obvious_check_and_rewrite

MODEL_generation = 'gpt-4o-mini'
MODEL_validation = 'gpt-4o'
client = OpenAI(api_key = os.getenv('YOUR_KEY')

values_option={}
values = []
reader = jsonlines.open('WVQ_opinion.jsonl')
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
    # for option in options:
    #     if option.replace(' ','')=='':
    #          continue
    #     prompt = value + " -- " + option
    #     options_all.append(prompt)

def call_gpt(prompt,model="deepseek-chat"):
    if 'deepseek' in model:
        completion_same = client_ds.chat.completions.create(
        model = model,
        stream = False,
        messages=[
            {"role": "system", "content": "You are an expert in story generation and culture."}, 
            {"role": "user", "content": prompt}  
        ]
        )
    else:
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

# prompt ="""
# You will be provided by 5 culture values. Each of them follow the format [culture]--[value]. The first [culture] describe a statement or a situation, and [value] is how you agree with the culture or is the culture common or not.\n
#    Your task is to generate a scene including conversations and actions among multiple people and the scene needs to reflect the culture values provided.\n
#    Here are some requirements of the scene:\n
#    1. It cannot be too short. It should have multiple rounds of interaction among people. The whole story should be around 800 words.\n
#    2. It should not be too obvious. It cannot directly spit out the values.\n
#    3. It cannot be too easy to human to understand the culture values behind.n
#    4. You do not need to follow the order of the values. You could mention the values multiple times through the conversation. Make sure the conversation flows well.
#    5. You should provide a location or a context for the conversation.
#    Here are the culture values you should follow when generating:\n
#     {values}
    
#    Now using the culture values to generate a scene."""

prompt_character_different_attitudes ="""
You will be provided by multiple culture values and each value belongs to one character. Each of them follow the format [character name]:[statement]--[attitude]. The first [statement] describe a statement or a situation, and [attitude] is how you agree with the culture or is the culture common or not.\n
   Your task is to generate a long conversation including only conversations among multiple people and the converation needs to reflect the culture values provided.\n
  
   Here are some requirements of the scene:\n
   1. It cannot be too short. It should have multiple rounds of interaction among people.
   2. It should not be too obvious. It cannot directly spit out or rephrase the values.
   3. It cannot be easy to human to understand the culture values behind.
   4. You do not need to follow the order of the values. You could mention the values multiple times through the conversation. Make sure the conversation flows well.\n
   5. The character names are provided. Use the provided character name to generate stories.\n
   6. Remember each value is assigned to one specific character. Make sure the value differences between characters are reflected in the story.\n
  """

prompt_character_1_value ="""
You will be provided by 1 culture values. It follow the format [culture]--[attitude options]. The first [culture] describe a statement or a situation, and [attitude options] is how you agree with the culture or is the culture common or not.\n
   
   Your task is to generate a scene including conversations and actions among multiple people and the scene needs to reflect the culture value provided.\n

   Here are some requirements of the scene:\n
   1. It cannot be too short or too long. It should have multiple rounds of interaction among people.\n
   2. It should not be too obvious. It cannot directly spit out the values.\n
   3. It cannot be too easy to human to understand the culture values behind.n
   4. You should provide a location or a context for the conversation in the beginning.\n
   5. All the characters should share the same value.\n
   Here is the culture value you should follow when generating:\n
    {value}
   Now using the culture value to generate a scene."""

stories = []
ground_truth = []
names = ["Priya", "Sam", "Brian", "Alice"]
predefined_scene = ['company', 'school','neighborhood','national park','restaurant','amusement park','airplane']
first_result=[]
final_story=[]
reflect_check = []
reflect_result=[]
consistency_result=[]
consistent_check =[]
obvious_rewrites=[]
obvious_checks =[]

locations = []
for i in range(3):
    print(i)
    question_prompts=[]
    selected_values = random.sample(values,5)
    for value in selected_values:       
        # for i in range(5):
        select_options = random.choices(values_option[value],k=4)
        for i,option in enumerate(select_options):
            question_prompts.append(names[i]+":"+value+'--'+option.strip())
       
    question_prompt = '\n'.join(question_prompts)
    location = random.choice(predefined_scene)
    # first story
    prompt_first = prompt_character_different_attitudes  + '\n'.join(question_prompts) + "\nHere is the pre-defined location of the scene: "+location+'\nNow using the culture values to generate a story.'
    story_first = call_gpt(prompt_first,MODEL_generation)
    # check values not reflected and refine 
    result_check_reflect = call_gpt(check_reflect_prompt_multiple.format(story = story_first,values = question_prompt),model=MODEL_validation)
    result_check_reflect_reasoning,to_add_values = result_check_reflect.split('Values not reflected:')
    # to_add_values = result_check_reflect[-1]
    if len(to_add_values.strip())>=5:
        story_reflect = call_gpt(refine_the_story_prompt.format(story = story_first, values = to_add_values),model=MODEL_generation)
    else:
        story_reflect = story_first
   
    # check obvious statement and rewrite
    obvious_check, obvious_story, obvious_rewrite = _obvious_check_and_rewrite(story_reflect,question_prompt)
    
    ground_truth.append(question_prompt)

    locations.append(location)
    first_result.append(story_first)
    reflect_check.append(result_check_reflect)
    reflect_result.append(story_reflect)

    obvious_checks.append(obvious_check)
    obvious_rewrites.append(obvious_rewrite)
    
    final_story.append(obvious_story)


dataframe = pd.DataFrame({"First story":first_result,
                          "Location":locations,
                         "values":ground_truth,
                         "Reflect check": reflect_check,
                         "Reflected story":reflect_result,
                         "Obvious check": obvious_check,
                         "Obvious rewrite":obvious_rewrites,
                         "Final story":final_story})

dataframe.to_csv('generated_story_5_value_all_steps_opinion_multiple_attitude.csv', index=False)
