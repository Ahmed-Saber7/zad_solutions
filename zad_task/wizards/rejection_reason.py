# -*- coding: utf-8 -*-

from odoo import models, fields


class RejectionReason(models.TransientModel):
    _name = 'rejection.reason'
    _description = 'Create Rejection Reason'

    rejection_reason = fields.Text(string="Rejection Reason", required=False, )

    def confirm(self):
        active_id = self.env.context.get('active_id')
        object = self.env['purchase.request'].browse(active_id)
        object.rejection_reason = self.rejection_reason
        object.state = 'reject'
