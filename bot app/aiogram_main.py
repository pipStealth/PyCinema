############################## IMPORTING ##############################
from aiogram_config import token, admin_id
from aiogram_keyboard import start_Keyboard, back_Keyboard, admin_Keyboard
import asyncio
import logging
from datetime import datetime
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    BufferedInputFile, CallbackQuery, Message, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter

from aiogram.fsm.context import FSMContext, StorageKey
import uuid
import re
import json
from functools import wraps
from datetime import datetime
import ssl
import os
from PIL import Image
import io
from tempfile import NamedTemporaryFile
import pyperclip
import random
import sys
sys.path.append('D:/Kinopoisk project')
from mysql.mysql_main import add_db, take_db 
from mysql.mysql_command import get_poster_by_code, get_all_codes, get_last_code

##########################################################################
# REGISTRATION AND INITIALIZATION BOT

logging.basicConfig(level=logging.INFO) #  Setting the level of logs to INFO
bot = Bot(token) #  Creating bot instance with token
dp = Dispatcher() # Create dispatcher type


##########################################################################
# JSON LOGGING

def add_user_to_json(file_path):
    def decorator(func):
        @wraps(func)
        def wrapper(user_id, day):
            try:
                with open(file_path, 'r') as f:
                    users = json.load(f)
            except FileNotFoundError:
                users = {"USER": {}}

            if f"user{user_id}" not in users["USER"]:
                users["USER"][f"user{user_id}"] = {"id": user_id, "date": f"{day}", "ban": False}
                with open(file_path, 'w') as f:
                    json.dump(users, f, indent=4)
                print(f"User {user_id} add in json.")
            else:
                print(f"User {user_id} have already done.")

            return func(user_id, day)
        return wrapper
    return decorator

@add_user_to_json('users.json')
def process_user(user_id, day):
    print(f"Work wit: {user_id}... Check result! | {day}")

def get_user_ban_status(user_id, file_path="users.json"):
    try:
        with open(file_path, 'r') as f:
            users = json.load(f)
        return users["USER"][f"user{user_id}"]["ban"]
    except (FileNotFoundError, KeyError):
        return f"User {user_id} not found."


def get_user_date(user_id, file_path="users.json"):
    try:
        with open(file_path, 'r') as f:
            users = json.load(f)
        return users["USER"][f"user{user_id}"]["date"]
    except (FileNotFoundError, KeyError):
        return f"User {user_id} not found."
    
def ban_user_by_id(user_id, file_path="users.json"):
    try:
        with open(file_path, 'r') as f:
            users = json.load(f)
        with open(file_path, "a") as _:
            users["USER"][f"user{user_id}"]["ban"] = True
        return True
    except (FileNotFoundError, KeyError):
        return f"User {user_id} not found."
    
def unban_user_by_id(user_id, file_path="users.json"):
    try:
        with open(file_path, 'r') as f:
            users = json.load(f)
        with open(file_path, "a") as _:
            users["USER"][f"user{user_id}"]["ban"] = False
        return True
    except (FileNotFoundError, KeyError):
        return f"User {user_id} not found."

def read_image(file_path):
    sys.path.append('D:/Kinopoisk project/bot app')
    with open(file_path, 'rb') as file:
        return file.read()
    

##########################################################################
# STATES

class Users(StatesGroup):
    film = State()
    add_photo = State()
    add_text = State()

class Admins(StatesGroup):
    ban = State()
    unban = State()
    add_film_poster = State()
    add_film_headline = State()
    add_film_description = State()

##########################################################################
### USERS FUNCTION ###
##########################################################################

### START COMMANDS ###
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(None)
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        day = datetime.now().date()
        process_user(message.from_user.id, day)
        await message.reply(
            f"👋 Hello, {message.from_user.first_name}!\n\n"
            "🌞 I'am Cinema Bot, bot with libary!\n\n"
            "🌟 You can use me for find film by code!\n\n"
            "🤚 For abusing the bot's functionality, you may be blocked!",
            reply_markup=start_Keyboard()
        )

######################################################################################
### BACK COMMAND ###


