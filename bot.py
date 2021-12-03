import telegram.ext
from nsetools import Nse
# from dotenv import load_dotenv
from os import environ

nse = Nse()

# load_dotenv()

TOKEN = environ.get('TOKEN')

def start(update, context):
    update.message.reply_text("""
    Hi, Algo trading bot here!

1. /start

    Menu of commands

2. <your_nse_code>

    Current price of stock
        for e.g. 
        sbin

3. /details  <your_stock_code>

    Basic details about the Stock.
        for e.g.
        /details nifty 50
""")   

def details(update, context):
    # /command arg0 arg1 arg2   -- args are stored in context.args[]
    # nseCodes can be multi word. for e.g. "nifty 50"
    code = ""
    for sub_str in context.args:
        code += sub_str + " "
    
    # remove trailing extra space
    code = code.strip()

    # Check whether any code is provided
    if (not(code)):
        update.message.reply_text("Please provide code along with the command.")
        return

    quote = nse.get_quote(code)        # return none for 'invalid code' or 'index code'
    if (quote):
        type = "Stock"
        stock = quote
        name = stock['companyName']
        price = stock['lastPrice']
        code = stock['symbol']
    else:
        stock = nse.get_index_quote(code)
        # whether the code is invalid
        if (not(stock)):
            update.message.reply_text("Please Enter a valid code.")
            return
        type = "Index"
        name = stock['name']
        price = stock['lastPrice']
        code = name 

    update.message.reply_text(f""" 
Code : {code}
Name : {name}
Type : {type}
Price: {price}
""")

def handle_message(update, context):
    code = update.message.text
    stock = nse.get_quote(code) or nse.get_index_quote(code)
    
    if (stock):
        update.message.reply_text(stock['lastPrice'])
    else:
        update.message.reply_text("Invalid code.")

updater = telegram.ext.Updater(TOKEN)
disp = updater.dispatcher


disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("details", details))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))


updater.start_polling()
updater.idle()
