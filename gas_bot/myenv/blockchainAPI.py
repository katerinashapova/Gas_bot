from config import API_KEY_ETHEREUM, API_KEY_ARBITRUM
import requests

from datetime import datetime


def get_transactions(address, network):
    if network == 'Ethereum':
        api_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY_ETHEREUM}'
    elif network == 'Arbitrum':
        api_url = f'https://api.arbiscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={API_KEY_ARBITRUM}'

    else:
        return None
    

    response = requests.get(api_url)

    #Проверка статуса запроса
    if response.status_code == 200:
        response_json= response.json()
  

        
        # Проверка наличия ключей и успешности запроса
        if 'result' in response_json and response_json['status'] == '1':
            return response_json['result']
        else:
            print("Error in API response:", response_json.get('message', 'Unknown error'))
            return None
    else:
        print(f"Error: API request failed with status {response.status_code}")
        return None
    

def get_historical_eth_price(timestamp):
    date = date = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y')
    url = f'https://api.coingecko.com/api/v3/coins/ethereum/history?date={date}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'market_data' in data:
            return data['market_data']['current_price']['usd']
    return None    



def calculate_gas_spent(transactions):
    total_gas = 0
    total_usd_execution_rate = 0
    total_gas_for_execution_rate = 0

    
    max_tx = None
    min_tx = None
    
    for tx in transactions:
        gas_used = int(tx['gasUsed'])
        gas_price = int(tx['gasPrice'])
        gas_eth = gas_used * gas_price / 1e18
        
        total_gas += gas_eth
        
        eth_price_at_execution = get_historical_eth_price(int(tx['timeStamp']))
        if eth_price_at_execution:
            gas_usd = gas_eth * eth_price_at_execution
            total_usd_execution_rate += gas_usd
            total_gas_for_execution_rate += gas_eth
        
        # Определяем самые дорогие и дешевые транзакции
        if max_tx is None or gas_eth > int(max_tx['gasUsed']) * int(max_tx['gasPrice']) / 1e18:
            max_tx = tx
        if min_tx is None or gas_eth < int(min_tx['gasUsed']) * int(min_tx['gasPrice']) / 1e18:
            min_tx = tx

    # Средний курс исполнения 
    if total_gas_for_execution_rate > 0:
        average_execution_rate = total_usd_execution_rate / total_gas_for_execution_rate
    else:
        average_execution_rate = 0

    return total_gas, average_execution_rate, max_tx, min_tx


def get_current_rate(network):
    if network == 'Ethereum':
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    elif network == 'Arbitrum':
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=arbitrum&vs_currencies=usd')
    else:
        return 0
    
    if response.status_code == 200:
        response_json = response.json()
        if network.lower() in response_json and 'usd' in response_json[network.lower()]:
            return response_json[network.lower()]['usd']
        else:
            print(f"Error: {network} rate not found in API response.")
            return 0
    else:
        print(f"Error: API request failed with status {response.status_code}")
        return 0
    

def format_output(address, network, total_gas, max_tx, min_tx, current_rate, execution_rate, transactions):
    max_gas_eth = int(max_tx['gasUsed']) * int(max_tx['gasPrice']) / 1e18
    min_gas_eth = int(min_tx['gasUsed']) * int(min_tx['gasPrice']) / 1e18
    
    output = f"""
    Суммарно затраченный газ ({network})
    Адрес: {address}
    ▪️ В нативной монете: {total_gas:.4f} ETH
    ▪️ По текущему курсу: ${total_gas * current_rate:.2f}
    ▪️ По курсу исполнения: ${total_gas * execution_rate:.8f}

    
    Самая дорогая транзакция: {max_gas_eth:.6f} ETH)
    Самая дешевая транзакция: {min_gas_eth:.6f} ETH)

    Обработано транзакций: {len(transactions)}
    """
    
    return output

#def main(address, network):
 #   transactions = get_transactions(address, network)
  #  if transactions is None:
   #     return "Ошибка при получении транзакций."
    
    
    #total_gas, max_tx, min_tx = calculate_gas_spent(transactions)
    #current_rate = get_current_rate(network)
    
    #if not max_tx or not min_tx:
     #   return "Ошибка при обработке транзакций."
    
    #return format_output(address, network, total_gas, max_tx, min_tx, current_rate)


        

