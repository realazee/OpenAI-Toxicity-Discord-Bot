import bisect
import json
import numpy as np
import openai

async def checkToxicity(messagesToCheck):

    # Initialize OpenAI API key
    secretFile = open("hackathon week 1/OpenAI-Reddit-Toxicity-Calculator-main/clientsecret.json", "r")
    secrets = json.load(secretFile)
    openai.api_key = secrets['OPENAI_KEY']

    print(messagesToCheck)
    response = openai.Moderation.create(input=str(messagesToCheck))
    output = response["results"][0]
    print(output)
    hate = str(output["category_scores"]["hate"])
    hate_threatening = str(output["category_scores"]["hate/threatening"])
    self_harm = str(output["category_scores"]["self-harm"])
    sexual = str(output["category_scores"]["sexual"])
    sexual_minors = str(output["category_scores"]["sexual/minors"])
    violence = str(output["category_scores"]["violence"])
    violence_graphic = str(output["category_scores"]["violence/graphic"])

    #code to take results from openAI and round to 6 decimal places for ease of usability
    hate_formatted = float("{:.3f}".format(float(hate)))
    hate_threatening_formatted = float("{:.3f}".format(float(hate_threatening)))
    self_harm_formatted = float("{:.3f}".format(float(self_harm)))
    sexual_formatted = float("{:.3f}".format(float(sexual)))
    sexual_minors_formatted = float("{:.3f}".format(float(sexual_minors)))
    violence_formatted = float("{:.3f}".format(float(violence)))
    violence_graphic_formatted = float("{:.3f}".format(float(violence_graphic)))

    # Define a list and add data field into it
    openAI_data = []
    openAI_data.append(hate_formatted)
    openAI_data.append(hate_threatening_formatted)
    openAI_data.append(self_harm_formatted)
    openAI_data.append(sexual_formatted)
    openAI_data.append(sexual_minors_formatted)
    openAI_data.append(violence_formatted)
    openAI_data.append(violence_graphic_formatted)

    #print("Hate Pre Format", hate)
    #print("Hate Formatted", hate_formatted)
    #print("Sexual Pre Format", sexual)
    #print("Sexual Formatted", sexual_formatted)
    print(openAI_data)

    # # Define the intervals
    # #intervals = [1e-6, 1.995e-6, 3.981e-6, 7.943e-6, 1.585e-5, 3.162e-5, 6.310e-5, 1.259e-4, 2.512e-4, 5.012e-4, 1e-3, 1.995e-3, 3.981e-3, 7.943e-3, 1.585e-2, 3.162e-2, 6.310e-2, 1.259e-1, 2.512e-1, 5.012e-1]
    # intervals = np.linspace(0.01,1,20)
    # openAI_data_interval_score = []

    # # Use a for loop to loop through values in openAI_data and find which interval they fall under
    # for index, value in enumerate(openAI_data):
    #      # Find the index of the interval that the value belongs to
    #     intervalVal = bisect.bisect_left(intervals, value)
        
    #     # The 100 data range of gauge diagram is split apart into 20 regions
    #     openAI_data_interval_score.append(intervalVal * 5)

    # # hate = openAI_data_interval_score[0]
    # # hate_threatening = openAI_data_interval_score[1]
    # # self_harm = openAI_data_interval_score[2]
    # # sexual = openAI_data_interval_score[3]
    # # sexual_minors = openAI_data_interval_score[4]
    # # violence = openAI_data_interval_score[5]
    # # violence_graphic = openAI_data_interval_score[6]

    categories = ["Hate", "Hate Threatening", "Self Harm", "Sexual", "Sexual Minors", "Violence", "Violence Graphic"]

    max_value = 0
    max_category = ""

    for i, score in enumerate(openAI_data):
        print(score)
        if score > max_value:
            max_value = score
            max_category = categories[i]
        
        
    return min(max_value * 120, 100), max_category

        

    #plan: return the max value of the 7 categories. This will be the overall toxicity score