from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """
    Рассылка(настройки).
    """
    TIME_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('finished', 'Завершена'),
    )

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    send_datetime = models.TimeField()
    frequency = models.CharField(max_length=10, choices=TIME_CHOICES)
    status = models.CharField(max_length=20, default=STATUS_CHOICES, choices=STATUS_CHOICES)

    send_from_user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='отправитель')

    send_to_client = models.ManyToManyField(
        to='main.Client',
        related_name='client',
        verbose_name='получатель')

    is_active = models.BooleanField(
        default=True,
        verbose_name='активен')
    """
    Сообщение для рассылки.
    """
    subject = models.CharField(
        max_length=255,
        verbose_name='тема письма')
    message = models.TextField(
        verbose_name='сообщение')

    def __str__(self):
        return f"Рассылка {self.subject}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    server_response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f"Лог рассылки {self.mailing}"

    class Meta:
        verbose_name = 'Логи рассылка'
        verbose_name_plural = 'Логи рассылки'
