# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    fold = fields.Boolean(string="Folded in Kanban", related='stage_id.fold', store=True)
