from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from tickets.models import TicketQueues


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    menu_tabs = {
        'Change oil': 'change_oil',
        'Inflate tires': 'inflate_tires',
        'Get diagnostic test': 'diagnostic',

    }

    template_name = 'Processing.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'Menu/contents.html',
                      context={'menu_tabs': self.menu_tabs})


class QView(View):
    template_name = 'Menu/ticket1.html'

    def get(self, request, *args, **kwargs):

        text = request.path

        if 'change_oil' in text:
            time = TicketQueues.c_oil * 2
            TicketQueues.c_oil += 1
            TicketQueues.ticket_number += 1
            TicketQueues.q_oil.appendleft(TicketQueues.ticket_number)

        if 'inflate_tires' in text:
            time = TicketQueues.c_oil * 2 + TicketQueues.c_tires * 5
            TicketQueues.c_tires += 1
            TicketQueues.ticket_number += 1
            TicketQueues.q_tires.appendleft(TicketQueues.ticket_number)

        if 'diagnostic' in text:
            time = TicketQueues.c_oil * 2 + TicketQueues.c_tires * 5 + TicketQueues.c_diag * 30
            TicketQueues.c_diag += 1
            TicketQueues.ticket_number += 1
            TicketQueues.q_diag.appendleft(TicketQueues.ticket_number)

        return render(request, self.template_name,
                      context={'num': TicketQueues.ticket_number, 'time': time})


class ProcessingView(View):


    template_name = 'processing.html'



    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name,
                      context={'oil_count': TicketQueues.c_oil,
                               'tires_count': TicketQueues.c_tires,
                               'diag_count': TicketQueues.c_diag})

    def post(self, request, *args, **kwargs):
        if TicketQueues.c_oil > 0:
            TicketQueues.c_oil -= 1
        elif TicketQueues.c_tires > 0:
            TicketQueues.c_tires -= 1
        elif TicketQueues.c_diag > 0:
            TicketQueues.c_diag -= 1

        if len(TicketQueues.q_oil) > 0:
            TicketQueues.current_number = TicketQueues.q_oil.pop()
        elif len(TicketQueues.q_tires) > 0:
            TicketQueues.current_number = TicketQueues.q_tires.pop()
        elif len(TicketQueues.q_diag) > 0:
            TicketQueues.current_number = TicketQueues.q_diag.pop()
        else:
            TicketQueues.current_number = 0



        return redirect('/processing')



class NextView(View):

    template_name = 'Next.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      context={'num': TicketQueues.current_number})
