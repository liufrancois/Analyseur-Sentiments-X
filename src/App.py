from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, M2M100ForConditionalGeneration, M2M100Tokenizer
from langdetect import detect
from types import SimpleNamespace
import tweepy, re


BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANgt0AEAAAAANYkORCuhZu5gBYNvKFo6hD0gd7E%3Db3oE4KEesPlGnDKbKtuDqpQK1iSF6B5RzgRXCh9A1qalmchvkB"
client = tweepy.Client(bearer_token=BEARER_TOKEN)


model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
translator_model = M2M100ForConditionalGeneration.from_pretrained(model_name)

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def translate_to_english(text):
    lang = detect(text)
    tokenizer.src_lang = lang
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = translator_model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("en"))
    return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

def analyze_sentiment(text):
    translated = translate_to_english(text)
    print(text + "  |||  " + translated)
    result = sentiment_pipeline(translated)[0]
    print(result)
    return result['label'].lower()


app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    hashtag = data.get("hashtag", "")

    try:
        response = client.search_recent_tweets(query=hashtag, max_results=10)
        tweets = response.data or []
        #variable test
        """
        tweets = [ 
            SimpleNamespace(text="RT @TheTransFat: The floor isnt Lava, but The Sky is void?!?!\nWere doing some #minecraft #allthemods9 today since Ark update is apparently…"),
            SimpleNamespace(text="RT @smallpopo_2332: Apple \n#Minecraft \n#minecraft建築コミュ https://t.co/61eh09ZXY4"),
            SimpleNamespace(text="RT @silentwisperer_: Me and the boys about to start some air raids in #minecraft https://t.co/iqaTce2sXd"),
            SimpleNamespace(text="RT @MYCRFT_: @Minecraft 🎶 I mine stuff to craft with, I craft stuff to mine with...\n\nLet's.... play Minecraft 🎶\n\n@Minecraft #Minecraft #Min…"),
            SimpleNamespace(text="RT @zozozrob1: Absolute peak\n#Minecraft https://t.co/HMETyJSe3O"),
            SimpleNamespace(text="RT @AidanVEnki1: This is single handedly the coolest change to the game ever, I love the leash changes SOOO MUCHHHHH!!!\n#Minecraft 💙🛶\nhttps…"),
            SimpleNamespace(text="RT @mcmovieupdates: A Minecraft Movie Woodland Mansion Throwdown Pack 👀⛏️\n\n#Minecraft #MinecraftMovie https://t.co/VR1ErUeGLF"),
            SimpleNamespace(text="A totally normal Minecraft cave...\n\nRight..?\n\n#ANostalgicMinecraftHangout #ANostalgicHangout #Minecraft https://t.co/oAZcOe2dP1"),
            SimpleNamespace(text="RT @RobinsBlade: @AlexicoReborn No sabía si algún dia vería a mi compa Alexico dibujando a Mystique, suave.\n#Minecraft #Mystique #XMen http…"),
            SimpleNamespace(text="RT @mcmovieupdates: A Minecraft Movie Explosive Minecart Escape Pack! ⛏️👀\n\n#Minecraft #MinecraftMovie https://t.co/p4bWO8bQxs"),
        ]
        """

        if not tweets:
            return jsonify({"tweets": [{"text": "Aucun tweet trouvé.", "sentiment": "neutre"}]})

        resultats = []

        for tweet in tweets[:10]:
            original_text = tweet.text

            mentions = re.findall(r"@(\w+)", original_text)
            hashtags = re.findall(r"#(\w+)", original_text)
            cleaned_text = re.sub(r"(?:@|#)\w+|http\S+", "", original_text).strip()

            sentiment = analyze_sentiment(cleaned_text)

            resultats.append({
                "text": cleaned_text,
                "original": original_text,
                "sentiment": sentiment,
                "mentions": mentions,
                "hashtags": hashtags
            })


        return jsonify({"tweets": resultats})
    except tweepy.TweepyException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
