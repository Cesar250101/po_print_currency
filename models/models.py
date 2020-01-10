# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta

class ImprimirOrdenCompra(models.Model):
    _inherit = 'purchase.order'

    imprimir_moneda_extranjera = fields.Boolean(string="Imprimir en moneda extranjera",  )
    moneda_adic = fields.Many2one(comodel_name="res.currency", string="Moneda Adicional", required=False, )
    tasa_cambio = fields.Float(string="Tasa de Cambio",  required=False, store=True)

    @api.model
    @api.onchange('moneda_adic')
    def _onchange_moneda_Adic(self):
        if self.tasa_cambio in(1,0):
            tasacambio=1
            strfecha=self.date_order[0:10]
            paridades=self.env["res.currency.rate"].search([('currency_id','=',self.moneda_adic.id)])
            for i in paridades:
                if i.name==strfecha:
                    tasacambio=i.inverse_rate
            self.tasa_cambio=tasacambio

class ImprimirOrdenCompraLinea(models.Model):
    _inherit = 'purchase.order.line'

    precio_dolar = fields.Float(string="Precio en Dolar",  required=False, store=True)

    @api.model
    @api.onchange('precio_dolar')
    def _onchange_precio_dolar(self):
        if self.order_id.tasa_cambio!=0:
            precio_unitario=self.precio_dolar*self.order_id.tasa_cambio
        self.price_unit = precio_unitario



