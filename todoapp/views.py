from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from todoapp.models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs: Any):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.username == "top":
            pass
        else:
            context["tasks"] = context["tasks"].filter(user=user)

        searchInputText = self.request.GET.get("search") or ""
        if searchInputText:
            context["tasks"] = context["tasks"].filter(prod_name__icontains=searchInputText)

        context["search"] = searchInputText
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["prod_name", "device_num", "model_year", "work_date", "divA", "divB", "disassemble_fig", "order_fig"]
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")
    context_object_name = "task"


class TaskListLoginView(LoginView):
    fields = "__all__"
    template_name = "todoapp/login.html"

    def get_success_url(self):
        return reverse_lazy("tasks")


class RegisterTodoApp(FormView):
    template_name = "todoapp/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            print("ddddd")
            login(self.request, user)
        return super().form_valid(form)


from django.shortcuts import render
import requests, re
from bs4 import BeautifulSoup

def main(request):
    url = 'https://www.jma.go.jp/jp/yoho/329.html' #気象庁のHP
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")
    weathers = soup.find_all(class_='weather')
    date_list = weather_list = []
    for i  in weathers:
        j = str(i).replace('\n','')
        date = re.findall('<th class="weather">(.*?)<br/>', str(j))
        date_list = date_list + date
        weather = re.findall('alt="(.*?)" src', str(j))
        weather_list = weather_list + weather
    context = {
        'seibu_today':date_list[0], 'seibu_tomorrow':date_list[1],
        'seibu_today_w':weather_list[0], 'seibu_tomorrow_w':weather_list[1],
        }
    return render(request, 'main.html', context)
