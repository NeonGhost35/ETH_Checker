import telebot
import blocksmith
import pyetherbalance 
import os
from threading import Thread

iduser = "" # Your TelegramID
api_key = "" #Your TelegramBotApi
infura_url = 'https://mainnet.infura.io/v3/95e61773fe7742b49cce2e4f9fe0db81'

bot = telebot.TeleBot(api_key)

keyboard0 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard0.row('Добавить кошелек через seed', 'Запустить Чекер', 'CheckAll')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Остановить Чекер')



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(iduser, 'Вас приветствует ETH CHECKER', reply_markup=keyboard0)

@bot.message_handler(content_types=['text'])
def send_text(message):
    def update():
        addresslist = open('addresslist.txt',"a",encoding='utf-8', errors='ignore')
        addresslist.close()
        addresslist = open('addresslist.txt',"r",encoding='utf-8', errors='ignore')
        seeds = open('seedlist.txt',"a",encoding='utf-8', errors='ignore')
        seeds.close()
        seeds = open('seedlist.txt',"r",encoding='utf-8', errors='ignore')
        for seed in seeds:
            kg = blocksmith.KeyGenerator()
            kg.seed_input(seed)
            key = kg.generate_key()
            address = blocksmith.EthereumWallet.generate_address(key)
            x = os.stat("addresslist.txt").st_size
            if x  == 0:
                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                balance_eth = ethbalance.get_eth_balance(address)
                balance_eth = balance_eth['balance']
                balance_eth = str(balance_eth)
                balance_eth = balance_eth[1:]
                f = open('addresslist.txt', 'a')
                f.write(str(str(address) + ":" + str(balance_eth)))
                f.write(" \n")
                f.close()
            for adress in addresslist:
                adress = adress[:42]
                if address == adress:
                    pass
                else:
                    ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                    balance_eth = ethbalance.get_eth_balance(address)
                    balance_eth = balance_eth['balance']
                    balance_eth = str(balance_eth)
                    with open('addresslist.txt', 'rb') as final:
                        data = final.read()
                    with open('addresslist.txt', 'wb') as final:    
                        final.writelines([(str(address) + ':' + str(balance_eth) + '\n').encode()])
                        final.write(data)
    def checkwallet(cmd):
        update()
        while True:
            if cmd == 0: 
                return "Остановленно"
            elif cmd == 1:
                pass
            addresslistc = open('addresslist.txt',"r",encoding='utf-8', errors='ignore')
            for line in addresslistc:
                addr = line[:42]
                ethbalance = pyetherbalance.PyEtherBalance(infura_url)
                balance_eth = ethbalance.get_eth_balance(addr)
                balance_eth = balance_eth['balance']
                balance = line
                balance = balance.split(":")
                balance = balance[1]
                balance = str(balance)

                balance_eth = str(balance_eth)
                
                print(str(balance) + " " + str(balance_eth))
                if str(balance) == str(balance_eth):
                    pass
                else:
                    bot.send_message(iduser, 'Баланс кошелька ' + addr + ' обновился\nНовый баланс ' + str(balance_eth), reply_markup=keyboard1)
                    required = str(addr) + " " + str(balance)
                    for num_line, line in enumerate(addresslistc):
                        if required in line:
                            lines = addresslistc.readlines()
                            lines[num_line] = str(addr) + str(balance_eth) + '\n'
                            save_changes = open('addresslist.txt', 'w')
                            save_changes.writelines(lines)
                            save_changes.close()
                            break

    seed = message.text
    seed = seed[:4]

    if seed.lower() == "seed":
        seed = message.text
        seed = seed[6:]
        f = open('seedlist.txt', 'a')
        f.write(str(seed))
        f.write(" \n")
        f.close()
        bot.send_message(iduser, 'Сид ' + str(seed) + " успешно добвален", reply_markup=keyboard0)
    
    if message.text == 'Добавить кошелек через seed':
        bot.send_message(iduser, 'Введите данные в формате seed: Seed фраза', reply_markup=keyboard0)
    if message.text == 'Запустить Чекер':
        th = Thread(target=checkwallet, args=(1, ))
        th.start()
        bot.send_message(iduser, 'Чекер запущен', reply_markup=keyboard1)
    if message.text == 'Остановить Чекер':
        th1 = Thread(target=checkwallet, args=(0, ))
        th1.start()
        bot.send_message(iduser, 'Чекер остановлен', reply_markup=keyboard0)
    if message.text == "CheckAll":
        f = open("addresslist.txt","rb")
        bot.send_document(iduser, f) 
        f.close()
bot.polling(none_stop=True)