from allauth.account.forms import SignupForm
from django.forms import ModelForm
from .models import Profile, StudySessionModel, Class
from django import forms
from django.contrib.auth.models import User

class EditProfileForm(ModelForm):
    # Grab profile from request to filter course options by enrolled courses:
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['Enrolled_Courses'].queryset = Class.objects.filter(profile=self.request.user.profile)
        self.fields['Following'].queryset = self.request.user.profile.Following

    class Meta:
        model = Profile
        fields = ['Age', 'Major', 'Enrolled_Courses', 'Bio', 'Following']

    # Set Enrolled_Courses to NOT be required - allow to save profile with no courses.
    Enrolled_Courses = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # Set Following to NOT be required.
    Following = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def save(self, commit=True):
       profile = super(EditProfileForm, self).save(commit=False)
       profile.user = self.request.user
       # Make sure to save many to many field.
       self.save_m2m()
       if commit:
           profile.save()
       return profile
    


class SignupProfileForm(SignupForm):
    class Meta:
        model = Profile
        fields = ['Age', 'Major', 'Enrolled_Courses', 'Bio']

        def save(self, request):
            # Ensure you call the parent class's save.
            # .save() returns a User object.
            user = super(SignupProfileForm, self).save(request)

            # Add your own processing here.

            # You must return the original result.
            return user


class StudySessionForm(ModelForm):
    class Meta:
        model = StudySessionModel
        fields = ('title','class_name', 'text','duration','start_time','address')

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs = {'class':'form-control'}),
            'duration':forms.TextInput(attrs={'class':'form-control','placeholder':'eg: 2 hours'}),
            'start_time':forms.DateTimeInput(format=('%m/%d/%y %H:%M'), attrs = {'class':'form-control','placeholder':'10/25/06 14:30'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'eg: clark, rice, discord..'}),
            }

        error_messages = {
            'start_time': {
                'invalid': "Please enter a valid start time below in the format of '10/25/06 14:30'.",
            },
        }


class StudySessionEditForm(ModelForm):
    class Meta:
        model = StudySessionModel
        fields = ('title', 'text','duration','start_time','address')

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs = {'class':'form-control'}),
            'duration':forms.TextInput(attrs={'class':'form-control','placeholder':'eg: 2 hours'}),
            'start_time':forms.DateTimeInput(format=('%m/%d/%y %H:%M'), attrs = {'class':'form-control','placeholder':'10/25/06 14:30'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'eg: clark, rice, discord..'}),
            }


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['description_field', 'subject_field', 'course_number_field', 'instructor_field']
