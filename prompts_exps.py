instruction_prompt_text = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided 15 options and you need to select {number} correct answers from the options. (Only {number}  options are correct).\n 
You need to choose the whole option, for example:\n
Being a housewife is just as fulfilling as working for pay-- agree\n
Make sure you include '--' in the answer.\n
Here is the scenario:\n
"""
instruction_prompt_number_only = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided 15 options and you need to select {number}  correct answers from the options. (Only {number}  options are correct).\n 
We will provide index for each option. You only need to reply number in this case. 


"""
instruction_prompt_reasoning_setting_1_step_by_step_zero_shot="""You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided a statement and you need to detect what attitude they hold to the value.
For example, the statement is "The people who don't work turn lazy" and the options are "disagree,agree,neither disagree or agree". And you need to read the story and choose one attitude from the options.
The options could also describe something happening around. For example, the statement is "How often does this happen in your neighborhood:Racist behaviors", the options are "Very often, not often, not at all often", you need to choose one based on the story.

Here is the scenario:
{story}

Here is the statement:
{statement}

Here are the options:
{options}

Now choose one option based on the story. Let's think step by step!

First extract the speech that related to the statement.
Then analyse the attitude of those people from the speech.
Finally output the answer.

Follow the format:
[Related speech]: speeches
[Analysis]: analysis of attitude
[Answer]:answer
"""

instruction_prompt_reasoning_setting_1_step_by_step_one_shot="""You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided a statement and you need to detect what attitude they hold to the value.
For example, the statement is "The people who don't work turn lazy" and the options are "disagree,agree,neither disagree or agree". And you need to read the story and choose one attitude from the options.
The options could also describe something happening around. For example, the statement is "How often does this happen in your neighborhood:Racist behaviors", the options are "Very often, not often, not at all often", you need to choose one based on the story.



Now choose one option based on the story. Let's think step by step!

First extract the speech that related to the statement.
Then analyse the attitude of those people from the speech.
Finally output the answer.

Follow the format:
[Related speech]: speeches
[Analysis]: analysis of attitude
[Answer]:answer

{demonstration}

Here is the scenario:
{story}

Here is the statement:
{statement}

Here are the options:
{options}
"""

