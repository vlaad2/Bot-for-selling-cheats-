from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

### Adminka ###
adminka = types.ReplyKeyboardMarkup(resize_keyboard=True)
percent = types.KeyboardButton(text = '📈 Статистика',callback_data = 'per')
chbal = types.KeyboardButton(text = '💰 Выдать баланс',callback_data = 'cbal')
returnn = types.KeyboardButton(text = '❌ Выйти из админки')
rass = types.KeyboardButton(text = '📨 Рассылка')
adminka.add(percent,chbal,rass,returnn)



### Main menu ###
home = types.ReplyKeyboardMarkup(resize_keyboard= True,row_width=2)
nakrutka = types.KeyboardButton(text = '📊сделать заказ📊',callback_data = 'nakr')
account = types.KeyboardButton(text = '⚙️Профиль⚙️',callback_data = 'akk')
support = types.KeyboardButton(text = '🆘 SUPPORT 🆘',callback_data = 'tp')
ref = types.KeyboardButton(text = ' 💸Реферальная система💸',callback_data = 'rf')
police = types.KeyboardButton(text = '📚ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ📚')
rrr = types.KeyboardButton(text = '🧾УСЛУГИ ОТ SAKURA🧾',callback_data = 'rr')
home.add(nakrutka,account,support,ref,police,rrr)

sakura = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
kill = types.KeyboardButton(text = 'УБИТЬ ЧАТ 💬 ',callback_data = 'ki')
piar = types.KeyboardButton(text = '📊РЕКЛАМА📊',callback_data = 'rekl')
sakura.add(kill,piar)

lk = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
balance = types.KeyboardButton(text = '💳 Пополнить баланс',callback_data = 'bal')
myorders = types.KeyboardButton(text = '👨🏼‍💻 Мои заказы',callback_data = 'mo')
lk.add(balance,myorders)

### order_execept ###
confirm = types.InlineKeyboardMarkup(resize_keyboard = True)
yes = types.InlineKeyboardButton(text = 'Да',callback_data= 'da')
no = types.InlineKeyboardButton(text = 'Отменить заказ',callback_data='net')
confirm.add(yes,no)


### return_button ###
retu = types.ReplyKeyboardMarkup(resize_keyboard = True)
otmena = types.KeyboardButton(text = '❌ Отмена',callback_data = 'otm')
retu.add(otmena)


### services ###
services = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
youtube = types.InlineKeyboardButton(text = '🎆 Youtube',callback_data = 'yt')
instagram = types.InlineKeyboardButton(text = '🎆 Instagram',callback_data = 'inst')
telegram = types.InlineKeyboardButton(text = '🎆 Telegram',callback_data = 'tg')
vkontakte = types.InlineKeyboardButton(text = '🎆 Вконтакте',callback_data = 'vk')
discord = types.InlineKeyboardButton(text = '🎆 Discord',callback_data = 'ds')
tiktok = types.InlineKeyboardButton(text = '🎆 TikTok',callback_data = 'tt')
handler = types.InlineKeyboardButton(text = '🎆 Ручная накрутка',callback_data = 'hand')
services.add(telegram,instagram,youtube,vkontakte,discord,tiktok,handler)

handls = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
han = tgb3 = types.InlineKeyboardButton(text = '🎆Боты в чат [ТГ]',callback_data='tggb3')
han1 = types.InlineKeyboardButton(text = '🎆Боты в канал[ТГ]',callback_data='han11')
handls.add(han,han1)

zakazat = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
zakaz = types.InlineKeyboardButton(text = 'Заказать',callback_data='tggbf3',url = 't.me/admricker')
zakazat.add(zakaz)

### Youtube ###
youtubeserv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
ytw = types.InlineKeyboardButton(text = 'YouTube Просмотры',callback_data='yttw')
yts = types.InlineKeyboardButton(text = 'YouTube Подписчики',callback_data='ytts')
ytl = types.InlineKeyboardButton(text = 'Youtube Лайки',callback_data='yttl')
youtubeserv.add(ytw,yts,ytl)

### Instagram ###
instagramserv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
inst1 = types.InlineKeyboardButton(text = 'Instagram Подписчики',callback_data= 'innst1')
inst2 = types.InlineKeyboardButton(text = 'Instagram Лайки',callback_data= 'innst2')
inst3 = types.InlineKeyboardButton(text = 'Instagram Просмотры поста',callback_data= 'innst3')
instagramserv.add(inst1,inst2,inst3)

### Telegram ###
telegramserv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
tgb1 = types.InlineKeyboardButton(text = 'Telegram Просмотры',callback_data='tggb1')
tgb2 = types.InlineKeyboardButton(text = 'Telegram Подписчики',callback_data='tggb2')
telegramserv.add(tgb1,tgb2)

### Вконтакте ###
vkserv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
vks = types.InlineKeyboardButton(text = 'Вконтакте подписчики в группу',callback_data='vkss')
vkf = types.InlineKeyboardButton(text = 'Вконтакте друзья',callback_data='vkff')
vkl = types.InlineKeyboardButton(text = 'Вконтакте лайки',callback_data='vkll')
vkr = types.InlineKeyboardButton(text = 'Вконтакте репосты',callback_data='vkrr')
vkserv.add(vks,vkf,vkl,vkr)

### TikTok ###
tiktokserv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
ttw = types.InlineKeyboardButton(text = 'TikTok Просмотры',callback_data='ttww')
tts = types.InlineKeyboardButton(text = 'TikTok Подписчики',callback_data='ttss')
ttl = types.InlineKeyboardButton(text = 'TikTok Лайки',callback_data='ttll')
tiktokserv.add(ttw,tts,ttl)

### Discord ###
discordserv = types.InlineKeyboardMarkup(resize_keyboard = True,row_width=1)
dis = types.InlineKeyboardButton(text = 'Discord Подписчики на сервер',callback_data='diss')
discordserv.add(dis)

