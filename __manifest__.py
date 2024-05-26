# -*- coding: utf-8 -*-
{
    'name': "HR Extend IPAC",

    'summary': """
    
        """,

    'description': """
        It added some 
    """,

    'author': "Arash Homayounfar",
    'website': "https://github.com/gilaneh/hr_extend_ipac",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Service Desk/Service Desk',
    'application': True,
    'version': '15.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web','hr', 'hr_skills',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'report/resume_en.xml',
        'report/resume_en_template.xml',

    ],
    'assets': {
        'web.report_assets_common': [
            'hr_extend_ipac/static/src/css/report_styles.css',
            ],
    },
    'license': 'LGPL-3',

}