demonstration_t1="""
Here is one demonstration:

Here is the scenario:\n
**Title: The Dinner Table Debate**\n\n**Setting:** A bustling restaurant, adorned with soft overhead lights and a rich ambiance mixed with laughter and clinking silverware. Booths filled with families enjoying meals, friends catching up, and couples celebrating milestones create a warm, vibrant atmosphere. \n\n**Characters:** \n- **Maria**, a successful marketing executive, early 30s, known for her ambitious nature.\n- **James**, Maria\u2019s husband, mid-30s, who is a freelance graphic designer.\n- **Elena**, Maria\u2019s childhood friend, late 20s, a stay-at-home mom who often feels torn about her choices.\n- **Carlos**, their mutual friend, early 40s, a small business owner with strong opinions about society.\n\n---\n\nAs the evening unfolds, the friends are seated in a cozy booth, enjoying a meal. Maria is animatedly discussing an upcoming project, her eyes shining with excitement.\n\n**Maria:** \u201cSo, I\u2019m finally leading this campaign for the new product launch! It\u2019s a big deal for me, and I couldn\u2019t be more thrilled!\u201d\n\n**James** (smiling, but slightly reserved): \u201cThat\u2019s awesome, Maria. You\u2019ve worked hard for this. Just remember to balance it with everything else.\u201d\n\n**Elena** (stirring her drink): \u201cThat sounds incredible, Maria! But, James, how do you feel about her taking the lead? Doesn\u2019t it overshadow your work sometimes?\u201d\n\n**James** (sighing): \u201cI mean, it can be tricky. I\u2019ve been freelancing for a while, and I guess\u2026 it\u2019s just hard. Traditionally, it\u2019s the men who get the spotlight. Sometimes I wonder if it\u2019s why I struggle to secure larger contracts.\u201d\n\n**Carlos** (leaning forward, nodding): \u201cI get where you\u2019re coming from. You know, with business, people generally expect men to take charge. It\u2019s just how it\u2019s been. But Maria, a headstrong woman like you, it\u2019s fascinating to see!\u201d\n\n**Maria** (smiling warmly, yet contemplative): \u201cInteresting perspective, Carlos. I see where you're coming from. Historically, men have been at the forefront in business, and some might say they have a natural knack for it. But I think it really depends on the individual, you know? Talent and drive aren't bound by gender. Besides, if we're always thinking one way, how can we expect to innovate and grow?\u201d\n\nCarlos chuckles, but Elena, feeling the tension between the friends, quickly changes the subject.\n\n**Elena:** \u201cSpeaking of competition, did any of you vote in the recent elections? I heard there were some sketchy things happening.\u201d\n\n**Maria:** \u201cI did! But honestly, I wasn't surprised. You know, it's like every election season you hear about people getting swayed by cash or favors. It almost feels expected these days..\u201d\n\n**Carlos** (grinning): \u201cVery true, and it\u2019s disheartening! At least in this country, we still get to see different candidates fight for the spotlight\u2014unlike some countries where it's just a one-man show. That\u2019s something to appreciate, right??\u201d\n\n**James** (pensive): \u201cIt's puzzling. You\u2019d think with all the candidates running, things could change for the better. But money drives everything. You wouldn\u2019t catch me running for office.\u201d\n\n**Elena** (playfully): \u201cWhat, scared of all the bribery? Or the fact that a woman might outshine you?\u201d\n\n**James** (laughing): \u201cNah! Just realistic! And let\u2019s be honest, Maria would probably run circles around me in debates. I\u2019d need her back for every question!\u201d\n\n**Carlos**: \u201cWhat\u2019s the point if you\u2019re just going to have a woman at the helm? That\u2019s like giving the best chair in the office to the less suitable candidate just because she\u2019s a friend.\u201d\n\nThe conversation shifts, the group engaging in thoughtful disagreements while picking at their meals. Maria raises her glass, spotlighting the fun in the discussions.\n\n**Maria:** \u201cTo us, then! Challenging norms and pushing boundaries\u2014who needs to fit labels, right?\u201d\n\n**Elena** (raising her glass): \u201cAbsolutely! It\u2019s all about making our parents proud while we\u2019re at it. Mine always said to aim higher than them, although they would get worried when I talked about my goals.\u201d\n\n**James**: \u201cCheers to that! Sort of the dream\u2014becoming more than what they expected and working hard for our own futures!\u201d \n\nAs they clink glasses, the atmosphere lightens, their laughter mixing with the restaurant's hum. The topics may run deep, but the friendships are what hold them together amid the contrasts of societal expectations and personal aspirations. \n\nThe dinner continues, shaped by camaraderie, reflections on gender roles, and the ever-present challenges of navigating a complex world, all wrapped in the joys and tensions that come with passionate friendships.",
  
Here is the statement:
One of my main goals in life has been to make my parents proud

Here are the options:
agree,disagree

Here is the reasoning process and final answer:
[Related speech]: \u201cAbsolutely! It\u2019s all about making our parents proud while we\u2019re at it. Mine always said to aim higher than them, although they would get worried when I talked about my goals.\u201d\n\n[Analysis]: Elena\u2019s statement clearly shows that making her parents proud is an important value in her life. It illustrates a strong cultural emphasis on filial respect and living up to parental expectations. Given this positive reinforcement and pride in achieving her goals to honor her parents, the attitude reflected in the conversation aligns with the idea that making parents proud is a key personal goal.\n\n[Answer]: agree",
"""
# instruction_prompt_text_setting2_decompose = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
# You will be provided 15 options and you need to select {number} correct answers from the options. (Only {number}  options are correct).\n 
# You need to choose the whole option, for example:\n
# Being a housewife is just as fulfilling as working for pay-- agree\n
# Make sure you include '--' in the answer.\n
# Here is the scenario:\n
# {story}

# Here are the options:
# {options}

# You need to firstly detect what topics the story mentioned according to the options. 
# Then for each topic, decide what attitude stories reflected. You should output final answer in the end only.

# Follow the format:
# [Topic]: 
# topic1
# topic2
# .....

# [Reasoning]: 
# topic1: reasoning
# topic2: reasoning

# [Final answer]: 
# [text] -- [text] \n
# [text] -- [text]\n
# [text] -- [text]\n
# .....

# """

