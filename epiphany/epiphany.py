from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from cleaner import remove_chat_metadata

app = Flask("epiphany")

# initialize the chatbot
chatbot = ChatBot("epiphany")

# train the chatbot with cleaned messages
CORPUS_FILE = "chat.txt"
remove_chat_metadata = remove_chat_metadata(CORPUS_FILE)
trainer = ListTrainer(chatbot)
trainer.train(remove_chat_metadata)

# define sample responses as well
sample_responses = {
    "greetings": ["hey it's epiphany! how are you?", "hey! how are you?", "hello :) how are you doing today?", "hii how is it going", "hey hey how are you today?"],
    "empathy": ["i'm so sorry to hear that. i know situations like this can be tough. i'm here to listen for however long you'd like.",
                "i'm sorry. that sounds tough. i'm here to listen.",
                "i'm sorry to hear that. please talk more about it if you'd like. i'm always here for you. feel free to tell me what's up/",
                "i just want you to know that this is normal and you are going to get through this."],
    "anxiety": ["it's normal to be anxious about the world around us. but, i want you to know that you're not alone. take a second to take a deep breath and take your mind off of this. i love reading a book or listening to music when i'm in this position",
                "anxiety can be overwhelming but i want you to know that you are not alone. many people face anxiety on the daily and you will get through this.",
                "i understand. anxiety can be hard to deal with. please make sure you're taking care of yourself and taking deep breaths. you will get through this"],
    "stress": ["i know it's difficult. but, it's important to relax. when i'm stressed i like to listen to taylor swift. i would recommend listening to your favourite artist",
               "i'm sorry. i know stress can be overwhelming at times. but, remember that it's normal and you will get through this.",
               "yeah that's totally understandable. when i'm stressed i like going for a walk or getting some fresh air. it helps take my mind off of whatever i'm stressed about!"],
    "affirmations": ["you are loved and valued",
                     "you are capable and strong",
                     "you are worthy of happiness",
                     "you are deserving of respect and kindness",
                     "you are enough, just as you are",
                     "you are making progress no matter how small"],
    "sad": ["sounds cliche but the sad moments in life are ones that make happy ones look happy.",
            "feeling sad can be tough. please make sure you're taking time to yourself to process your emotions",
            "remember that it's okay and normal to feel sad. you got this and will get through it. i believe in you"],
    "goodbye": ["bye! please reach out when you're upset again.",
                "hope you feel better. bye!", "have a great day or night, bye!",
                "bye bye! talk to you soon."]
}

# application
@app.route('/sms', methods=['POST', 'GET'])
def sms():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'hey' in incoming_msg or 'hi' in incoming_msg or 'hello' in incoming_msg:
        msg.body(random.choice(sample_responses["greetings"]))
        responded = True

    if 'bad' in incoming_msg or 'upsetting' in incoming_msg or 'upset' in incoming_msg or 'horrible' in incoming_msg:
        msg.body(random.choice(sample_responses["empathy"]))
        responded = True

    if 'anxious' in incoming_msg or 'anxiety' in incoming_msg:
        msg.body(random.choice(sample_responses["anxiety"]))
        responded = True

    if 'stressed' in incoming_msg or 'stress' in incoming_msg or 'stressing' in incoming_msg:
        msg.body(random.choice(sample_responses["stress"]))
        responded = True

    if 'affirmation' in incoming_msg or 'need some positivity' in incoming_msg:
        msg.body(random.choice(sample_responses["affirmations"]))
        responded = True

    if 'bye' in incoming_msg or 'goodbye' in incoming_msg:
        msg.body(random.choice(sample_responses["goodbye"]))
        responded = True

    if not responded:
        response = chatbot.get_response(incoming_msg)
        msg.body(str(response))

    return str(resp)

if __name__ == '__main__':
    app.run()