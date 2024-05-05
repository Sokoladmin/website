from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from .functions import get_timestamp_path_user


class VarCharField(models.CharField):
    def db_type(self, connection):
        longtext: str = super().db_type(connection)
        varchar: str = longtext.replace('longtext', 'varchar')
        return varchar


class User(AbstractUser):
    # username_validator = UnicodeUsernameValidator()

    patronymic = models.CharField(verbose_name='Отчество', max_length=150, blank=False)
    birthday = models.DateField(verbose_name='Дата рождения', blank=False, null=True)
    gen = [
        (1, 'Мужской'),
        (2, 'Женский')
    ]
    gender = models.PositiveSmallIntegerField(verbose_name='Пол', choices=gen, blank=False)
    email = models.EmailField(verbose_name='Email', unique=True)
    phone_regex_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                           message="Номер телефона должен быть в формате: '+999999999'. "
                                                   "Допускается до 15 цифр.")
    phone_number = models.CharField(verbose_name='Номер телефона', validators=[phone_regex_validator], max_length=17,
                                    blank=False)
    snils = models.FileField(verbose_name='СНИЛС', blank=False, upload_to=get_timestamp_path_user,
                             validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                message='Выберите файл в формате PDF')])
    inn = models.CharField(verbose_name='ИНН', max_length=150, blank=True)
    avatar = models.ImageField(verbose_name='Фото', blank=True, upload_to=get_timestamp_path_user,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'bmp', 'png'],
                                                                  message='Выберите файл в формате PDF')])
    passport = models.FileField(verbose_name='Паспорт', blank=False, upload_to=get_timestamp_path_user,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                   message='Выберите файл в формате PDF')])
    name_change_document = models.FileField(verbose_name='Документ о перемене имени', blank=True,
                                            upload_to=get_timestamp_path_user,
                                            validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                               message='Выберите файл в формате PDF')])
    document_on_marriage_or_divorce = models.FileField(verbose_name='Документ о заключении или расторжении брака',
                                                       blank=True, upload_to=get_timestamp_path_user,
                                                       validators=[
                                                           FileExtensionValidator(allowed_extensions=['pdf'],
                                                                                  message='Выберите файл в формате PDF')
                                                       ])
    other_document1 = models.FileField(verbose_name='Иной документ', blank=True, upload_to=get_timestamp_path_user,
                                       validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                          message='Выберите файл в формате PDF')])
    bachelors_diploma = models.FileField(verbose_name='Диплом бакалавра', blank=False,
                                         upload_to=get_timestamp_path_user,
                                         validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                            message='Выберите файл в формате PDF')])
    masters_diploma = models.FileField(verbose_name='Диплом магистра', blank=True, upload_to=get_timestamp_path_user,
                                       validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                          message='Выберите файл в формате PDF')])
    employment_history = models.FileField(verbose_name='Трудовая книжка', blank=False,
                                          upload_to=get_timestamp_path_user,
                                          validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                             message='Выберите файл в формате PDF')])
    advanced_training_certificate = models.FileField(verbose_name='Сертификат о повышении квалификации ', blank=True,
                                                     upload_to=get_timestamp_path_user,
                                                     validators=[
                                                         FileExtensionValidator(allowed_extensions=['pdf'],
                                                                                message='Выберите файл в формате PDF')])
    other_document2 = models.FileField(verbose_name='Иной документ', blank=True, upload_to=get_timestamp_path_user,
                                       validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                          message='Выберите файл в формате PDF')])
    nostroy = models.FileField(verbose_name='Уведомление о включении в НРС НОСТРОЙ', blank=True,
                               upload_to=get_timestamp_path_user,
                               validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                  message='Выберите файл в формате PDF')])
    nopriz = models.FileField(verbose_name='Уведомление о включении в НРС НОПРИЗ', blank=True,
                              upload_to=get_timestamp_path_user,
                              validators=[FileExtensionValidator(allowed_extensions=['pdf'],
                                                                          message='Выберите файл в формате PDF')])
    data_processing_agreement = models.FileField(verbose_name='Согласие на обработку данных', blank=False,
                                                 upload_to=get_timestamp_path_user,
                                                 validators=[
                                                     FileExtensionValidator(allowed_extensions=['pdf'],
                                                                            message='Выберите файл в формате PDF')])



   # is_nrs = models.BooleanField(verbose_name='Загружен НРС?', default=True)



    # username = models.CharField(
    #     max_length=150,
    #     unique=False,
    #     help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    #     validators=[username_validator],
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'
        ordering = ['last_name']

    def natural_key(self):
        return self.get_full_name()

    def __str__(self):
        return f'Участник {self.first_name} {self.last_name}: {self.email}'