from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Menu'),
#                                     ]],
 
 #                                    resize_keyboard=True,
  #                                   input_field_placeholder ='Нажмите на пункт menu ...')


menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ethereum', callback_data='Ethereum')],
    [InlineKeyboardButton(text='Arbitrum', callback_data='Arbitrum')]])