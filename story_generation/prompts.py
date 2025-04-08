# first prompt
first_generation_prompt = """You will be provided by 5 culture values and a location where the conversation happens. Each of them follow the format [culture]--[value]. The first [culture] describe a statement or a situation, and [value] is how you agree with the culture or is the culture common or not.\n
   Your task is to generate a scene including conversations and actions among multiple people and the scene needs to reflect the culture values provided.\n
   Here are some requirements of the scene:\n
   1. It cannot be too short. It should have multiple rounds of interaction among people.
   2. It should not be too obvious. It cannot directly spit out or rephrase the values.
   3. It cannot be easy to human to understand the culture values behind.
   4. You do not need to follow the order of the values. You could mention the values multiple times through the conversation. Make sure the conversation flows well.  
   5. All the characters should follow the given values. There should not be contradictions between character's value and given value.
   Here are the culture values you should follow when generating:\n
"""
#check obvious reflection and rewrite (gpt4o-mini)
#TODO: split check and rewrite into two steps. 
#TODO: 1. first prompt 2. check values unreflected 3. add values. 4. check obvious mentioned 5. rewrite. 6. check inconsistency 7. resolved
#check obvious part, gpt4o
#check if all the values are reflected (gpt4o)
check_reflect_prompt = """You will be provided a story and values reflected in the story.\n
Your task is to check if the story reflect the values? The story would not mention the values directly. 
You will need some reasoning to analyse the story.

Here is the original story:
{story}\n

Here are the values to reflect in the story:
{values}

For each value, output if the value is reflected and provide reasoning.
In the end, output the values not reflected without the reasoning. 
Only output the exact and comprehensive value including "--" within it, do not rephrase! If all the values are reflected, just leave it blank. 
Follow the format:
[Value]:[Reasoning, Yes/No]\n
.....
Values not reflected:
[Value]"""
check_reflect_prompt_multiple = """You will be provided a story and values reflected in the story.\n
Your task is to check if the story reflect the values? The story would not mention the values directly. 
The values are related to characters. Therefore, you need to check if specific characters have the value.
You will need some reasoning to analyse the story.

Here is the original story:
{story}\n

Here are the values to reflect in the story:
{values}

For each value, output if the value is reflected and use reasoning steps to support the answer.
In the end, output the values not reflected without reasoning. 
Only output the exact and comprehensive value including "--" and character name within it, do not rephrase! If all the values are reflected, just leave it blank. 
Follow the format:
[Value]:[Reasoning,Yes/No]\n
.....
Values not reflected:
[Name:Value]
"""

#rewrite based on gpt4o's detection(gpt4o-mini)
refine_the_story_prompt = """You will be provided a story and values which need to be reflected in the story.\n
Your task is to refine the story to reflect the value provided. 
You cannot remove anything or replace existing speeches from the story, you can only add conversations to reflect the value.

The refinement should flow with original story well. You cannot add new conversation randomly.
Here is the original story:
{story}\n

Here are the values to reflect in the story:
{values}

Now refine the story.
"""
#check consistency prompt (gpt4o) 
#
check_consistency_prompt = """You will be provided a story and values reflected in the story.\n
Your task: for each value, check if all the characters agree with the value. If there is characters who does not agree with the value, you should output the character name and his speech, and why the speech does not align with the value.
Here is the original story:
{story}\n

Here are the values to reflect in the story:
{values}

Now check the story and output if there is any contradiction. You can output reasoning to help you analyse. However, in the end, only output where is the contradiction one by one. If there isn't contradiction, just reply NO. Otherwise, reply where is the contradiction.

Follow the format strictly, do not change the format, output exact values from the values provided, do not rephrase:\n
[Reasoning]:
[Value--attitude]:[If all the speeches are aligned with the value]\n
[Contradictions]:
[Value--attitude]: [*character name*:speech]\n\n
......
"""

resolve_consistency_prompt = """You will be provided a story and values which need to be reflected in the story.\n
However, the story includes some contradiction where characters do not agree on certain values. You will be provided where is the contradiction.
The contradiction includes 3 parts: 
1. Correct value to follow
2. Character name
3. Character speech

Your task is to replace the speech mentioned in the contradications with a new speech to make sure the speech is aligned with the values
The refinement should flow with original story well. You cannot add new conversation randomly.
Here is the original story:
{story}\n


Here are the contradictions:
{contradiction}

Ignore the original character speech. Directly write a new speech which reflect the value.

Here is the rewritten speech:
"""
resolve_consistency_prompt_from_last = """You will be provided a story and values which need to be reflected in the story.\n

Your task is to write a speech to follow the value and flow with the previous speech.

Here is the original story:
{story}\n

Here is the last speech from last character:
{last_speech}

Here is the value you need to follow:
{value}

Here is the character name for new speech:
{name}

You should output a speech in a converstation style aligned with the story. Keep it short and casual. Make sure the speech follows the value even it is against the value of diversity and gender equality.

Here is the new speech:
"""

