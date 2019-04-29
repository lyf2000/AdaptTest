from django.contrib.auth.models import User
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import ModelForm
import random
from .  import views

from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Enter username"}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Enter email"}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Enter name"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Enter lastname"}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Enter password", 'type':"password" }))
    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Enter password again", 'type':"password" }))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

class QuestionAnswerForm(forms.Form):
    radios = forms.ChoiceField(widget=forms.RadioSelect(), label="Chose answer")
    # question = Question()
    CHOICES = []
    question1 = Question()

    def put_answers (self, question_id):
        # views.getinfo(f'In put_answers  {views.wrong_count}', question)

        all_answers = Answer.objects.all().filter(question_id=question_id)


        all_answers = all_answers.order_by('?')

        for answer in all_answers:
            # print('answer', answer)
            self.CHOICES.append((answer.id, answer.answer_text))
        self.fields['radios'].choices = self.CHOICES

        self.CHOICES.clear()

class TestCreationForm(ModelForm):
    class Meta:
        model = Test
        fields = ('test_name', 'questions_number')

        widgets = {
            'test_name': forms.TextInput(attrs={ 'type':'text','class': 'form-control', 'placeholder':'Enter test name'}),
            'questions_number': forms.TextInput(attrs={'type':'number', 'class': "form-control", 'placeholder':'10'})
        }

    def clean_questions_number(self):
        quest_num = self.cleaned_data['questions_number']

        if (quest_num < 10):
            raise ValidationError('Question number can not be less than 10')
        if (quest_num > 300):
            raise  ValidationError('Question number can not be greater than 300')
        return quest_num

class QuestionCreationForm(forms.Form):
    question_text = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter the question text"}))
    answer1 = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter 1st answer"}))
    answer2 = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter 2nd answer"}))
    answer3 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter 3d answer"}))
    correct_answer = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter 4th and correct answer"}))

    test = Test()

    def get_test_id(self):
        return self.test

    def __init__(self, *args, **kwargs):
        self.test = kwargs.pop('test', None)
        super(QuestionCreationForm, self).__init__(*args, **kwargs)

    def save(self):
        new_question =  Question()
        ans1 = Answer()
        ans2 = Answer()
        ans3 = Answer()


        new_question.question_text = self.cleaned_data['question_text']
        new_question.lvl = 1
        new_question.correct_answers_num = 0
        new_question.all_answers_num = 0
        new_question.test = self.test
        new_question.save()


        ans1.answer_text = self.cleaned_data['answer1']
        ans1.question = new_question
        ans1.save()

        ans2.answer_text = self.cleaned_data['answer2']
        ans2.question = new_question
        ans2.save()

        ans3.answer_text = self.cleaned_data['answer3']
        ans3.question = new_question
        ans3.save()

        cor_ans = Answer()
        cor_ans.answer_text = self.cleaned_data['correct_answer']
        print('NEW QUESTION', new_question)
        cor_ans.question = new_question
        cor_ans.save()
        new_question.correct_answer = cor_ans
        new_question.save()








