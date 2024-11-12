from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.dialogs.bot_menu.states import MainMenu, ProfileMenu

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.main, mode=StartMode.RESET_STACK)

@user_router.message(Command("profile"))
async def start_profile_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfileMenu.view, mode=StartMode.RESET_STACK)

@user_router.message(Command("add_funds"))
async def add_funds_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ProfileMenu.add_funds, mode=StartMode.RESET_STACK)