# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class HrExtendEmployeeResume(models.Model):
    _inherit = "hr.employee"

    name_cv = fields.Char(translate=True)
    job_title = fields.Char(translate=True)
    # capabilities = fields.Many2one('hr_extend_ipac.resume')
    resume_extend = fields.Many2one('hr_extend_ipac.resume')
    resume_projects = fields.Text(related='resume_extend.projects', readonly=False)
    resume_capabilities = fields.Text(related='resume_extend.capabilities', readonly=False)
    resume_qualifications = fields.Text(related='resume_extend.qualifications', readonly=False)
    resume_software = fields.Text(related='resume_extend.software', readonly=False)
    resume_trainings = fields.Text(related='resume_extend.trainings', readonly=False)
    resume_awards = fields.Text(related='resume_extend.awards', readonly=False)

    @api.model
    def create(self, vals):
        # res = super().create(vals)
        # resume_extend = self.env['hr_extend_ipac.resume'].create({'employee': res.id}).id
        # vals['resume_extend'] = resume_extend
        return super().create(vals)

    def write(self, vals):
        if not self.resume_extend:
            resume_extend = self.env['hr_extend_ipac.resume'].create({'employee': self.id}).id
            vals['resume_extend'] = resume_extend
        return super().write(vals)


    def print_resume(self):
        # print(f'\n=================== Print Resume =========================\n')
        data = {'form_data': {'a': 1}}
        # print(f'\n {read_form.get("calendar")}')
        return self.env.ref('hr_extend_ipac.resume_en_report').report_action(self,)
        # return self.env.ref('hr_extend_ipac.resume_en_report').report_action(self, data=data)







