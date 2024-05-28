# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrExtendIpacResume(models.Model):
    _name = 'hr_extend_ipac.resume'
    _description = 'hr_extend_ipac.resume'
    _inherit = ['mail.thread', 'mail.activity.mixin',]
    _rec_name = 'employee'

    employee = fields.Many2one('hr.employee')
    projects = fields.Text()
    capabilities = fields.Text()
    qualifications = fields.Text()
    software = fields.Text()
    trainings = fields.Text()

# class HrExtendIpacCapabilities(models.Model):
#     _name = 'hr_extend_ipac.capabilities'
#     _description = 'hr_extend_ipac.capabilities'
#     _inherit = ['mail.thread', 'mail.activity.mixin',]
#
#     employee = fields.Many2one('hr.employee')
#     capabilities = fields.Text()
#
# class HrExtendIpacTraining(models.Model):
#     _name = 'hr_extend_ipac.training'
#     _description = 'hr_extend_ipac.training'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#
#     employee = fields.Many2one('hr.employee')
#     training = fields.Text()

