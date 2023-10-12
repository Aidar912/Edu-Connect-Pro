from django.urls import path
from .views import *

urlpatterns = [
    path('students/create/', StudentCreateView.as_view(), name='student-create'),
    path('accounts/create/', AccountCreateView.as_view(), name='account-create'),
    path('paymenthistories/create/', PaymentHistoryCreateView.as_view(), name='paymenthistory-create'),
    path('transcripts/create/', TranscriptCreateView.as_view(), name='transcript-create'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('grades/create/', GradeCreateView.as_view(), name='grade-create'),
    path('attendance/create/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('schedules/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('teachers/create/', TeacherCreateView.as_view(), name='teacher-create'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
]
