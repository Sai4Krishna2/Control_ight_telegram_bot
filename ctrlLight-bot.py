from telegram.ext import Updater,CommandHandler,MessageHandler,Filters # import the required handlers from telegram.ext package
from Adafruit_IO import Client,Feed,Data   # import the libraries to create feeds and send data to it
import requests # getting data from cloud
import os   #operating system

ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')   # adafruit username and password should be given as 'Config Vars' in the settings of your app on Heroku 
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')
aio = Client('ADAFRUIT_IO_USERNAME','ADAFRUIT_IO_KEY') # create instance of REST client
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # similar to the adafruit username and password

# for displaying the /start command message so that the user knows what the bot does 
def start(update, context):
    print(str( update.effective_chat.id ))
    context.bot.send_message(chat_id = update.effective_chat.id, text="Welcome! Type 'Turn on the Light' or /lighton to switch on the light bulb. Type 'Turn off the Light' or /lightoff to switch off the light bulb.")
# if the user types some unknown command
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oops, I didn't understand that. Try again!")

# function to send values to adafruit.io
def value_send(value):
  to_feed = aio.feeds('light') # put your own feed name here
  aio.send_data(to_feed.key,value)  # append a new value to a feed

# function to switch on light and send value '1' to adafruit
def lighton(update, context):
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id, text="Light has been turned ON")
  context.bot.send_photo(chat_id, photo='https://i5.walmartimages.com/asr/e62054e3-f6a2-46ce-8d0e-efe72943f485_1.3044d777832a0e874651e80fe3fa1ca1.jpeg')
  value_send(1)
#function to switch off the light and send value '0' to adafruit
def lightoff(update, context):
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id, text="Light has been turned OFF")
  context.bot.send_photo(chat_id=update.effective_chat.id,photo='https://jooinn.com/images/isolated-light-bulb-1.jpg')
  value_send(0)
# function to control the bot without giving commands
def given_message(bot, update):
  text = update.message.text.upper()
  text = update.message.text
  if text == 'Turn on the Light':
    lighton(bot,update)
  
  elif text == 'Turn off the Light':
    lightoff(bot,update)

u = Updater('TELEGRAM_TOKEN',use_context = True) 
dp = u.dispatcher
dp.add_handler(CommandHandler('lighton',lighton))  # register a handler
dp.add_handler(CommandHandler('lightoff',lightoff))
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.command, unknown)) # Filters.command allows messages starting with a bot command
dp.add_handler(MessageHandler(Filters.text, given_message)) # Filters.text allows text messages

u.start_polling()  # starts polling updates from Telegram
u.idle() # blocks until one of the signals are received and stops the updater
