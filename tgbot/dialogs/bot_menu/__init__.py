from aiogram_dialog import Dialog
from .windows import categories_window, products_window, product_info_window

def bot_menu_dialogs():
    """
    Return dialogs related to the bot menu.
    """
    return [
        Dialog(
            categories_window(),
            products_window(),
            product_info_window()
        )
    ]
