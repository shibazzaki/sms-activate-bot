from aiogram_dialog import Dialog
from .windows import main_menu, purchase_menu, profile_menu, info_menu


def bot_menu_dialogs():
    """
    Return dialogs related to the bot menu.
    """
    return [
        Dialog(
            main_menu(),
            purchase_menu(),
            profile_menu(),
            info_menu()
        )
    ]
