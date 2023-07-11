import telebot
from etherscan import Etherscan
import os

check = 0

eth = Etherscan('') # API ETHERSCAN
iduser = "" # Your TelegramID
api_key = "" #Your TelegramBotApi

def save_addres(message):
    print(message.text)
    eth_balance = int(eth.get_eth_balance(message.text)) / 1000000000000000000
    addr = open('addrlist.txt', 'a')
    addr.write(message.text + ":" + str(eth_balance))
    addr.write(" \n")
    addr.close()
    bot.send_message(iduser, "Сохранил! \nТекущий баланс кошелька:" + str(eth_balance) + " ETH")

bot = telebot.TeleBot(api_key)

keyboard0 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard0.row('Добавить кошелек', 'Запустить Чекер')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Остановить Чекер')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(iduser, 'Вас приветствует ETH CHECKER', reply_markup=keyboard0)

@bot.message_handler(content_types=['text'])
def send_text(message):
    INFILE = "addrlist.txt"
    OUTFILE   = "temp_addrlist.txt"
    if message.text == 'Добавить кошелек':
        sent = bot.send_message(iduser, "Введите аддрес:")
        bot.register_next_step_handler(sent, save_addres)
    if message.text == 'Запустить Чекер':
        check = 1
        while 1:
            if check == 1:
                wordlist = open('addrlist.txt',"r",encoding='utf-8', errors='ignore')
                for line in wordlist:
                    addres = line.split(':')[0]
                    oldbalance = line.split(':')[1]
                    newbalance = int(eth.get_eth_balance(message.text)) / 1000000000000000000
                    if oldbalance == newbalance:
                        pass
                    else:
                        f = open('file.txt').read()
                        f = f.replace(addres + newbalance + '\n','')
                        if oldbalance > newbalance:
                            bot.send_message(iduser, "Баланс кошелька " + addres + " уменьшился \nНовый баланс: " + newbalance)
                        elif oldbalance < newbalance:
                            bot.send_message(iduser, "Баланс кошелька " + addres + " увеличился \nНовый баланс: " + newbalance)
                with open(INFILE) as orig, open(OUTFILE, "w") as edited:
                    for line in orig:
                        if line.strip():
                            edited.write(line)
                os.remove(INFILE)
                os.rename(OUTFILE, INFILE)
            else:
                break
    if message.text == 'Остановить Чекер':
        check = 0
bot.polling()
