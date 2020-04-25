from django.db import models
from collections import deque


# Create your models here.
class TicketQueues:
    c_oil = 0
    c_tires = 0
    c_diag = 0
    ticket_number = 0
    q_oil = deque()
    q_tires = deque()
    q_diag = deque()
    current_number = 0
