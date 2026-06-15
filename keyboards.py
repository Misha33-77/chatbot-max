from maxapi.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import SERVICES, AVAILABLE_DATES, AVAILABLE_TIMES, format_date

def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='📋 Записаться на услугу',
                             callback_data='start_booking')
    ]])

def services_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=s['name'], callback_data=f"service:{s['id']}")]
        for s in SERVICES
    ]
    buttons.append([InlineKeyboardButton(text='◀ Назад', callback_data='back_to_start')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def dates_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=format_date(d), callback_data=f"date:{d}")]
        for d in AVAILABLE_DATES
    ]
    buttons.append([InlineKeyboardButton(text='◀ Назад', callback_data='back_to_services')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def times_keyboard() -> InlineKeyboardMarkup:
    # Формируем кнопки по 3 в ряд
    rows = []
    row = []
    for i, t in enumerate(AVAILABLE_TIMES):
        row.append(InlineKeyboardButton(text=t, callback_data=f"time:{t}"))
        if (i + 1) % 3 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text='◀ Назад', callback_data='back_to_dates')])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Подтвердить запись', callback_data='confirm')],
        [InlineKeyboardButton(text='❌ Отменить',           callback_data='cancel')],
    ])