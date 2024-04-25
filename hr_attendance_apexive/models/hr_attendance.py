# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    """ This HrAttendance model extends the existing hr.attendance model by adding three new 
    fields: project_id, task_id, task_domain_ids, and description. These fields allow for more 
    detailed tracking and categorization of attendance records within the Odoo system. 
    The task_domain_ids field further enhances functionality by providing a way to define a 
    domain for filtering related tasks.
    """

    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    task_domain_ids = fields.Many2many('project.task', string='Tasks', compute='_get_tasks')
    description = fields.Char(string="Description")

    @api.depends('project_id')
    def _get_tasks(self):

        """ This computed method ensures that whenever the project_id field of an attendance record changes,
        the related tasks for that project are computed and stored in the task_domain_ids field. This allows
        for dynamic updating of related tasks based on the selected project.

        Args:
        - self: A recordset containing attendance records.

        Returns:
        - None
        """

        for rec in self:
            if rec.project_id:
                task_ids = self.env['project.task'].search([('project_id', '=', rec.project_id.id), ('fold', '=', False)])
                if task_ids:
                    rec.task_domain_ids = task_ids.ids
                else:
                    rec.task_domain_ids = []
            else:
                rec.task_domain_ids = []