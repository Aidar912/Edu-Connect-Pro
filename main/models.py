from django.db import models

# Create your models here.


class Student(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    fio = models.CharField(max_length=100, verbose_name="ФИО")
    birthdate = models.DateField(verbose_name="Дата рождения")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    email = models.EmailField()
    admission_year = models.PositiveIntegerField(verbose_name="Год поступления")
    student_id = models.CharField(max_length=20, verbose_name="Номер ст билета")
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True, verbose_name="Фото")
    credits = models.PositiveIntegerField(verbose_name="Количество кредитов")
    STUDENT_TYPES = (
        ('budget', 'Бюджет'),
        ('contract', 'Контракт'),
    )
    student_type = models.CharField(max_length=10, choices=STUDENT_TYPES, verbose_name="Статус студента")
    account = models.OneToOneField('Account', on_delete=models.CASCADE, verbose_name="Счет",
                                   related_name='student_account', null=True)
    transcript = models.OneToOneField('Transcript', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ведомость", related_name='transcripts_for_students')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")

    def __str__(self):
        return self.fio


class Account(models.Model):
    contract_number = models.CharField(max_length=20, verbose_name="Номер контракта")
    date = models.DateField(verbose_name="Дата")
    contract_term = models.DateField(verbose_name="Срок контракта")
    payment_status = models.CharField(max_length=20, verbose_name="Статус оплаты")
    payment_history = models.ForeignKey("PaymentHistory", on_delete=models.CASCADE, verbose_name="История оплаты",
                                        null=True)

    def __str__(self):
        return self.contract_number

    def get_total_payment_amount(self):
        if self.payment_history:
            total_payment_amount = PaymentHistory.objects.filter(account=self).aggregate(models.Sum('amount_paid'))[
                'amount_paid__sum']
            return total_payment_amount or 0
        else:
            return 0


class PaymentHistory(models.Model):
    transaction_number = models.CharField(max_length=20, verbose_name="Номер транзакции")
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Студент")
    payment_date = models.DateField(verbose_name="Дата оплаты")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    PAYMENT_TYPES = (
        ('online', 'Онлайн'),
        ('cash', 'Наличными'),
    )
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, verbose_name="Тип оплаты")

    def __str__(self):
        return self.transaction_number


class Transcript(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Предмет")
    grades = models.ManyToManyField('Grade', verbose_name="Оценки")
    attendance = models.ManyToManyField('Attendance', verbose_name="Времена посещения")

    def __str__(self):
        if self.student:
            return f"{self.student.fio} - {self.subject}"
        else:
            return f"Transcript {self.id} - {self.subject}"


class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Студент")
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, verbose_name="Расписание")
    ATTENDANCE_CHOICES = (
        ('present', 'Был'),
        ('absent', 'Не был'),
        ('sick', 'Болел'),
        ('excused', 'Уважительная причина'),
    )
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, verbose_name="Статус")

    def __str__(self):
        return f"{self.student} - {self.schedule} - {self.status}"
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    subject_code = models.CharField(max_length=20, verbose_name="Номер предмета")
    description = models.TextField(verbose_name="Описание")
    credits = models.PositiveIntegerField(verbose_name="Количество кредитов")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name='Преподаватель')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    fio = models.CharField(max_length=100, verbose_name="ФИО")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    birthdate = models.DateField(verbose_name="Дата рождения")
    phone_number = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    subjects = models.ManyToManyField('Subject', related_name='teachers', verbose_name="Список предметов",blank=True)

    def __str__(self):
        return self.fio


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название кафедры")
    head_of_department = models.CharField(max_length=100, verbose_name="Заведующий кафедрой")
    subjects = models.ManyToManyField('Subject', related_name='departments', verbose_name="Список предметов")
    teachers = models.ManyToManyField('Teacher', related_name='departments', verbose_name="Список преподавателей")

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    year_created = models.PositiveIntegerField(verbose_name='Дата создания')
    subjects = models.ManyToManyField('Subject', related_name='groups', verbose_name='Предметы')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    WEEKDAYS = (
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    )
    weekday = models.CharField(max_length=10, choices=WEEKDAYS, verbose_name="День недели")
    time = models.TimeField(verbose_name="Время")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Предмет")
    LESSON_TYPES = (
        ('lecture', 'Лекция'),
        ('practice', 'Практика'),
    )
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPES, verbose_name='Тип занятий')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name="Преподаватель")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")
    classroom = models.CharField(max_length=20, verbose_name="Аудитория")

    def __str__(self):
        return f"{self.get_weekday_display()}, {self.time} - {self.subject} - {self.classroom}"


class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Предмет")
    grade = models.DecimalField(max_digits=20, decimal_places=1, verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name="Преподаватель")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"


class Library(models.Model):
    book_title = models.CharField(max_length=100, verbose_name="Название книги")
    author = models.CharField(max_length=100, verbose_name="Автор")
    publication_year = models.PositiveIntegerField(verbose_name="Год издания")
    students = models.ManyToManyField('Student', related_name='libraries', verbose_name="Студенты")
    book_file = models.FileField(upload_to='library_books/', verbose_name="Файл для книги")

    def __str__(self):
        return self.book_title


class Test(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название теста")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Предмет")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность (в минутах)")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, verbose_name="Оценка")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name="Преподаватель")
    attempts = models.PositiveIntegerField(verbose_name="Количество попыток")

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название модуля")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    description = models.TextField(verbose_name="Описание модуля")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Предмет")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название сессии")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Предмет")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    subjects = models.ManyToManyField('Subject', related_name='sessions', verbose_name="Предметы")
    students = models.ManyToManyField('Student', related_name='sessions', verbose_name="Студенты")
    grades = models.ManyToManyField('Grade', verbose_name="Оценки")

    def __str__(self):
        return self.name