instruction_prompt_text_setting2_decompose_one_shot = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided 15 options and you need to select {number} correct answers from the options. (Only {number}  options are correct).\n 
You need to choose the whole option, for example:\n
Being a housewife is just as fulfilling as working for pay--agree\n
Make sure you include '--' in the answer.\n



To think step by step:
1. You need to firstly detect what topics the story mentioned according to the options. You need to list the speeched related to the topic. 
2. Then for each topic, detect what values might be related to the topic. Sometimes, you might find multiiple options might be correct, for uncertain options, you should compare them. 
3. Based on the previous detection, analyse what values are aligned with the story, you should always priortize those values that are strongly related. 
4. In the end, output the final answers only. Only choose the required number of values.


Follow the format:
[Topic]: 
topic1: speeches related to the topic
topic2: speeches related to the topic
.....

[Value detection]: 
topic1: what values are related to the topic
topic2: what values are related to the topic

[Reasoning]:
Reasoning

[Final answer]: 
[text] -- [text] \n
[text] -- [text]\n
[text] -- [text]\n
.....

{demonstrations}

Here is the scenario:\n
{story}

Here are the options:
{options}
"""



instruction_prompt_text_setting2_decompose_zero_shot = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided 15 options and you need to select {number} correct answers from the options. (Only {number}  options are correct).\n 
You need to choose the whole option, for example:\n
Being a housewife is just as fulfilling as working for pay--agree\n
Make sure you include '--' in the answer.\n

Here is the scenario:\n
{story}

Here are the options:
{options}

To think step by step:
1. You need to firstly detect what topics the story mentioned according to the options. You need to list the speeched related to the topic. 
2. Then for each topic, detect what values might be related to the topic. Sometimes, you might find multiiple options might be correct, for uncertain options, you should compare them. 
3. Based on the previous detection, analyse what values are aligned with the story, you should always priortize those values that are strongly related. 
4. In the end, output the final answers only. Only choose the required number of values.

Follow the format:
[Topic]: 
topic1: speeches related to the topic
topic2: speeches related to the topic
.....

[Value detection]: 
topic1: what values are related to the topic
topic2: what values are related to the topic

[Reasoning]:
Reasoning

[Final answer]: 
[text] -- [text] \n
[text] -- [text]\n
[text] -- [text]\n
.....

"""

