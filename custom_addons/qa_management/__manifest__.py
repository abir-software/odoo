{
    'name': 'QA Testing Management System',
    'version': '1.0',
    'category': 'Project Management',
    'summary': 'Universal QA Testing Management System for standardizing software testing lifecycles.',
    'description': """
QA Testing Management Module
============================
This module helps QA Leads, QA Testers, Developers, and Management manage the full testing lifecycle.

Features:
- Project & Module Management
- Test Case Management
- Test Execution Tracking
- Bug and Issue Reporting
- Defect Lifecycle Management
- Sprint & Go-Live Readiness
    """,
    'author': 'Md Abir Hassan',
    'depends': ['base', 'mail', 'project'],
    'data': [
        'security/qa_security.xml',
        'security/ir.model.access.csv',
        'data/qa_sequence.xml',
        'views/qa_menus.xml',
        'views/qa_project_views.xml',
        'views/qa_module_views.xml',
        'views/qa_test_case_views.xml',
        'views/qa_bug_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
