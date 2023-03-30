# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Analytic Distribution Access Control",
    "category": "Reporting",
    "version": "16.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": ["analytic", "purchase", "sale", "account"],
    "data": [
        "views/purchase_views.xml",
        "views/sale_order_views.xml",
        "security/ir.model.access.csv",
        "security/analytic_security.xml",
    ],
    "installable": True,
}
