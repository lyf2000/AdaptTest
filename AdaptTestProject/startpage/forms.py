from django.contrib.auth.models import User
from django import forms
from .models import Question, Answer
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import ModelForm

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
    # this_question = Question()
    #answer_text = forms.ChoiceField()

    # def __init__(self, question):
    #     self.this_question = question

    radios = forms.ChoiceField(widget=forms.RadioSelect(), label="Chose answer")


    def __init__(self, question, *args, **kwargs):
        self.this_question = question
        super(QuestionAnswerForm, self).__init__(*args, **kwargs)
        self.fields['radios'].choices = self.make()


    def make(self):
        self.all_answers =  Answer.objects.all().filter(question_id=self.this_question.id)

        print('all_answers:', self.all_answers)

        self.CHOICES = []
        # self.answer_text = forms.ChoiceField()

        iteration = 0
        for answer in self.all_answers:
            print('answer', answer)
            self.CHOICES.append(('select{0}'.format(iteration), answer.answer_text))
            iteration +=1

        print (self.CHOICES)

        # self.answer_text = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect)
        # print(self.answer_text.choices)
        # self.MY_CHOICES = tuple(self.MY_CHOICES)
        return self.CHOICES

    # class Meta:
    #     model = Answer
    #     fields = (
    #         'answer_text',
    #     )

    # def __str__(self):
    #     return '{0} {1}'.format(self.this_question, self.CHOICES)
class A(forms.Form):
    radios = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, students, *args, **kargs):
        super().__init__(*args, **kargs)
        self.students = students
        self.fields['radios'].choices = self.make()

    def make(self):
        self.MY_CHOICES = []
        iteration = 0
        for student in self.students:
            l = [f'select{iteration}', student.name]
            self.MY_CHOICES.append(tuple(l))
            iteration += 1
        self.MY_CHOICES = tuple(self.MY_CHOICES)
        return self.MY_CHOICES







