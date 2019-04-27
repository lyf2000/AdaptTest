from django.contrib.auth.models import User
from django import forms
from .models import Question, Answer, QuestionResult
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import ModelForm
from .  import views

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

    # def clean_username(self):
    #     username =  self.cleaned_data['username']
    #
    #     try:
    #         match = User.objects.get(username=username)
    #     except:
    #         return forms.ValidationError("Email is already exist")
    #     return  username

class QuestionAnswerForm (forms.Form):
    radios = forms.ChoiceField(widget=forms.RadioSelect(), label="Chose answer")
    # question = Question()
    CHOICES = []
    question1 = Question()

    def put_answers (self, question):
        views.getinfo(f'In put_answers {views.correct_count}, {views.wrong_count}', question)



        all_answers = Answer.objects.all().filter(question_id=question.id)

        for answer in all_answers:
            # print('answer', answer)
            self.CHOICES.append((answer.answer_text, answer.answer_text))
        question1 = question
        self.fields['radios'].choices = self.CHOICES

        self.CHOICES.clear()


    # def __init__(self, *args, question, **kwargs):
    #     self.this_question = question
    #     super(QuestionAnswerForm, self).__init__(*args, **kwargs)
    #     self.fields['radios'].choices = self.make()


    # def make(self):
    #     self.all_answers =  Answer.objects.all().filter(question_id=self.this_question.id)
    #
    #     print('all_answers:', self.all_answers)
    #
    #     self.CHOICES = []
    #
    #     iteration = 0
    #     for answer in self.all_answers:
    #         print('answer', answer)
    #         self.CHOICES.append((answer.answer_text, answer.answer_text))
    #         iteration +=1
    #
    #
    #     return self.CHOICES




