from aiogram.fsm.state import State, StatesGroup

class WalletStates(StatesGroup):
    awaiting_eth_address = State()
    awaiting_arbitrum_address = State()