demonstration = """Here is one demonstration:

Here is the scenario:\n
**Title: The Dinner Table Debate**\n\n**Setting:** A bustling restaurant, adorned with soft overhead lights and a rich ambiance mixed with laughter and clinking silverware. Booths filled with families enjoying meals, friends catching up, and couples celebrating milestones create a warm, vibrant atmosphere. \n\n**Characters:** \n- **Maria**, a successful marketing executive, early 30s, known for her ambitious nature.\n- **James**, Maria\u2019s husband, mid-30s, who is a freelance graphic designer.\n- **Elena**, Maria\u2019s childhood friend, late 20s, a stay-at-home mom who often feels torn about her choices.\n- **Carlos**, their mutual friend, early 40s, a small business owner with strong opinions about society.\n\n---\n\nAs the evening unfolds, the friends are seated in a cozy booth, enjoying a meal. Maria is animatedly discussing an upcoming project, her eyes shining with excitement.\n\n**Maria:** \u201cSo, I\u2019m finally leading this campaign for the new product launch! It\u2019s a big deal for me, and I couldn\u2019t be more thrilled!\u201d\n\n**James** (smiling, but slightly reserved): \u201cThat\u2019s awesome, Maria. You\u2019ve worked hard for this. Just remember to balance it with everything else.\u201d\n\n**Elena** (stirring her drink): \u201cThat sounds incredible, Maria! But, James, how do you feel about her taking the lead? Doesn\u2019t it overshadow your work sometimes?\u201d\n\n**James** (sighing): \u201cI mean, it can be tricky. I\u2019ve been freelancing for a while, and I guess\u2026 it\u2019s just hard. Traditionally, it\u2019s the men who get the spotlight. Sometimes I wonder if it\u2019s why I struggle to secure larger contracts.\u201d\n\n**Carlos** (leaning forward, nodding): \u201cI get where you\u2019re coming from. You know, with business, people generally expect men to take charge. It\u2019s just how it\u2019s been. But Maria, a headstrong woman like you, it\u2019s fascinating to see!\u201d\n\n**Maria** (smiling warmly, yet contemplative): \u201cInteresting perspective, Carlos. I see where you're coming from. Historically, men have been at the forefront in business, and some might say they have a natural knack for it. But I think it really depends on the individual, you know? Talent and drive aren't bound by gender. Besides, if we're always thinking one way, how can we expect to innovate and grow?\u201d\n\nCarlos chuckles, but Elena, feeling the tension between the friends, quickly changes the subject.\n\n**Elena:** \u201cSpeaking of competition, did any of you vote in the recent elections? I heard there were some sketchy things happening.\u201d\n\n**Maria:** \u201cI did! But honestly, I wasn't surprised. You know, it's like every election season you hear about people getting swayed by cash or favors. It almost feels expected these days..\u201d\n\n**Carlos** (grinning): \u201cVery true, and it\u2019s disheartening! At least in this country, we still get to see different candidates fight for the spotlight\u2014unlike some countries where it's just a one-man show. That\u2019s something to appreciate, right??\u201d\n\n**James** (pensive): \u201cIt's puzzling. You\u2019d think with all the candidates running, things could change for the better. But money drives everything. You wouldn\u2019t catch me running for office.\u201d\n\n**Elena** (playfully): \u201cWhat, scared of all the bribery? Or the fact that a woman might outshine you?\u201d\n\n**James** (laughing): \u201cNah! Just realistic! And let\u2019s be honest, Maria would probably run circles around me in debates. I\u2019d need her back for every question!\u201d\n\n**Carlos**: \u201cWhat\u2019s the point if you\u2019re just going to have a woman at the helm? That\u2019s like giving the best chair in the office to the less suitable candidate just because she\u2019s a friend.\u201d\n\nThe conversation shifts, the group engaging in thoughtful disagreements while picking at their meals. Maria raises her glass, spotlighting the fun in the discussions.\n\n**Maria:** \u201cTo us, then! Challenging norms and pushing boundaries\u2014who needs to fit labels, right?\u201d\n\n**Elena** (raising her glass): \u201cAbsolutely! It\u2019s all about making our parents proud while we\u2019re at it. Mine always said to aim higher than them, although they would get worried when I talked about my goals.\u201d\n\n**James**: \u201cCheers to that! Sort of the dream\u2014becoming more than what they expected and working hard for our own futures!\u201d \n\nAs they clink glasses, the atmosphere lightens, their laughter mixing with the restaurant's hum. The topics may run deep, but the friendships are what hold them together amid the contrasts of societal expectations and personal aspirations. \n\nThe dinner continues, shaped by camaraderie, reflections on gender roles, and the ever-present challenges of navigating a complex world, all wrapped in the joys and tensions that come with passionate friendships.",

Here are the options:\n\nHere are 15 options:\nIn your view, how often do the following things occur in this country\u2019s elections: Journalists provide fair coverage of elections?--Very often\nIn your view, how often do the following things occur in this country\u2019s elections: TV news favors the governing party?--Not often\nWhen jobs are scarce, men should have more right to a job than women--Neither agree nor disagree\nIt is a duty towards society to have children--Disagree\nIn your view, how often do the following things occur in this country\u2019s elections: Voters are bribed?--Very often\nIn terms of the effects of immigration on the development of your country, do you agree with Offers people from poor countries a better living?--Disagree\nOn the whole, men make better business executives than women do--agree\nBeing a housewife is just as fulfilling as working for pay--agree\nHow frequently do the following things occur in your neighborhood: Street violence and fights?--Not at all frequently\nIn your view, how often do the following things occur in this country\u2019s elections: Opposition candidates are prevented from running?--Not at all often\nWork is a duty towards society--agree\nIn your view, how often do the following things occur in this country\u2019s elections: Voters are offered a genuine choice in the elections?--Not often\nHow frequently do the following things occur in your neighborhood: Drug sale in streets?--Not at all frequently\nOne of my main goals in life has been to make my parents proud--agree\nIf a woman earns more money than her husband, it's almost certain to cause problems--agree\n\n
Here is the reasoning process and final answer:
[Topic]: \ntopic1: Political corruption in elections \u2013 speeches related: Maria mentioning elections swayed by cash or favors; Carlos remarking on bribery and comparing it to one-man shows in other countries  \ntopic2: Gender roles in business and leadership \u2013 speeches related: James lamenting that traditionally men receive the spotlight; Carlos stating that business expects men to take charge; Maria countering that individual talent matters regardless of gender  \ntopic3: Parental aspirations \u2013 speeches related: Elena remarking about making her parents proud and aiming higher  \ntopic4: Duty of work towards society \u2013 speeches related: James\u2019 toast celebrating hard work and building one\u2019s future  \ntopic5: The value of domestic roles \u2013 speeches related: Elena\u2019s underlying conflict as a stay-at-home mom, highlighting questions about fulfillment in traditional domestic roles  \n\n[Value detection]: \ntopic1: Reflects concerns about corruption and bribery in elections  \ntopic2: Reflects traditional gender biases regarding leadership and business competence  \ntopic3: Reflects the cultural value of making one\u2019s parents proud  \ntopic4: Reflects the belief that contributing through work is a societal duty  \ntopic5: Reflects the notion that domestic work (being a housewife) is equally fulfilling as working for pay  \n\n[Reasoning]:  \nThe conversation touches on the problematic prevalence of bribery in elections, making the option about voters being bribed (\u201cVoters are bribed?--Very often\u201d) a good match. The discussion about leadership roles\u2014where Carlos asserts that business generally expects men to lead\u2014aligns with the option \u201cOn the whole, men make better business executives than women do--agree.\u201d Elena\u2019s subtle emphasis on parental pride (\u201caim higher than them\u201d and making her parents proud) supports \u201cOne of my main goals in life has been to make my parents proud--agree.\u201d Additionally, the discourse celebrating hard work and personal achievements aligns with \u201cWork is a duty towards society--agree.\u201d Finally, Elena\u2019s internal struggle as a stay-at-home mom points to the value that domestic roles are respected and fulfilling, matching \u201cBeing a housewife is just as fulfilling as working for pay--agree.\u201d\n\n[Final answer]:  \nIn your view, how often do the following things occur in this country\u2019s elections: Voters are bribed?--Very often  \nOn the whole, men make better business executives than women do--agree  \nOne of my main goals in life has been to make my parents proud--agree  \nWork is a duty towards society--agree  \nBeing a housewife is just as fulfilling as working for pay--agree"
"""

