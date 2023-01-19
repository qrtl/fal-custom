# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountMoveSolomonCsv(models.AbstractModel):
    _name = "report.account_move_solomon_csv.report_solomon_csv"
    _inherit = "report.report_csv.abstract"

    def _get_field_dict(self):
        labels = {
            1: "Company",
            2: "Account",
            3: "Project",
            4: "Task",
            5: "Sub",
            6: "Ref Nbr",
            7: "Date",
            8: "Employee Id",
            9: "Labor Class",
            10: "Billable",
            11: "Quantity",
            12: "Debit",
            13: "Credit",
            14: "Description",
            15: "Reconsiliation Status",
            16: "Clear Date",
            17: "Tax Inclusive",
            18: "Category ID",
            19: "Tax ID",
            20: "Tax Amount",
        }
        return labels

    def _check_records(self, records):
        invalid_records = records.filtered(lambda x: x.state != "posted")
        if invalid_records:
            raise UserError(
                _(
                    "Following records are not in a valid state (posted) for export."
                    "\n%s"
                )
                % ("\n".join(invalid_records.mapped("name")))
            )
        exported_records = records.filtered(lambda x: x.is_exported)
        if exported_records:
            raise UserError(
                _(
                    "Following records have been exported already. Please "
                    "unselect 'Exported' as necessary to export them again.\n%s"
                )
                % ("\n".join(exported_records.mapped("name")))
            )

    @api.model
    def _get_line_description(self, line):
        if line.product_id:
            return line.product_id.name
        if line.display_type == "tax":
            return line.tax_line_id.description
        return line.name

    def generate_csv_report(self, writer, data, records):
        records = records.with_context(lang="en_US")
        self._check_records(records)
        writer.writeheader()
        labels = self._get_field_dict()
        for record in records:
            solomon_company_code = record.company_id.solomon_company_code
            for line in record.line_ids:
                if line.display_type in ("line_section", "line_note"):
                    continue
                analytic_lines = line.analytic_line_ids
                project_line = analytic_lines.filtered(
                    lambda x: x.plan_type == "project"
                )[:1]
                sub_line = analytic_lines.filtered(lambda x: x.plan_type == "sub")[:1]
                vals = {
                    labels[1]: solomon_company_code,
                    labels[2]: line.account_id.code[:4],
                    labels[3]: project_line.account_id.name or "",
                    labels[4]: project_line.account_id.code or "",
                    labels[5]: sub_line.account_id.name or "0000-0000-0000-00-00",
                    labels[7]: record.date,
                    labels[10]: "",  # Billable - FIXME: need to fill in?
                    labels[11]: 0,
                    labels[12]: line.debit,
                    labels[13]: line.credit,
                    labels[14]: self._get_line_description(line),
                    labels[15]: "Did not affect CA",
                }
                writer.writerow(vals)
            record.is_exported = True

    def csv_report_options(self):
        res = super().csv_report_options()
        field_dict = self._get_field_dict()
        for _k, v in field_dict.items():
            res["fieldnames"].append(v)
        res["delimiter"] = ","
        res["quoting"] = csv.QUOTE_MINIMAL
        return res
