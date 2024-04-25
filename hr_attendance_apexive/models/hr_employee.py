# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    """ This HrEmployee model extends the existing hr.employee model by adding three new computed 
    fields: login_project_id, login_task_id, and login_description. These fields are used to store 
    information about the employee's current login session, such as the associated project, task, and description.    
    """

    login_project_id = fields.Many2one("project.project", string="Project", readonly=True, compute="_get_login_info")
    login_task_id = fields.Many2one("project.task", string="Task", readonly=True, compute="_get_login_info")
    login_description = fields.Char(string="Description", readonly=True, compute="_get_login_info")

    def _get_login_info(self):

        """This method is used to get the project associated with the current employee's ongoing attendance.

            It iterates through each employee record in the current recordset.
            For each employee, it searches for the ongoing attendance record where the check-out time is not recorded.
            If found, it assigns the project ID of the ongoing attendance to the employee's login_project_id,
            login_task_id and login_description fields.

            Args:
            - self: A recordset containing employee records.

            Returns:
            - None
        """

        for employee in self:
            attendance = self.env["hr.attendance"].search(
                [("employee_id", "=", employee.id), ("check_out", "=", False)], limit=1
            )
            employee.login_project_id = attendance.project_id.id
            employee.login_task_id = attendance.task_id.id
            employee.login_description = attendance.description

    def _attendance_action_change(self):

        """
            This method handles changes in attendance actions for an employee.

            If multiple employee records are present in the recordset, it delegates the action change processing
            to the superclass method for handling multiple records.

            For a single employee record:
            - It checks if the employee is checked in or checked out.
            - If the employee is checked out, it ensures that project, task, and description information is provided
              in the context to start a new attendance record. If not provided, it raises UserError.
            - It then updates the attendance record with the provided project, task, and description information.

            Args:
            - self: A recordset containing employee records.

            Returns:
            - Attendance record: The updated attendance record.
            """

        if len(self) > 1:
            return super(HrEmployee, self)._attendance_action_change()

        checked_out = False
        if self.attendance_state != "checked_in":
            checked_out = True
        attendance = super(HrEmployee, self)._attendance_action_change()

        if checked_out:
            # If checked out, ensure project, task, and description information is provided
            if not self._context.get("project_id"):
                raise UserError('You must enter the project to start.')
            if not self._context.get("task_id"):
                raise UserError('You must enter the task to start.')
            if not self._context.get("description"):
                raise UserError('You must enter the description to start.')

            # Update attendance record with project, task, and description information
            attendance.task_id = int(self._context.get("task_id"))
            attendance.project_id = int(self._context.get("project_id"))
            attendance.description = self._context.get("description")
        return attendance
