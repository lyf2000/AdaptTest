from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.


class Test(models.Model):
	test_name = models.CharField(max_length=100) #LENGTH
	questions_number = models.PositiveIntegerField()
	user_creator = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.test_name}: {self.questions_number}'


class Question(models.Model):
	#static
	correct_answers_num = models.PositiveIntegerField(default=0)
	all_answers_num = models.PositiveIntegerField(default=0)

	question_text = models.CharField(max_length=250)
	correct_answer = models.OneToOneField('Answer')
	test = models.ForeignKey('Test', on_delete=models.CASCADE)
	lvl = models.PositiveSmallIntegerField(default=1)

	def __str__(self):
		return f'{question_text}, lvl={self.lvl}'


class Answer(models.Model):
	answer_text = models.CharField(max_length=20)
	question = models.ForeignKey('Question', on_delete=models.CASCADE)

	def __str__(self):
		return f'{answer_text} from {question}'


class MyTest(models.Model):
	test = models.OneToOneField('Test', on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey('User', on_delete=models.CASCADE)


class QuestionResult(models.Model):
	question = models.OneToOneField('Question')
	mytest = models.ForeignKey('Mytest', on_delete=models.CASCADE)
	selected_answer = models.OneToOneField('Answer')

