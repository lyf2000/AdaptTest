import math
import operator
import random

from django.shortcuts import render
from django.shortcuts import render_to_response, redirect, get_object_or_404

from django.contrib import auth
from django.http import HttpResponseNotFound

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


def index(request):
    return render(request, 'startpage/index.html')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'startpage/profile.html')
    else:
        return redirect('/')


# промежуточная страница при создании теста
@login_required(login_url='/')
def create_test1(request):
    args = {}
    args.update(csrf(request))
    args['form'] = TestCreationForm(instance=request.user)

    if request.method == 'POST':
        form = TestCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=False)

            test = Test()
            test.test_name = form.cleaned_data['test_name']
            test.questions_number = form.cleaned_data['questions_number']
            test.user_creator = request.user
            test.save()
            return redirect('/create_test/{0}/question_creation/{1}'.format(test.id, 1))
        else:
            args['form'] = form
            args['errors'] = form.errors

    return render(request, 'startpage/test_creation_first.html', args)


@login_required(login_url='/')
def question_creation(request, testid, questioncount):
    global QUESTIONCOUNTER, QUESTIONCOUNT
    args = {}
    args.update(csrf(request))
    test = Test.objects.get(id=testid)
    args['form'] = QuestionCreationForm()
    args['question_count'] = questioncount
    questions_number = test.questions_number
    args['questions_number'] = questions_number

    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, test=test)
        if form.is_valid():
            form.save()
            if questions_number != questioncount:
                return redirect('/create_test/{0}/question_creation/{1}'.format(testid, questioncount + 1))
            else:
                return redirect('/create_test/{0}/success/'.format(testid))
        else:
            args['form'] = form
            args['errors'] = form.errors

    return render(request, 'startpage/question_creation.html', args)


@login_required(login_url='/')
def test_created_successfully(request, testid):
    args = {}
    test = Test.objects.get(id=testid)
    args['test_name'] = test.test_name
    args['questions_number'] = test.questions_number
    args['created_questions_number'] = Question.objects.all().filter(test_id=test.id).count()
    return render(request, 'startpage/test_created_successfully.html', args)


@login_required(login_url='/')
def my_created_tests(request):
    user = request.user
    tests = Test.objects.all().filter(user_creator=user)
    args = {}
    args['tests'] = tests
    created_questions_number = {}
    print('tests ', tests)

    for test in tests:
        print('TEST', test)
        created_questions_number['{0}'.format(test_id)] = Question.objects.all().filter(test_id=test.id).count()
        print('Кол-во вопросов созданных : ', test.questions.all().count())
    # args['created_questions_number']['{0}'.format(test_id)] =

    print('CREATED_questions_number', created_questions_number)
    return render(request, 'startpage/my_created_tests.html', args)


@login_required(login_url='/')
def created_questions(request, testid):
    args = {}
    args['test'] = Test.objects.get(id=testid)
    question = Question.objects.all().filter(test_id=testid)
    args['questions'] = question
    return render(request, 'startpage/created_questions.html', args)


@login_required(login_url='/')
def tests_page(request):
    tests = Test.objects.all()
    content = {}
    content['tests'] = tests
    return render(request, 'startpage/tests_page.html', content)


@login_required(login_url='/')
def all_my_attempts(request, testid):
    test = Test.objects.get(id=testid)
    mytests = MyTest.objects.all().filter(test_id=test.id)
    content = {}
    content['test'] = test
    content['mytests'] = mytests
    return render(request, 'startpage/all_my_attempts.html', content)


@login_required(login_url='/')
def test_result(request, testid, mytestid):
    mytest = MyTest.objects.get(id=mytestid)
    qrs = QuestionResult.objects.all().filter(mytest_id=mytest.id)
    print('QRS', qrs)
    content = {}
    content['mytest'] = mytest
    content['qrs'] = qrs
    for qr in qrs:
        print('qr.question.answer_set', qr.question)

    # print('My test id', mytest.id)
    # content['questions'] = mytest.test.questions
    # print('mytest.test', mytest.test)
    # print('mytest.test.id', mytest.test.id)
    # print('mytest.test.questions', mytest.test.questions)
    # print('content[questions]', content['questions'])

    return render(request, 'startpage/test_result.html', content)


# try:
# 	mytest =  MyTest.objects.get(id=mytestid)
# 	content = {}
# 	content['mytest'] = mytest
# 	content['questions'] = mytest.test.questions
# 	return render(request, 'startpage/test_result.html', content)
# except:
# 	print('Нет такого')
# 	return HttpResponseNotFound('<h1>Page not found</h1>')


def login(request):
    if request.user.is_authenticated:
        return render(request, 'startpage/profile.html')
    else:
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


