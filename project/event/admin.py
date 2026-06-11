from django.contrib import admin
from .models import Problem, ParticipantProgress, Submission, EventConfig

# Register your models here.
admin.site.register(Problem)
admin.site.register(ParticipantProgress)
admin.site.register(Submission)
admin.site.register(EventConfig)