instruction_prompt_text_setting2_reasoning ="""You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided 15 options and you need to select {number} correct answers from the options. (Only {number}  options are correct).\n 
You need to choose the whole option, for example:\n
Being a housewife is just as fulfilling as working for pay-- agree\n
Make sure you include '--' in the answer.\n
Here is the scenario:\n
{story}

Here are the options:\n
{options}

Now choose {number}  answers from the options provided. Do not rephrase the options, just use the original word.\n
You should include reasoning for each option you choose. You can explain why you choose this option, what evidence from context help you to decide. Reasoning for each value should be at most 3 sentences. \n
You should only return {number} answers in the end, no extra sentences should be included in the final answer.\n
You can output reasoning first and then output the final answers.

The choice should include '--' and output exact value /

Follow the format:

[Reasoning]: 
[value]:[reasoning]

[Final answer]: 
[value]\n
[value]\n
"""
format_prompt_text = """\nNow choose {number}  answers from the options provided. Do not rephrase the options, just use the original word.\n
Your output should follow this format and reasoning is not necessary. Do not include any extra sentences except for the answers:\n
[text] -- [text] \n
[text] -- [text]\n
[text] -- [text]\n
[text] -- [text]\n
[text] -- [text]\n
"""
format_prompt_number_only = """\nNow choose {number} answers from the options provided. Only reply numbers. The numbers should be separated by ','.
"""
format_prompt_with_reasoning = """\nNow choose {number}  answers from the options provided. Do not rephrase the options, just use the original word.\n
You should include reasoning for each option you choose. You can explain why you choose this option, what evidence from context help you to decide. Reasoning for each value should be at most 3 sentences. \n
You should only return {number} answers in the end, no extra sentences should be included in the final answer.\n
You can output reasoning first and then output the final answers.

The choice should include '--' and output exact value /

Follow the format:

[Reasoning]: 
[value]:[reasoning]

[Final answer]: 
[value]\n
[value]\n
......
Here is your output, make sure you output final answer:
"""


