# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Report Qweb Decimal Place",
    "category": "Reporting",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": ["account", "sale", "purchase"],
    "data": [
        "reports/price_unit_value_format.xml",
        "reports/invoice_report.xml",
        "reports/sale_report.xml",
        "reports/purchase_report.xml",
        "views/res_currency_views.xml",
    ],
    "installable": True,
}
