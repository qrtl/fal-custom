# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Move Line Create Payment Entry",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "depends": ["account"],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "data/server_action.xml",
        "wizards/account_payment_entry_wizard_views.xml",
    ],
    "installable": True,
}
