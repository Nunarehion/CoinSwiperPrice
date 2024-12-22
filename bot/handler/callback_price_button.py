from bot.__init__ import *

@bot.callback_query_handler(func=lambda call: call.data.startswith("cash_"))
def price__button_filter(call: CallbackQuery):
    message_id = call.message.message_id
    chat_id    = call.message.chat.id
    
    user_state = user_states[chat_id]
    cash_msg   = user_state.cash[message_id]
    filter_mode = cash_msg.filter_mode
    
    
    keyboard = InlineKeyboardMarkup()
    filter_value = call.data[len("cash_"):]
    
    if filter_value == filter_mode.NEUTRAL:
        filter_mode.set_neutral()
        keyboard.add(InlineKeyboardButton("Позитивный", callback_data='cash_' +  filter_mode.POSITIVE))
        keyboard.add(InlineKeyboardButton("Негативный", callback_data='cash_' + filter_mode.NEGATIVE))
    
    elif filter_value == filter_mode.POSITIVE:
        filter_mode.set_positive()
        # print("позитивный", filter_mode.POSITIVE, filter_mode)
        keyboard.add(InlineKeyboardButton("Нейтральный", callback_data='cash_' + filter_mode.NEUTRAL))
        keyboard.add(InlineKeyboardButton("Негативный", callback_data='cash_' + filter_mode.NEGATIVE))
    elif filter_value == filter_mode.NEGATIVE:
        filter_mode.set_negative()
        # print("негативный", filter_mode.NEGATIVE, filter_mode)
        keyboard.add(InlineKeyboardButton("Нейтральный", callback_data='cash_' + filter_mode.NEUTRAL))
        keyboard.add(InlineKeyboardButton("Позитивный", callback_data='cash_' + filter_mode.POSITIVE))
    
    message =  cash_msg.header
    message += cash_msg.load_cash(user_state)
    bot.answer_callback_query(call.id) 
    bot.edit_message_text(text=message, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML', reply_markup= keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("global_"))
def filter__button_filter(call: CallbackQuery):
    print(call.data)
    callbackGroup = "global_"
    filter_value = call.data[len(callbackGroup):]
    chat_id    = call.message.chat.id
    bot.answer_callback_query(call.id)
    
    if chat_id not in user_states:
        user_states[chat_id] = UserState()
    filter_mode = user_states[chat_id].filter_mode
    if filter_value == filter_mode.NEUTRAL:
        filter_mode.set_neutral()
    elif filter_value == filter_mode.POSITIVE:
        filter_mode.set_positive()
    elif filter_value == filter_mode.NEGATIVE:
        filter_mode.set_negative()
        
    bot.edit_message_text(text=filter_mode.condition, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML', reply_markup= None)

   
@bot.callback_query_handler(func=lambda call: True)
def button_handler(call: CallbackQuery):
    bot.answer_callback_query(call.id) 
    