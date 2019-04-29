import math
import operator
import random
from . import helper

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
        created_questions_number['{0}'.format(test.id)] = Question.objects.all().filter(test_id=test.id).count()
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





def question1(request, testid):

    if request.method == 'POST':
        form = QuestionAnswerForm(request.POST)

        helper.getinfo('POST', form)
        helper.getinfo('Current question id', request.session['current_question_id'])

        if form.is_valid:
            selected_answer_id = request.POST['radios']
            helper.getinfo('Selected answ id', selected_answer_id)
            result = helper.make(request, selected_answer_id)

            if result:
                return result
        else:
            print(str(form.errors))
    else:
        print('START TEST')
        user = request.user
        helper.start_test(request, user.id, testid)

    QUESTIONS_ID = request.session['QUESTIONS_ID']
    if len(QUESTIONS_ID) == 0:
        request.session['current_lvl'] += 1
        helper.get_questions_in_lvl(request)
    if request.session['current_lvl'] > 5:
        return end_test(request)
    random.shuffle(QUESTIONS_ID)
    helper.getinfo('QUESTIONS_ID', None, *QUESTIONS_ID)
    args = {}
    args.update(csrf(request))
    new_question_id = QUESTIONS_ID.pop()
    helper.getinfo('New created question id', new_question_id)
    helper.getinfo('After pop', None, *request.session['QUESTIONS_ID'])

    request.session['current_question_id'] = new_question_id
    helper.getinfo('Current_question_id', request.session['current_question_id'])
    form = QuestionAnswerForm()
    form.put_answers(new_question_id)
    args['form'] = form
    args['question'] = Question.objects.get(id=new_question_id)

    return render(request, 'startpage/question.html', args)


def end_test(request):

    MT = MyTest.objects.get(id = request.session['MT_ID'])
    current_lvl = request.session['current_lvl']
    helper.getinfo('TEST IS ENDED', f'LVL = {current_lvl}')
    helper.change_lvl_of_questions(request)
    return redirect(f'/tests/{MT.test.id}/result/{MT.id}')