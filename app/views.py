from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, UpdateView,DeleteView
import requests
from django.http import HttpResponseRedirect
from .models import Profile, StudySessionModel, Class, Discussions
from .forms import EditProfileForm, StudySessionForm, StudySessionEditForm
from django.views.generic import DetailView
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("homepage")
def edit_profile(request, pk):
    # Check if the user has a profile:
    try:
        profile = request.user.profile
    except Profile.DoesNotExist: 
        # If user has no profile, create one.
        profile = Profile(user=request.user)
    
    if request.method == 'POST':
        # Set form instance to be the current user's profile.
        form = EditProfileForm(request.POST, instance=profile, request=request)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return HttpResponseRedirect(reverse('user_profile', args=(pk,)))    
    else:
        form = EditProfileForm(instance=profile, request=request)

    return render(request, 'editProfile.html', {'form': form})

def friendslist(request):
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    return render(request, 'friendsList.html', context)

# Updated profile view to see other users' profiles using pk.
def profile(request, pk=None):
    if pk:
        profile = get_object_or_404(Profile, pk=pk)
    else:
        profile = request.user.profile
    args = {'profile': profile}
    return render(request, 'profile.html', args)


def index(request):
    return HttpResponse("Hello, world. You're at the app page.")

# Only loads CS department classes by default to the course list page.
def get_class(request):
    url = "http://luthers-list.herokuapp.com/api/dept/CS/"
    response = requests.get(url).json()
    return render(request, 'classinfo.html', {'response': response})

def get_search(request):
    if request.method == "POST":
        query_name = request.POST.get('name')
        # Checks courses from all departments for search results:
        dept_list = requests.get("http://luthers-list.herokuapp.com/api/deptlist/").json()
        response = []
        all_results = []
        for d in dept_list:
            dept = d['subject']
            url = "http://luthers-list.herokuapp.com/api/dept/" + dept + "/"
            response = requests.get(url).json()
            result = list(filter(lambda x: (x['description'].upper().__contains__(query_name.upper()) or (x['subject']+" "+x['catalog_number']).upper().__contains__(query_name.upper()) or x['instructor']['name'].upper().__contains__(query_name.upper())), response))
            all_results += result
        return render(request, 'search.html', {"result":all_results})
    return render(request, 'search.html',{"result":{"n"}})

# Add class to user profile's Enrolled Courses field.
# Triggered by 'Add' button on Course List page, classinfo.html, search.html.
def add_class(request):
    profile = request.user.profile
    if request.method == "POST":
        # Course numbers are unique -- use it to check if course exists.
        course_number = request.POST.get('course_number')
        
        # If course does not already exist, create it.
        if not Class.objects.filter(course_number_field=course_number).exists():
            subject = request.POST.get('subject')
            catalog_number = request.POST.get('catalog_number')
            description = request.POST.get('description')
            instructor = request.POST.get('instructor')
            new_course = Class(subject_field=subject, catalog_number_field=catalog_number, 
                course_number_field=course_number, description_field=description, instructor_field=instructor)
            new_course.save()
        else:
            # Otherwise, get the existing instance.
            new_course = Class.objects.get(course_number_field=course_number)

        # Add the course to the user profile if it isn't already there.
        if not profile.Enrolled_Courses.filter(course_number_field=course_number).exists():
            profile.Enrolled_Courses.add(new_course)
            profile.save()
    return HttpResponseRedirect(reverse('user_profile', args=(profile.id,)))

# Add other profile to current user profile's Following list.
# Triggered by 'Friend' button on buddy page, userList.html, userSearch.html.
def follow(request):
    profile = request.user.profile
    if request.method == 'POST':
        other_profile_id = request.POST.get('other_profile_id')
        profile.Following.add(other_profile_id)
        profile.save()
    return HttpResponseRedirect(reverse('user_profile', args=(profile.id,)))



def AddSessionView(request):

    if request.method == 'POST':
        # Set form instance to be the current user's profile.
        form = StudySessionForm(request.POST)
        if 'class_name' in form.errors:
            del form.errors['class_name']
        if form.is_valid():
            session = form.save(commit=False)
            session.class_name = request.POST.get("class_name")
            session.author = request.user
            session.save()
            return HttpResponseRedirect(reverse('my_post_session'))
    else:
        form = StudySessionForm()

    def get_form(form, *args, **kwargs):
        profile = request.user.profile
        set = list(profile.Enrolled_Courses.all())
        result = []

        for i in set:

            b = i.subject_field + i.catalog_number_field
            a = (str(b), str(b))
            result.append(a)
        form.fields['class_name'].choices = result

        return form

    return render(request, 'study_session_post.html', {'form': get_form(form)})

