from aiogram.fsm.state import StatesGroup, State

class MainMenu(StatesGroup):
    main = State()
    profile = State()
    buy_number = State()
    info = State()
    admin_panel = State()

class ProfileMenu(StatesGroup):
    view = State()
    edit = State()
    add_funds = State()

class AdminMenu(StatesGroup):
    view_users = State()
    show_stats = State()
    manage_orders = State()

class PurchaseMenu(StatesGroup):
    confirm_payment = State()
    choose_service = State()
    select_country = State()
    check_balance = State()
    payment = State()

class InfoMenu(StatesGroup):
    faq = State()
    rules = State()
    tech_support = State()
    our_projects = State()