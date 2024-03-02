from functools import wraps
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from warnings import filterwarnings
import datetime
from telegram.warnings import PTBUserWarning
import logging
from typing import Final, List
import traceback
from telegram import (InlineKeyboardButton, Update, InlineKeyboardMarkup, 
                      Bot ,ChatMember)
from telegram.ext import (CommandHandler, CommandHandler,CallbackQueryHandler, 
                          MessageHandler, filters, ContextTypes,
                          ConversationHandler, ApplicationBuilder, CallbackContext
                        )

from telegram.error import TimedOut
import texts as msg_texts
# import checker as ch
import wallet as company_wallet_txt
import micro_controller as controller

# Creating a constant variable for TOKEN and BOT_USERNAME
TOKEN: Final = 'Your Token name'
BOT_USERNAME: Final = '@Your username bot in telegram'
SupportChatID: Final = 'Chat-ID in your bot'

"""packages price"""
Bronze_I_price: Final = 30
Bronze_II_price: Final =60
Silver_I_price: Final =100
Silver_II_price: Final =200
Gold_price: Final = 350
Platinum_price: Final = 500
Diamond_price: Final =750
Master_price: Final =1000

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

#Global Varibale -  Stages
START_ROUTES, PACKAGE_ROUT, PURCHASE_ROUT, DEPOSIT_ROUT, USER_PROFILE_ROUT, WITHDRAW_REQUEST_ROUT, ENTER_TXHASH_DEP, ENTER_AMOUNT_WITHD, ENTER_AMOUNT_WITHD_ROUT, ENTER_WALLET_WITHD, AMOUNT_WALLET_CONDIRM_WITHD, ENTER_EMAIL_NEW, ENTER_EDIT_EMAIL, ENTER_TX_ADD, ENTER_WALLET = range(15)

# Callback data
RETS = 0

