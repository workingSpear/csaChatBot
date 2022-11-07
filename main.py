import transformers
from transformers import Conversation,pipeline,AutoTokenizer, AutoModelForCausalLM
import random

transformers.logging.set_verbosity_error()

class Chatbot:

    def __init__(self):
        self.model = pipeline("conversational", model="microsoft/DialoGPT-medium")
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.memory = Conversation()
        self.tv_shows = ["breaking bad","arcane","better call saul","mr robot","family guy","the simpsons","spongebob","friends","game of thrones","stranger things","tv","television","show","anime"]
        self.poss = ["breaking bad","arcane","better call saul","mr robot","family guy","the simpsons","spongebob","friends","game of thrones","stranger things"]
        self.followup = False
        self.followups = []


    def findkeywords(self,message):

        for keyword in self.tv_shows:
            if keyword in message:
                if self.followup:
                    return self.response(keyword)
                else:
                    return ""

        if random.randint(0,1):
            if self.followup:
                return self.response(message)
            return self.steer_conversation()
        else:
            return ""



    def steer_conversation(self):
        thing = random.randint(1,4)
        self.followup = True
        # random prompts about tv shows
        if thing == 1:
            return "How is " + random.choice(self.poss)
        elif thing == 2:
            return "Did you like " + random.choice(self.poss)
        elif thing == 3:
            return "I love " + random.choice(self.poss)
        elif thing == 4:
            return "I watch a lot of tv shows, what are your favorites"



    def response(self,keyword):

        thing = random.randint(1,3)
        self.followup = False

        if thing == 1:
            return "I love " + keyword
        elif thing == 2:
            return "i heard " + keyword + " was good"
        elif thing == 3:
            return "i heard " + keyword + " was bad"



    def respond(self,prompt):

        prompt = prompt.lower()
        self.memory.add_user_input(prompt)

        thing = self.findkeywords(prompt)
        if len(thing) == 0 or prompt == "hello":
            thingy = self.model(self.memory,
                                        do_sample=True,
                                        max_length=1000,
                                        top_k=50,
                                        top_p=0.95)
            formatted = str(thingy).split("\n")
            messy = formatted[-2][6:]
            # clear memory
            if len(formatted) >= 10:
                self.memory = Conversation()

            return messy
        else:

            self.memory.append_response(thing)
            return thing

def main():

    # chatbot loop
    inp = ""
    print("***")
    print("type in quit to quit")
    print("***")

    conversation = Conversation()
    bot = Chatbot()
    print(bot.respond("hello"))

    while inp != "quit":

        inp = input()
        print(bot.respond(inp))





if __name__ == "__main__":
    main()
