TOKEN = open("hidden.txt").readline()
HELP = "Это - бот-расписание. Он умеет создавать расписание для тебя с делами, которые необходимо сделать. Также его можно попросить отметить задание как сделанное или удалить совсем)"
'''@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
    buttons = ['help', 'add_schedule', 'show_schedule']
    keyboard.add(*buttons)
    await message.answer('Привет!', reply_markup=keyboard)'''