# args = {}
# args.update(csrf(request))
# if request.POST:
# 	username = request.POST.get('username', '')
# 	password = request.POST.get('password', '')
# 	user = auth.authenticate(username=username, password=password)
# 	if user is not None:
# 		auth.login(request, user)
# 		return redirect('/profile')
# 	else:
# 		args['login_error'] = "User is not found"
# 		return render_to_response('startpage/index.html', args)
# else:
# 	return render_to_response('startpage/index.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')


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
    test = Test.objects.get(id=testid)
    return render(request, 'startpage/start_test.html', {'test': test})


current_lvl = 0
wrong_count = 0
correct_count = 0
test_id = 0

QUESTIONS = []
MY_LAST_TEST = MyTest()
MT = MyTest()
current_question = Question()


def start_test(userid, testid):
    # print('Check', User.objects.all().get(id=userid).username)
    global test_id
    test_id = testid
    # user = request.user
    # my_last_test = MyTest.objects.all().filter(test_id=testid, user_id = user.id).order_by('-date').first()

    getinfo('User', User.objects.get(id=userid))
    global MY_LAST_TEST
    MY_LAST_TEST = MyTest.objects.all().filter(test_id=testid, user_id=userid).order_by('-date').first()
    # if len(MY_LAST_TEST) == 0:
    #     MY_LAST_TEST = MyTest(test_id=test_id, user_id=userid)
    #     MY_LAST_TEST.save()
    #     q = Question.objects.all().filter(test_id=testid, )
    getinfo("My last test", MY_LAST_TEST.id)
    global MT
    MT = MyTest(test=MY_LAST_TEST.test, user_id=userid)

    MT.save()

    getinfo('My new test', MT.id)

    get_questions_in_lvl()


def question1(request, testid):
    global current_question, QUESTIONS
    global current_lvl

    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST)
        getinfo('POST', form)
        getinfo('Current question', current_question)

        if form.is_valid():
            print('-----CLEANED DATA RADIOS___', form.cleaned_data['radios'])
            selected_answer_text = request.POST['radios']
            result = make(current_question, selected_answer_text)
            if result:
                return result
        else:
            print(str(form.errors))
    else:
        current_lvl = 1
        print('START TEST')
        user = request.user
        start_test(user.id, testid)

    if len(QUESTIONS) == 0:
        current_lvl += 1
        get_questions_in_lvl()

    getinfo('QUESTIONS', None, *QUESTIONS)
    args = {}
    args.update(csrf(request))

    new_question = QUESTIONS.pop()
    getinfo('New created question', new_question)
    getinfo('After pop', None, *QUESTIONS)

    # make global current question
    current_question = new_question

    form = QuestionAnswerForm()
    form.put_answers(new_question)
    args['form'] = form
    args['question'] = new_question

    return render(request, 'startpage/question.html', args)


def get_questions_in_lvl():
    global current_lvl, correct_count, wrong_count

    getinfo('In get_questions_in_lvl, LVL is', current_lvl)

    if (current_lvl == 6):
        return

    global MY_LAST_TEST
    allQRs = QuestionResult.objects.all().filter(mytest_id=MY_LAST_TEST.id, question__lvl=current_lvl)
    getinfo('Get allQRs', None, *allQRs)

    wrong_answered_questions = list()

    for qr in allQRs:
        if (qr.selected_answer != qr.question.correct_answer):
            wrong_answered_questions.append(qr.question)

    getinfo('Wrong', False, *wrong_answered_questions)

    questions_in_lvl = Question.objects.all().filter(lvl=current_lvl, test_id=MY_LAST_TEST.test.id)
    getinfo('Questions_in_lvl', None, questions_in_lvl)
    question_num_in_lvl = questions_in_lvl.count()
    # getinfo('Question_num_in_lvl', question_num_in_lvl)
    correct_count = math.ceil(question_num_in_lvl / 3)
    getinfo('Correct_count', correct_count)
    wrong_answered_questions = wrong_answered_questions[:math.ceil(correct_count * 2 / 3)]
    # getinfo('Wrong_answered_questions', *wrong_answered_questions)
    wrong_count = math.ceil(correct_count / 3)
    getinfo('Wrong_count', wrong_count)

    rest_questions_in_lvl = list()

    for question in questions_in_lvl:
        if question not in wrong_answered_questions:
            rest_questions_in_lvl.append(question)

    # getinfo('Rest_questions_in_lvl', *rest_questions_in_lvl)

    asked_question_result__list = list()
    not_asked_questions_list = list()

    for i in rest_questions_in_lvl:
        j = QuestionResult.objects.all().filter(question_id=i.id)
        if len(j) != 0:
            asked_question_result__list.append(j.order_by('-mytest__date').first())
        else:
            not_asked_questions_list.append(i)

    getinfo('Not_asked_questions_list ', None, *not_asked_questions_list)

    asked_question_result__list.sort(key=operator.attrgetter('mytest.date'))

    asked_question_result__list.reverse()

    asked_question_list = list()
    for i in asked_question_result__list:
        asked_question_list.append(i.question)

    getinfo('Asked_question_list', None, *asked_question_list)
    random.shuffle(not_asked_questions_list)
    all_rest_questions_list = list()
    for i in not_asked_questions_list:
        all_rest_questions_list.append(i)

    for i in asked_question_list:
        all_rest_questions_list.append(i)

    getinfo('All_rest_questions_list', None, *all_rest_questions_list)
    all_rest_questions_list = all_rest_questions_list[: correct_count - len(wrong_answered_questions)]

    global QUESTIONS
    QUESTIONS = wrong_answered_questions + all_rest_questions_list
    if len(QUESTIONS) == 0:
        getinfo('QUESTIONS', 'Is EMPTY')
        current_lvl += 1
        get_questions_in_lvl()
    else:
        random.shuffle(QUESTIONS)


