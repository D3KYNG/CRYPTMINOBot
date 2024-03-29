from datetime import datetime
import time
import requests
from requests.exceptions import RequestException

# Define the USDT contract address on TRON network
usdt_contract = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

# Define the base URL for TRONSCAN API
base_url = "https://apilist.tronscan.org/api"
    
def get_tx_info(tx_hash, wallet_customer, wallet_bugs):
    try: 
        # Get the transaction details by hash
        tx_url = base_url + "/transaction-info?hash=" + tx_hash
        tx_response = requests.get(tx_url)

        # Check if the response status code is 200
        if tx_response. status_code != 200:
            return {'status': False, 'msg': f"Error: Received non-200 status code: {tx_response.status_code}"}

        # Check if the content type is application/json
        if not tx_response.headers["content-type"].strip().startswith("application/json"):
            return {'status': False, 'msg': "Error: Received non-JSON content type"}

        tx_data = tx_response.json()
        
        if not tx_data["contractRet"] == "SUCCESS":
            return {'status': False, 'msg': "The transaction didn't complete curractly(FAILED)."}
        
        confirmations = tx_data["confirmations"]
        min_confirmations = 20 # Change this to your desired number
        if confirmations < min_confirmations or not tx_data["confirmed"]:
            return {'status': False, 'msg': "Warning: The transaction is not confirmed by enough blocks."}
        
        sender = tx_data["ownerAddress"]
        if not wallet_customer == sender:
            return {'status': False, 'msg': "The sender of the amount is not authrized. please double check the TX"}

        receiver = tx_data['trc20TransferInfo'][0]['to_address']
        if not receiver == wallet_bugs:
            return {'status': False, 'msg': "The reciever wallet doesn't belong to us. Please double-check the TX."}
        
        contract_type = tx_data["contract_type"]
        if not contract_type == "trc20":
            return {'status': False, 'msg': "The format of the TX is not trc20. Please double-check the TX."}
        
        revert = tx_data["revert"]
        if revert == True:
            return {'status': False, 'msg': "revert happened. probably your money will come back to your wallet."}
        # below here is accepted tx.
        time_TX = tx_data["timestamp"]
        timestamp = time_TX / 1000
        now = time.time()
        now = (now // 60) * 60
        time_difference = now - time_TX
        if time_difference >600:
            return {'status': False, 'msg': "Your submission time for the TX hash has expired. However, you can contact our support team for further information and assistance."}
        
        date_time = datetime.fromtimestamp(timestamp)
        # Get the amount of USDT transferred (in sun, need to divide by 10**6)
        amount = float(tx_data["trigger_info"]["parameter"]["_value"]) / 10**6
        return {'status': True, 'msg': "TX was successfully added", 'time': date_time, 'amount': round(amount, 2)}
        
    except RequestException as e:
        return {'status': False, 'msg': f"Request error: {e}"}
    except Exception as e:
        return {'status': False, 'msg': f"TX checker has error: {e}"}

# Define the transaction hash
# tx_hash = "Your sample"
# wallet_customer = "customer wallet sample"
# wallet_company = "Your wallet"
# print(get_tx_info(tx_hash, wallet_customer, wallet_company))
# # tx_hash = "sample for Transaction hash"
# result = get_tx_info(tx_hash, "customer tx hash", "your wallet tx hash")
# print(result)
# Print the results
        # print(f"Sender: {sender}")
        # print(f"Receiver: {receiver}")
        # print(f"Amount: {amount} USDT")
        # print(f"Status: {status}")
        # print(f"time: {date_time}")
        # print(f"contract_type: {contract_type}")
        # print(f"revert: {revert}")
        # print(f"confirmations: {confirmations}")
        # print(f"Result: The transaction was completed successfully.")