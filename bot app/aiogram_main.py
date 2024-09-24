############################## IMPORTING ##############################
from aiogram_config import token
from aiogram_keyboard import start_Keyboard, back_Keyboard
import asyncio
import logging
from datetime import datetime
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    BufferedInputFile, CallbackQuery, Message
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

import sys
sys.path.append('D:/Kinopoisk project')
from mysql.mysql_main import execute_db 

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

##########################################################################
# STATES

class Users(StatesGroup):
    film = State()
    asking = State()

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
async def back(message: types.Message, state: FSMContext):
    await state.set_state(None)
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")
    else:
        day = datetime.now().date()
        process_user(message.from_user.id, day)

        await message.reply(
            f"👋 {message.from_user.first_name}!\n\n"
            "🌞 Give me the code of film!\n\n",
            reply_markup=back_Keyboard()
        )

@dp.message(F.text, StateFilter(Users.film))
async def userGpt4o(message: types.Message, state: FSMContext):

    await state.set_state(None)
    if get_user_ban_status(message.from_user.id) == True:
        await message.answer("😡 You are banned!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())