def make(question, selected_answer_text):
    print('Зашел в make')

    # print('quest:', question)
    global correct_count, wrong_count, MT, current_lvl
    # selected_answer2 = Answer.objects.filter(question_id=question.id)
    # print('Достал selected_answer2 :', selected_answer2)
    getinfo('Selected_answer_text', selected_answer_text)
    getinfo('Make question', question)
    selected_answer = Answer.objects.all().get(question_id=question.id, answer_text=selected_answer_text)
    getinfo('Selected_answer', selected_answer)
    qr = QuestionResult(question=question, mytest=MT, selected_answer=selected_answer)
    getinfo('New QR', qr)

    qr.save()

    question.all_answers_num += 1

    if selected_answer == question.correct_answer:
        getinfo('Answer is', 'Correct')
        question.correct_answers_num += 1
        question.save()
        correct_count -= 1
        getinfo('correct_count is', f'{correct_count}')
        if (correct_count == 0):
            current_lvl += 1
            get_questions_in_lvl()
    else:
        question.save()
        getinfo('Answer is', 'Wrong')
        wrong_count -= 1
        getinfo('wrong_count is', f'{wrong_count}')
        if (wrong_count == 0):
            current_lvl -= 1
            return end_test()

    return False
    # get_questions_in_lvl()


# end


def end_test():
    # new_question_results = QuestionResult.objects.all().filter(mytest=MT)
    #
    # for new_question_result in new_question_results:
    #     question = new_question_result.question
    #     if (question.correct_answer == new_question_result.selected_answer):
    #         question.correct_answers_num += 1
    #     question.all_answers_num += 1
    # \

    global current_lvl, MT

    getinfo('TEST IS ENDED', f'LVL = {current_lvl}')
    change_lvl_of_questions()
    return redirect(f'/tests/{MT.test.id}/result/{MT.id}')


def change_lvl_of_questions():
    getinfo('In change_lvl_of_questions', False)
    global MT
    q = Question.objects.all().filter(question_results__mytest_id=MT.id)

    for i in q:
        all = i.all_answers_num
        correct = i.correct_answers_num
        num = correct / all
        if num < 0.2:
            i.lvl = 1
        elif num < 0.4:
            i.lvl = 2
        elif num < 0.6:
            i.lvl = 3
        elif num < 0.8:
            i.lvl = 4
        else:
            i.lvl = 5
        i.save()


# DO NOT TOUCH!!!!
# CREATE
# def create(request):
#     with open('read.txt', 'r') as f:
#         test = Test.objects.all().get(id=1)
#         for i in range(6):
#             text = f.readline()
#             q = Question(question_text=text, test=test)
#             q.save()
#             for i in range(2):
#                 ans = f.readline()
#                 ans = ans[:len(ans) - 1]
#                 a = Answer(answer_text=ans, question=q)
#                 a.save()
#             q.correct_answer = a
#             q.save()
#
#             return HttpResponse('<h1/>Hi')


def getinfo(text, someth, *args):
    print('------------')
    print(text + ':')
    if someth:
        print(someth)
    if len(args) > 0:
        print(len(args))

        for i in args:
            print('||||', i)
    print('------------')

# DO NOT TOUCH!!!!
# def delete():
#     mt = MyTest.objects.all()
#     for i in mt:
#         if i.id > 4:
#             i.delete()
#             i.save()
#     return HttpResponse('<h1/>QWETYU')