instruction_prompt_text_setting_1 = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided a statement and you need to detect what attitude they hold to the value.
For example, the statement is "The people who don't work turn lazy" and the options are "disagree,agree,neither disagree or agree". And you need to read the story and choose one attitude from the options.
The options could also describe something happening around. For example, the statement is "How often does this happen in your neighborhood:Racist behaviors", the options are "Very often, not often, not at all often", you need to choose one based on the story.

Here is the scenario:
{story}

Here is the statement:
{statement}

Here are the options:
{options}

Now choose one option based on the story. Only output the option.
"""
instruction_prompt_text_setting_1_multiple = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected of the character from the conversation.\n
You will be provided a statement and a character name and you need to detect what attitude the character hold to the value.
For example, the statement is "The people who don't work turn lazy" and the options are "disagree,agree,neither disagree or agree". And you need to read the story and choose one attitude from the options.
The options could also describe something happening around. For example, the statement is "How often does this happen in your neighborhood:Racist behaviors", the options are "Very often, not often, not at all often", you need to choose one based on the story.

Here is the scenario:
{story}

Here is the statement:
{statement}

Here are the options:
{options}

Here is the character name:
{name}

Now choose one option based on the story and {name}'s speech. Only output the option.
"""

instruction_prompt_reasoning_setting_1 = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected from the conversation.\n
You will be provided a statement and you need to detect what attitude they hold to the value.
For example, the statement is "The people who don't work turn lazy" and the options are "disagree,agree,neither disagree or agree". And you need to read the story and choose one attitude from the options.
The options could also describe something happening around. For example, the statement is "How often does this happen in your neighborhood:Racist behaviors", the options are "Very often, not often, not at all often", you need to choose one based on the story.

Here is the scenario:
{story}

Here is the statement:
{statement}

Here are the options:
{options}

Now choose one option based on the story. Provide reasoning first, then answer.
Follow the format:
[Reasoning]: reasoning
[Answer]:answer
"""


instruction_prompt_reasoning_setting_1_multiple = """You will be given a scenario including background, conversation and actions in a location. You task is to detect the culture values reflected of the character from the conversation.\n
You will be provided a statement and a character name and you need to detect what attitude the character hold to the value.
For example, the statement is "The people who don't work turn lazy" and the options are "disagree,agree,neither disagree or agree". And you need to read the story and choose one attitude from the options.
The options could also describe something happening around. For example, the statement is "How often does this happen in your neighborhood:Racist behaviors", the options are "Very often, not often, not at all often", you need to choose one based on the story.

Here is the scenario:
{story}

Here is the statement:
{statement}

Here are the options:
{options}

Here is the character name:
{name}

Now choose one option based on the story. Provide reasoning first, then answer.
Follow the format:
[Reasoning]: reasoning
[Answer]:answer
"""

multi_step_prompt_p1 = """
    You will be provided with a story. Your goal is to summarize the main themes in the story. Please provide 4-5 sentences to summarize the ideas.
    You should be specifically looking for: {topic} themes. Please pay attention to the character's responses and attitudes towards {topic}. 
    Here is the story to summarize: {story}.
    Please return the ouput as a valid JSON object with topic as key:

"""

# multi_step_prompt_p2 = """
#     You will be provided with a story. Your goal is to identify the most prevalent {topic} values in the story.
#     For example, one religious value could be: I strongly believe in God and the afterlife. 
#     The value should be a complete sentence, it should not be a phrase like work-life balance.
#     The value should hold a attitude or it reflects social phenomena, it should not be a overview of topic. 
#     For example, one social value could be: I think work is a duty towards the society.
#     And one political value could be: I think voters are bribed in our election system.
#     Please identify the values in this story: {story} by paying attention to how the characters in the story discuss {topic}.
#     You need to generate 10 values in total, make sure values are specific and detailed. Only focus on one topic in one value. Do not mention several themes in one value.
#     Here is the story: {story} 
#     Here is a story summary with some key ideas: {summary}. 
#     You could output reasoning before you output final answer. But in the end, your output should follow the JSON format:
#     [Final answer]:
#     Please return the ouput as a valid JSON object with topic as key and for each key, if you do not detect any values, just output empty list, otherwise, output a list of values. Make sure in total 10 values for all categories.  
# """

