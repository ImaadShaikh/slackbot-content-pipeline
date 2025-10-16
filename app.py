from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
from cleaner import reading_words , clean_words
from clustering import cluster
from content_builder import gen_clusters , get_content
from generating_content import generating_idea_via_clusters
from Report_Generator import pdf_generator
from slack_sdk import WebClient

import requests

load_dotenv()

app = App(
    token = os.getenv("SLACK_BOT_TOKEN"),
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")
)

@app.command('/keywords')

def handling_keywords(ack, respond , command):
    ack()
    inputs = command.get('text',"").strip()

    if inputs:
        raw_val = [word.strip() for word in inputs.split(",")]
        cleaned = clean_words(raw_val)
        
        respond(' Generating clusters')
        clusters = cluster(cleaned)

    

        respond('Fetching output')
        outlines = gen_clusters(clusters)

        respond('Generating post ideas')
        ideas = generating_idea_via_clusters(clusters)
        final_output = " Keywords"
        for name in clusters.keys():
            outline = outlines.get(name, "")
            idea = ideas.get(name, "no idea generated")
            final_output += f"\n\n{outline}\n\n Post Idea: {idea}\n" 


        respond('Generating pdf')

        pdf = pdf_generator(clusters , outlines , ideas)

        respond('Uploading to Slack')

        client = WebClient(token = os.environ['SLACK_BOT_TOKEN'])

        client.files_upload_v2(
            channel = command['channel_id'],
            file = pdf,
            name = "Report.pdf",
            title = "Report",
        )
        print("DEBUG - Channel ID:", command.get("channel_id"))

    
        respond(final_output)
       
    else:
        respond("please upload the file") 

@app.event('file_shared')

def handling_file(event, client, say):
    file_id = event["file_id"]
    info = client.files_info(file = file_id)['file']
    url = info['url_private_download']

    headers = {"authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"}
    reponse = requests.get(url, headers = headers)

    if reponse.status_code == 200:
        try:
            raw_csv_data =reading_words(reponse.content)
            cleaned = clean_words(raw_csv_data)
            clusters = cluster(cleaned)
            formated = formatcluster(clusters)

            say(
                f"processed{len(cleaned)} keywords:\n"
                f"here are a few: {' , '.join(cleaned[:10])}"
            )

        except Exception as e:
            say(f"error reading csv file: {e}")
    
    else:
        say('unable to download the file. Please check')

@app.command('/outline')

def handling_title(ack, respond, command):
    ack()
    keyword = command.get('text',"").strip()
    if not keyword:
        respond('Add:/add your keyword here')
        return
    outline = get_content(keyword)
    respond(outline)

def formatcluster(cluster):
    message = 'Keyword clusters:\n'
    for name, kws in cluster.items():
        joined = ', '.join(kws)
        message += f"\n {name}:{joined}"
    return message

if __name__ == "__main__":
    print("bot is running")
    app.start(port=3000)