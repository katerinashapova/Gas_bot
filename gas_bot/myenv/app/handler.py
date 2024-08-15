from aiogram import F, Router 
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



import app.keyboard as kb

from blockchainAPI import get_transactions, calculate_gas_spent, get_current_rate, format_output

router = Router()

class WalletStates(StatesGroup):
    awaiting_eth_address = State()
    awaiting_arbitrum_address = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Наш бот посчитает сколько вы потратили на комиссии в разных сетях' )
    await message.reply('Введите /menu для выбора сети и проверки завтрат на газ')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Чем я могу Вам помочь? Введите /menu для выбора сети')


@router.message(Command('menu'))
async def cmd_menu(message:Message):
    await message.answer('Это меню Gas_calculate_bot.\nЗдесь вы можете выбрать интерисующую вас сеть и проверить сумму затраченного газа в ней.', reply_markup=kb.menu)


@router.message(F.text == 'Menu')
async def menu (message: Message):
    await message.answer('Выберите сеть с представленных ниже', reply_markup=kb.menu)

@router.callback_query(F.data == "Ethereum")
async def ethereum (callback:CallbackQuery, state: FSMContext):
    await callback.answer('Вышлите номер кошелька, выбранной сети Ethereum')
    await callback.message.answer('Вышлите номер кошелька, выбранной сети Ethereum') 
    await state.set_state(WalletStates.awaiting_eth_address)


@router.callback_query(F.data == "Arbitrum")
async def arbitrum (callback:CallbackQuery, state:FSMContext):
    await callback.answer('Вышлите номер кошелька, выбранной сети Arbitrum')
    await callback.message.answer('Вышлите номер кошелька, выбранной сети Arbitrum') 
    await state.set_state(WalletStates.awaiting_arbitrum_address)


@router.message(WalletStates.awaiting_eth_address)
async def handle_eth_wallet(message:Message, state:FSMContext):
    address = message.text
    await calculate_gas_and_send_result(message, address, 'Ethereum')
    await state.clear()


@router.message(WalletStates.awaiting_arbitrum_address)
async def handle_arbitrum_wallet(message:Message, state:FSMContext):
    address = message.text
    await calculate_gas_and_send_result(message, address, 'Arbitrum')
    await state.clear()




async def calculate_gas_and_send_result(message:Message, address:'str',network:str):
    await message.answer(f'Получаю данные по адресу{address} в сети {network}...')
   

    transactions = get_transactions(address, network)
    if transactions:
        total_gas, average_execution_rate, max_tx, min_tx = calculate_gas_spent(transactions)
        current_rate = get_current_rate(network)
        total_usd_current_rate = total_gas * current_rate
        total_usd_execution_rate = total_gas * average_execution_rate

        if max_tx and min_tx:
            max_gas_eth = int(max_tx['gasUsed']) * int(max_tx['gasPrice']) / 1e18
            min_gas_eth = int(min_tx['gasUsed']) * int(min_tx['gasPrice']) / 1e18
            
            await message.answer(
                f"*Суммарно затраченный газ \\({network}\\):*\n"
                f"Адрес: `{address}`\n"
                f"▪️ *В нативной монете:* `{total_gas:.4f} ETH`\n"
                f"▪️ *По текущему курсу:* `\\${total_usd_current_rate:.2f}`\n"
                f"▪️ *По курсу исполнения:* `\\${total_usd_execution_rate:.2f}`\n"
                '\n'
                f"▪️ *Самая дорогая транзакция:* `{max_gas_eth:.6f} ETH`\n"
                f"▪️ *Самая дешевая транзакция:* `{min_gas_eth:.6f} ETH`\n"
                '\n'
                f"*Обработано транзакций:* `{len(transactions)}`",
                parse_mode="MarkdownV2"
            )
                #f"Суммарно затраченный газ ({network}):\n"
                #f"Адрес: {address}\n"
                #f"▪️ В нативной монете: {total_gas:.4f} ETH\n"
                #f"▪️ По текущему курсу: ${total_usd_current_rate:.2f}\n"
                #f"▪️ По курсу исполнения: ${total_usd_execution_rate:.2f}\n"
                #'\n'
                #f"▪️ Самая дорогая транзакция: {max_gas_eth:.6f} ETH)\n"
                #f"▪️ Самая дешевая транзакция: {min_gas_eth:.6f} ETH)\n"
                #'\n'
                #f"Обработано транзакций: {len(transactions)}"
                #)
        else:
            await message.answer("Не удалось найти данные по транзакциям.")
    else:
        await message.answer("Не удалось получить данные по этому адресу. Проверьте корректность введенного адреса.")







            #await message.answer(
               # f"Суммарно затраченный газ ({network}):\n"
                #f"Адрес: {address}\n"
                #f"▪️ В нативной монете: {total_gas:.8f} ETH\n"
                #f"▪️ По текущему курсу: ${total_usd:.2f}\n"
                #f"▪️ Самая дорогая транзакция: {max_gas_eth:.8f} ETH (https://arbiscan.io/tx/{max_tx['hash']})\n"
                #f"▪️ Самая дешевая транзакция: {min_gas_eth:.8f} ETH (https://arbiscan.io/tx/{min_tx['hash']})\n"
                #f"Обработано транзакций: {len(transactions)}"
           # )
       # else:
        #    await message.answer("Не удалось найти данные по транзакциям.")
    #else:
     #   await message.answer("Не удалось получить данные по этому адресу. Проверьте корректность введенного адреса.")  



                