def log_function(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.callback_query:
            user = update.callback_query.from_user
        else:
            user = update.message.from_user

        logger.info(f"Entering function: {func.__name__} - user: {user}")
        result = await func(update, context, *args, **kwargs)
        # logger.info(f"Exiting function: {func.__name__} - user: {user}")
        return result
    return wrapper

async def delete_messages(context: ContextTypes.DEFAULT_TYPE, chat_id: int, messages_to_delete: List[int]) -> None:
    message_id_not = [1, 2]
    print("deleted2")
    message_id = 2
    
    for message_id in messages_to_delete:
        print("deleted3")
        
        print("deleted")
        await context.bot.deleteMessage(
            message_id=message_id,
            chat_id=chat_id
            )
        message_id += 1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text
    message_id=update.effective_message.message_id 
    chat_id=update.effective_chat.id
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    response: str = handle_response(update.message.chat.id, text)
    print('Bot:', response)
    await update.message.reply_text(response)

def handle_response(chatID, text: str) -> str:
    # Create your own response logic
    if 'hello' in text:
        return 'Hey there!'
    
    # Check if the chat_id matches the Support Chat ID
    chatID = str(chatID)
    if '1' in text and chatID in SupportChatID:
        return 'to use supporter menu, use this command: /supporter'
    
    return 'I don\'t understand'


#page ziro
# commands function /strat /package_picture /user_profile /contact_us /supporter /help 
@log_function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        keyboard = [
            [
                InlineKeyboardButton("Packages", callback_data='1'),
                InlineKeyboardButton("Deposit", callback_data='2'),
            ],
            [
                InlineKeyboardButton("User Profile", callback_data='3'),
                InlineKeyboardButton("Withdraw Request", callback_data='4'),
            ],
            [
                InlineKeyboardButton("Contact Admins", callback_data='5'),
                InlineKeyboardButton("Privacy & policy", callback_data='6'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(msg_texts.start_text(), reply_markup=reply_markup)
        return START_ROUTES

    except Exception as e:
        print(f"Error in start function: {e}")
        traceback.print_exc()  # Print traceback information

# start menu 
@log_function
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        """Prompt same text & keyboard as `start` does but not as new message"""
        # Get CallbackQuery from Update
        query = update.callback_query
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer()
        keyboard = [
            [
                InlineKeyboardButton("Packages", callback_data='1'),
                InlineKeyboardButton("Deposit", callback_data='2'),
            ],
            [
                InlineKeyboardButton("User Profile", callback_data='3'),
                InlineKeyboardButton("Withdraw Request", callback_data='4'),
            ],
            [
                InlineKeyboardButton("Contact Admins", callback_data='5'),
                InlineKeyboardButton("Privacy & policy", callback_data='6'),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Instead of sending a new message, edit the message that
        # originated the CallbackQuery. This gives the feeling of an
        # interactive menu.
        await query.edit_message_text(msg_texts.start_text(), reply_markup=reply_markup)
        return START_ROUTES
    except Exception as e:
        print(f"Error in main menu function: {e}")
        traceback.print_exc()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@log_function
async def packages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        """Show new choice of buttons"""
        chat_id=update.effective_chat.id
        query = update.callback_query
        await query.answer()
        if controller.user_exists(chat_id):
            user_info = controller.read_info(chat_id)
            available_amount = user_info["available_amount"]
            keyboard = [
                [
                    InlineKeyboardButton("bronze I", callback_data='30'),
                    InlineKeyboardButton("bronze II", callback_data='60'),
                ], 
                [
                    InlineKeyboardButton("silver I", callback_data='100'),
                    InlineKeyboardButton("silver II", callback_data='200'),
                ],
                [
                    InlineKeyboardButton("gold", callback_data='350'),
                    InlineKeyboardButton("platinum", callback_data='500'),
                ], 
                [
                    InlineKeyboardButton("diamond", callback_data='750'),
                    InlineKeyboardButton("master", callback_data='1000'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='0'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.packages_main_page(chat_id, available_amount), reply_markup=reply_markup)

        else: 
            keyboard = [
                [
                    InlineKeyboardButton("create an account", callback_data='3'), # it will go to user info page and can create his account
                ],  
                [
                InlineKeyboardButton("Back", callback_data='0'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.packages_new_user_main_page(), reply_markup=reply_markup)
        return PACKAGE_ROUT
    except Exception as e:
        print(f"Error in package function: {e}")
        traceback.print_exc()
 
@log_function
async def bronze_I_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        
        if "Bronze_I" in [pkg[0] for pkg in user_info["activated_packages"]]:
            keyboard = [
                [
                    InlineKeyboardButton("Packages", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.same_package_error("Bronze I"), reply_markup=reply_markup)
            return PURCHASE_ROUT
        
        if available_amount >= Bronze_I_price:
            purchase_differences = available_amount - Bronze_I_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='30'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Bronze_I_price + 1) - available_amount 
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.bronze_I_purchasing(available_amount, purchase_differences),reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in bronze_I_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def bronze_I_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Bronze_I_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in bronze_I_confirm function: {e}")
        traceback.print_exc()

@log_function
async def bronze_II_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Bronze_II_price:
            purchase_differences = available_amount - Bronze_II_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='60'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Bronze_II_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.bronze_II_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in bronze_II_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def bronze_II_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Bronze_I_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in bronze_II_confirm function: {e}")
        traceback.print_exc()

@log_function
async def silver_I_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Silver_I_price:
            purchase_differences = available_amount - Silver_I_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='100'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Silver_I_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.silver_I_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in silver_I_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def silver_I_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Silver_I_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in silver_I_confirm function: {e}")
        traceback.print_exc()

@log_function
async def silver_II_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Silver_II_price:
            purchase_differences = available_amount - Silver_II_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='200'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Silver_II_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.silver_II_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in silver_II_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def silver_II_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Silver_II_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in silver_II_confirm function: {e}")
        traceback.print_exc()

@log_function
async def gold_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Gold_price:
            purchase_differences = available_amount - Gold_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='350'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Gold_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.gold_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in gold_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def gold_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Gold_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in gold_confirm function: {e}")
        traceback.print_exc()

@log_function
async def platinum_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Platinum_price:
            purchase_differences = available_amount - Platinum_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='500'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Platinum_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.platinum_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in platinum_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def platinum_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Platinum_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in platinum_confirm function: {e}")
        traceback.print_exc()

@log_function
async def diamond_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Diamond_price:
            purchase_differences = available_amount - Diamond_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='750'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Diamond_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.diamond_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in diamond_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def diamond_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Diamond_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in diamond_confirm function: {e}")
        traceback.print_exc()

@log_function
async def master_purchasing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        available_amount = user_info["available_amount"]
        if available_amount >= Master_price:
            purchase_differences = available_amount - Master_price
            keyboard = [
                [
                    InlineKeyboardButton("confirm purchase", callback_data='1000'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        else:
            purchase_differences = (Master_price + 1) - available_amount
            keyboard = [
                [
                    InlineKeyboardButton("Deposit", callback_data='2'),
                ], 
                [
                    InlineKeyboardButton("back", callback_data='1')
                ],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg_texts.master_purchasing(available_amount, purchase_differences), reply_markup=reply_markup)
        return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in master_purchasing function: {e}")
        traceback.print_exc()

@log_function
async def master_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        tele_id=update.effective_chat.id
        user_info = controller.read_info(tele_id)
        result = controller.purchase_package(tele_id, user_info, Master_price)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [
                [
                    InlineKeyboardButton("user profile", callback_data='3'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.successfully_purchased(), reply_markup=reply_markup)
            return START_ROUTES
        else: 
            keyboard = [
                [
                    InlineKeyboardButton("try again", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("main menu", callback_data='0')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"somethings happened, please try again the server: {msg}", reply_markup=reply_markup)
            return PURCHASE_ROUT
    except Exception as e:
        print(f"Error in master_confirm function: {e}")
        traceback.print_exc()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@log_function
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        chat_id=update.effective_chat.id
        query = update.callback_query    
        if query:
            await query.answer()
        if controller.user_exists(chat_id):
            #we should read the file, then user can edit 
            user_info = controller.read_info(chat_id)
            available_amount = user_info["available_amount"]
            tx_hash_pending_deposit  = user_info["tx_hash_pending_deposit"]
            wallet = user_info["wallet"]
            if wallet:
                keyboard = [
                    [
                        InlineKeyboardButton("bugs bunny wallet", callback_data='1'),
                    ],            
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if query:
                    await query.edit_message_text(msg_texts.diposit(available_amount, tx_hash_pending_deposit, wallet), reply_markup=reply_markup)
                else:
                    await update.message.reply_text(msg_texts.diposit(available_amount, tx_hash_pending_deposit, wallet), reply_markup=reply_markup)
            else:
                keyboard = [
                    [
                        InlineKeyboardButton("Enter Your Wallet", callback_data='4'),
                    ],            
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if query:
                    await query.edit_message_text(msg_texts.diposit(available_amount, tx_hash_pending_deposit, wallet), reply_markup=reply_markup)
                else:
                    await update.message.reply_text(msg_texts.diposit(available_amount, tx_hash_pending_deposit, wallet), reply_markup=reply_markup)
        else:
            keyboard = [
                [
                    InlineKeyboardButton("create an account", callback_data='3'), # it will go to user info page and can create his account
                ],  
                [
                InlineKeyboardButton("main menu", callback_data='0'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.diposit_new_user(), reply_markup=reply_markup)
        return DEPOSIT_ROUT
    except Exception as e:
        print(f"Error in deposit function: {e}")
        traceback.print_exc()
        
@log_function
async def company_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        # Get the current day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        today = datetime.datetime.today().weekday()
        chat_id=update.effective_chat.id
        query = update.callback_query    
        await query.answer()
        # Call the appropriate function based on the current day
        if today in [5, 6, 0]:
            current_wallet = company_wallet_txt.wallet_N1()
        elif today in [1, 2]:
            current_wallet = company_wallet_txt.wallet_N2()
        else: #[3, 4]
            current_wallet = company_wallet_txt.wallet_N3()

        keyboard = [
            [
                InlineKeyboardButton("entering TX hash", callback_data='2'),
            ],            
            [
                InlineKeyboardButton("main menu", callback_data='0'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # wallet_text = f"```\n{current_wallet}\n```"  # wrap wallet text in code block
        await query.edit_message_text(msg_texts.company_wallet(current_wallet), reply_markup=reply_markup)  # set parse_mode to MarkdownV2 to enable code block formatting
        return DEPOSIT_ROUT
    except Exception as e:
        print(f"Error in company_wallet function: {e}")
        traceback.print_exc()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@log_function
async def user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        if query:
            await query.answer()
            first_name = update.callback_query.from_user.first_name
        else:
            first_name = update.effective_user.first_name
        
        chat_id=update.effective_chat.id
        if not controller.user_exists(chat_id): #new users
            keyboard = [
                [
                    InlineKeyboardButton("Enter Your Email", callback_data='1'),
                ], 
                [
                    InlineKeyboardButton("Main Menu", callback_data='0'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if query:
                await query.edit_message_text(msg_texts.user_info_new(first_name), reply_markup=reply_markup)
            else:
                await update.message.reply_text(msg_texts.user_info_new(first_name), reply_markup=reply_markup)
            return USER_PROFILE_ROUT
        else:#existed users
            user_info = controller.read_info(chat_id)
            email = user_info["email"]
            email_verify_status = user_info["email_verify_status"]
            if email_verify_status == True :
                email_status = "approved ✅"
            else:
                email_status = "not approved 🚫"
            
            available_amount = user_info["available_amount"]
            total_amount = user_info["total_amount"]
            activated_packages = user_info["activated_packages"]
            daily_profit = controller.daily_profit(user_info["activated_packages"])
            
            active_ackage = user_info["activated_packages"]
            txt_remaining_day = ""
            for active_packages in active_ackage:
                remaining_days = controller.remaining_days(active_packages)
                txt_remaining_day += remaining_days['msg']
            
            tx_hash_successfully_deposit = user_info["tx_hash_successfully_deposit"]
            tx_hash_pending_deposit = user_info["tx_hash_pending_deposit"]
            tx_hash_failed_deposit = user_info["tx_hash_failed_deposit"]       
            wallet = user_info["wallet"]
            withdraw_request = user_info["withdraw_request"]
            withdraw_amount = user_info["withdraw_amount"]
            tx_hash_successfully_withdraw = user_info["tx_hash_successfully_withdraw"]
            if not withdraw_request and not user_info["tx_hash_pending_deposit"]:
                keyboard = [
                    [
                        InlineKeyboardButton("Edit email", callback_data='2'),
                        InlineKeyboardButton("ََAdd TX hash", callback_data='4'),
                    ], 
                    [
                        InlineKeyboardButton("Edit wallet", callback_data='5'),
                        InlineKeyboardButton("Main Menu", callback_data='0'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if query:
                    await query.edit_message_text(msg_texts.user_info_existed(first_name, email, email_status, available_amount,
                                total_amount, daily_profit, activated_packages, 
                                tx_hash_successfully_deposit, tx_hash_pending_deposit, 
                                tx_hash_failed_deposit, 
                                wallet, withdraw_request, withdraw_amount, tx_hash_successfully_withdraw, txt_remaining_day), 
                                reply_markup=reply_markup)
                else:
                    await update.message.reply_text(msg_texts.user_info_existed(first_name, email, email_status, available_amount,
                                total_amount, daily_profit, activated_packages, 
                                tx_hash_successfully_deposit, tx_hash_pending_deposit, 
                                tx_hash_failed_deposit, 
                                wallet, withdraw_request, withdraw_amount, tx_hash_successfully_withdraw, txt_remaining_day), 
                                reply_markup=reply_markup)
                return USER_PROFILE_ROUT
            else:
                keyboard = [
                    [
                        InlineKeyboardButton("Edit email", callback_data='2'),
                        InlineKeyboardButton("Add TX hash", callback_data='4'),
                    ], 
                    [
                        InlineKeyboardButton("check TX hash", callback_data='7'),
                        InlineKeyboardButton("Main Menu", callback_data='0'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if query:
                    await query.edit_message_text(msg_texts.user_info_existed(first_name, email, email_status, available_amount,
                                total_amount, daily_profit, activated_packages, 
                                tx_hash_successfully_deposit, tx_hash_pending_deposit, 
                                tx_hash_failed_deposit, 
                                wallet, withdraw_request, withdraw_amount, tx_hash_successfully_withdraw, txt_remaining_day), 
                                reply_markup=reply_markup)
                else:
                    await update.message.reply_text(msg_texts.user_info_existed(first_name, email, email_status, available_amount,
                                total_amount, daily_profit, activated_packages, 
                                tx_hash_successfully_deposit, tx_hash_pending_deposit, 
                                tx_hash_failed_deposit, 
                                wallet, withdraw_request, withdraw_amount, tx_hash_successfully_withdraw, txt_remaining_day), 
                                reply_markup=reply_markup)
                return USER_PROFILE_ROUT
    except Exception as e:
        print(f"Error in user_info function: {e}")
        traceback.print_exc()

@log_function
async def check_TX_by_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        tx_user = user_info["tx_hash_pending_deposit"]
        result = controller.tx_hash_successfully_deposit(chat_id, user_info, tx_user)
        status = result['status']
        if status:
            await query.edit_message_text("User added transaction to pending")    
            return START_ROUTES
        else:
            msg = result['msg']
            await query.edit_message_text(f"{msg}")    
            return START_ROUTES
    except Exception as e:
        print(f"Error in check_TX_by_user function: {e}")
        traceback.print_exc()
        
@log_function
async def enter_email_newuser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(msg_texts.enter_email())    
        return ENTER_EMAIL_NEW
    except Exception as e:
        print(f"Error in enter_email_newuser function: {e}")
        traceback.print_exc()

@log_function
async def handle_entered_newemail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        if query:
            await query.answer()

        user_entry = update.effective_message.text  # Use update.effective_message instead of update.message
        
        if user_entry == "/empty": 
            keyboard = [                    
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_cancel_email(), reply_markup=reply_markup)
            return START_ROUTES
        chat_id=update.effective_chat.id
        result = controller.create_account(chat_id, user_entry)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [                    
                    [
                        InlineKeyboardButton("User Profile", callback_data='3'),
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.enter_newemail(msg), reply_markup=reply_markup)
            return USER_PROFILE_ROUT
        else:
            print(msg)
            # await query.edit_message_text(msg_texts.enter_wrong_email(msg))
            if query:
                await query.edit_message_text(msg_texts.enter_wrong_email(msg))
                return ENTER_EMAIL_NEW
            await update.message.reply_text(msg_texts.enter_wrong_email(msg))
            return ENTER_EMAIL_NEW
    except Exception as e:
        print(f"Error in handle_entered_newemail function: {e}")
        traceback.print_exc()

@log_function
async def enter_email_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(msg_texts.email_edit())    
        return ENTER_EDIT_EMAIL
    except Exception as e:
        print(f"Error in enter_email_edit function: {e}")
        traceback.print_exc()

@log_function
async def handle_email_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        if query:
            await query.answer()
        user_entry = update.message.text
        if user_entry == "/empty": 
            keyboard = [                    
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_cancel_email(), reply_markup=reply_markup)
            return START_ROUTES
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        result = controller.change_email(chat_id, user_info, user_entry)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [                    
                    [
                        InlineKeyboardButton("User Profile", callback_data='3'),
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.enter_email_edit(), reply_markup=reply_markup)
            return USER_PROFILE_ROUT
        else:
            if query:
                await query.edit_message_text(msg_texts.enter_wrong_email(msg))
                return ENTER_EDIT_EMAIL
            await update.message.reply_text(msg_texts.enter_wrong_email(msg))
            return ENTER_EDIT_EMAIL
    except Exception as e:
        print(f"Error in handle_email_edit function: {e}")
        traceback.print_exc()

@log_function
async def enter_tx_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(msg_texts.enter_tx_add())    
        return ENTER_TX_ADD
    except Exception as e:
        print(f"Error in enter_tx_add function: {e}")
        traceback.print_exc()

@log_function
async def handle_tx_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        if query:
            await query.answer()
        user_entry = update.message.text
        if user_entry == "/empty": 
            keyboard = [                    
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_cancel_tx_add(), reply_markup=reply_markup)
            return START_ROUTES
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        result = controller.add_tx_hash_pending_deposit(chat_id, user_info, user_entry)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [                    
                    [
                        InlineKeyboardButton("User Profile", callback_data='3'),
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_tx_add(msg), reply_markup=reply_markup)
            return USER_PROFILE_ROUT
        else:
            if query:
                await query.edit_message_text(msg_texts.enter_wrong_tx(msg))
                return ENTER_TX_ADD
            await update.message.reply_text(msg_texts.enter_wrong_tx(msg))
            return ENTER_TX_ADD
    except Exception as e:
        print(f"Error in handle_tx_add function: {e}")
        traceback.print_exc()

@log_function
async def enter_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        withdraw_request = user_info["withdraw_request"]
        if withdraw_request: 
            await query.edit_message_text("Sorry, you have to wait until your withdraw request is complete. /start")    
            return START_ROUTES
        await query.edit_message_text(msg_texts.enter_wallet())    
        return ENTER_WALLET
    except Exception as e:
        print(f"Error in enter_wallet function: {e}")
        traceback.print_exc()

@log_function
async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        if query:
            await query.answer()
        user_entry = update.message.text
        if user_entry == "/empty": 
            keyboard = [                    
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_cancel_wallet(), reply_markup=reply_markup)
            return START_ROUTES
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        result = controller.change_wallet(chat_id, user_info, user_entry)
        status = result['status']
        msg = result['msg']
        if status:
            keyboard = [                    
                    [
                        InlineKeyboardButton("User Profile", callback_data='3'),
                        InlineKeyboardButton("Deposit", callback_data='6'),
                    ],
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_wallet(msg), reply_markup=reply_markup)
            return USER_PROFILE_ROUT
        else:
            if query:
                await query.edit_message_text(msg_texts.enter_wrong_wallet(msg))
                return ENTER_WALLET
            await update.message.reply_text(msg_texts.enter_wrong_wallet(msg))
            return ENTER_WALLET
    except Exception as e:
        print(f"Error in handle_wallet function: {e}")
        traceback.print_exc()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# need work not complite
# if email status == false -> they can not withdraw
@log_function
async def withdraw_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        chat_id=update.effective_chat.id
        query = update.callback_query    
        await query.answer()
        if controller.user_exists(chat_id):
            #we should read the file, then user can edit 
            user_info = controller.read_info(chat_id)
            withdraw_request = user_info["withdraw_request"]
            available_amount = user_info["available_amount"]
            total_amount = user_info["total_amount"]
            if available_amount >= 2.0 and not withdraw_request:
                stage = 1
                keyboard = [
                    [
                        InlineKeyboardButton("withdraw", callback_data='1'),
                    ],            
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(msg_texts.withdraw_request(available_amount, total_amount,stage), reply_markup=reply_markup)
            elif available_amount >= 2.0 and withdraw_request:
                stage = 2
                keyboard = [                           
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ] 
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(msg_texts.withdraw_request(available_amount, total_amount, stage), reply_markup=reply_markup)     
            elif available_amount < 2.0 and not withdraw_request:
                stage = 3
                keyboard = [                           
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ] 
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(msg_texts.withdraw_request(available_amount, total_amount, stage), reply_markup=reply_markup)
            elif available_amount < 2.0 and withdraw_request:
                stage = 4
                keyboard = [                           
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ] 
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(msg_texts.withdraw_request(available_amount, total_amount, stage), reply_markup=reply_markup)

            

        else:
            keyboard = [
                [
                    InlineKeyboardButton("create an account", callback_data='3'), # it will go to user info page and can create his account
                ],  
                [
                InlineKeyboardButton("main menu", callback_data='0'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(msg_texts.withdraw_request_new_user(), reply_markup=reply_markup)
        return WITHDRAW_REQUEST_ROUT
    except Exception as e:
        print(f"Error in withdraw_request function: {e}")
        traceback.print_exc()

@log_function
async def enter_amount_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(msg_texts.enter_amount_withdraw())    
        return ENTER_AMOUNT_WITHD
    except Exception as e:
        print(f"Error in enter_amount_withdraw function: {e}")
        traceback.print_exc()

@log_function
async def handle_entered_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        user_entry = update.message.text
        query = update.callback_query
        if query:
            await query.answer()
        if user_entry == "/empty": 
            keyboard = [
                    [
                        InlineKeyboardButton("main menu", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_entered_amount_cancel(), reply_markup=reply_markup)            
            return START_ROUTES
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        wallet = user_info["wallet"]
        user_info = controller.read_info(chat_id)
        result = controller.withdraw_amount(chat_id, user_info, float(user_entry))
        status = result['status']
        msg = result['msg']
        if status and wallet:
            keyboard = [
                    [
                    InlineKeyboardButton("Yes, change wallet", callback_data='4'),
                    ],
                    [
                    InlineKeyboardButton("No, Let's review last time", callback_data='1'),
                    ],
                    [
                    InlineKeyboardButton("back", callback_data='0'),
                    ]
                ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_entered_amount_have_wallet(msg, wallet), reply_markup=reply_markup)
            return AMOUNT_WALLET_CONDIRM_WITHD 
        elif not wallet and status: #user do the withdraw for the first time or didn't enter his wallet
            keyboard = [
                        [
                        InlineKeyboardButton("Your wallet", callback_data='1'),
                        ],
                        [
                        InlineKeyboardButton("back", callback_data='0'),
                        ]
                    ]   
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg_texts.handle_entered_amount_enter_wallet(msg), reply_markup=reply_markup)
            return ENTER_AMOUNT_WITHD_ROUT    
        elif not status:
            # this means user entered an unvalid number or higher amount
            if query:
                await query.edit_message_text(msg_texts.handle_entered_amount_wrong_entry(msg))
                return ENTER_AMOUNT_WITHD
            await update.message.reply_text(msg_texts.handle_entered_amount_wrong_entry(msg))
            return ENTER_AMOUNT_WITHD
    except Exception as e:
        print(f"Error in handle_entered_amount function: {e}")
        traceback.print_exc()

@log_function
async def amount_wallet_confirm_withd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try: 
        query = update.callback_query
        if query:
            await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        withdraw_amount = user_info["withdraw_amount"]
        ballance = user_info["available_amount"] - withdraw_amount
        wallet = user_info["wallet"]
        keyboard = [                    
                    [
                    InlineKeyboardButton("Yes, they are currect", callback_data='20'),
                    ],
                    [
                    InlineKeyboardButton("No, something missing.", callback_data='0'),
                    ]
                ]   
        reply_markup = InlineKeyboardMarkup(keyboard)
        if query:
            await query.edit_message_text(msg_texts.confirm_withdraw(ballance, withdraw_amount, wallet), reply_markup=reply_markup)
            return AMOUNT_WALLET_CONDIRM_WITHD
        else:
            await update.message.reply_text(msg_texts.confirm_withdraw(ballance, withdraw_amount, wallet), reply_markup=reply_markup)            
            return AMOUNT_WALLET_CONDIRM_WITHD
    except Exception as e:
        print(f"Error in amount_wallet_confirm_withd function: {e}")
        traceback.print_exc()

@log_function
async def withdraw_success(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        if query:
            await query.answer()
        chat_id=update.effective_chat.id
        user_info = controller.read_info(chat_id)
        result = controller.withdraw_request(chat_id, user_info)
        status = result['status']
        msg = result['msg']
        if status:
            if query:
                await query.edit_message_text(msg_texts.confirmed_withdraw_request(msg))    
                return START_ROUTES
            else:
                await update.message.reply_text(msg_texts.confirmed_withdraw_request(msg))    
                return START_ROUTES
        else:
            if query:
                await query.edit_message_text(msg_texts.rejected_withdraw(msg))    
                return START_ROUTES
            else:
                await update.message.reply_text(msg_texts.rejected_withdraw(msg))    
                return START_ROUTES
    except Exception as e:
        print(f"Error in withdraw_success function: {e}")
        traceback.print_exc()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@log_function
async def contact_us(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        if query:
            await query.answer()
            
        keyboard = [
            [
                InlineKeyboardButton("Main Menu", callback_data='0'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if query:
            await query.edit_message_text(msg_texts.contact_us(), reply_markup=reply_markup)
        else:
            await update.message.reply_text(msg_texts.contact_us())
        return START_ROUTES
    except Exception as e:
        print(f"Error in contact_us function: {e}")
        traceback.print_exc()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@log_function
async def privacy_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:    
    try:
        query = update.callback_query
        if query:
            await query.answer()
        first_name = update.callback_query.from_user.first_name
        keyboard = [        
            [
                InlineKeyboardButton("Main Menu", callback_data='0'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if query:
            await query.edit_message_text(msg_texts.privacy_policy(first_name), reply_markup=reply_markup)
        else:
            await update.message.reply_text(msg_texts.privacy_policy(first_name), reply_markup=reply_markup)
        return START_ROUTES
    except Exception as e:
        print(f"Error in privacy_policy function: {e}")
        traceback.print_exc()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# Run the program
if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(TOKEN).build()
    
        # ^ means "start of line/string"
        # $ means "end of line/string"
        # So ^ABC$ will only allow 'ABC'
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                START_ROUTES: [
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(packages, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(deposit, pattern="^" + '2' + "$"),
                    CallbackQueryHandler(user_profile, pattern="^" + '3' + "$"),
                    CallbackQueryHandler(withdraw_request, pattern="^" + '4' + "$"),
                    CallbackQueryHandler(contact_us, pattern="^" + '5' + "$"),
                    CallbackQueryHandler(privacy_policy, pattern="^" + '6' + "$"),               
                ],
                PACKAGE_ROUT: [
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(user_profile, pattern="^" + '3' + "$"),
                    CallbackQueryHandler(bronze_I_purchasing, pattern="^" + '30' + "$"),
                    CallbackQueryHandler(bronze_II_purchasing, pattern="^" + '60' + "$"),
                    CallbackQueryHandler(silver_I_purchasing, pattern="^" + '100' + "$"),
                    CallbackQueryHandler(silver_II_purchasing, pattern="^" + '200' + "$"),
                    CallbackQueryHandler(gold_purchasing, pattern="^" + '350' + "$"),
                    CallbackQueryHandler(platinum_purchasing, pattern="^" + '500' + "$"),
                    CallbackQueryHandler(diamond_purchasing, pattern="^" + '750' + "$"),
                    CallbackQueryHandler(master_purchasing, pattern="^" + '1000' + "$"),
                ], 
                PURCHASE_ROUT: [
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(packages, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(deposit, pattern="^" + '2' + "$"),
                    CallbackQueryHandler(bronze_I_confirm, pattern="^" + '30' + "$"),
                    CallbackQueryHandler(bronze_II_confirm, pattern="^" + '60' + "$"),
                    CallbackQueryHandler(silver_I_confirm, pattern="^" + '100' + "$"),
                    CallbackQueryHandler(silver_II_confirm, pattern="^" + '200' + "$"),
                    CallbackQueryHandler(gold_confirm, pattern="^" + '350' + "$"),
                    CallbackQueryHandler(platinum_confirm, pattern="^" + '500' + "$"),
                    CallbackQueryHandler(diamond_confirm, pattern="^" + '750' + "$"),
                    CallbackQueryHandler(master_confirm, pattern="^" + '1000' + "$"),
                ], 
                DEPOSIT_ROUT: [
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(user_profile, pattern="^" + '3' + "$"),
                    CallbackQueryHandler(company_wallet, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(enter_tx_add, pattern="^" + '2' + "$"),
                    CallbackQueryHandler(enter_wallet, pattern="^" + '4' + "$"),
                ],
                USER_PROFILE_ROUT: [
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(user_profile, pattern="^" + '3' + "$"),
                    CallbackQueryHandler(enter_email_newuser, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(enter_email_edit, pattern="^" + '2' + "$"),
                    CallbackQueryHandler(enter_tx_add, pattern="^" + '4' + "$"),
                    CallbackQueryHandler(enter_wallet, pattern="^" + '5' + "$"),
                    CallbackQueryHandler(deposit, pattern="^" + '6' + "$"),
                    CallbackQueryHandler(check_TX_by_user, pattern="^" + '7' + "$"),
                ], 
                WITHDRAW_REQUEST_ROUT: [
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(enter_amount_withdraw, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(user_profile, pattern="^" + '3' + "$"),
                ],
                ENTER_AMOUNT_WITHD: [
                    MessageHandler(filters.TEXT, handle_entered_amount)
                ],
                ENTER_AMOUNT_WITHD_ROUT: [
                    CallbackQueryHandler(enter_amount_withdraw, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(enter_wallet, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(amount_wallet_confirm_withd, pattern="^" + '2' + "$"),
                ],
                ENTER_WALLET_WITHD: [
                    MessageHandler(filters.TEXT, handle_wallet)
                ],
                AMOUNT_WALLET_CONDIRM_WITHD: [
                    CallbackQueryHandler(amount_wallet_confirm_withd, pattern="^" + '1' + "$"),
                    CallbackQueryHandler(enter_wallet, pattern="^" + '4' + "$"),
                    CallbackQueryHandler(main_menu, pattern="^" + '0' + "$"),
                    CallbackQueryHandler(withdraw_success, pattern="^" + '20' + "$"),
                ],
                ENTER_EMAIL_NEW: [
                    MessageHandler(filters.TEXT, handle_entered_newemail)
                ],
                ENTER_EDIT_EMAIL: [
                    MessageHandler(filters.TEXT, handle_email_edit)
                ], 
                ENTER_TX_ADD: [
                    MessageHandler(filters.TEXT, handle_tx_add)
                ],
                ENTER_WALLET: [
                    MessageHandler(filters.TEXT, handle_wallet)
                ],   

            },
            fallbacks=[CommandHandler("start", start)],
        )

        # Add ConversationHandler to application that will be used for handling updates
        application.add_handler(conv_handler)   
        # Commands
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('help', help))
        application.add_handler(CommandHandler('package', packages))
        application.add_handler(CommandHandler('user_profile', user_profile))
        application.add_handler(CommandHandler('contact_us', contact_us))
        # application.add_handler(CommandHandler('supporter', supporter))
        # application.add_handler(MessageHandler(filters.Text & ~filters.Command, on_supporter_response))

        # Messages
        application.add_handler(MessageHandler(filters.TEXT, handle_message))

        # Run the bot
        print('Polling...')
        application.run_polling()
    except Exception as e:
        print(f"Error in main if: {e}")
        traceback.print_exc()