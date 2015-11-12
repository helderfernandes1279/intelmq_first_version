from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import json

class IntelMQParserBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
	   event = utils.generate_observation_time(event, "observation_time")
           self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = IntelMQParserBot(sys.argv[1])
    bot.start()
