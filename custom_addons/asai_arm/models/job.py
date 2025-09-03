from odoo import api, fields, models
from odoo.exceptions import UserError


class AsaiJob(models.Model):
    _name = "asai.job"
    _description = "ASAI Job (Задание/Деталь)"

    name = fields.Char(string="Имя", required=True)
    stage = fields.Selection([
        ('cut', 'Раскрой'),
        ('edge', 'Кромка'),
        ('drill', 'Присадка'),
        ('pack', 'Упаковка'),
    ], string="Этап", default='cut', required=True)

    status = fields.Selection([
        ('ready', 'Готово к работе'),
        ('in_progress', 'В работе'),
        ('done', 'Готово'),
        ('scrap', 'Брак'),
        ('blocked', 'Невозможно выполнить'),
    ], string="Статус", default='ready', index=True)

    priority = fields.Integer(string="Приоритет", default=0)
    start_time = fields.Datetime(string="Начало")
    end_time = fields.Datetime(string="Окончание")
    duration = fields.Float(string="Длительность, ч", compute="_compute_duration", store=True)

    operator_ids = fields.Many2many('res.users', string="Операторы")
    drawing_url = fields.Char(string="Чертёж (URL)")

    # Поле для причины брака или блокировки
    reason = fields.Text(string="Причина")

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                rec.duration = (rec.end_time - rec.start_time).total_seconds() / 3600.0
            else:
                rec.duration = 0.0

    def action_take(self):
        for rec in self:
            if rec.status == 'in_progress':
                continue
            rec.status = 'in_progress'
            rec.start_time = fields.Datetime.now()
            if self.env.user not in rec.operator_ids:
                rec.operator_ids = [(4, self.env.user.id)]

    def action_done(self):
        for rec in self:
            if rec.status != 'in_progress':
                raise UserError("Задание должно быть 'В работе'.")
            rec.end_time = fields.Datetime.now()
            rec.status = 'done'

    def action_scrap(self):
        for rec in self:
            if not rec.reason:
                raise UserError("Укажите причину брака перед подтверждением.")
            rec.status = 'scrap'

    def action_blocked(self):
        for rec in self:
            if not rec.reason:
                raise UserError("Укажите причину блокировки перед подтверждением.")
            rec.status = 'blocked'