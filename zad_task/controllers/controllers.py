# -*- coding: utf-8 -*-
# from odoo import http


# class ZadTask(http.Controller):
#     @http.route('/zad_task/zad_task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zad_task/zad_task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zad_task.listing', {
#             'root': '/zad_task/zad_task',
#             'objects': http.request.env['zad_task.zad_task'].search([]),
#         })

#     @http.route('/zad_task/zad_task/objects/<model("zad_task.zad_task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zad_task.object', {
#             'object': obj
#         })