#class UpadateSessionView(UpdateView):
#    model = StudySessionModel
#    form_class = StudySessionEditForm
#    template_name = 'editStudySession.html'

def update_session(request, pk):
    obj = get_object_or_404(StudySessionModel, pk=pk)
    form = StudySessionForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if 'class_name' in form.errors:
            del form.errors['class_name']
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_post_session'))

    def get_form(form, *args, **kwargs):
            profile = request.user.profile
            set = list(profile.Enrolled_Courses.all())
            result = []

            for i in set:

                b = i.subject_field + i.catalog_number_field
                a = (str(b), str(b))
                result.append(a)
            form.fields['class_name'].choices = result

            return form

    return render(request, 'editStudySession.html', {'form': get_form(form)})


class DeleteSessionView(DeleteView):
    model = StudySessionModel
    template_name = 'delete_session.html'
    success_url = reverse_lazy('list')

def get_user_search(request):
    if request.method == "POST":
        query_name = request.POST.get('name')
        # user = get_object_or_404(User, username=query_name)
        try:
            user = User.objects.get(username=query_name)
        except User.DoesNotExist:
            user = None
        
        user_filter = Profile.objects.filter(Q(user=user) |Q(Enrolled_Courses__subject_field__contains=query_name) 
            | Q(Age__contains=query_name) |  Q(Major__contains=query_name) | Q(Enrolled_Courses__catalog_number_field__contains=query_name)).distinct()
        return render(request, 'userSearch.html', {"u_filter": user_filter})

def UnenrollView(request,pk):
    study_session = get_object_or_404(StudySessionModel, id=pk)
    study_session.enroll.remove(request.user)
    return HttpResponseRedirect(reverse('home'))

def post_list(request):
    profile = request.user.profile
    set = list(profile.Enrolled_Courses.all())
    result = []

    for i in set:
        a = i.subject_field + i.catalog_number_field
        result.append(a)
    formset = []
    for i in result:
        formset.append(StudySessionModel.objects.filter(class_name=i))
    return render(request, 'list.html', {'formset': formset})

def friendspost(request):
    profile = request.user.profile
    set = profile.Following.all()

    formset = []
    for i in set:
        try:
            user = User.objects.get(username=i)
        except User.DoesNotExist:
            user = None
        formset.append(StudySessionModel.objects.filter(author=user))
    return render(request, 'list.html', {'formset': formset})

class StudySessionDetailView(DetailView):
    model = StudySessionModel
    template_name = 'session_details.html'
    def get_context_data(self, *args, **kwargs):
        context = super(StudySessionDetailView, self).get_context_data(**kwargs)
        studysession = get_object_or_404(StudySessionModel,id=self.kwargs['pk'])
        context["enroll_list"] = studysession.enroll.all()
        context["replies"] = Discussions.objects.filter(post=studysession)
        return context
        
def EnrollView(request,pk):
    study_session = get_object_or_404(StudySessionModel, id=pk)
    study_session.enroll.add(request.user)
    return HttpResponseRedirect(reverse('post_detail',args=[str(pk)]))
    
def EnrolledSessionsView(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        user = None
    if user:
        enrolled = user.user_enroll.all()
    else: 
        enrolled = []
    return render(request, 'index.html', {"enroll":enrolled})

def ListMyPostSessions(request):
    user = User.objects.get(username=request.user.username)
    my_posts = StudySessionModel.objects.filter(author=user)
    return render(request,'my_post_sessions.html',{"m_posts":my_posts})

def user_list(request):
    userList = Profile.objects.all()
    context = {'userList': userList}
    return render(request, 'userList.html', context)


def discussion(request, pk):
    study_session = get_object_or_404(StudySessionModel, id=pk)
    if request.method=="POST":
        user = request.user
        desc = request.POST.get('desc','') #html id
        reply = Discussions(author = user, text = desc, post=study_session)
        reply.save()
    return HttpResponseRedirect(reverse('post_detail',args=[str(pk)]))


#https://dev.to/earthcomfy/django-user-profile-3hik

# def submit(request):
#     description_text = request.POST.get('Class Name')
#     course_number_text = request.POST.get('Course Number')
#     instructor_text = request.POST.get('Instructor')
#     thought = UserClass(description_field=decsription_text, course_number_field=course_number_text, instructor_field=instructor_text)
#     thought.save()
#     # Always return an HttpResponseRedirect after successfully dealing
#     # with POST data. This prevents data from being posted twice if a
#     # user hits the Back button.
#     return HttpResponseRedirect('/class')