resolve_consistency_prompt_templated = """You will be provided a story and values which need to be reflected in the story.\n

Your task is to write a speech to follow the value and flow with the previous speech.

Here is the original story:
{story}\n

Here is the last speech from last character:
{last_speech}

Here is the value you need to follow:
{value}

Here is the character name for new speech:
{name}

You should output a speech in a converstation style aligned with the story. Keep it short and casual. Make sure the speech follows the value even it is against the value of diversity and gender equality.

You need to follow the value in the beginning and oppose the value in the last sentence. Make sure the character name only occurs before their speech.
Here is the new speech:
"""

rewrite_speech_prompt = """You will be provided a story and a value you need to follow. Your task is to write a speech for the character and the speech should reflect the value.
To make sure the speech flows well with the original story, we provide you the nearest context.

Here is the original story:
{story}

Here is the speech from last character:
{context}

Here is the value you need to follow:
{value}

Write a speech.
"""
check_obvious_speech_prompt="""You will be provided a story and values reflected in the story.\n
Your task is to check if there is obvious speech which directly mention or rephrase the values? If the story mention phrases or sentences from values, that would be also counted as directly mentioned\n
If it just reflects the value but not rephrase the values, it is not considered as obvious speech.
Here are some examples for obvious speech:

[Example 1]
Value: In your view, how often do the following things occur in this country’s elections:Journalists provide fair coverage of elections—Very often
Speech: "I think journalists do their best to cover things fairly"
Explanation: The speech bascially rephrase the value without providing supporting evidence

[Example 2]:
Value: How frequently do the following things occur in your neighborhood: Robberies?--Not frequently  
Speech: “Well, at least we’re not dealing with robberies or anything in our area.” 
Explanation: The speech directly reflect the value.

[Example 3]:
Value: In your view, how often do the following things occur in this country’s elections:Voters are bribed?--Not often
Speech: "Like, I saw that poll about whether voters were bribed or not—completely not a thing here." 
Explanation: The speech basically rephrase the value without providing supporting evidence

[Example 4]:
Value: In your view, how often do the following things occur in this country’s elections: Voters are threatened with violence at the polls?--Not often
Speech: "And let’s not forget—when was the last time someone actually got threatened at the polls?" 
Explanation: Instead of providing some example, the speech directly says it is rare that someone got threatened at the polls.

You should output places where the values are directly mentioned. If the values are not directly spit out, do not output it!!! 

Here is the original story:
{story}\n

Here are the values to reflect in the story:
{values}

Now check if any parts of stories directly mentioned the values. You can output reasoning or evidence and help you analyse.
However, in the final answer, output speeches where the values are directly mentioned and the corresponding values. If there is no directly mentioned values, just output NO in the final answer.

Follow the format:
[Reasoning]: reasoning
[Final answer]: [value]:[speech]\n
[value]:[speech]\n
.....
"""
# rewrite the obvious part (gpt4o-mini)
resolve_obvious_speech_prompt="""You will be provided a story and values reflected in the story.\n
You will be also provided with some comments where the values are directly mentioned in the story.\n
Each comment includes a value and a speech where the speech directly reflect the value.
Your task is to refine the speech by rewriting the places where they directly mention the values.\n
Instead of speaking out values directly, characters should reflect values implicitly by using anecdotes.\n
Imagine the place is not a safe place to speak out, characters need to respect each other and not to offend others.\n
You need to make sure after rewriting, people are able to detect values by the speech. It cannot be too abstract.

Here are some examples:

[Example 1]:
Value:  How frequently do the following things occur in your neighborhood: Robberies?--Not frequently
Original speech: “Well, at least we’re not dealing with robberies or anything in our area.” 
Refined speech: "You know in other counties, cars got breaking in is common. At least we don't have to worry about that."

[Example 2]:
Value: In your view, how often do the following things occur in this country’s elections:Journalists provide fair coverage of elections—Very often
Original speech: "I think journalists do their best to cover things fairly"
Refined speech: "I remember watching the last election coverage—there was this debate where the journalist made sure both candidates had their say and pushed back equally when things didn’t add up. It stuck with me how they kept it balanced, asking tough questions to both sides." 

[Example 3]:
Value: When a mother works for pay, the children suffer -- agree
Original speech: " I don't think mom should work you know, their children will suffer."
Refined speech: "Low key, but look at Maria's kids. How poor they are, can you imagine how they live. Their mom is working and I bet she does not have time to take care of them."

[Example 4]:
Value: People who don’t work turn lazy -- disagree
Original speech: "I don't think people who don't work will turn lazy"
Refined speech: "We should relax! We work enough in work days. It won't change anything to take a break for a month."

Here is the original story:
{story}\n

Here are the values to reflect in the story:
{values}

Here is the comments that you need to refer when refining the story:
{comments}

Please rewrite the speech one by one in the story. Do not miss any comments.

For each rewritten speech, you need to follow this format:
Value:[value]
Original speech: [Speech in the comment]
Refined speech: [You rewritten speech]

Here is your output:
"""



