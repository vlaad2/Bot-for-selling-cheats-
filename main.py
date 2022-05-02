### modules ###
import json
from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime
import sqlite3
from sqlite3 import Error
import menu as kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import aiohttp
from aiogram.types import CallbackQuery
from models import *
from telebot import TeleBot

db.create_tables([Users])
ref_link = 'https://telegram.me/{}?start={}'

### bot_data ###
TOKEN = '1737238548:AAEviNUWC5bzhs-2o-9bcgSVPUJ9UflAGqQ' 
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage = MemoryStorage())


### payment_data ###
QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Ijg5emk0MS0wMCIsInVzZXJfaWQiOiI3OTM5Mzg1MTMzMCIsInNlY3JldCI6IjQ3Y2JjYTRhYmM5ZWFlMDUyODMyMmRiMDA0YmI5NmE0YTI4ODQ0NGQ1NTc5YTEwZmRlZTNhZjE1ZTI1YWYzNjEifX0="
p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)


### database_create ###
with sqlite3.connect("smm.db") as conn:
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS users
  (user INTEGER, name TEXT,allorders INTEGER,balance FLOAT,allmoney FLOAT,orders TEXT)
  """)
orderr = 0
bal = 0 
allm = 0

global key
key = 'd48272e2934efccc410978e4712bbb2d'
### states ###
class order(StatesGroup):
    count = State()
    link = State()
class balans(StatesGroup):
    price = State()
class givebalance(StatesGroup):
    userad = State()
    summa = State()
class admad(StatesGroup):
    ad = State()

### menu ###
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.chat.id
    splited = message.text.split()
    if not Users.user_exists(user_id):
        Users.create_user(user_id)
        if len(splited) == 2:
            Users.increase_ref_count(splited[1])
    await bot.send_message(message.chat.id,text = f'👋 Привет,<b>👨‍👩‍👦‍👦{message.from_user.first_name}👨‍👩‍👦‍👦</b>\nВаш <b>🆔 {message.from_user.id}</b>\n<b>Для использования бота используйте кнопки ниже</b>',parse_mode = 'HTML',reply_markup = kb.home)
    print(f'Новый юзер - {message.from_user.first_name}')
    cursor.execute("select * from users where user = ?",(message.from_user.id,))
    usr = cursor.fetchone()
    if not usr:
        cursor.execute("INSERT INTO users values (:user, :name, :allorders, :balance, :allmoney, :orders);" ,
        {'user':message.from_user.id,
        'name':message.from_user.first_name,
        'allorders':orderr,
        'balance':bal,
        'allmoney':allm,
        'orders': ""})
        conn.commit()

### adm_enter ###
@dp.message_handler(commands=['adm'])
async def send_welcome(message: types.Message):
    if message.from_user.id == 1546182461:
        await bot.send_message(message.chat.id,text = 'Вы перешли в режим администратора 🩸',reply_markup= kb.adminka)
    else:
        await bot.send_message(message.chat.id,text ='Вы не являетесь администратором сервиса ☹️')


### menu_logics ###
@dp.message_handler(content_types = ['text'])
async def get_text(message: types.message):
    if message.text == '📊сделать заказ📊':
        await bot.send_message(message.chat.id,text ='🎆',reply_markup=kb.retu)
        await bot.send_message(message.chat.id,text = 'Куда Вы хотите накрутить?',reply_markup=kb.services)
    if message.text == '⚙️Профиль⚙️':
        balan = cursor.execute(f"SELECT balance FROM users WHERE user = {message.from_user.id}").fetchone()[0]
        allmo = cursor.execute(f"SELECT allmoney FROM users WHERE user = {message.from_user.id}").fetchone()[0]
        orderss = cursor.execute(f"SELECT allorders FROM users WHERE user = {message.from_user.id}").fetchone()[0]
        await bot.send_message(message.chat.id,text = f'🆔 {message.from_user.id}\n\n<b>🔐 Ваш баланс:</b> {balan}₽\n<b>📮 Всего заказов:</b> {orderss}\n<b>📥 Всего денег пополнено:</b> {allmo}₽',parse_mode='HTML',reply_markup=kb.lk)
    if message.text == '🆘 SUPPORT 🆘':
        await bot.send_message(message.chat.id,text = '<b>🆘 SUPPORT 🆘 @admricker\n\nПри обращении указывать:\n\n1: проблему.\n2: ваш 🆔\n3: все 1 четким сообщением.</b>',parse_mode='HTML')
    if message.text == '📚ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ📚':
        await bot.send_message(message.chat.id,text = """1.1 Оказание услуг продвижения в социальных сетях предоставляются в полном объеме при условии их 100% (сто процентов) оплаты Заказчиком. Для этого создана система оплаты и пополнения баланса.\n\n1.2. Возврат средств при отказе от заказа одной из сторон (Заказчика или Исполнителя) возможен только на баланс аккаунта. Эти средства Вы можете потратить в будущем на новые заказы. Заказчик - клиент сервиса, Исполнитель - администрация сервиса.\n\n1.3 Если вы начали пользоваться сервисом, то по умолчанию считается, что вы приняли его правила.\n\n1.4 Сервис не несёт ответственности за то, что услуга была списана/частично списана. \n\n1.5 Сервис не несет ответственности за содержание контента на страницах продвижения. Много заказов стартует в автоматическом режиме, лишая администрацию возможности проверять содержание контента клиента. Клиент несет всю полноту ответственности за свою деятельность, не уведомляя об этом поддержку.\n\n1.6 Живая накрутка не обязательно должна быть активной! Люди сами считают, нравится ли им Ваш контент или нет, сервис не несёт никакой ответственности за актив.\n\n1.7 Возврат средств осуществляется только на баланс пользователя.\n\n1.8 Сервис не несет ответственности за ошибки в ссылках, оставленные пользователем в заказе.\n\n1.9 Сервис не несёт отвественности за задержки, вызванные мерами, принятыми социальными сетями против раскрутки, - возможен лишь возврат денег на баланс бота, а так же несёт лишь ограниченную ответственность за ошибки самого бота SAKURA - администрация сделает все возможное для их устранения, но деньги так же могут быть возвращены лишь на баланс бота.
