from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from core.utils.states_reception import StateAllRecordings
from core.utils.dbconnect import ReceptionDatabase
from core.utils.color_calendar import create_colormap

router = Router()

@router.callback_query(F.data == 'all_recordings')
async def month_of_colormap(call: CallbackQuery, state: FSMContext):
    await call.message.answer('write number of month you want to see')
    await state.set_state(StateAllRecordings.first_state)
    await call.answer()

@router.message(StateAllRecordings.first_state)
async def get_colormap(msg: Message, state: FSMContext, reception: ReceptionDatabase):
    data, min_date, max_date = await reception.get_reception(msg.text)
    try:
        await create_colormap(data, min_date, max_date)
    except TypeError:
        await msg.answer('there\'re no receptions in this month')
    else:

        img = FSInputFile(path='assets/colormap.png')

        await msg.answer_photo(photo=img, caption='here is map.\n Red dates are 2:00 p.m and blue dates are 11:00 a.m')
        await state.clear()
    
