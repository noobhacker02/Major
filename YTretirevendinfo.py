# Chat with an intelligent assistant in your terminal
from openai import OpenAI
from googleapiclient.discovery import build

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Function to retrieve YouTube video links
def get_youtube_video_links(search_query, max_results=5):
    """
    This function retrieves YouTube video links using the YouTube Data API v3.

    Args:
        search_query: A string representing the search query.
        max_results: (Optional) The maximum number of video links to retrieve (default: 5).

    Returns:
        A list of YouTube video links (strings) or an empty list if no results are found.
    """

    # Replace with your own YouTube Data API v3 key
    DEVELOPER_KEY = "AIzaSyDfMbEz564iDRRn-P8ZrkRHBq3MOGCvE6s"

    youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)

    # Set search parameters
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",
        maxResults=max_results
    )

    # Execute the search request
    response = request.execute()

    # Extract video links from the response
    video_links = []
    if response.get("items", []):
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append(video_link)

    return video_links

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time and also tell them you can retrieve video's from youtube. Be concise."},
]

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
    
    print()
    
    user_input = input("What topic do you want to learn about? > ")
    
    history.append({"role": "user", "content": user_input})
    
    # Retrieve YouTube video links based on user input
    video_links = get_youtube_video_links(user_input, max_results=3)

    if video_links:
        print("Here are some YouTube video links:")
        for link in video_links:
            print(link)
    else:
        print("No results found for", user_input)
