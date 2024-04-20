from django.conf import settings
from django.db import models
from django.urls import reverse


class Exam(models.Model):
    title = models.CharField(verbose_name='Название экзамена', max_length=30, unique=True)
    authors = models.ManyToManyField(verbose_name='Организация, проводящая экзамен', to=settings.AUTH_USER_MODEL, db_table='exam_authors',
                                     related_name='authors')
    description = models.TextField(verbose_name='Описание экзамена', max_length=200)
    start_date = models.DateField(verbose_name='Дата проведения экзамена')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность')
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True)
    # count_lessons = models.PositiveIntegerField(verbose_name='Количество уроков')

    class Meta:
        verbose_name_plural = 'Экзамены'
        verbose_name = 'Экзамен'
        ordering = ['title']
        # Set permissions for model in format: (<codename>, <name>) where field <name> - comment
        permissions = (
            ('modify_exam', 'Can modify exam content'),
        )

    def __str__(self):
        return f'{self.title}: Старт {self.start_date}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'course_id': self.pk})


class Tracking(models.Model):
    exam = models.ForeignKey(verbose_name='Экзамен', to=Exam, on_delete=models.PROTECT)
    user = models.ForeignKey(verbose_name='Ученик', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    passed = models.BooleanField(verbose_name='Пройден?', default=None)

    class Meta:
        ordering = ['-user']
