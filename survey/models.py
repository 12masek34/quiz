from django.db import models


class Question(models.Model):
    text = models.TextField(verbose_name='Вопрос')

    def __str__(self):
        return self.text


class Choice(models.Model):
    text = models.CharField(verbose_name='Ответ', max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    uuid = models.CharField(max_length=255)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
