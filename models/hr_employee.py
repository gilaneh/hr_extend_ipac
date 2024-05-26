# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class HrExtendEmployeeResume(models.Model):
    _inherit = "hr.employee"

    name_cv = fields.Char(translate=True)
    job_title = fields.Char(translate=True)

    def print_resume(self):
        # print(f'\n=================== Print Resume =========================\n')
        data = {'form_data': {'a': 1}}
        # print(f'\n {read_form.get("calendar")}')
        return self.env.ref('hr_extend_ipac.resume_en_report').report_action(self,)
        # return self.env.ref('hr_extend_ipac.resume_en_report').report_action(self, data=data)







