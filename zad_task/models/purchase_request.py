# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('cancel', 'Cancel')], required=True, default='draft', )

    request_name = fields.Char(string="Request name", required=True, )

    requested_by = fields.Many2one(comodel_name="res.users", string="Requested by", required=True,
                                   default=lambda self: self.env.user)

    start_date = fields.Date(string="Start Date", required=False, default=fields.Datetime.now)

    end_date = fields.Date(string="End Date", required=False, )

    rejection_reason = fields.Text(string="Rejection Reason", required=False, )

    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id,
                                 required="1")

    order_lines = fields.One2many('purchase.request.line', 'purchase_request_reference',
                                  string="Order Lines")
    total_price = fields.Float(string="Total Price", required=False, compute="_get_total_price")

    @api.depends('order_lines')
    def _get_total_price(self):
        if self.order_lines:
            for line in self.order_lines:
                self.total_price += line.total
        else:
            self.total_price = 0.0

    def submit_for_approval(self):
        self.state = 'to_be_approved'

    def cancel(self):
        self.state = 'cancel'

    def reset_to_draft(self):
        self.state = 'draft'

    def approve(self):
        self._action_send_email()
        # self.state = 'approve'

    # TODO function to send email to all user in purchase manager group
    def _action_send_email(self):
        if self.state == "to_be_approved":
            template_id = self.env.ref('zad_task.mail_template_data_purchase_request')
            for use in self:
                group_purchase_manager = use.env.ref(
                    'purchase.group_purchase_manager').users
                users_list = group_purchase_manager
                print(users_list)
                print(use.company_id.email)
                for user_work_email in users_list:
                    employee_login_email = user_work_email.login
                    template_id.subject = "Purchase Request : %s" % user_work_email.name
                    template_id.email_from = use.company_id.email
                    template_id.email_to = employee_login_email
                    template_id.body_html = """
                   <div style="margin: 10px auto;direction:ltr;">
                   <p> Purchase Request ( ${object.request_name} ) has been approved </p>
                   </div>
                   """
                    template_id.send_mail(use.id, force_send=True)
                    print("ahmed")


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'

    product_id = fields.Many2one('product.product', string="Product Id", required=True)
    description = fields.Char(string="Description", required=False, related="product_id.name")
    quantity = fields.Float(string="Quantity", required=False, default=1)
    cost_price = fields.Float(string="Cost Price", required=False, related="product_id.standard_price")
    total = fields.Float(string="Total", required=False, compute="_get_total_price")
    purchase_request_reference = fields.Many2one(comodel_name="purchase.request", required=False)

    @api.depends('product_id', 'quantity', 'cost_price')
    def _get_total_price(self):
        for rec in self:
            if rec.product_id and rec.quantity and rec.cost_price:
                rec.total = rec.quantity * rec.cost_price
            else:
                rec.total = 0.0
