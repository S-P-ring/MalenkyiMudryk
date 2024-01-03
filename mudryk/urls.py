from django.urls import path
from mudryk.views import MainPageView, OurTeamView, FaqView, OurCoursesView, FeedbackView, ScheduleView, \
    get_course_days, submit_record

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('our_team/', OurTeamView.as_view(), name='our_team'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('our_courses/', OurCoursesView.as_view(), name='our_courses'),
    path('feedbacks/', FeedbackView.as_view(), name='feedbacks'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('get_course_days/', get_course_days, name='get_course_days'),
    path('submit_record/', submit_record, name='submit_record'),
]
