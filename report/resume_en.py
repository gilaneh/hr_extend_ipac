# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api , _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import pytz
import jdatetime
from odoo import http


# ########################################################################################
class ReportHrExtendIpacResumeEnBw(models.AbstractModel):
    _name = 'report.hr_extend_ipac.resume_en_template_bw'
    # _name = 'report.hr_employee.resume_en_report'
    _description = 'IPAC Resume'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        report = self.env['report.hr_extend_ipac.resume_en_template']
        data['report_color'] = 'bw'
        return report.get_report_values(docids, data)

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

        doc_list = []
        educations = {}
        experiences = {}
        projects_1 = {}
        projects_2 = {}
        qualifications = {}
        capabilities_1 = {}
        capabilities_2 = {}
        software = {}
        trainings = {}
        awards = {}
        languages = {}
        for doc in docs:
            educa = []
            exper = []
            proj = []
            quali = []
            capab = []
            soft = []
            train = []
            awar = []
            langu = []

            educa_count = 0
            exper_count = 0
            proj_count = 0
            quali_count = 0
            capab_count = 0
            soft_count = 0
            train_count = 0
            award_count = 0
            langu_count = 0
            for line in doc.resume_line_ids:
                if line.line_type_id.name == 'Education':
                    educa_count += 1 + len(line.description.split('\n')) if line.description else 0
                    educa.append({'id': doc.id,
                                   'name': line.name,
                                   'description': line.description.split('\n') if line.description else [],
                                   'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                   'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                   })
                elif line.line_type_id.name == 'Experience':
                    exper_count += 1 + len(line.description.split('\n')) if line.description else 0
                    exper.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                       'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                       })
                elif line.line_type_id.name == 'Projects':
                    proj_count += 1 + len(line.description.split('\n')) if line.description else 0
                    proj.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                       'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                       })
                elif line.line_type_id.name == 'Qualifications':
                    quali_count += 1 + len(line.description.split('\n')) if line.description else 0
                    quali.append({'name': line.name,
                                  'description': line.description.split('\n') if line.description else [],
                                  'date_start': self.date_converter(line.date_start, context.get('lang'))['date'],
                                       'date_end': self.date_converter(line.date_end, context.get('lang'))['date'] if line.date_end else _('Current'),
                                       })

            for skill in doc.employee_skill_ids:
                if skill.skill_type_id.name == 'Language':
                    # langu_count += (1 + len(line.description.split('\n'))) if line.description else 0
                    langu.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
                elif skill.skill_type_id.name == 'Capabilities':
                    # capab_count += 1 + len(line.description.split('\n')) if line.description else 0
                    capab.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
                elif skill.skill_type_id.name == 'Software':
                    # soft_count += 1 + len(line.description.split('\n')) if line.description else 0
                    soft.append({  'id': doc.id,
                                    'name': skill.skill_id.name,
                                    'level': skill.skill_level_id.name,
                                    })
            if doc.resume_projects and doc.resume_projects.strip() != '':
                resume_projects = doc.resume_projects.split('\n')
                for record_name in resume_projects:
                    proj_count += len(record_name) // 80 or 1
                    proj.append({'id': doc.id,
                             'name': record_name,
                             'description': '',
                             'date_start': '',
                             'date_end': '',
                             })
            if doc.resume_capabilities and doc.resume_capabilities.strip() != '':
                resume_capabilities = doc.resume_capabilities.split('\n')
                capab_count += len(resume_capabilities)
                for record_name in resume_capabilities:
                    capab_count += len(record_name) // 80 or 1
                    capab.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })
            if doc.resume_qualifications and doc.resume_qualifications.strip() != '':
                resume_qualifications = doc.resume_qualifications.split('\n')
                quali_count += len(resume_qualifications)
                for record_name in resume_qualifications:
                    quali.append({'id': doc.id,
                             'name': record_name,
                             'description': '',
                             'date_start': '',
                             'date_end': '',
                             })

            if doc.resume_software and doc.resume_software.strip() != '':
                resume_software = doc.resume_software.split('\n')
                soft_count += len(resume_software)
                for record_name in resume_software:
                    soft.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })
            if doc.resume_trainings and doc.resume_trainings.strip() != '':
                resume_trainings = doc.resume_trainings.split('\n')
                train_count += len(resume_trainings)
                for record_name in resume_trainings:
                    train.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })
            if doc.resume_awards and doc.resume_awards.strip() != '':
                resume_awards = doc.resume_awards.split('\n')
                award_count += len(resume_awards)
                for record_name in resume_awards:
                    awar.append({'id': doc.id,
                             'name': record_name,
                             'level': '',
                             })

            educations[doc.id] = educa
            experiences[doc.id] = exper

            edu_exp_count = educa_count + exper_count
            if 26 - edu_exp_count <= 0:
                projects_1[doc.id] = []
                projects_2[doc.id] = proj
            else:
                projects_1[doc.id] = proj[0: 26 - edu_exp_count]
                projects_2[doc.id] = proj[26 - edu_exp_count:]

            edu_exp_proj_count = educa_count + exper_count + proj_count
            if 21 - edu_exp_proj_count <= 0:
                capabilities_1[doc.id] = []
                capabilities_2[doc.id] = capab
            else:
                capabilities_1[doc.id] = capab[0: 21 - edu_exp_proj_count]
                capabilities_2[doc.id] = capab[21 - edu_exp_proj_count:]

            qualifications[doc.id] = quali
            software[doc.id] = soft
            trainings[doc.id] = train
            awards[doc.id] = awar
            languages[doc.id] = sorted(langu, key=lambda x: x['name'])

        return {
            'docs': docs,
            'doc_ids': docids,
            'educations': educations,
            'experiences': experiences,
            'projects_1': projects_1,
            'projects_2': projects_2,
            'qualifications': qualifications,
            'capabilities_1': capabilities_1,
            'capabilities_2': capabilities_2,
            'software': software,
            'trainings': trainings,
            'awards': awards,
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

