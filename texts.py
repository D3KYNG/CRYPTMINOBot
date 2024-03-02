def start_text():
    return """  Welcome to our CRYPTMINO platform! 🎉
We are excited to have you on board and provide you with the best crypto packages in the market. 💰

With our bot, you can purchase packages that offer different profitability rates for one to three months. Our goal is to make investing in cryptocurrency easy and accessible for everyone. 💻

We pride ourselves on providing secure and reliable services to our users. Your money is safe with us. 💪

Thank you for choosing our bot and we look forward to helping you grow your investments. 🚀
    """

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def user_info_new(first_name):
    return f"""Welcome to our bot, {first_name}!

To get started with our services, please create an account by entering your email. By creating an account, you agree to our policies.

We look forward to providing you with a seamless and secure experience.
    """

def user_info_existed(first_name, email, email_status, available_amount,
                            total_amount, daily_profit, activated_packages, 
                            tx_hash_successfully_deposit, tx_hash_pending_deposit, 
                            tx_hash_failed_deposit, 
                            wallet, withdraw_request, withdraw_amount, tx_hash_successfully_withdraw, txt_remaining_day):
    
    text = f"""Hello {first_name}!
Please note that once you have confirmed your withdrawal request, or you have some transaction pending on the list, you won't be able to change your wallet. However, you can always modify your information at any other time.

Here's an overview of your account:
    
🔹 Email address: {email} {email_status}
🔹 Available amount: {available_amount} 💰
🔹 Total amount: {total_amount} 💵 \n"""
    if daily_profit:
        text += f"""🔹 Daily profit from activated packages: {daily_profit} 📈\n"""
    # if len(activated_packages) > 2:
    #     text += f"""🔹 Activated packages: {activated_packages}\n"""
    if txt_remaining_day != "":# this has the name and the time of the package
        text += f"""🔹 Remaining days for activated packages: \n{txt_remaining_day}\n"""
    if withdraw_request:
        text += f"""🔹 Withdraw amount: {withdraw_amount} USDT 💸\n"""
    if tx_hash_successfully_withdraw:
        text += f"""🔹 Latest withdraw request status: {tx_hash_successfully_withdraw} ✅\n"""
    if tx_hash_successfully_deposit: 
        text += f"""🔹 Deposited TX hashes: {tx_hash_successfully_deposit} ✅\n"""
    if tx_hash_pending_deposit:
        text += f"""🔹 Pending TX hashes: {tx_hash_pending_deposit} 🕐\n"""
    if tx_hash_failed_deposit:
        text += f"""🔹 Failed TX hashes: {tx_hash_failed_deposit} 🚫\n"""
    if wallet:
        text += f"""🔹 Wallet for withdraw: {wallet} 💼\n"""
    # else:
    #     text += """you currently have no TX hash and packages in your account! \n"""
    text += "Please let us know if you have any questions or concerns. Thank you for choosing our services!"
    return text

def enter_email():
    return """Please provide a valid email address: You can use the /empty command to cancel the sign-up process."""

def email_edit():
    return """⚠️ WARNING: If you change your email, your email status will expire, and you won't be able to use our services until you authorize again. Please enter a valid email address. You can use the /empty command to cancel the sign-up process."""
    
def enter_newemail(msg):
    return f"""Congratulations! {msg}. You are now a member of CRYPTMINO! 🎉
To complete your profile, please click on the "User Profile" button. From there, you can fill out the rest of your information.
To explore our services, please click on the "Main Menu" button to see all of your options. Enjoy! 😊"""

def enter_wrong_email(msg):
    return f"""Sorry, It looks like there was an error while saving your Email. Please make sure you have entered a valid Email and try again. If the issue persists, please contact our support team. The server message is: {msg}. You can use the /empty command to cancel the process."""
def enter_email_edit():
    return """Great! Your email has been successfully updated. Please note that you need to re-authorize your email for further services. Thank you for choosing our bot!"""
def handle_cancel_email():
    return """Process canceled. If you'd like to try again later, you can always type /start to restart the sign-up process. """

