from aiogram import types

def start_Keyboard():
    kb = [
        [types.KeyboardButton(text="📚 Films"),
         types.KeyboardButton(text="💬 Profile"),
        types.KeyboardButton(text="♻️ Add Film")],
        [types.KeyboardButton(text="📊 Film libary")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def admin_Keyboard():
    kb = [
        [types.KeyboardButton(text="$ ban"),
         types.KeyboardButton(text="$ unban")],
        [types.KeyboardButton(text="$ add film")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def back_Keyboard():
    kb = [
        [types.KeyboardButton(text="Back ⏪")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    return keyboard