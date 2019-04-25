from django.shortcuts import render
from django.shortcuts import render_to_response, redirect 
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from .forms import RegistrationForm, QuestionAnswerForm
from .models import *
import math
import operator

#главная страница - вход 
def index(request):
	return render(request, 'startpage/index.html')

#регистрация


#личный кабинет
def profile(request):
	if request.user.is_authenticated:
		return render(request,'startpage/profile.html')
	else: 
		return redirect('/')

#промежуточная страница при создании теста
def create_test1(request):
	return render(request,'startpage/test_creation_first.html')

#страница сооздания теста, где будут вноситься вопросы, варианты ответов и правильный ответы
def create_test2(request):
	return render(request,'startpage/test_creation_second.html')

def test_created_successfully(request):
	return render(request, 'startpage/test_created_successfully.html')

def my_created_tests(request):
	return render(request, 'startpage/my_created_tests.html')

def tests_page(request):
	tests =1212
	return render(request, 'startpage/tests_page.html', {'tests':tests})

def all_my_attempts(request):
	return render(request, 'startpage/all_my_attempts.html')

def test_result(request):
	return render(request, 'startpage/test_result.html')

def question1(request):
	args = {}
	args.update(csrf(request))
	args['form'] = QuestionAnswerForm()

	if request.method == 'POST':
		form = QuestionAnswerForm(request.POST)
		print("Да, это пост!")

		args['errors'] = form.errors

		if form.is_valid():
			print("Да, валид!")
			return redirect('/succes_signup')
	return render(request, 'startpage/question.html', args)


def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/profile')
		else:
			args['login_error'] = "User is not found"
			return render_to_response('startpage/index.html', args)
	else:
		return render_to_response('startpage/index.html', args)

def logout(request):
	auth.logout(request)
	return redirect('/')

def sign_up1(request):
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm ()
	if request.POST:
		new_user_form = UserCreationForm(request.POST)
		if new_user_form.is_valid():
			new_user_form.save()
			return redirect('/')
		else:
			args['form'] = new_user_form
	return render(request, 'startpage/signup.html', args)

def sign_up(request):
	args = {}
	args.update(csrf(request))
	args['form'] = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)


		if form.is_valid():
			form.save()
			return redirect('/succes_signup')


	return render(request, 'startpage/signup.html', args)

def account_created_successfully(request):
	return render(request, 'startpage/success_signup.html')

def start_test_page(request, testid):
	# user = request.user
	# my_last_test = MyTest.objects.all().filter(test_id=testid, user_id = user.id).order_by('-date').first()
	# user = request.user
	# global MY_LAST_TEST
	# MY_LAST_TEST = MyTest.objects.all().filter(test_id=testid, user_id=user.id).order_by('-date').first()
	# # Creating new MyTest
	# global MT
	# MT = MyTest(test=MY_LAST_TEST.test, user=user.id)


	return render(request, 'startpage/start_test.html', {'testid':testid})


def question (request, testid, questionid=12):
	global count
	global lvl
	global correct_count
	global wrong_count

	#
	#Идея! Достаем тут вопросы уровня через метод get_questions_in_lvl
	#он возвращает вопросы,  correct_count, wrong_count
	#42
	#


	while (True):
		if (correct_count == 0):
			break
		correct_count-=1

		args = {}
		args.update(csrf(request))
		args['form'] = QuestionAnswerForm()
		args['count'] = correct_count
		if request.method == 'POST':
			form = QuestionAnswerForm(request.POST)

			print("Да, это пост!")

			args['errors'] = form.errors

			if form.is_valid():
				print("Да, валид!")
		return render(request, 'startpage/question.html', args)

	correct_count = -1
	count = 0
	return redirect('/succes_signup')
#-------------------------------------------------
current_lvl = 0
wrong_count = 0
correct_count = 0
test_id = 0

QUESTIONS = set()
MY_LAST_TEST = MyTest()
MT = MyTest()