multi_step_prompt_p2 = """
    You will be provided with a story. Your goal is to identify the most prevalent {topic} values in the story.
    For example, one religious value could be: I strongly believe in God and the afterlife. 
    The value should be a complete sentence, it should not be a phrase like work-life balance.
    The value should hold a attitude or it reflects social phenomena, it should not be a overview of topic. 
    For example, one social value could be: I think work is a duty towards the society.
    And one political value could be: I think voters are bribed in our election system.
    Please identify the values in this story: {story} by paying attention to how the characters in the story discuss {topic}.
    You need to generate 10 values in total, make sure values are specific and detailed. Only focus on one topic in one value. Do not mention several themes in one value.
    Here is the story: {story} 
    Here is a story summary with some key ideas: {summary}. 
    You could output reasoning before you output final answer. But in the end, your output should follow the format:
    [Final answer]:
    value1\n
    value2\n
    .....
    """

value_prompt = """
    You will be provided with a story. Your goal is to identify the 5 most prevalent {topic} themes/values in the story.
    For example, one religious theme/value could be: I strongly believe in God and the afterlife. 
    Please identify the themes/values in this story: {story} by paying attention to how the characters in the story discuss {topic}.
    Please return the ouput as a valid JSON object with the following keys: theme1, theme2, theme3, theme4, theme5.
"""

rephrase_prompt = """
    Your job is to summarize/rephrase statements with '--term' tags such that it does not include any terms like '--Agree', '--Important', etc. 
    For example, for the value: 'How important is it for people with minority religions to practice their faith freely? --Not important', you should return 'It is not important for people with minority religions to practice their faith freely.'
    Now, please rephrase the following value: {value}.
    Please return the output as a valid JSON object with the following keys: value_rephrased.
"""

resolve_values = """
   You will be provided with a set of values and a set of contradictions (values that might not be correct). 
   Your job is to return a set of resolved values that incorporate contradictory value into the gold values.
   The value consists of two parts, a statement and an attitude, you job is to add contradictory attitude into the value set.
   For example, if the "One of my main goals in life has been to make my parents proud--agree" is contradictory, it means that someone's value is disagree with the statement.
   What you need to do is to incorporate One of my main goals in life has been to make my parents proud--disagree in the ground truth.
   You need to find the opposite term for the attitude and then attach them with the statement.
   Here is the values set: {values} and contradiction: {contradiction}.
   Please return the output as a valid JSON object with the following keys: resolved_values. 
"""

llm_judge = """
   You will be given two sets of texts: a set of predicted values and a ground truth set of values.
   Your task is to determine how many of the ground truth values are fully represented in the predicted values.
   A ground truth value is considered correct if all of its components are meaningfully discussed in the predicted value, even if there is no exact 1-to-1 match. It could be many-to-1 match i.e. many values to 1 ground truth value.
   If the ground truth value is fully presented, score 1, if it is partially presented, score 0.5, if it is not mentioned at all, score 0.
   Additionally, provide a brief justification for your score, explaining which values were correctly or incorrectly represented, in the justification, you should explicitly mention which predicted values are related to the ground truth value.
   Here are the predictions: {pred} and ground truth: {gt}
   In the reasoning, if the ground truth value is fully represented, you need to point out which predicted value is related to it.
   Return the results in this format:
   [Reasoning]:
   [Ground truth 1]: [reasoning]
   .....
   [Final answer]:
   [Ground truth 1]:1
   [Ground truth 2]:0.5
   ......
"""

llm_judge_topic_mentioned="""
You will be given two sets of texts: a set of predicted values and a ground truth set of values.
   Your task is to determine if there is overlapped topic between predicted values and ground truth values.
   For example, if the both values mention fair election, or sexual harrasement. 
   Here are the predictions: {pred} and ground truth: {gt}
   In the reasoning, if the ground truth value has overlapping with predicted value, you need to point out which predicted value is related to it.
   In the final answer, only output yes/no.
   Return the results in this format:
   [Reasoning]:
   [Ground truth 1]: [reasoning]
   .....
   [Final answer]:
   [Ground truth 1]:no
   [Ground truth 2]:yes
   ......
"""




