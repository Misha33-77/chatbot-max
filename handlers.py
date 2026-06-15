from maxapi import Bot
from maxapi.types import Message, CallbackQuery
from states import States, get_state, set_state
from keyboards import (main_menu_keyboard, services_keyboard,
                        dates_keyboard, times_keyboard, confirm_keyboard)
from data import get_service_by_id, format_date

async def handle_message(bot: Bot, message: Message):
    """Обработчик входящих текстовых сообщений"""
    user_id = message.from_user.user_id
    text = message.text or ''

    if text == '/start':
        set_state(user_id, States.START)
        await bot.send_message(
            chat_id=message.chat.chat_id,
            text=('👋 Добро пожаловать!\n\n'
                  'Я помогу вам записаться на услугу.\n'
                  'Нажмите кнопку ниже, чтобы начать.'),
            reply_markup=main_menu_keyboard()
        )
    else:
        # Неизвестная команда
        await bot.send_message(
            chat_id=message.chat.chat_id,
            text='Используйте кнопки меню или введите /start для начала.',
            reply_markup=main_menu_keyboard()
        )

async def handle_callback(bot: Bot, callback: CallbackQuery):
    """Обработчик нажатий на inline-кнопки"""
    user_id = callback.from_user.user_id
    chat_id = callback.message.chat.chat_id
    data = callback.payload

    # Подтверждаем получение callback (убирает часики на кнопке)
    await bot.answer_callback_query(callback.callback_id)

    # ── Главное меню ──────────────────────────────
    if data == 'start_booking':
        set_state(user_id, States.CHOOSE_SERVICE)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text='🗂 Выберите услугу:',
            reply_markup=services_keyboard()
        )

    # ── Выбор услуги ──────────────────────────────
    elif data.startswith('service:'):
        service_id = data.split(':', 1)[1]
        service = get_service_by_id(service_id)
        if not service:
            return
        set_state(user_id, States.CHOOSE_DATE, service=service_id)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text=(f'✅ Услуга: {service["name"]}\n'
                  f'💰 Стоимость: {service["price"]}\n'
                  f'⏱ Длительность: {service["duration"]}\n\n'
                  '📅 Выберите удобную дату:'),
            reply_markup=dates_keyboard()
        )

    # ── Выбор даты ────────────────────────────────
    elif data.startswith('date:'):
        date = data.split(':', 1)[1]
        state = get_state(user_id)
        service = get_service_by_id(state['service'])
        set_state(user_id, States.CHOOSE_TIME, date=date)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text=(f'✅ Услуга: {service["name"]}\n'
                  f'📅 Дата: {format_date(date)}\n\n'
                  '🕐 Выберите время:'),
            reply_markup=times_keyboard()
        )

    # ── Выбор времени ─────────────────────────────
    elif data.startswith('time:'):
        time = data.split(':', 1)[1]
        state = get_state(user_id)
        service = get_service_by_id(state['service'])
        set_state(user_id, States.CONFIRM, time=time)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text=('📋 Проверьте данные записи:\n\n'
                  f'🔹 Услуга: {service["name"]}\n'
                  f'🔹 Дата: {format_date(state["date"])}\n'
                  f'🔹 Время: {time}\n'
                  f'🔹 Стоимость: {service["price"]}\n\n'
                  'Подтвердить запись?'),
            reply_markup=confirm_keyboard()
        )

    # ── Подтверждение ─────────────────────────────
    elif data == 'confirm':
        state = get_state(user_id)
        service = get_service_by_id(state['service'])
        set_state(user_id, States.START)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text=('🎉 Вы успешно записаны!\n\n'
                  f'✅ Услуга: {service["name"]}\n'
                  f'📅 Дата: {format_date(state["date"])}\n'
                  f'🕐 Время: {state["time"]}\n\n'
                  'Ждём вас! Если нужно изменить запись — введите /start.'),
            reply_markup=None
        )

    # ── Отмена ────────────────────────────────────
    elif data == 'cancel':
        set_state(user_id, States.START)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback.message.message_id,
            text='❌ Запись отменена. Нажмите «Записаться», чтобы начать заново.',
            reply_markup=main_menu_keyboard()
        )

    # ── Навигация назад ───────────────────────────
    elif data == 'back_to_start':
        set_state(user_id, States.START)
        await bot.edit_message_text(
            chat_id=chat_id, message_id=callback.message.message_id,
            text='Нажмите кнопку ниже, чтобы записаться.',
            reply_markup=main_menu_keyboard()
        )

    elif data == 'back_to_services':
        set_state(user_id, States.CHOOSE_SERVICE)
        await bot.edit_message_text(
            chat_id=chat_id, message_id=callback.message.message_id,
            text='🗂 Выберите услугу:',
            reply_markup=services_keyboard()
        )

    elif data == 'back_to_dates':
        state = get_state(user_id)
        service = get_service_by_id(state['service'])
        set_state(user_id, States.CHOOSE_DATE)
        await bot.edit_message_text(
            chat_id=chat_id, message_id=callback.message.message_id,
            text=(f'✅ Услуга: {service["name"]}\n\n📅 Выберите дату:'),
            reply_markup=dates_keyboard()
        )