# Bot-for-selling-cheats-

#For stable operation of the bot, Python version 3.9 is required
 Before running the script (main.py), you need to open it and fill in the following fields:

 - TOKEN - token of your bot (24 line of code)
 - QIWI_PRIV_KEY - secret key of your qiwi wallet for receiving transfers (30th line of code)
 - key - your api key from the panel with which we will resell services (45 line of code)
 - admid - Your telegramID - to access the admin panel (78 code line)


 You can get the TOKEN value through the TG bot @BotFather
 You can get the QIWI_PRIV_KEY value from the link - https://qiwi.com/p2p-admin/transfers/api
 You can get the key value from the link - https://justanotherpanel.com/api

 If you have done the steps above, then you can run the "main.py" file and enjoy the work of the bot

#установка
$ git clone https://github.com/vlaad2/Bot-for-selling-cheats
$ cd Bot-for-selling-cheats
$ python3 main.py
$ pip3 install pyqiwip2p
