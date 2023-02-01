# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Move Solomon CSV",
    "version": "16.0.1.0.1",
    "category": "Accounting",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": [
        "account",
        "report_csv",
    ],
    "data": [
        "data/solomon_csv_report_data.xml",
        "views/account_analytic_plan_views.xml",
        "views/account_move_views.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
}
