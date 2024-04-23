from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth import login, logout, authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import logging

from .models import Course
from employees.models import UserProfile

logger = logging.getLogger(__name__)

def employee_list(request):
    employees = UserProfile.objects.all()
    return render(request, 'adminsite/employee_list.html', {'employees': employees})
class CourseListView(generic.ListView):
    template_name = 'adminsite/course_list.html'
    context_object_name = 'course_list'
    def get_queryset(self):
        courses = Course.objects.order_by('-total_enrollment')[:10]
        return courses

class EnrollView(View):
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse('adminsite:course_details', args=(course.id, )))


class CourseDetailsView(ModelViewSet):
    model = Course
    template_name = 'adminsite/course_detail.html'

class TestDetailsView(ModelViewSet):
    @action(
        detail=True,
        methods=['get'],
    )
    def test(self, request, pk):
        return None


def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('adminsite:popular_course_list')
    
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('adminsite:popular_course_list')
        else:
            return render(request, 'adminsite/user_login.html', context)
    else:
        return render(request, 'adminsite/user_login.html', context)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'adminsite/user_registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("adminsite:popular_course_list")
        else:
            return render(request, 'adminsite/user_registration.html', context)