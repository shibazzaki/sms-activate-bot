from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia

from tgbot.dialogs.bot_menu.callbacks import handle_payment
from tgbot.dialogs.bot_menu.getters import get_services, get_countries
from tgbot.dialogs.bot_menu.states import MainMenu, ProfileMenu, PurchaseMenu, InfoMenu

# Main menu dialog
main_menu = Dialog(
    Window(
        StaticMedia(
            path='tgbot.misc.stains.gif',  # Update with actual image path or URL
            type=ContentType.PHOTO,
        ),
        Const("Welcome! How can I assist you today?"),
        Group(
            Button(Const("💸 Buy Number"), id="buy", on_click=SwitchTo(PurchaseMenu.choose_service)),
            Button(Const("👤 Profile"), id="profile", on_click=SwitchTo(ProfileMenu.view)),
            Button(Const("ℹ️ Info"), id="info", on_click=SwitchTo(InfoMenu.faq)),
            Button(Const("🔧 Admin Panel"), id="admin", on_click=SwitchTo(MainMenu.admin_panel)),
        ),
        state=MainMenu.main,
    )
)

# Purchase menu dialog
purchase_menu = Dialog(
    Window(
        Const("Please choose a service:"),
        ScrollingGroup(
            Select(
                Format("{item}"),  # Display available services
                id="service_selection",
                item_id_getter=lambda x: x,
                items="services",  # Pass services fetched from the getter
                on_click=SwitchTo(PurchaseMenu.select_country),
            ),
            width=1,
            height=6
        ),
        state=PurchaseMenu.choose_service,
        getter=get_services  # Fetch services dynamically using SMSActivate API
    ),
    Window(
        Const("Please choose a country:"),
        ScrollingGroup(
            Select(
                Format("{item}"),  # Display available countries
                id="country_selection",
                item_id_getter=lambda x: x,
                items="countries",  # Pass countries fetched from the getter
                on_click=SwitchTo(PurchaseMenu.payment),
            ),
            width=1,
            height=6
        ),
        state=PurchaseMenu.select_country,
        getter=get_countries  # Fetch countries dynamically using SMSActivate API
    ),
    Window(
        Const("Proceed to payment"),
        Group(
            Button(Const("💳 Pay"), id="pay", on_click=lambda c, b, d: handle_payment(d)),
            Button(Const("🔙 Back"), id="back", on_click=SwitchTo(PurchaseMenu.choose_service)),
        ),
        state=PurchaseMenu.payment
    ),
    Window(
        Const("Waiting for payment confirmation..."),
        state=PurchaseMenu.confirm_payment,
    )
)

# Profile menu dialog
profile_menu = Dialog(
    Window(
        Const("Profile: What would you like to do?"),
        Group(
            Button(Const("View Profile"), id="view", on_click=SwitchTo(ProfileMenu.view)),
            Button(Const("Edit Profile"), id="edit", on_click=SwitchTo(ProfileMenu.edit)),
            Button(Const("Add Funds"), id="add_funds", on_click=SwitchTo(ProfileMenu.add_funds)),
        ),
        state=ProfileMenu.view
    )
)

# Info menu dialog
info_menu = Dialog(
    Window(
        Const("Information"),
        Group(
            Button(Const("FAQ"), id="faq", on_click=SwitchTo(InfoMenu.faq)),
            Button(Const("Rules"), id="rules", on_click=SwitchTo(InfoMenu.rules)),
            Button(Const("Tech Support"), id="tech_support", on_click=SwitchTo(InfoMenu.tech_support)),
            Button(Const("Our Projects"), id="our_projects", on_click=SwitchTo(InfoMenu.our_projects)),
        ),
        state=InfoMenu.faq  # Starting with FAQ
    )
)