@dp.message(F.text == "Back ⏪")
async def back(message: types.Message, state: FSMContext):
    await state.set_state(None)
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        day = datetime.now().date()
        process_user(message.from_user.id, day)
        await message.reply(
            f"👋 Hello, {message.from_user.first_name}!\n\n"
            "🌞 I'am Cinema Bot, bot with libary!\n\n"
            "🌟 You can use me for find film by code!\n\n"
            "🤚 For abusing the bot's functionality, you may be blocked!",
            reply_markup=start_Keyboard()
        )

######################################################################################
### FILM COMMAND ###

@dp.message(F.text == "📚 Films", StateFilter(None))
async def films(message: types.Message, state: FSMContext):
    
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        await state.set_state(Users.film)
        day = datetime.now().date()
        process_user(message.from_user.id, day)

        await message.reply(
            f"👋 {message.from_user.first_name}!\n\n"
            "🌞 Give me the code of film!\n\n",
            reply_markup=back_Keyboard()
        )

@dp.message(F.text, StateFilter(Users.film))
async def take_film_code(message: types.Message, state: FSMContext):
    answer = take_db(get_poster_by_code(message.text), 0)   
    if answer.get("photo"):
        random_name = ''.join([str(random.randint(0, 9)) for _ in range(24)])
        image = Image.open(io.BytesIO(answer["photo"]))
        image.save(f"{random_name}.png")
        await bot.send_photo(message.chat.id, photo=types.FSInputFile(f"{random_name}.png"))
        os.remove(f"{random_name}.png")
        await message.answer(f"<b>{answer["headline"]}</b>\n\n{answer["description"]}", reply_markup=back_Keyboard(), parse_mode=ParseMode.HTML)    
    else:
        await message.answer("🔍 No poster found for this film.")



######################################################################################
### PROFILE COMMAND ###

