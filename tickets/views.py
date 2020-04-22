from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}
    menu_tabs = {
        'Change oil': 'change_oil',
        'Inflate tires': 'inflate_tires',
        'Get diagnostic test': 'diagnostic',

    }

    template_name = 'Processing.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, 'Menu/contents.html',
                      context={'menu_tabs': self.menu_tabs})





class QView(View):
    c_oil = 0
    c_tires = 0
    c_diag = 0
    c = 0
    q_oil = deque()
    q_tires = deque()
    q_diag = deque()

    template_name = 'Menu/ticket1.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        text = request.path
        if 'change_oil' in text:
            time = QView.c_oil * 2
            QView.c_oil += 1
            num = QView.c_oil
            QView.c+=1
            QView.q_oil.appendleft(QView.c)

        if 'inflate_tires' in text:
            time = QView.c_oil * 2 + QView.c_tires * 5
            QView.c_tires += 1
            num = QView.c_oil + QView.c_tires
            QView.c += 1
            QView.q_tires.appendleft(QView.c)

        if 'diagnostic' in text:
            time = QView.c_oil * 2 + QView.c_tires * 5 + QView.c_diag * 30
            QView.c_diag += 1
            num = QView.c_oil + QView.c_tires + QView.c_diag
            QView.c += 1

            QView.q_diag.appendleft(QView.c)

        # self.counter += 1
        # QView.c += 1

        return render(request, self.template_name,
                      context={'num': QView.c, 'time': time})


class ProcessingView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}

    template_name = 'processing.html'
    nm = 0
    flag = 0

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      context={'oil_count': QView.c_oil,
                               'tires_count': QView.c_tires,
                               'diag_count': QView.c_diag})

    def post(self, request, *args, **kwargs):
        if(QView.c_oil>0):
            QView.c_oil-=1
        elif(QView.c_tires>0):
            QView.c_tires-=1
        elif(QView.c_diag>0):
            QView.c_diag-=1


        if (len(QView.q_oil) > 0):
            ProcessingView.nm = QView.q_oil.pop()
        elif (len(QView.q_tires) > 0):
            ProcessingView.nm = QView.q_tires.pop()
        elif (len(QView.q_diag) > 0):
            ProcessingView.nm = QView.q_diag.pop()
        else:
            ProcessingView.nm = 0

        ProcessingView.flag+=1

        return redirect('/processing')







class NextView(View):
    # form_class = MyForm
    # initial = {'key': 'value'}


    template_name = 'Next.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        '''if(ProcessingView.flag == 0):
            if (QView.c_oil > 0):
                QView.c_oil -= 1
            elif (QView.c_tires > 0):
                QView.c_tires -= 1
            elif (QView.c_diag > 0):
                QView.c_diag -= 1

            if (len(QView.q_oil) > 0):
                ProcessingView.nm = QView.q_oil.pop()
            elif (len(QView.q_tires) > 0):
                ProcessingView.nm = QView.q_tires.pop()
            elif (len(QView.q_diag) > 0):
                ProcessingView.nm = QView.q_diag.pop()
            else:
                ProcessingView.nm = 0'''

        return render(request, self.template_name,
                      context={'num':ProcessingView.nm })
