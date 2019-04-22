from django.shortcuts import render
from django.shortcuts import render_to_response, redirect 
from django.contrib import auth
from .models import *
from django.template.context_processors import csrf

#главная страница - вход 
def index(request):
	return render(request, 'startpage/index.html')

#регистрация
def sign_up(request):
	return render(request, 'startpage/signup.html')

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
	return render(request, 'startpage/tests_page.html')

def all_my_attempts(request):
	return render(request, 'startpage/all_my_attempts.html')

def test_result(request):
	return render(request, 'startpage/test_result.html')

def start_test(request):
	return render(request, 'startpage/start_test.html')

def question(request):
	return render(request, 'startpage/question.html')

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









#DAMIR

# Hit 'Start Test'--> send POST[user.id, test.id]
def startTest(self, user_id, test_id):

	# Searhing for last user's test
	my_last_test = MyTest.objects.all().filter(user_id == user_id and test_id == test_id).orderby('date')[0]
	# Creating new MyTest
	mt = MyTest(test=my_last_test.test, user=user_id)
	startTestInLvl(my_last_test, 1, mt) # ---> startTestInLvl()

# By defining lvl we're construct list of wrong answers from my_last_test
def startTestInLvl(my_last_test, current_lvl, mt):

	if (current_lvl == 6):
		pass


	allQRs = QuestionResult.objects.all().filter(mytest_id == my_last_test.id and question.lvl == current_lvl)

	question_num_in_lvl = Question.objects.all().filter(lvl == current_lvl).count()
	correct_count = round(question_num_in_lvl / 3)
	wrong_count = round(correct_count / 3)

	someth = allQRs.filter(question__correct_answer.id != selected_answer_id)[:2 * correct_count]
	wrong_questions = []
	for i in someth:
		wrong_questions.append(i.question)	

	someth = QuestionResult.objects.all().orderby('mytest__date').exclude(question__in = wrong_questions)
	newlist = []

	for i in someth:
		if (i.question not in newlist):
			newlist.append(i.question)

	newlist.reverse()
	newlist = newlist[0 : correct_count - wrong_questions.length + (2 * (wrong_count - 1))]



	heh = set(wrong_questions) + set(newlist)
	
	newquestion = heh.pop()

	return(request, '.http', newquestion, mt, heh, wrong_count, correct_count)


# Hit 'Next Question'
def newQuestion(request, wrong_count, correct_count, question, selected_answer, heh, mt):
    
    qr = QuestionResult(Question, mt, selected_answer)
    qr.save()

	if selected_answer == question.correct:
		correct_count = correct_count - 1
		if (correct_count == 0):
			startTestInLvl(Mytest.objects.all().filter(test = mt.test)[-2], question.lvl+1, mt)#???
		# else:
		wrong_count -= 1
		if (wrong_count == 0):
			# end
			pass
		correct_count += 2

    newquestion = wrong_count.pop()	

    return (request, wrong_count, correct_count, newquestion, heh, mt)

# end
def result(request, mt, )
	#quest+=1

	