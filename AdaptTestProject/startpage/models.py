from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


# Create your models here.


class Test(models.Model):
	test_name = models.CharField(max_length=100) #LENGTH
	questions_number = models.PositiveIntegerField()
	user_creator = models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return f'{self.test_name}: {self.questions_number}'


class Question(models.Model):
	correct_answers_num = models.PositiveIntegerField(default=0)
	all_answers_num = models.PositiveIntegerField(default=0)

	question_text = models.CharField(max_length=250)
	correct_answer = models.OneToOneField('Answer', on_delete=models.CASCADE, related_name = 'question_correct_answer', null=True, blank=True)
	test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name = 'questions')
	lvl = models.PositiveSmallIntegerField(default=1)

	def __str__(self):
		return f'{self.question_text}, lvl={self.lvl}'


class Answer(models.Model):
	answer_text = models.CharField(max_length=20)
	question = models.ForeignKey('Question', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.answer_text} from {self.question}'


class MyTest(models.Model):
	test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='mytest_test')
	date = models.DateTimeField(default = timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mytest_user')

	def __str__(self):
		return f'{self.test}, {self.user}, {self.date}'


class QuestionResult(models.Model):
	question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question_results')
	mytest = models.ForeignKey('MyTest', on_delete=models.CASCADE, related_name='mytests')
	selected_answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='selected_answer')

	def __str__(self):
		return f'{self.question}, {self.selected_answer}'
