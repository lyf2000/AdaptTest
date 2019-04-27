import math
import operator
import random

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from .forms import RegistrationForm, QuestionAnswerForm
from .models import *


# главная страница - вход
def index(request):
    return render(request, 'startpage/index.html')


# регистрация


# личный кабинет
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'startpage/profile.html')
    else:
        return redirect('/')


# промежуточная страница при создании теста
def create_test1(request):
    return render(request, 'startpage/test_creation_first.html')


# страница сооздания теста, где будут вноситься вопросы, варианты ответов и правильный ответы
def create_test2(request):
    return render(request, 'startpage/test_creation_second.html')


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
    args['form'] = UserCreationForm()
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

    return render(request, 'startpage/start_test.html', {'testid': testid})


def question(request, testid, questionid=12):
    global count
    global lvl
    global correct_count
    global wrong_count

    #
    # Идея! Достаем тут вопросы уровня через метод get_questions_in_lvl
    # он возвращает вопросы,  correct_count, wrong_count
    # 42
    #

    while (True):
        if (correct_count == 0):
            break
        correct_count -= 1

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


# -------------------------------------------------
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

    global MY_LAST_TEST
    MY_LAST_TEST = MyTest.objects.all().filter(test_id=testid, user_id=userid).order_by('-date').first()
    getinfo("My last test", MY_LAST_TEST.id)
    global MT
    MT = MyTest(test=MY_LAST_TEST.test, user_id=userid)

    MT.save()

    getinfo('My new test', MT.id)

    get_questions_in_lvl()


def question1(request, testid):
    global current_question, QUESTIONS

    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST)
        getinfo('POST', form)
        getinfo('Current question', current_question)

        if form.is_valid:
            selected_answer_text = request.POST['radios']
            result = make(current_question, selected_answer_text)
            if result:
                return result
    else:
        global current_lvl
        current_lvl = 1
        print('START TEST')
        user = User.objects.get(username='admin11')
        start_test(user.id, testid)

    if len(QUESTIONS) == 0:
        return end_test()

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
    # print('questions_in_lvl', questions_in_lvl)
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

    global current_lvl

    getinfo('TEST IS ENDED', f'LVL = {current_lvl}')
    change_lvl_of_questions()
    return HttpResponse(f'<h1/>{current_lvl}')


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


# CREATE
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


# DO NOT TOUCH!!!!


# DO NOT TOUCH!!!


# DO NOT TOUCH!!!

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


# def delete():
#     mt = MyTest.objects.all()
#     for i in mt:
#         if i.id > 4:
#             i.delete()
#             i.save()
#     return HttpResponse('<h1/>QWETYU')