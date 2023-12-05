from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from core.utils.states_reception import StateCancelReception
from core.keyboards.reception_keyboard import reception_keyboard, end_cancel_reception_keyboard
from core.utils.dbconnect import ReceptionDatabase

from calendar import monthrange
from datetime import datetime

router = Router()

@router.callback_query(F.data == 'cancel_reception')
async def reception(call: CallbackQuery, state: FSMContext):
    await call.message.answer('write number of month you want to cancel the reception')
    await state.set_state(StateCancelReception.first_state)
    
    await call.answer()

@router.message(StateCancelReception.first_state)
async def choose_month(msg: Message, state: FSMContext):
    try:
        if datetime.now().month > int(msg.text):
            current_year = datetime.now().year + 1
        else:
            current_year = datetime.now().year

        days_of_month = monthrange(current_year, int(msg.text))[1]

        await state.update_data(month=int(msg.text))
        await state.update_data(year=int(current_year))
        await msg.answer(f'choose day within {days_of_month} days of month. The same way')
        await state.set_state(StateCancelReception.second_state)
    except:
        await msg.answer(f'{msg.text} is not month')

@router.message(StateCancelReception.second_state)
async def choose_day(msg: Message, state: FSMContext):
    await state.update_data(day=int(msg.text))
    await state.set_state(StateCancelReception.third_state)
    await msg.answer('What\'s hour to cancel. \n You can choose between 11:00 a.m and 02:00 p.m.', reply_markup=reception_keyboard)

@router.message(StateCancelReception.third_state, F.text.casefold() == '11:00 a.m')
async def hour_01(msg: Message, state: FSMContext):
    await state.update_data(hour=msg.text)
    data = await state.get_data()
    month = data.get('month')
    day = data.get('day')
    hour = msg.text
    await state.set_state(StateCancelReception.four_state)
    await msg.answer(f'month: {month} \n your day: {day} \n your hour: {hour}. It\'s correct?', reply_markup=end_cancel_reception_keyboard)

@router.message(StateCancelReception.third_state, F.text.casefold() == '02:00 p.m')
async def hour_02(msg: Message, state: FSMContext):
    await state.update_data(hour=msg.text)
    data = await state.get_data()
    month = data.get('month')
    day = data.get('day')
    hour = msg.text
    await state.set_state(StateCancelReception.four_state)
    await msg.answer(f'month: {month} \n your day: {day} \n your hour: {hour}. It\'s correct?', reply_markup=end_cancel_reception_keyboard)

@router.message(StateCancelReception.four_state, F.text.casefold() == 'yes')
async def ending1_of_reception(msg: Message, state: FSMContext, reception: ReceptionDatabase):
    data = await state.get_data()
    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    hour = data.get('hour')
    try:
        date = datetime(year, month, day, int(hour.split(':')[0]))
    except ValueError:
        await msg.answer('day is out of range for month', reply_markup=ReplyKeyboardRemove())
    else:
        if month//10 == 0: x=0 
        else: x='' 
        
        try:
            await reception.cancel_reception(datetime=date, user_id=msg.from_user.id)
        except Exception:
            await msg.answer(f'you haven\'t reception on {x}{month}.{day} {hour}', reply_markup=ReplyKeyboardRemove())
        else:
            await msg.answer('you canceled reception now', reply_markup=ReplyKeyboardRemove())
    
    await state.clear()

@router.message(StateCancelReception.four_state, F.text.casefold() == 'no')
async def ending2_of_reception(msg: Message, state: FSMContext):
    await msg.answer('ok', reply_markup=ReplyKeyboardRemove())
    await state.clear()