from django.core.validators import RegexValidator
from django.db import models


class MainPageInfo(models.Model):
    tagline = models.CharField(max_length=255, verbose_name='Слоган')
    center_mission = models.CharField(max_length=255, verbose_name='Місія центру')

    def __str__(self):
        return self.tagline

    class Meta:
        verbose_name = 'Головна сторінка'
        verbose_name_plural = 'Головна сторінка'
        ordering = ["id"]


class ReasonToChoose(models.Model):
    text = models.CharField(max_length=255, verbose_name='Чому варто обрати?')
    reason_to_choose_id = models.ForeignKey('MainPageInfo', on_delete=models.CASCADE, related_name='reasons_to_choose')

    def __str__(self):
        return self.text


class Advantage(models.Model):
    text = models.CharField(max_length=255, verbose_name='Наші переваги')
    advantage = models.ForeignKey('MainPageInfo', on_delete=models.CASCADE, related_name='advantages')

    def __str__(self):
        return self.text


class Discount(models.Model):
    text = models.CharField(max_length=255, verbose_name='Знижки')
    discount = models.ForeignKey('MainPageInfo', on_delete=models.CASCADE, related_name='discounts')

    def __str__(self):
        return self.text


class SmallDescription(models.Model):
    text = models.CharField(max_length=255, verbose_name='Маленький Мудрик - це...')
    description = models.ForeignKey('MainPageInfo', on_delete=models.CASCADE, related_name='descriptions')

    def __str__(self):
        return self.text


class InfoForParents(models.Model):
    title = models.CharField(max_length=255, verbose_name='Батькам (жирний шрифт)')
    text = models.CharField(max_length=255, verbose_name='Батькам')
    for_parents = models.ForeignKey('MainPageInfo', on_delete=models.CASCADE, related_name='info_for_parents')

    def __str__(self):
        return self.text


class TeamMember(models.Model):
    name = models.CharField(max_length=255, verbose_name='ПІБ')
    photo = models.ImageField(upload_to='team_members/%Y/%m/%d')
    description = models.TextField(verbose_name='Опис')

    class Meta:
        verbose_name = 'Член команди'
        verbose_name_plural = 'Члени команди'
        ordering = ["id"]

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=255, verbose_name='Питання')
    answer = models.TextField(verbose_name='Відповідь')

    class Meta:
        verbose_name = 'Часте питання'
        verbose_name_plural = 'Часті питання'
        ordering = ["id"]

    def __str__(self):
        return self.question


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва курсу')
    max_members = models.PositiveIntegerField(verbose_name='Максимальна кількість учнів на занятті')
    price = models.CharField(max_length=255, verbose_name='Опис вартості курсу чи уроку курсу')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'
        ordering = ["id"]

    def __str__(self):
        return self.name


class TextForCourse(models.Model):
    text = models.TextField(blank=True, verbose_name="Текст для заповнення курсу (необов'язково)")
    text_for_course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='text_for_course')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Блок текста>'
        verbose_name_plural = 'Блоки текста'
        ordering = ["id"]


class TextWithListForCourse(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    under_title = models.CharField(blank=True, max_length=255, verbose_name="Підзаголовок (необов'язково)")
    text_with_list_for_course = models.ForeignKey('Course', on_delete=models.CASCADE,
                                                  related_name='text_with_list_for_course')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блок текста зі списком'
        verbose_name_plural = 'Блоки текста зі списком'
        ordering = ["id"]


class ListItemForText(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст елемента списку')
    list_item_for_text = models.ForeignKey('TextWithListForCourse', on_delete=models.CASCADE,
                                           related_name='list_item_for_text')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Елемент списка'
        verbose_name_plural = 'Елементи списка'
        ordering = ["id"]


class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name='ПІБ')
    email = models.EmailField(max_length=255, verbose_name='email')
    feedback_text = models.TextField(verbose_name="Відгук")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    is_published = models.BooleanField(default=False, verbose_name='Показувати на сайті')
    phone_message = 'Номер телефону повинен бути введений у такому форматі: 0639999999'
    phone_regex = RegexValidator(
        regex=r"\d{10}",
        message='Номер телефону повинен бути введений у такому форматі: 0639999999'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ["id"]


class Proposal(models.Model):
    name = models.CharField(max_length=255, verbose_name='ПІБ')
    email = models.EmailField(max_length=255, verbose_name='email')
    proposal_text = models.TextField(verbose_name="Пропозиція")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    phone_message = 'Номер телефону повинен бути введений у такому форматі: 0639999999'
    phone_regex = RegexValidator(
        regex=r"\d{10}",
        message=phone_message
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пропозиція'
        verbose_name_plural = 'Пропозиції'
        ordering = ["id"]


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва курсу')
    datetime_start = models.DateTimeField(verbose_name='Дата та час початку урока')
    max_participants = models.PositiveIntegerField(verbose_name='Максимальна кількість учнів на занятті')
    current_participants = models.PositiveIntegerField(default=0, verbose_name='Поточна кількість учнів на це заняття')

    def __str__(self):
        return f"{self.title}  ({self.datetime_start})"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ["id"]


class Record(models.Model):
    parent_name = models.CharField(max_length=255, verbose_name="Ім'я та прізвище одного з батьків")
    child_name = models.CharField(max_length=255, verbose_name="Ім'я та прізвище дитини")
    email = models.EmailField(max_length=255, verbose_name='email')
    phone_message = 'Номер телефону повинен бути введений у такому форматі: 0639999999'
    phone_regex = RegexValidator(
        regex=r"\d{10}",
        message=phone_message
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True, null=True, verbose_name='Телефон')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='records')

    def __str__(self):
        return f"{self.parent_name} - {self.child_name} ({self.lesson.title})"

    class Meta:
        verbose_name = 'Запис'
        verbose_name_plural = 'Записи'
        ordering = ["id"]


class Contact(models.Model):
    email = models.EmailField(max_length=255, verbose_name='email')
    facebook_link = models.URLField(blank=True, null=True, verbose_name='Посилання на Facebook сторінку')
    instagram_link = models.URLField(blank=True, null=True, verbose_name='Посилання на Instagram сторінку')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адреса')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'
        ordering = ["id"]


class Phone(models.Model):
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name='phones')

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'Номер телефону'
        verbose_name_plural = 'Номера телефонів'
        ordering = ["id"]
