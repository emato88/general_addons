# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    login_project_id = fields.Many2one("project.project", string="Project", readonly=True, compute="_get_login_project")
    login_task_id = fields.Many2one("project.task", string="Task", readonly=True, compute="_get_login_task")
    login_description = fields.Char(string="Description", readonly=True, compute="_get_login_description")

    def _get_login_project(self):
        for employee in self:
            attendance = self.env["hr.attendance"].search(
                [("employee_id", "=", self.id), ("check_out", "=", False)], limit=1
            )
            employee.login_project_id = attendance.project_id.id

    def _get_login_task(self):
        for employee in self:
            attendance = self.env["hr.attendance"].search(
                [("employee_id", "=", self.id), ("check_out", "=", False)], limit=1
            )
            employee.login_task_id = attendance.task_id.id

    def _get_login_description(self):
        for employee in self:
            attendance = self.env["hr.attendance"].search(
                [("employee_id", "=", self.id), ("check_out", "=", False)], limit=1
            )
            employee.login_description = attendance.description

    def _attendance_action_change(self):
        if len(self) > 1:
            return super(HrEmployee, self)._attendance_action_change()

        checked_out = False
        if self.attendance_state != "checked_in":
            checked_out = True
        attendance = super(HrEmployee, self)._attendance_action_change()

        if checked_out:
            if not self._context.get("project_id"):
                raise UserError('You must enter the project to start.')
            if not self._context.get("task_id"):
                raise UserError('You must enter the task to start.')
            if not self._context.get("description"):
                raise UserError('You must enter the description to start.')

            attendance.task_id = int(self._context.get("task_id"))
            attendance.project_id = int(self._context.get("project_id"))
            attendance.description = self._context.get("description")
        return attendance
