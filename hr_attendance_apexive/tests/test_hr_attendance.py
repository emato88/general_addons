# -*- coding: utf-8 -*-
import logging
from odoo.tests import TransactionCase
from odoo.tools import mute_logger

_logger = logging.getLogger(__name__)


class TestHrAttendance(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestHrAttendance, self).setUp(*args, **kwargs)
        self.hr_attendance_model = self.env['hr.attendance']

    @mute_logger('odoo.sql_db')
    def test_create_attendance(self):

        # Create a project
        project = self.env['project.project'].create({'name': 'Test Project'})

        # Create a task associated with the project
        task = self.env['project.task'].create({
            'name': 'Test Task',
            'project_id': project.id,
            'fold': False,
        })
        # Create a employee
        employee_id = self.env['hr.employee'].create({
            'name': 'Test Test',
            'resource_calendar_id': 1,
        })

        # Create an attendance record with the project assigned
        try:
            self.hr_attendance_model.create({'project_id': project.id,
                                             'description': 'Test description',
                                             'employee_id': employee_id.id,
                                             'task_id': task.id,
                                             'check_in': '2024-04-24 08:00:00',
                                             'check_out': '2024-04-24 17:00:00',
                                             'worked_hours': 08.00,
                                             })
        except Exception as e:
            _logger.error(e.args[0], exc_info=True)

    @mute_logger('odoo.sql_db')
    def test_get_tasks(self):

        # Create a project
        project = self.env['project.project'].create({'name': 'Test Project'})

        # Create a employee
        employee_id = self.env['hr.employee'].create({
            'name': 'Test Test',
            'resource_calendar_id': 1,
        })

        # Create a task associated with the project
        task = self.env['project.task'].create({
            'name': 'Test Task',
            'project_id': project.id,
            'fold': False,
        })

        # Create an attendance record without description
        try:
            attendance = self.hr_attendance_model.create({
                'description': 'Test description',
                'employee_id': employee_id.id,
                'project_id': project.id,
                'task_id': task.id,
                'check_in': '2024-04-24 08:00:00',
                'check_out': '2024-04-24 17:00:00',
                'worked_hours': 08.00,
            })
        except Exception as e:
            _logger.error(e.args[0], exc_info=True)

        # Call the _get_tasks method
        try:
            attendance._get_tasks()
        except Exception as e:
            _logger.error(e.args[0], exc_info=True)

        # Check if the task_domain_ids field is correctly updated
        self.assertEqual(attendance.task_domain_ids, task.ids)