def start_test(userid, testid):
	print('Check', User.objects.all().get(id=userid).username)
	global test_id
	test_id = testid
	# user = request.user
	# my_last_test = MyTest.objects.all().filter(test_id=testid, user_id = user.id).order_by('-date').first()

	global MY_LAST_TEST
	MY_LAST_TEST = MyTest.objects.all().filter(test_id=testid, user_id=userid).order_by('-date').first()
	print("Проверка MTL:", MY_LAST_TEST)
	# Creating new MyTest
	global MT
	MT = MyTest(test=MY_LAST_TEST.test, user_id=userid)

	print("Проверка MT:", MT)

	get_questions_in_lvl()

def question1(request, testid):


	if request.method == 'GET':
		global current_lvl
		current_lvl = 1
		print("Проверка левел:", current_lvl)
		user = User.objects.get(username='admin11')
		start_test(user.id, testid)
	print('QUESTIONS', QUESTIONS)
	args = {}
	args.update(csrf(request))

	new_question = QUESTIONS.pop()
	print('Новый вопрос', new_question)
	# args['form'] = QuestionAnswerForm(question=new_question)
	form = QuestionAnswerForm()
	print('Новый вопрос',new_question)
	form.put_answers(new_question)
	args['form'] = form
	args['question'] = new_question
	print('Новый вопрос', new_question)
	print('args[question]',args['question'])

	#form = QuestionAnswerForm(question=new_question)

	if request.method == 'POST':
		form =  QuestionAnswerForm(request.POST)
		print('Это форма:', form)

		if form.is_valid:
			print('Валидна или нет ?', form.is_valid)
			# selected_answer = request.POST['radios']
			selected_answer = form.cleaned_data['radios']
			current_question = form.question1
			print('CURRENT QUESTION:', current_question.question_text)
			#make(form.question, selected_answer)


		# form = QuestionAnswerForm(data=request.POST, question=new_question)
		#
		# print('Форма', form)
		#
		#
		# print('Is VALID?',form.is_valid())
		# print('form.cleaned_data', form.cleaned_data)
		# selected_answer = request.POST['radios']
		# print('selected answer', selected_answer)
		# # selected_answer = form.cleaned_data.get('radios')
		# # print('выбранный ответ',selected_answer )
		# make(new_question, selected_answer)

		# if form.is_valid():
		# 	selected_answer = form.cleaned_data['radios']
		# 	print('выбранный ответ',selected_answer )
		# 	make(new_question, selected_answer)

		#if len(QUESTIONS) == 0:

	return render(request, 'startpage/question.html', args)



def get_questions_in_lvl():
	print('In get_questions_in_lvl')
	global current_lvl
	if (current_lvl == 6):
		pass
	global MY_LAST_TEST
	allQRs = QuestionResult.objects.all().filter(mytest_id = MY_LAST_TEST.id, question__lvl=current_lvl)
	print('Get allQRs: ',allQRs)

	wrong_answered_questions = list()

	for qr in allQRs:
		if (qr.selected_answer != qr.question.correct_answer):
			wrong_answered_questions.append(qr.question)

	print('Wrong:', wrong_answered_questions)

	questions_in_lvl = Question.objects.all().filter(lvl=current_lvl, test_id=MY_LAST_TEST.test.id)
	print('questions_in_lvl', questions_in_lvl)
	question_num_in_lvl = questions_in_lvl.count()
	print('question_num_in_lvl: ', question_num_in_lvl)
	correct_count = math.ceil(question_num_in_lvl / 3)
	print('correct_count: ', correct_count)
	wrong_answered_questions = wrong_answered_questions[:math.ceil(correct_count*2/3)]
	print('wrong_answered_questions: ', wrong_answered_questions)
	wrong_count = math.ceil(correct_count / 3)
	print('wrong_count: ', wrong_count)


	rest_questions_in_lvl = list()

	for question in questions_in_lvl:
		if question not in wrong_answered_questions:
			rest_questions_in_lvl.append(question)

	print('rest_questions_in_lvl ', rest_questions_in_lvl)


	asked_question_result__list = list()
	not_asked_questions_list = list()

	for i in rest_questions_in_lvl:
		j = QuestionResult.objects.all().filter(question_id=i.id)
		if len(j) != 0:
			asked_question_result__list.append(j.order_by('-mytest__date').first())
		else:
			not_asked_questions_list.append(i)


	print('not_asked_questions_list ', not_asked_questions_list)

	asked_question_result__list.sort(key=operator.attrgetter('mytest.date'))


	asked_question_result__list.reverse()

	asked_question_list = list()
	for i in asked_question_result__list:
		asked_question_list.append(i.question)

	print('asked_question_list: ', asked_question_list)
	all_rest_questions_list = list()
	for i in not_asked_questions_list:
		all_rest_questions_list.append(i)

	for i in asked_question_list:
		all_rest_questions_list.append(i)

	print('rest_questions_list: ', all_rest_questions_list)
	all_rest_questions_list = all_rest_questions_list[: correct_count - len(wrong_answered_questions)]

	all_questions_set = set(wrong_answered_questions + all_rest_questions_list)
	global QUESTIONS
	QUESTIONS = all_questions_set
	print('QUESTIONS: ', QUESTIONS)


