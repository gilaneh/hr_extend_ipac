# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportHrExtendIpacResumeEn(models.AbstractModel):
    _name = 'report.hr_extend_ipac.resume_en_template'
    # _name = 'report.hr_employee.resume_en_report'
    _description = 'IPAC Resume'

    # ########################################################################################
    def get_report_values(self, docids=None, data=None):
        return self._get_report_values(docids, data)

    # ########################################################################################
    @api.model
    def _get_report_values(self, docids=None, data=None):
        docs = self.env['hr.employee'].browse(docids)
        errors = []
        doc_data_list = []
        PAGE_LINES = 25
        context = self.env.context
        time_z = pytz.timezone(context.get('tz'))
        date_time = datetime.now(time_z)
        calendar = context.get('lang')
        date_time1 = self.date_converter(date_time, context.get('lang'))

        # print(f'\n==============\n'
        #       f'date_time: {date_time}  date_time1:{date_time1}  ')
        doc_list = []
        educations = {}
        experiences = {}
        projects = {}
        qualifications = {}
        capabilities = {}
        languages = {}
        for doc in docs:
            educa = []
            exper = []
            proj = []
            quali = []
            capab = []
            langu = []
            for line in doc.resume_line_ids:
                if line.line_type_id.name == 'Education':
                    educa.append({'id': doc.id,
                                   'name': line.name,
                                   'description': line.description.split('\n') if line.description else [],
                                   'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                   'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                   })
                elif line.line_type_id.name == 'Experience':
                    exper.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                       'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                       })
                elif line.line_type_id.name == 'Projects':
                    proj.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                       'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                       })
                elif line.line_type_id.name == 'Qualifications':
                    quali.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                       'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                       })
                # elif line.line_type_id.name == 'Capabilities':
                #     capab.append({'name': line.name,
                #                   'description': line.description.split('\n') if line.description else [],
                #                   'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                #                        'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                #                        })
            for skill in doc.employee_skill_ids:
                if skill.skill_type_id.name == 'Language':
                    langu.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
                elif skill.skill_type_id.name == 'Capabilities':
                    capab.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
            educations[doc.id] = educa
            experiences[doc.id] = exper
            projects[doc.id] = proj
            qualifications[doc.id] = quali
            capabilities[doc.id] = capab
            languages[doc.id] = sorted(langu, key=lambda x: x['name'])

        return {
            'docs': docs,
            'doc_ids': docids,
            'educations': educations,
            'experiences': experiences,
            'projects': projects,
            'qualifications': qualifications,
            'capabilities': capabilities,
            'languages': languages,
        }



    # ########################################################################################
    def date_converter(self, date_time, lang):
        if lang == 'fa_IR':
            date_time = jdatetime.datetime.fromgregorian(datetime=date_time)
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                  'time': date_time.strftime("%H:%M:%S")}
        else:
            date_time = {'date': date_time.strftime("%Y/%m/%d"),
                        'time': date_time.strftime("%H:%M:%S")}
        return date_time

    # ########################################################################################
    def _table_record(self, items, start_date, first_day, last_day, record_type=False):
        day = len(list([item for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = len(list([item for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = len(list([item for item in items if (not record_type or item.record_type.name == record_type)]))
        return day, month, total

    # ########################################################################################
    def _table_record_sum_of_records(self, items, start_date, first_day, last_day, record_type=False):
        day = sum(list([item.man_hours for item in items
                        if (not record_type or item.record_type.name == record_type)
                        and item.record_date == start_date]))

        month = sum(list([item.man_hours for item in items
                          if (not record_type or item.record_type.name == record_type)
                          and item.record_date <= start_date
                          and item.record_date >= first_day ]))

        total = sum(list([item.man_hours for item in items if (not record_type or item.record_type.name == record_type)]))
        day = int(round(day, 0))
        month = int(round(month, 0))
        total = int(round(total, 0))
        return day, month, total

