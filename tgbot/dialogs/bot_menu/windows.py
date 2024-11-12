from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia
from tgbot.dialogs.bot_menu.states import MainMenu, ProfileMenu, PurchaseMenu, InfoMenu
from tgbot.dialogs.bot_menu.getters import get_services, get_countries
from aiogram.enums import ContentType

# Main menu dialog
main_menu = Dialog(
    Window(
        StaticMedia(
            path='tgbot.misc.stains.gif',  # Update with actual image path or URL
            type=ContentType.PHOTO,
        ),
        Const("Welcome! How can I assist you today?"),
        Group(
            SwitchTo(Const("💸 Buy Number"), id="buy", state=PurchaseMenu.choose_service),
            SwitchTo(Const("👤 Profile"), id="profile", state=ProfileMenu.view),
            SwitchTo(Const("ℹ️ Info"), id="info", state=InfoMenu.faq),
            SwitchTo(Const("🔧 Admin Panel"), id="admin", state=MainMenu.admin_panel),
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
                Format("{item}"),
                id="service_selection",
                item_id_getter=lambda x: x,
                items="services",
                on_click=lambda c, b, d: c.dialog().switch_to(PurchaseMenu.select_country)
            ),
            width=1,
            height=6,
            id="scrolling_services"
        ),
        state=PurchaseMenu.choose_service,
        getter=get_services
    ),
    Window(
        Const("Please choose a country:"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="country_selection",
                item_id_getter=lambda x: x,
                items="countries",
                on_click=lambda c, b, d: c.dialog().switch_to(PurchaseMenu.payment)
            ),
            width=1,
            height=6,
            id="scrolling_countries"
        ),
        state=PurchaseMenu.select_country,
        getter=get_countries
    ),
    Window(
        Const("Proceed to payment"),
        Group(
            Button(Const("💳 Pay"), id="pay", on_click=lambda c, b, d: c.dialog().switch_to(PurchaseMenu.confirm_payment)),
            Button(Const("🔙 Back"), id="back", on_click=lambda c, b, d: c.dialog().switch_to(PurchaseMenu.choose_service)),
        ),
        state=PurchaseMenu.payment
    ),
    Window(
        Const("Waiting for payment confirmation..."),
        Group(
            Button(Const("🔄 Check Payment Status"), id="check_payment", on_click=lambda c, b, d: c.dialog().switch_to(PurchaseMenu.payment)),
            Button(Const("🔙 Back"), id="back", on_click=lambda c, b, d: c.dialog().switch_to(PurchaseMenu.choose_service)),
        ),
        state=PurchaseMenu.confirm_payment,
    )
)

# Profile menu dialog
profile_menu = Dialog(
    Window(
        Const("Profile: What would you like to do?"),
        Group(
            SwitchTo(Const("View Profile"), id="view", state=ProfileMenu.view),
            SwitchTo(Const("Edit Profile"), id="edit", state=ProfileMenu.edit),
            SwitchTo(Const("Add Funds"), id="add_funds", state=ProfileMenu.add_funds),
        ),
        state=ProfileMenu.view
    )
)

# Info menu dialog
info_menu = Dialog(
    Window(
        Const("Information"),
        Group(
            SwitchTo(Const("FAQ"), id="faq", state=InfoMenu.faq),
            SwitchTo(Const("Rules"), id="rules", state=InfoMenu.rules),
            SwitchTo(Const("Tech Support"), id="tech_support", state=InfoMenu.tech_support),
            SwitchTo(Const("Our Projects"), id="our_projects", state=InfoMenu.our_projects),
        ),
        state=InfoMenu.faq  # Starting with FAQ
    )
)
