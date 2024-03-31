# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful and summerize any appened history.."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise and always start you conversation and summerize any appened history."},
    
]

string1 = "API Reference bookmark_borderThe YouTube Data API lets you incorporate functions normally executed on the YouTube website into your own website or application. The lists below identify the different types of resources that you can retrieve using the API. The API also supports methods to insert, update, or delete many of these resources.This reference guide explains how to use the API to perform all of these operations. The guide is organized by resource type. A resource represents a type of item that comprises part of the YouTube experience, such as a video, a playlist, or a subscription. For each resource type, the guide lists one or more data representations, and resources are represented as JSON objects. The guide also lists one or more supported methods (LIST, POST, DELETE, etc.) for each resource type and explains how to use those methods in your application.Calling the API The following requirements apply to YouTube Data API requests:Every request must either specify an API key (with the key parameter) or provide an OAuth 2.0 token. Your API key is available in the Developer Console's API Access pane for your project.You must send an authorization token for every insert, update, and delete request. You must also send an authorization token for any request that retrieves the authenticated user's private data.In addition, some API methods for retrieving resources may support parameters that require authorization or may contain additional metadata when requests are authorized. For example, a request to retrieve a user's uploaded videos may also contain private videos if the request is authorized by that specific user.The API supports the OAuth 2.0 authentication protocol. You can provide an OAuth 2.0 token in either of the following ways:Use the access_token query parameter like this: ?access_token=oauth2-token Use the HTTP Authorization header like this: Authorization: Bearer oauth2-token Complete instructions for implementing OAuth 2.0 authentication in your application can be found in the authentication guide.Resource types Activities An activity resource contains information about an action that a particular channel, or user, has taken on YouTube. The actions reported in activity feeds include rating a video, sharing a video, marking a video as a favorite, uploading a video, and so forth. Each activity resource identifies the type of action, the channel associated with the action, and the resource(s) associated with the action, such as the video that was rated or uploaded.For more information about this resource, see its resource representation and list of properties."
history.append({"role": "user", "content": string1})

while True:
    completion = client.chat.completions.create(
        model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
   
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

   
    history.append(new_message)
    
    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})