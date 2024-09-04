from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, SwitchTo, Start, Cancel
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from tgbot.dialogs.getters import get_services, get_countries
from tgbot.dialogs.states import MainMenu, ProfileMenu, PurchaseMenu, AdminMenu
from callbacks import is_it_admin, handle_payment

# Main menu dialog
main_menu = Dialog(
    Window(
            StaticMedia(path='tgbot.misc.', type=ContentType.PHOTO),
            Const("Welcome! How can I assist you today?"),
        Group(
            Button(Const("💸 Buy"), id="buy",
                   on_click=SwitchTo(PurchaseMenu.choose_service)),
            Button(Const("👤 Profile"), id="profile",
                   on_click=SwitchTo(ProfileMenu.view)),
            Button(Const("ℹ️ Info"), id="info",
                   on_click=SwitchTo(ProfileMenu.view)),
        state=MainMenu.main,
        )
    )
)

# Purchase menu dialog
purchase_menu = Dialog(
    Window(
        Const("Please choose a service:"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="service_selection",
                item_id_getter=lambda x: x,
                items="services",
                on_click=SwitchTo(PurchaseMenu.select_country),
            ),
            width=1,
            height=6
        ),
        state=PurchaseMenu.choose_service,
        getter=[get_services]
    ),
    Window(
        Const("Please choose a country:"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="country_selection",
                item_id_getter=lambda x: x,
                items="countries",
                on_click=SwitchTo(PurchaseMenu.payment),
            ),
            width=1,
            height=6
        ),
        state=PurchaseMenu.select_country,
        getter=[get_countries]
    ),
    Window(
        Const("Proceed to payment"),
        Group(
            Button(Const("💳 Pay"), id="pay", on_click=handle_payment),
            Button(Const("🔙 Back"), id="back", on_click=SwitchTo(PurchaseMenu.choose_service)),
        ),
        state=PurchaseMenu.payment
    ),
    Window(
        Const("Waiting for payment confirmation..."),
        state=PurchaseMenu.confirm_payment,
    )
)