def make(question, selected_answer):
	print('Зашел в make')
	print('selected_answer:', selected_answer)
	global correct_count, wrong_count, test_id, MT, current_lvl
	selected_answer2 = Answer.objects.filter(question_id=question.id)
	print('Достал selected_answer2 :', selected_answer2)
	qr = QuestionResult(question, MT, selected_answer2)
	print('qr: ',qr)
	qr.save()

	if selected_answer == question.correct_answer:
		correct_count -= 1
		if (correct_count == 0):
			current_lvl += 1
			get_questions_in_lvl()
	else:
		wrong_count -= 1
		if (wrong_count == 0):
			current_lvl -= 1
			pass





# def get_questions_in_lvl(request, current_lvl):
# 	if (current_lvl == 6):
# 		pass
#
# 	allQRs = QuestionResult.objects.all().filter(mytest_id = MY_LAST_TEST.id, question__lvl=current_lvl)
#
# 	wrong_answered_questions = list()
#
# 	for qr in allQRs:
# 		if (qr.selected_answer != qr.question.correct_answer):
# 			wrong_answered_questions.append(qr.question)
#
#
# 	question_num_in_lvl = Question.objects.all().filter(lvl = current_lvl, test_id=MY_LAST_TEST.test.id).count()
# 	correct_count = round(question_num_in_lvl / 3) # 1/3 из всего кол-во вопросов в уровне
# 	wrong_answered_questions = wrong_answered_questions[:math.ceil(correct_count*2/3)]
# 	wrong_count = round(correct_count / 3) # (1/3)/3 из всего кол-во вопросов в уровне
#
#
#
# 	questions_in_lvl = Question.objects.all().filter(lvl = current_lvl, test_id=MY_LAST_TEST.test.id)
#
#
#
# 	rest_questions_in_lvl = list()
#
# 	for question in questions_in_lvl:
# 		if question not in wrong_answered_questions:
# 			rest_questions_in_lvl.append(question)
#
#
#
# 	asked_question_result__list = list()
# 	not_asked_questions_list = list()
#
# 	for i in rest_questions_in_lvl:
# 		j = QuestionResult()
# 		j = QuestionResult.objects.all().filter(question_id=i.id)
# 		if j != None:
# 			asked_question_result__list.append(j.order_by('-mytest__date').first())
#
# 		else:
# 			not_asked_questions_list.append(i)
#
# 	asked_question_result__list.sort(key=operator.attrgetter('mytest.date'))
# 	asked_question_result__list.reverse()
#
#
# 	asked_question_list = list()
# 	for i in asked_question_result__list:
# 		asked_question_list.append(i.question)
#
#
# 	rest_questions_list = list()
# 	for i in not_asked_questions_list:
# 		rest_questions_list.append(i)
#
# 	for i in asked_question_list:
# 		rest_questions_list.append(i)
#
#
# 	rest_questions_list = rest_questions_list[0: correct_count - len(wrong_answered_questions)]
#
# 	all_questions_set = set(wrong_answered_questions + rest_questions_list)
# 	global QUESTIONS
# 	QUESTIONS = all_questions_set
#
# 	new_question = QUESTIONS.pop()
# 	return render(request, '.question_page.html', new_question)
#
# 	preaperead_questions = {
# 		'QUESTIONS': QUESTIONS,
# 		'correct_count':correct_count,
# 		'wrong_count': wrong_count
#
# 	}
#
# 	return preaperead_questions
#
#
#