def enter_tx_add():
    return """Please enter a valid transaction hash. Your transaction will be in a pending state until it is accepted or rejected. If you want to cancel the process, You can use the /empty command to cancel the process."""
def handle_cancel_tx_add():
    return """Process canceled. If you'd like to try again later, you can always type /start to restart the sign-up process. """
def handle_tx_add(msg):
    return """Thank you for submitting your transaction hash. We have received it and it is currently under review. Once it is approved, your available amount will be increased accordingly. We appreciate your trust in us and thank you for using our services."""
def enter_wrong_tx(msg):
    return f"""Sorry, It looks like there was an error while saving your TX hash. Please make sure you have entered a valid hash and try again. If the issue persists, please contact our support team. The server message is: {msg}. You can use the /empty command to cancel the process."""

def enter_wallet():
    return """Please enter your TRC20 USDT wallet address carefully. WARNING: Make sure to double-check your wallet address to avoid any errors. This wallet should be the same as the wallet you are depositing for us. You can use the /empty command to cancel the process."""
def handle_cancel_wallet():
    return """Process canceled. If you'd like to try again later, you can always type /start to restart the sign-up process. """
def handle_wallet(msg):
    return """Thank you for providing your wallet address. You can now proceed with deposit and withdraw requests."""
def enter_wrong_wallet(msg):
     return f"""Sorry, It looks like there was an error while saving your Wallet. Please make sure you have entered a valid TRC20 USDT wallet and try again. If the issue persists, please contact our support team. The server message is: {msg}.\n You can use the /empty command to cancel the process."""

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def packages_main_page(chat_id, available_amount):
    return f""" 👋 Welcome! Your current available amount is {available_amount}.

Please note that our packages are designed for a one-month period and by purchasing a package, you agree that your package funds will be locked for one month.

Here are our available packages with their corresponding monthly percentage rates:

🔹 Bronze I ≈ $30 with 50% daily profitability
🔹 Bronze II ≈ $60 with 100% daily profitability
🔹 Silver I ≈ $100 with 150% daily profitability
🔹 Silver II ≈ $200 with 200% daily profitability
🔹 Gold ≈ $350 with 250% daily profitability
🔹 Platinum ≈ $500 with 300% daily profitability
🔹 Diamond ≈ $750 with 350% daily profitability
🔹 Master ≈ $1000 with 400% daily profitability

Invest in any of our packages to enjoy great returns on your investment! 💰
    """

def packages_new_user_main_page():
    return """ you cuurencly have no account 
Please note that our packages are designed for a one-month period and by purchasing a package, you agree that your package funds will be locked for one month.

Here are our available packages with their corresponding monthly percentage rates:

🔹 Bronze I ≈ $30 with 50% daily profitability
🔹 Bronze II ≈ $60 with 100% daily profitability
🔹 Silver I ≈ $100 with 150% daily profitability
🔹 Silver II ≈ $200 with 200% daily profitability
🔹 Gold ≈ $350 with 250% daily profitability
🔹 Platinum ≈ $500 with 300% daily profitability
🔹 Diamond ≈ $750 with 350% daily profitability
🔹 Master ≈ $1000 with 400% daily profitability

Invest in any of our packages to enjoy great returns on your investment! 💰
    """

def same_package_error(package):
    return f"The same package cannot be bought twice.(You already have {package}) Please wait until the current package expires.(You can check this out in /user_profile)"

def bronze_I_purchasing(available_amount, purchase_differences):
    if available_amount < 30: #this means user can not affortd the package
        return f""" You need to deposit ${purchase_differences} more to buy your target package. Your choice is 🥉 bronze I which will cost 30 💰(USDT) + fee(1 💰) = 31 💰 USDT.

You can deposit right here and return to this page to buy the package. 💳
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""After purchasing this package, you will have {purchase_differences} in your available amount.
By confirming this process, you accept our policy:
        """

