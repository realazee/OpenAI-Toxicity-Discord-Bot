# OpenAI-Toxicity-Discord-Bot
### Overview:
A Discord bot that checks the toxicity of current chat, and outputs a weighted toxicity score out of 100. Powered by OpenAI
### Features:
#### Commands:
/check_toxicity: checks the toxicity of the current chat, specifying the amount of messages to check for context.<br />
/check_user_toxicity: checks the toxicity of the mentioned user in the current chat, specifying the amount of mesages sent by that user to check for context. Due to limits on Discord's API, it can only scan the past 1000 messages sent in the chat by all members. 

### Instructions to Host
Create a file clientsecret.json in the repository root, and fill in variables DISCORD_KEY and OPENAI_KEY with the respective client secrets/private keys from the Discord and OpenAI developer portals.<br />
This bot will require the view message history, send messages, use application commands and embed links permissions to function at a minimum, and a role that gives the bot access to the corresponding channel (unless it has permissions granted that allow all channels to be viewed. The Discord permissions integer 563226979064896 is used for development work. <br />
For more information on creating a Discord application, refer to https://discord.com/developers/docs/quick-start/getting-started

