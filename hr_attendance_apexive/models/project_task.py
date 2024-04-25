# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    """ This ProjectTask model extends the existing project.task model by adding a new Boolean field fold, 
    which controls the visibility of tasks in the Kanban view. The value of this field is related to the fold
     field of the task's stage, allowing for dynamic folding behavior based on the task's stage.
    """

    fold = fields.Boolean(string="Folded in Kanban", related='stage_id.fold', store=True)