def bronze_II_purchasing(available_amount, purchase_differences):
    if available_amount < 61: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 60(USDT) + fee(1 USDT) = 61 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """

def silver_I_purchasing(available_amount, purchase_differences):
    if available_amount < 101: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 100(USDT) + fee(1 USDT) = 101 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """

def silver_II_purchasing(available_amount, purchase_differences):
    if available_amount < 201: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 200(USDT) + fee(1 USDT) = 201 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """
    
def gold_purchasing(available_amount, purchase_differences):
    if available_amount < 351: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 350(USDT) + fee(1 USDT) = 351 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """
    
def platinum_purchasing(available_amount, purchase_differences):
    if available_amount < 501: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 500(USDT) + fee(1 USDT) = 501 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """
    
def diamond_purchasing(available_amount, purchase_differences):
    if available_amount < 751: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 750(USDT) + fee(1 USDT) = 751 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """
    
def master_purchasing(available_amount, purchase_differences):
    if available_amount < 1001: #this means user can not affort the package
        return f""" you need to deposite ${purchase_differences} more to buy your target package
        your choice is bronze I which will cost 1000(USDT) + fee(1 USDT) = 1001 USDT
        you can deposit right here and return to this page to buy the package.
        """
    else:  #purchase_differences is updated available_amount and this means user can affort
        return f"""after purchasing this package you will have {purchase_differences} in your available amount
        by confirming this proccess, you will accept our policy:
        """

def successfully_purchased():
    return """ successfully purchased the package.
    you can see your daily profit and time remaining of your package. 
    we are very glad that you are a major part of our investors.❤️
    """

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def deposit(available_amount, TX_hash_pending_deposit, wallet):
    text = f""" Your current availabe amount is {available_amount}\n"""
    if TX_hash_pending_deposit:
        text += f"""Your perivous TX is still pending. (TX = {TX_hash_pending_deposit})\n"""
    if not wallet:
        text += """You don't have set your wallet yet, for safety purposes, you should add the TRC 20 USDT wallet that you are sending USDT to us then, you can have deposit."""
        return text
    text += """Also, here are a summery of our packages:
bronze I = $30 + $1(fee net) = $31
bronze II ≈ $60 + $1(fee net) = $61
silver I ≈ $100 + $1(fee net) = $101
silver II ≈ $200 + $1(fee net) = $201
gold ≈ $350 + $1(fee net) = $351
platinum ≈ $500 + $1(fee net) = $501
diamond ≈ $750 + $1(fee net) = $751
master ≈ $1000 + $1(fee net) = $1001
        choose your package and remeber the amount.
in next page, our wallet will be shown to you.
        """
    return text

def deposit_new_user(available_amount):
    return """please create an account, then you can see the options...    
    """

def company_wallet(wallet):
    return f""" your amount will automatically balance once your Transaction confirmed.
    you can Deposit any amount of money you want but consider that
    The cryptocurrency has its own risks and by sending us money 
    or purchasing packages, you have accepted our policy. 
    We hope nothing bad will happen, and we make money together.
WARNING:
our wallet will constantly change. So every time you want to deposit, please come here and check our wallet.  
    the wallet: ```{wallet}```
    """

def enter_TX_hash_deposit():
    return """please send us a valid TX hash. 
Transaction Hash is a unique 64 characters identifier that is generated whenever a transaction is executed. 
you can copy it from (https://tronscan.org ). 
You can use the /empty command to cancel the process.
    """

def handle_entered_txhash_succ(msg):
    return f""" Your TX hash successfully added. 
        now this TX is on pending mode. once we confirm the 
        transaction, the mode will change to approved.
        server message: {msg}"""

def handle_entered_txhash_rej(msg):
    return f"""fail to save TX hash.
server message:{msg},
please do the proccess again or back to main menu"""

