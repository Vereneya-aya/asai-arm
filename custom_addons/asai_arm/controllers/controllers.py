# -*- coding: utf-8 -*-
# from odoo import http


# class AsaiArm(http.Controller):
#     @http.route('/asai_arm/asai_arm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asai_arm/asai_arm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('asai_arm.listing', {
#             'root': '/asai_arm/asai_arm',
#             'objects': http.request.env['asai_arm.asai_arm'].search([]),
#         })

#     @http.route('/asai_arm/asai_arm/objects/<model("asai_arm.asai_arm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asai_arm.object', {
#             'object': obj
#         })