""")
    
    if message.text == '📑 Наличие услуг':
        await bot.send_message(message.chat.id,text = """<b>➖➖➖Накрутка Telegram➖➖➖</b>\nTelegram Просмотры | 0.108₽ (За 1 просмотр)\nTelegram Подписчики | 0.108₽ (За 1 подписчика)\n\n<b>➖➖➖Накрутка Instagram➖➖➖</b>\nInstagram Подписчики | 0.1₽ (За 1 подписчика)\nInstagram Лайки | 0.24₽ (За 1 лайк)\nInstagram Просмотры поста | 0.004₽ (За 1 просмотр)\n\n<b>➖➖➖Накрутка YouTube➖➖➖</b>\nYouTube Просмотры | 0.29₽ (За 1 просмотр)\nYouTube Подписчики | 0.56₽ (За 1 подписчика)\nYouTube Лайки | 0.1₽ (За 1 лайк)\n\n<b>➖➖➖Накрутка Вконтакте➖➖➖</b>\nВконтакте подписчики в группу | 0.5₽ (За 1 подписчика)\nВконтакте друзья | 0.46₽ (За 1 заявку)\nВконтакте лайки | 0.17₽ (За 1 лайк)\nВконтакте репосты | 0.24₽ (За 1 репост)\n\n<b>➖➖➖Накрутка Discord➖➖➖</b>\nDiscord Подписчики на сервер | 50₽ (За 1 пользоветеля)\n\n<b>➖➖➖Накрутка TikTok➖➖➖</b>\nTikTok Просмотры | 0.17₽ (За 1 просмотр)\nTikTok Подписчики | 0.17₽ (За 1 подписчика)\nTikTok Лайки | 0.08₽ (За 1 лайк)""",parse_mode= 'HTML')
    if message.text == '💰 Выдать баланс':
        await bot.send_message(message.chat.id,text = 'Введите User-ID пользователя')
        await givebalance.userad.set()
    if message.text == '📈 Статистика':
        allus = cursor.execute('SELECT Count(*) FROM users').fetchone()[0]
        allden = cursor.execute('SELECT SUM(allmoney) FROM users').fetchone()[0]
        allord = cursor.execute('SELECT SUM(allorders) FROM users').fetchone()[0]
        await bot.send_message(message.chat.id,text = f"<b>Статистика</b>\n\n<b>Всего пользователей:</b> {allus}\n<b>Всего денег пополучено:</b> {allden}₽\n<b>Всего заказов:</b> {allord}",parse_mode='HTML')
    if message.text == '❌ Выйти из админки':
        await bot.send_message(message.chat.id,text = 'Done!',reply_markup=kb.home)
    if message.text == '📨 Рассылка':
        await bot.send_message(message.chat.id,text = 'Введите текcт объявления')
        await admad.ad.set()         
    if message.text == '❌ Отмена':
        await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.home)
    if message.text == '💸Реферальная система💸':
        count = Users.get_ref_count(message.chat.id)
        await bot.send_message(message.chat.id,text = f'<b>Ваша реферальная ссылка:</b> {ref_link.format("SAKURANAKPYTKABOT",message.chat.id)}\n<b>Количество рефералов:</b> {count}\n\nЕсли пользователь перейдет в бота по Вашей реферальной ссылке и сделает пополнение,то на Ваш баланс будет зачислено 5% от суммы его пополнения.',parse_mode='HTML')
    if message.text == '🧾УСЛУГИ ОТ SAKURA🧾':
        await bot.send_message(message.chat.id,text = 'Наши услуги:',reply_markup=kb.sakura)
### adm_AD ###
@dp.message_handler(state=admad.ad)
async def getcount(message: types.Message, state: FSMContext):
    ad = message.text
    await state.update_data(ad=ad)
    await state.finish()
    cursor.execute("SELECT user FROM users")
    userbase = []
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        userbase.append(row)
    if len(userbase) > 1:
        for z in range(len(userbase)):
            await bot.send_message(userbase[z][0],text = f"Объявление!\n{ad}")
    else:
        await bot.send_message(userbase[0], f"Объявление!\n{ad}")  
    await bot.send_message(message.chat.id,text = 'Done!')

### adm_change_balance ###
@dp.message_handler(state=givebalance.summa)
async def getcount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    userad = data.get('userad')
    summa = float(message.text)
    newbalance = cursor.execute(f'SELECT balance FROM users WHERE user = {userad}').fetchone()[0]
    newbalance += summa
    cursor.execute(f'UPDATE users SET balance = {newbalance} WHERE user = {userad}')
    conn.commit()
    await bot.send_message(message.chat.id,text = 'Баланс был обновлен')


### adm_change_balance ###
@dp.message_handler(state=givebalance.userad)
async def getcount(message: types.Message, state: FSMContext):
    userad = message.text
    await state.update_data(userad=userad)
    await message.answer(f'Введите сумму которую хотите выдать')
    await givebalance.summa.set()


### replenishment_method ###
@dp.message_handler(state=balans.price)
async def getcount(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    data = await state.get_data()
    state.finish()
    ###
    if message.text == '❌ Отмена':
        await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.home)
        await state.finish()
        return
    amount = data.get('price')
    amount = int(amount)
    lifetime = 15
    comment = message.from_user.id
    bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment)
    ###
    markup_inline = types.InlineKeyboardMarkup(resize_keyboard=True)
    buy = types.InlineKeyboardButton(text='Перейти к оплате', url=f'{bill.pay_url}')
    check = types.InlineKeyboardButton(text='🎁 Проверить платеж', callback_data=f'check_pay:{bill.bill_id}')
    markup_inline.add(buy)
    markup_inline.add(check)
    await bot.send_message(message.chat.id,
                           text='1⃣ Для пополнения баланса совершите платеж нажатием кнопки ниже и перейдите ко второму пункту\n\n2⃣ После оплаты нажмите на кнопку "Проверить платеж" и Ваши  средства будут зачислены на счет')
    await bot.send_message(message.chat.id,
                           text='❗ Переходить по ссылке можно только через браузер.\n\nВ случае, если вы оплатите через приложение Qiwi и у Вас возникнут проблемы - обратитесь к саппорту: @admricker',
                           reply_markup=markup_inline)


### replenishment_check ###
@dp.callback_query_handler(text_startswith="check_pay", state="*")
async def give_win_user(call: CallbackQuery, state: FSMContext):
    bill_id = call.data.split(":")[1]
    status = p2p.check(bill_id=bill_id).status
    check = p2p.check(bill_id=bill_id).comment
    print(bill_id)
    print(status)
    print(check)
    if status == 'PAID' and check == str(call.from_user.id):
        data = await state.get_data()
        await bot.send_message(call.message.chat.id,text = 'Оплата прошла успешно!',reply_markup=kb.home)
        amount = float(data.get('price'))
        userid = int(call.from_user.id)
        allmonn = cursor.execute(f"SELECT allmoney FROM users WHERE user = {userid}").fetchone()[0]
        balance = cursor.execute(f"SELECT balance FROM users WHERE user = {userid}").fetchone()[0]
        allmonn = allmonn + amount
        balance = float(balance)
        balik = balance + amount
        cursor.execute(f'UPDATE users SET balance ={balik} WHERE user = {userid}')
        cursor.execute(f'UPDATE users SET allmoney ={allmonn} WHERE user = {userid}')
        conn.commit()
        print(balik)
        await state.finish()
    else:
        await bot.send_message(call.message.chat.id,'Вы не оплатили счет!')


### order ###
@dp.message_handler(state=order.count)
async def getcount(message: types.Message, state: FSMContext):
    count = message.text
    await state.update_data(count=count)
    if message.text == '❌ Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.home)
            await state.finish()
            return
    await message.answer(f'Введите ссылку')
    await bot.send_message(message.chat.id,text = '<b>‼️ ВАЖНО ‼️</b>\n\n📎 Пример ссылки: https://youtube.com/channel/Название\n\n<b>(Так для других сервисов также)\n\nВАЖНО ВВОДИТЬ СЫЛЛКУ ТОЛЬКО В ТАКОМ ФОРМАТЕ.\n\nПРИ НЕПРАВИЛЬНОМ ВВОДЕ ДЕНЬГИ ПРОПАДАЮТ📛</b>',parse_mode = 'HTML')
    await order.link.set()


### get_link ###
@dp.message_handler(state=order.link)
async def getlink(message: types.Message, state: FSMContext):
    global link
    link = message.text
    await state.update_data(link=link)
    data = await state.get_data()
    if message.text == '❌ Отмена':
        await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.home)
        await state.finish()
        return
    global count
    count = data.get("count")
    count = int(count)
    link = data.get("link")    
    global totalprice
    totalprice = price * count
    await state.finish()
    await bot.send_message(message.chat.id,text = f'<b>Стоимость заказа</b>: {totalprice}₽\nЗаказываем?',parse_mode='HTML',reply_markup=kb.confirm)




#servs
@dp.callback_query_handler(lambda c: c.data)
async def ans(call: CallbackQuery,state: FSMContext):
    if call.data == 'ki':
        await bot.send_message(call.message.chat.id,text = 'Данное действие 🤹‍♂️ поможет ой как напугать врага накрутив ему за 30 секунд в чат 1000 ботов = 150₽\nЗакрытые/открытые БЕЗ РАЗНИЦЫ😅\nЗаказать: https://t.me/admricker')
    if call.data == 'rekl':
        await bot.send_message(call.message.chat.id,text = 'Заказать рекламу рассылку в нашем боте по хорошей цене\n🚀 https://t.me/admricker')
    if call.data == 'refka':
        usid = call.message.from_user.id
        last = cursor.execute(f'Select ref FROM users where user_id = {usid}')
    if call.data == 'bal':
        await bot.send_message(call.message.chat.id,text = 'Введите сумму на которую желаете пополнить баланс 📥 ',reply_markup=kb.retu)
        await balans.price.set()
    if call.data == 'mo':
        userid = call.from_user.id
        zakaz = cursor.execute(f"SELECT orders FROM users WHERE user = {userid}").fetchone()[0]
        if zakaz == '':
            await bot.send_message(call.message.chat.id,text = 'Вы еще не делали заказов.')
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://justanotherpanel.com/api/v2/?key={key}&action=status&orders={zakaz}') as resp:
                    if resp.status == 200:
                        ors = await resp.text()
                        dannie = json.loads(ors)
                        zakazi = ""
                        for d in dannie:
                            zakaz_num = d
                            status = dannie[zakaz_num]['status']
                            remains = dannie[zakaz_num]['remains']
                            ans = f"<b>Заказ #{zakaz_num}</b>\nОсталось накрутить: {remains}\nСтатус: {status}"
                            if zakazi == "":
                                zakazi = ans
                            else:
                                zakazi = zakazi + "\n\n" + ans
                            answer = f"<b>Ваши заказы</b>:\n\n{zakazi}"
                        await bot.send_message(call.message.chat.id, text = answer,parse_mode='HTML')
                    else:
                        await bot.send_message(call.message.chat.id.text,text = 'Сервер временно не отвечает,повторите попытку позже.')
    if call.data == 'hand':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.handls)
    if call.data == 'yt':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.youtubeserv)
    if call.data == 'inst':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.instagramserv)
    if call.data == 'vk':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.vkserv)
    if call.data == 'ds':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.discordserv)
    if call.data == 'tt':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.tiktokserv)
    if call.data == 'tg':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите тип услуги:",reply_markup=kb.telegramserv)
    #### YOUTUBE serv ###
    if call.data == 'yttw':
        global price
        price = float(0.29)
        global serviceid
        serviceid = 4152
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nYouTube Просмотры\nЦена: {price}₽(За 1 просмотр)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'ytts':
        price = float(0.56)
        serviceid = 4395
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nYouTube подписчики\nЦена: {price}₽(За 1 подпиcчика)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'yttl':
        price = float(0.1)
        serviceid = 3475
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\YouTube лайки в канал\nЦена: {price}₽(За 1 лайк)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    #### INSTAGRAM serv ###
    if call.data == 'innst1':
        price = float(0.1)
        serviceid = 4448
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nInstagram Подписчики\nЦена: {price}₽(За 1 подписчика)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'innst2':
        price = float(0.24)
        serviceid = 3788
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nInstagram Лайки\nЦена: {price}₽(За 1 лайк)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'innst3':
        price = float(0.004)
        serviceid = 3350
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nInstagram Просмотры сторис\nЦена: {price}₽(За 1 просмотр)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    #### ВКОНТАКТЕ serv ###
    if call.data == 'vkss':
        price = float(0.5)
        serviceid = 3752
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nВконтакте подписчики в группу\nЦена: {price}₽(За 1 подписчика)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'vkff':
        price = float(0.46)
        serviceid = 3754
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nВконтакте друзья\nЦена: {price}₽(За 1 заявку)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'vkll':
        price = float(0.17)
        serviceid = 3756
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nВконтакте лайки\nЦена: {price}₽(За 1 лайк)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'vkrr':
        price = float(0.24)
        serviceid = 3761
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nВконтакте репосты\nЦена: {price}₽(За 1 репост)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    #### DIScORD serv ###
    if call.data == 'diss':
        price = float(50)
        serviceid = 5657
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nDiscord подписчики на сервер\nЦена: {price}₽(За 1 юзера)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    #### TIKTOK serv ###
    if call.data == 'ttww':
        price = float(0.17)
        serviceid = 5636
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nTikTok Просмотры\nЦена: {price}₽(За 1 просмотр)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'ttss':
        price = float(0.17)
        serviceid = 3882
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nTikTok Подписчики\nЦена: {price}₽(За 1 подписчка)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'ttll':
        price = float(0.08)
        serviceid = 4174
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\nTikTok Лайки\nЦена: {price}₽(За 1 лайк)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    #### TELEGRAM serv ###
    if call.data == 'tggb1':
        price = float(0.13)
        serviceid = 2163
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\Telegram Просмотры\nЦена: {price}₽(За 1 просмотр)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'tggb2':
        price = float(0.13)
        serviceid = 363
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Order</b>\Telegram Подписчики\nЦена: {price}₽(За 1 подписчика)\n\nВведите количестcво которое желаете приобрести\n(min: 100,max: 10000)",parse_mode='HTML')
        await order.count.set()
    if call.data == 'tggb3':
        await bot.send_message(call.message.chat.id,text = '<b>Накрутка в чат 💬 (телеграмм)\n\n🔰От 100 до 10000\n💷Цена за 100 = 15₽</b>',parse_mode='HTML',reply_markup = kb.zakazat)
    if call.data == 'han11':
        await bot.send_message(call.message.chat.id,text = '<b>🔰От 100 до 10000\n💷Цена за 100 = 15₽</b>',parse_mode='HTML',reply_markup = kb.zakazat)
    if call.data == 'da':
        userid = int(call.from_user.id)
        allmoney = cursor.execute(f"SELECT allmoney FROM users WHERE user = {userid}").fetchone()[0]
        balance = cursor.execute(f"SELECT balance FROM users WHERE user = {userid}").fetchone()[0]
        allorde = cursor.execute(f"SELECT allorders FROM users WHERE user = {userid}").fetchone()[0]
        if balance >= totalprice:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://justanotherpanel.com/api/v2/?key={key}&action=add&service={serviceid}&quantity={count}&link={link}') as resp:
                    if resp.status == 200:
                        await state.finish()
                        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Заказ принят в обработку.\nОтcледить статус заказа можно в 'Мои заказы'")
                        balance = balance - totalprice
                        allorde = allorde + 1
                        cursor.execute(f'UPDATE users SET balance ={balance} WHERE user = {userid}')
                        cursor.execute(f'UPDATE users SET allorders ={allorde} WHERE user = {userid}')
                        conn.commit()
                        resp = (await resp.text())
                        orde = cursor.execute(f"SELECT orders FROM users WHERE user = {userid}").fetchone()[0]
                        if orde == "":
                            orde = str(orde)
                            ordee = orde + resp[9:-1]
                            cursor.execute(f'UPDATE users SET orders = ? WHERE user = ?;', (ordee, userid))
                            conn.commit()
                        else:
                            orde = str(orde)
                            ordee = orde + ',' + resp[9:-1]
                            cursor.execute(f'UPDATE users SET orders = ? WHERE user = ?;', (ordee, userid))
                            conn.commit() 
        else:      
            await bot.send_message(call.message.chat.id,text = 'Недостаточно средств\nПополните баланс')     
    if call.data == 'net':
        await bot.send_message(call.message.chat.id,text = 'Заказ отменен',reply_markup=kb.home)


executor.start_polling(dp)