@dp.message(F.text == "💬 Profile", StateFilter(None))
async def profile(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        day = datetime.now().date()
        process_user(message.from_user.id, day)
        date_str = get_user_date(message.from_user.id)
        date_format = "%Y-%m-%d"
        date_obj = datetime.strptime(date_str, date_format)
        now = datetime.now()
        delta_days = (now - date_obj).days

        await message.reply(
            f"⚡ Hello, {message.from_user.first_name}!\n📝 It is your profile!\n\n"
            f"📊 Your name: {message.from_user.first_name}\n\n"
            f"📊 Your language: {message.from_user.language_code}\n\n"

            f"😲 You have been using me <b>{delta_days} days</b>! Thanks!", reply_markup=back_Keyboard(), parse_mode=ParseMode.HTML
            
        )

######################################################################################
### ADD-FILMS COMMAND ###

@dp.message(F.text == "♻️ Add Film", StateFilter(None))
async def add_film(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        day = datetime.now().date()
        process_user(message.from_user.id, day)
        await message.reply(
            f"✌ {message.from_user.first_name}\n\n"
            f"🎁 Give me the poster of this film.", reply_markup=back_Keyboard())
        await state.set_state(Users.add_photo)

@dp.message(StateFilter(Users.add_photo))
async def handle_photo(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        photo = message.photo[-1]
        file_id = photo.file_id

        await bot.send_photo(chat_id=admin_id, photo=file_id)

        await message.answer("✌ Good!\n\nActually give me title and description!")
        await state.set_state(Users.add_text)

@dp.message(F.text, StateFilter(Users.add_text))
async def take_film_code(message: types.Message, state: FSMContext):
    await message.answer("🌞 Thanks a lot!\n\n🔜 We'll add your film soon!", reply_markup=back_Keyboard())
    await bot.send_message(chat_id=admin_id, text=f"{message.text}", )


######################################################################################
### LIST OF FILM ###
@dp.message(F.text == "📊 Film libary", StateFilter(None))
async def add_film(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        day = datetime.now().date()
        process_user(message.from_user.id, day)
        answer = take_db(get_all_codes(), 1)
        res_str = ""
        await message.reply(f"✌ {message.from_user.first_name}",reply_markup=back_Keyboard())
        for i in answer:
            res_str += f"⚡ {i["code"]} - {i["headline"]}\n"
        await message.reply(res_str)

######################################################################################
### ADMINS FUNCTION 
######################################################################################

###  ADMIN PANEL
@dp.message(F.text == "$admin panel", StateFilter(None))
async def admin(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        if not (message.from_user.id == admin_id):
            await message.answer("😡 You are not admin!")
        else:
            await message.reply(
                f"⚡ Hello, {message.from_user.username}", reply_markup=admin_Keyboard()
            )

### BAN
@dp.message(F.text == "$ ban", StateFilter(None))
async def ban(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        if not (message.from_user.id == admin_id):
            await message.answer("😡 You are not admin!")
        else:
            await message.reply("🤔 Who do you want to ban by id?", reply_markup=back_Keyboard())
            await state.set_state(Admins.ban)

@dp.message(F.text, StateFilter(Admins.ban))
async def ban(message: types.Message, state: FSMContext):
    if message.text != admin_id:
        if ban_user_by_id(message.text):
            await message.reply("😜 Done!")
        else:
            await message.reply("😡 User not found!")
    else:
        await message.reply("😡 What do you doing!?")
    await state.set_state(None)

### UNBAN
@dp.message(F.text == "$ unban", StateFilter(None))
async def ban(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        if not (message.from_user.id == admin_id):
            await message.answer("😡 You are not admin!")
        else:
            await message.reply("🤔 Who do you want to unban by id?", reply_markup=back_Keyboard())
            await state.set_state(Admins.unban)

@dp.message(F.text, StateFilter(Admins.unban))
async def ban(message: types.Message, state: FSMContext):
    if message.text != admin_id:
        if unban_user_by_id(message.text):
            await message.reply("😜 Done!") 
        else:
            await message.reply("😡 User not found!")
    else:
        await message.reply("😡 What do you doing!?")
    await state.set_state(None)

### ADD FILM
@dp.message(F.text == "$ add film", StateFilter(None))
async def add_film(message: types.Message, state: FSMContext):
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        if not (message.from_user.id == admin_id):
            await message.answer("😡 You are not admin!")
        else:
            await message.reply("🤔 Give me the poster of film.", reply_markup=back_Keyboard())
            await state.set_state(Admins.add_film_poster)

@dp.message(StateFilter(Admins.add_film_poster))
async def handle_photo(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        random_name = ''.join([str(random.randint(0, 9)) for _ in range(24)])
        await bot.download_file(file_path, f"{random_name}.png")

        with open('add_film.log', 'a') as log_file:
            log_file.write(f'{random_name}.png\n')

        await message.reply("✅ Document downloaded to memory and saved to disk successfully!\n\n⚡ Now give me title!")
        await state.set_state(Admins.add_film_headline)
    
@dp.message(StateFilter(Admins.add_film_headline))
async def handle_photo(message: types.Message, state: FSMContext):
    with open('add_film.log', 'a') as log_file:
        log_file.write(f'{message.text}\n')
    await message.reply("😎 Actually give me description to 200 chars!")
    await state.set_state(Admins.add_film_description)

@dp.message(StateFilter(Admins.add_film_description))
async def handle_photo(message: types.Message, state: FSMContext):
    with open('add_film.log', 'a') as log_file:
        log_file.write(f'{message.text}\n')
    await message.reply("😎 Cool! Now I add it to database!")

    with open('add_film.log', 'r') as log_file:
        lines = [log_file.readline().strip() for _ in range(3)]
        poster = lines[0]

    print(lines)

    with open('add_film.log', 'w') as log_file:
        log_file.truncate(0)

    code = int(take_db(get_last_code(), 0)['code'])
    code += 1
    with open(lines[0], 'rb') as img_file:
        img_data = img_file.read()
        image = Image.open(io.BytesIO(img_data))

    if add_db(code, lines[1], lines[2], read_image(f"{poster}")):
        await message.reply("🌞Done it")
        
    else:
        await message.reply("📛 Error!")

    os.remove(f"{poster}.png")

async def main():
    await dp.start_polling(bot)

async def on_startup(dispatcher):
    await bot.delete_webhook() 

if __name__ == "__main__":
    asyncio.run(main())
    