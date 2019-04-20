from django.shortcuts import render
from django.shortcuts import render_to_response, redirect 
from django.contrib import auth 
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

# Hit 'Start Test'--> make POST[user.id, test.id]
def startTest(self, user_id, test_id):
	
    # Searhing for last user's test  
	my_last_test = MyTest.objects.all().filter(user.id == user_id && test.id == test_id).filter('-date')[0]
	# Creating new MyTest
	mt = MyTest(test=my_last_test, user=user_id)
	startTestInLvl(my_last_test, 1, mt)

# By defining lvl we're construct list of wrong answers from my_last_test
def startTestInLvl(self, my_last_test, currett_lvl, mt):

	allQRs = QuestionResult.objects.all().filter(mytest.id == my_last_test.id && question.lvl == lvl)

	question_num_in_lvl = Question.objects.all().filter(lvl == current_lvl)
	someth = allQRs.filter(question__correct_answer.id != selected_answer.id)[:2 * round(round(question_num_in_lvl / 3) / 3) ]
	for i in someth
		wrong_questions.append(someth.question)
	newquestion = wrong_questions.pop() #last
	return(request, '.http', newquestion, mt, wrong_questions)


# вызвать функцию через другую ф-ию , но только с методом ПОСТ???


# Hit 'Next Question'
def newQuestion(self, wrong_count, correct_count, question, selected_answer, wrong_questions, mt):
    
    
	if selected_answer == question.correct:
    	correct_count--
    	if (correct_count == 0):
    		#lvl up
    	newquestion = wrong_count.pop()
    	qr = QR(newQuestion, mt, selected_answer)

    else:
    	wrong_count--
    	if (wrong_count == 0):
    		# end
    	correct_count += 2

    return (request, wrong_count, correct_count, question, wrong_questions, mt)