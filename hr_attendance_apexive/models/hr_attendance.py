# -*- coding: utf-8 -*-

from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    description = fields.Char(string="Description")