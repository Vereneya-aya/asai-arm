from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestAsaiJob(TransactionCase):

    def setUp(self):
        super().setUp()
        # создаём тестовое задание
        self.job = self.env['asai.job'].create({
            'name': 'Тестовое задание',
            'stage': 'cut',
            'status': 'ready',
        })

    def test_01_take_job(self):
        """Проверка: задание берётся в работу"""
        self.job.action_take()
        self.assertEqual(self.job.status, 'in_progress', "Статус должен стать 'in_progress'")

    def test_02_done_job(self):
        """Проверка: задание переводится в done"""
        self.job.action_take()
        self.job.action_done()
        self.assertEqual(self.job.status, 'done', "Статус должен стать 'done'")
        self.assertIsNotNone(self.job.end_time, "У завершённого задания должно быть время окончания")

    def test_03_scrap_requires_reason(self):
        """Проверка: нельзя отметить брак без причины"""
        with self.assertRaises(UserError):
            self.job.action_scrap()

        self.job.reason = "Трещина в детали"
        self.job.action_scrap()
        self.assertEqual(self.job.status, 'scrap')

    def test_04_blocked_with_reason(self):
        """Проверка: задание можно заблокировать с причиной"""
        self.job.reason = "Нет материала"
        self.job.action_blocked()
        self.assertEqual(self.job.status, 'blocked')