def withdraw_request(available_amount, total_amount,stage):
    text =  f""" your available amount = {available_amount}
    your total amount = {total_amount}
    the differences between total and available 
    means that you have an active package. 
    when the packge time is over, you can 
    withdraw your amount. 
    NOTE: withdraw proccess would take one up to 3 whole days.
    NOTE2: minimum amount for withdraw is $2.
    NOTE3: The network fee is deducted from the amount. 
    NOTE4: during the withdraw process, you can not request again untill the last withdraw is done.
    NOTE5: Please do the levels until end and don't let it go.
    """
    if stage == 2:
        text = f"""You have already a request in due. """
    if stage == 3:
        text += """\n You don't have enough credit to withdraw"""
    if stage == 4:
        text = f"""You have already a request in due. """
    return text

def enter_amount_withdraw():
    return """please enter amount: You can use the /empty command to cancel the process."""

def handle_entered_amount_have_wallet(msg, wallet):
    return f"""({msg})amount stored. you have a wallet ({wallet}). do you want to change it?"""
def handle_entered_wallet():
    return """wallet saved, now let's review one last time."""
def handle_entered_wallet_wrong_entry(msg):
    return f"""Unfortunately, there was an issue on handling your wallet for withdraw. please try again. The server message is : {msg}. you can cancel the process by sending /empty"""

def handle_entered_amount_enter_wallet(msg):
    return f"""({msg})please insert your TRC20 wallet right here: 
         note: Tether TRC20 addresses can be compared to bank account numbers. 
         It consists of random numbers and letters and can be 
         over 26 symbols long. A cryptocurrency address represents 
         a destination in the blockchain."""

def handle_entered_amount_wrong_entry(msg):
    return f"""Unfortunately, there was an issue on handling your amount for withdraw. please try again. The server message is : {msg}. you can cancel the process by sending /empty"""

def handle_entered_amount_cancel():
    return """ you canceled the proccess. you can back to main menu to continue"""

def enter_wallet_withdraw():
    return """please insert your TRC20 USDT wallet. WARNING: we don't take responsible for the wrong wallet. so be carefull with that. You can use the /empty command to cancel the process."""


def confirm_withdraw(balance, withdraw_amount, wallet):
    return f"""Your balance after withdraw:{ballance},
Your withdraw amount requested:{withdraw_amount},
Your Wallet on TRC20 USDT: {wallet}, 
Do you confirm the informations?
"""

def confirmed_withdraw_request(msg):
    return f"""Your request accepted. the proccess would take 1 up to 3 days. However, we are trying to deliver your money as soon as possible.
server message: {msg},
you can /start for further purposes."""

def rejected_withdraw(msg):
    return f"""Unfortunately, there was an issue on requesting withdraw. please try again. The server message is : {msg}. if you think this is non-sense, you can make contact with us."""

def withdraw_request_new_user():
    return """ withdraw is specially for signed up users.
    please create an account first.     
    """

def contact_us():
    return """📞 Here are other ways to contact us!

👨‍💼 The owner is @keyurohit.

💬 You can reach us through our Telegram channel at @channel.

📧 Alternatively, you can contact us via email at gmail@gmail.com.
        """

def privacy_policy(first_name):
    return f""" Dear {first_name}, 

📜 This Policy is a legally binding agreement between you (“you” or “user”) and us. By visiting, accessing or using the Website or Telegram bot, or providing information to us in any other format, you agree to and accept the terms of this Privacy Policy, as amended from time to time, and you consent to the collection and use of information in the manner set out in this Policy. 

🔎 We encourage you to review this Policy carefully and to periodically refer to it so that you understand it and its subsequent changes if any. IF YOU DO NOT AGREE TO THE TERMS OF THIS PRIVACY POLICY, PLEASE STOP USING THE SERVICE IMMEDIATELY AND WHERE RELEVANT UNINSTALL.

📧 In case you have any questions or concerns, please feel free to contact us through any of the following channels:

👉 The owner is @keyurohit.
👉 Our Telegram channel is @channel
👉 You can also reach us via email at gmail@gmail.com

Thank you for your understanding and cooperation.
        """

def help_string():
    return """ 
        /start -> welcome to our bot and let's see the first menu \n
        /user_profile ->
        /contact_us
        /supporter
        /help
        /empty for canceling the proccess.
        """