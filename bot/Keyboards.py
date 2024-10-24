from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить мероприятие', callback_data='add_event')],
    [InlineKeyboardButton(text='Удалить мероприятие', callback_data='del_event')],
    [InlineKeyboardButton(text='Отметить сделанное', callback_data='mark_done')],
    [InlineKeyboardButton(text='Обновить расписание', callback_data='reload')],
    [InlineKeyboardButton(text='Расписание', callback_data='show_schedule'), InlineKeyboardButton(text='О боте', callback_data='help')],
])

com = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Автор', url='https://t.me/Superromaxa')],
    [InlineKeyboardButton(text='На главную', callback_data='start_point')]
])

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='На главную', callback_data='start_point')]
])

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/menu')]
    ], resize_keyboard=True)

delkey = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='delete_yes'), InlineKeyboardButton(text='Нет', callback_data='delete_no')]
])
