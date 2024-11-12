from aiogram.fsm.state import StatesGroup, State

class MainMenu(StatesGroup):
    main = State()
    profile = State()
    buy_number = State()
    info = State()
    admin_panel = State()
    main_menu_help = State()  # Стан для відображення додаткової інформації користувачу

class ProfileMenu(StatesGroup):
    view = State()
    edit = State()
    edit_confirm = State()  # Стан для підтвердження змін перед оновленням даних
    add_funds = State()

class AdminMenu(StatesGroup):
    view_users = State()
    show_stats = State()
    show_detailed_stats = State()  # Стан для перегляду детальної статистики
    manage_orders = State()
    send_notification = State()  # Стан для розсилки повідомлень користувачам

class PurchaseMenu(StatesGroup):
    confirm_payment = State()
    choose_service = State()
    select_country = State()
    check_balance = State()
    payment = State()
    review_order = State()  # Стан для перегляду деталей замовлення перед підтвердженням
    cancel_order = State()  # Стан для відміни покупки

class InfoMenu(StatesGroup):
    faq = State()
    rules = State()
    tech_support = State()
    contact_support = State()  # Стан для контакту з підтримкою
    our_projects = State()
    view_terms = State()  # Стан для перегляду умов використання
