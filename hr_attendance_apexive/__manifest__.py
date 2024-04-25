# -*- coding: utf-8 -*-
{
    'name': 'HR Attendance Project',
    'version': '1.0',
    'summary': 'This addons is for time tracking by projects and tasks.',
    'category': 'Human Resources/Employees',
    'author': 'Apexive',
    'website': 'https://us.apexive.com/',
    'license': 'LGPL-3',
    'depends': ['base', 'hr_attendance', 'project'],
    "data": [
        "views/hr_attendance_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/hr_attendance_apexive/static/src/js/my_attendances.js",
            "/hr_attendance_apexive/static/src/xml/*.xml",
        ],
    },    
    "installable": True,
    "application": True,
}
