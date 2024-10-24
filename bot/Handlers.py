from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import bot.Keyboards as kb
from HIDden import HELP

router = Router()

class UsersSchedule: #Класс для сохранения расписания пользователей
    def __init__(self):
        self.schedules = {}

    def addevent(self, user, event, time):
        if user not in self.schedules:
            self.schedules[user] = {}
        if event not in self.schedules[user]:
            self.schedules[user][event] = []
        self.schedules[user][event].append(time)
        return event

    def get_schedule(self, user):
        return self.schedules.get(user, [])

    def del_schedule(self, user, event):
        e = self.schedules[user].pop(event, 'Такого мероприятия нет')
        return e

    def mark_done(self, user, event):
        if user in self.schedules:
            if event in self.schedules[user]:
                if self.schedules[user][event][-1] != "\u2705":
                    self.schedules[user][event].append("\u2705")
                return 'Done'
            else:
                return 'No event'
        else:
            return 'No user'

    def isin(self, user, event):
        if event in self.schedules[user]:
            return True
        else:
            return False

    def reload(self, user):
        if user in self.schedules:
            events_to_del = []
            for eve in self.schedules[user]:
                if self.schedules[user][eve][-1] == '\u2705':
                    events_to_del.append(eve)
            for event in events_to_del:
                self.del_schedule(user, event)
sch_manager = UsersSchedule()

class InputState(StatesGroup): #Класс для получения расписания от пользователя
    waiting_event = State()
    waiting_time = State()
class DeletingState(StatesGroup):
    deleting_event = State()
class MarkingState(StatesGroup):
    marking_event = State()


@router.callback_query(F.data == 'add_event') #Метод добавляет мероприятие в список. В этой части начинается метод
async def add_eve_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Пожалуйста, введите название для мероприятия:")
    await state.set_state(InputState.waiting_event)

@router.message(InputState.waiting_event) #Продолжение метода. Получение названия мероприятия
async def add_eve_event(message: Message, state: FSMContext):
    event = message.text
    await state.update_data(event = event)
    await message.answer("Теперь укажите время мероприятия:")
    await state.set_state(InputState.waiting_time)

@router.message(InputState.waiting_time) #Продолжение метода. Получение времени и сохранение
async def add_eve_time(message: Message, state: FSMContext):
    time = message.text
    userid = message.from_user.id
    eve = await state.get_data()
    event = eve.get('event')

    res = sch_manager.addevent(userid, event, time)
    await message.answer('Мероприятие ' + res + ' успешно добавлено!', reply_markup=kb.main)
    await state.clear()

@router.callback_query(F.data == 'show_schedule') #Метод показывает все записанные мероприятия пользователя
async def show_sch(callback: CallbackQuery):
    userid = callback.from_user.id
    total_schedule = sch_manager.get_schedule(userid)
    schedule = []
    for ev in total_schedule:
        time = ' '.join(total_schedule[ev])
        s = str(ev) + ' - ' + time
        schedule.append(s)
    await callback.answer()
    if schedule:
        await callback.message.edit_text("Ваше расписание:\n" + '\n'.join(schedule), reply_markup=kb.main)
    else:
        await callback.message.edit_text("В Вашем расписании нет мероприятий", reply_markup=kb.main)

@router.callback_query(F.data == 'mark_done') #Метод отмечает мероприятие как сделанное
async def mark_event_done(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Какое мероприятие Вы хотите отметить?')
    await state.set_state(MarkingState.marking_event)

@router.message(MarkingState.marking_event) #Продолжение метода
async def marking_event_done(message: Message, state: FSMContext):
    event = message.text
    userid =  message.from_user.id
    res = sch_manager.mark_done(userid, event)
    await state.clear()
    if res == 'Done':
        await message.answer('Мероприятие ' + event + ' успешно отмечено!', reply_markup=kb.main)
    elif res == 'No event':
        await message.answer('К сожалению, в Вашем расписании нет мероприятия ' + event, reply_markup=kb.main)
    else:
        await message.answer("В Вашем расписании нет мероприятий", reply_markup=kb.main)

@router.callback_query(F.data == 'del_event') #Удаление мероприятия
async def delete_event(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Какое мероприятие Вы хотите удалить?')
    await state.set_state(DeletingState.deleting_event)

@router.message(DeletingState.deleting_event) #Уточнение по поводу удаления
async def deleting_event(message: Message, state: FSMContext):
    event = message.text
    userid = message.from_user.id
    res = sch_manager.isin(userid, event)
    if res:
        await state.update_data(event=event)
        await message.answer('Вы действительно хотите удалить мероприятие ' + event + '?', reply_markup=kb.delkey)
    else:
        await message.answer('К сожалению, в Вашем расписании нет мероприятия ' + event, reply_markup=kb.main)

@router.callback_query(F.data == 'delete_yes')
async def final_delete(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()  # Получаем данные из состояния
    event = user_data.get('event')
    await state.clear()
    userid = callback.from_user.id
    _ = sch_manager.del_schedule(userid, event)
    await callback.answer('Мероприятие успешно удалено!', show_alert=True)
    await callback.message.answer(event + ' удалено', reply_markup=kb.main)

@router.callback_query(F.data == 'delete_no')
async def cancel_delete(callback: CallbackQuery):
    await callback.answer('Отмена удаления')
    await callback.message.answer('Хорошо, не буду удалять это мероприятие', reply_markup=kb.main)

@router.message(CommandStart()) #Ответ на первую команду старт
async def cmd_start(message: Message):
    await message.answer('Привет, ' + message.from_user.first_name + '!', reply_markup=kb.menu)
    await message.answer('Выберите команду:', reply_markup=kb.key)

@router.callback_query(F.data == 'help') #Метод рассказывает о том, для чего создан этот бот и что он умеет
async def about_bot(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(HELP, reply_markup=kb.com)

@router.callback_query(F.data == 'start_point') #Метод возвращает бота к начальной странице
async def to_start(callback: CallbackQuery):
    await callback.answer('Главная страница')
    await callback.message.edit_text('Выберите команду:', reply_markup=kb.key)

@router.message(F.text == 'Как дела?') #Можно немного пообщаться с ботом
async def how_are_you(message: Message):
    await message.answer("У меня все хорошо!", reply_markup=kb.menu)

@router.message(Command('menu')) #Команда всегда присутствует в блоке под чатом, если нужно вернуться к командам
async def ret_menu(message: Message):
    await message.answer('Выберите команду:', reply_markup=kb.key)

@router.callback_query(F.data == 'reload')
async def reload(callback: CallbackQuery):
    userid = callback.from_user.id
    sch_manager.reload(userid)
    await callback.answer('Расписание обновлено!', show_alert=True)

@router.message(lambda message: not message.text.startswith('/'))
async def non_com(message: Message):
    name = message.from_user.first_name
    await message.answer('Привет, ' + name + '!\nК сожалкнию, я не понимаю сообщений(\nИспользуй, пожалуйста, команды', reply_markup=kb.key)