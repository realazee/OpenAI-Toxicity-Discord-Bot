import bisect
import json
import numpy as np
import openai

async def checkToxicity(messagesToCheck):

    # Initialize OpenAI API key
    secretFile = open("clientsecret.json", "r")
    secrets = json.load(secretFile)
    openai.api_key = secrets['OPENAI_KEY']

    #print(messagesToCheck)
    response = openai.Moderation.create(input=str(messagesToCheck))
    output = response["results"][0]
    #print(output)
    harassment = str(output["category_scores"]["harassment"])
    harassment_threatening = str(output["category_scores"]["harassment/threatening"])
    hate = str(output["category_scores"]["hate"])
    hate_threatening = str(output["category_scores"]["hate/threatening"])
    self_harm = str(output["category_scores"]["self-harm"])
    self_harm_instructions = str(output["category_scores"]["self-harm/instructions"])
    self_harm_intent = str(output["category_scores"]["self-harm/intent"])
    sexual = str(output["category_scores"]["sexual"])
    sexual_minors = str(output["category_scores"]["sexual/minors"])
    violence = str(output["category_scores"]["violence"])
    violence_graphic = str(output["category_scores"]["violence/graphic"])
    flagged = str(output["flagged"])
    #print("flagged is", flagged)

    #code to take results from openAI and round to 6 decimal places for ease of usability
    harassment_formatted = float("{:.3f}".format(float(harassment)))
    harassment_threatening_formatted = float("{:.3f}".format(float(harassment_threatening)))
    hate_formatted = float("{:.3f}".format(float(hate)))
    hate_threatening_formatted = float("{:.3f}".format(float(hate_threatening)))
    self_harm_formatted = float("{:.3f}".format(float(self_harm)))
    self_harm_instructions_formatted = float("{:.3f}".format(float(self_harm_instructions)))
    self_harm_intent_formatted = float("{:.3f}".format(float(self_harm_intent)))
    sexual_formatted = float("{:.3f}".format(float(sexual)))
    sexual_minors_formatted = float("{:.3f}".format(float(sexual_minors)))
    violence_formatted = float("{:.3f}".format(float(violence)))
    violence_graphic_formatted = float("{:.3f}".format(float(violence_graphic)))
    flagged_formatted = (flagged == "True")

    # Define a list and add data field into it
    openAI_data = []
    openAI_data.append(harassment_formatted)
    openAI_data.append(harassment_threatening_formatted)
    openAI_data.append(hate_formatted)
    openAI_data.append(hate_threatening_formatted)
    openAI_data.append(self_harm_formatted)
    openAI_data.append(self_harm_instructions_formatted)
    openAI_data.append(self_harm_intent_formatted)
    openAI_data.append(sexual_formatted)
    openAI_data.append(sexual_minors_formatted)
    openAI_data.append(violence_formatted)
    openAI_data.append(violence_graphic_formatted)

    print(openAI_data)


    categories = ["Harassment", "Harassment Threatening","Hate", "Hate Threatening", "Self Harm", "Self Harm Instructions", "Self Harm Intent" "Sexual", "Sexual Minors", "Violence", "Violence Graphic"]

    max_value = 0
    max_category = ""

    for i, score in enumerate(openAI_data):
        #print(score)
        if score > max_value:
            max_value = score
            max_category = categories[i]
        
    #print (max_value, max_category, flagged_formatted)
        
    return round(min(max_value * 120, 100), 2), max_category, flagged_formatted

        

    #plan: return the max value of the 7 categories. This will be the overall toxicity score