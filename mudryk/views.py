import datetime
from itertools import zip_longest
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView

from mudryk.calendar_client import get_lesson_days
from mudryk.models import MainPageInfo, TeamMember, Faq, Course, Feedback, Lesson, Record, Proposal, Contact
from mudryk.telegram_sending import send_record, send_feedback_or_proposal
from mudryk.utils import translate_date


class MainPageView(TemplateView):
    model = MainPageInfo
    template_name = 'mudryk/main_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        main_info = self.model.objects.first()
        context['main_info'] = main_info
        contact = Contact.objects.first()
        context['contact'] = contact
        return context


class OurTeamView(ListView):
    model = TeamMember
    context_object_name = 'members'
    template_name = 'mudryk/our_team.html'

    def get_queryset(self):
        all_objects = TeamMember.objects.all()
        queryset = [list(group) for group in zip_longest(*[iter(all_objects)] * 3)]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contact.objects.first()
        context['contact'] = contact
        return context


class FaqView(ListView):
    model = Faq
    context_object_name = 'faqs'
    template_name = 'mudryk/faq.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contact.objects.first()
        context['contact'] = contact
        return context

    def get_queryset(self):
        queryset = Faq.objects.all()
        return queryset


class OurCoursesView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'mudryk/our_courses.html'

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contact.objects.first()
        context['contact'] = contact
        return context


class FeedbackView(ListView):
    model = Feedback
    context_object_name = 'feedback_list'
    template_name = 'mudryk/feedback.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contact.objects.first()
        context['contact'] = contact
        return context

    def get_queryset(self):
        queryset = Feedback.objects.order_by('-created_date')
        return queryset

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            if data['selected_option'] == 'feedback':
                Feedback.objects.create(name=data['name'], email=data['email'], feedback_text=data['feedback_text'],
                                        phone_number=data['phone_number'])
                send_feedback_or_proposal(data['selected_option'], data['name'], email=data['email'],
                                          text=data['feedback_text'], phone_number=data['phone_number'])
            elif data['selected_option'] == 'proposal':
                Proposal.objects.create(name=data['name'], email=data['email'], proposal_text=data['feedback_text'],
                                        phone_number=data['phone_number'])
                send_feedback_or_proposal(data['selected_option'], data['name'], email=data['email'],
                                          text=data['feedback_text'], phone_number=data['phone_number'])
            else:
                return JsonResponse({'success': False})

            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False})


class ScheduleView(ListView):
    model = Course
    context_object_name = 'course_list'
    template_name = 'mudryk/schedule.html'

    def get_queryset(self):
        queryset = Course.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = Contact.objects.first()
        context['contact'] = contact
        return context


def get_course_days(request):
    if request.method == 'POST':
        selected_course = request.POST.get('selected_option', '')
        try:
            lesson_days = list(get_lesson_days(selected_course))
            datetime_list = []
            for lesson_day in lesson_days:
                for time in lesson_day['times']:
                    date_and_time = lesson_day['date'] + ' ' + time + '+02:00'
                    datetime_list.append(date_and_time)
            lessons = Lesson.objects.all()
            dates_to_delete = []
            for lesson in lessons:
                if lesson.current_participants == lesson.max_participants:
                    dates_to_delete.append(lesson.datetime_start)
            for date_to_delete in dates_to_delete:
                for lesson_day in lesson_days:
                    for time in lesson_day['times']:
                        date_and_time = lesson_day['date'] + ' ' + time + '+02:00'
                        if datetime.datetime.strftime(date_to_delete, '%Y-%m-%d %H:%M:%S') == date_and_time.split('+')[0]:
                            lesson_day['times'].remove(time)
                            if len(lesson_day['times']) == 0:
                                lesson_days.remove(lesson_day)
            for day in lesson_days:
                day['day_str'] = translate_date(day['day_str'])
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Something went wrong in schedule calendar.'})

        if len(lesson_days) == 0:
            return JsonResponse({'success': False, 'error': 'It seems that this course is not in the schedule.'})

        return JsonResponse({'success': True, 'days_list': lesson_days})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def submit_record(request):
    if request.method == 'POST':
        selected_course = request.POST.get('selected_course', '')
        selected_day = request.POST.get('selected_day', '')
        selected_time = request.POST.get('selected_time', '')
        if selected_time != '':
            selected_time += '+02:00'
        parent_name = request.POST.get('parent-name', '')
        child_name = request.POST.get('child-name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone_number', '')
        date_and_time = selected_day + ' ' + selected_time
        try:
            if Lesson.objects.filter(title=selected_course, datetime_start=date_and_time).exists():
                lesson = Lesson.objects.get(title=selected_course, datetime_start=date_and_time)
                current_participants = lesson.current_participants + 1
                lesson.current_participants = current_participants
                lesson.save()
                Record.objects.create(parent_name=parent_name, child_name=child_name, email=email, phone_number=phone,
                                      lesson=lesson)
                send_record(selected_course, selected_day, selected_time, parent_name, child_name, email, phone)
            else:
                max_members = Course.objects.get(name=selected_course).max_members
                lesson = Lesson.objects.create(title=selected_course, datetime_start=date_and_time,
                                               max_participants=max_members, current_participants=1)
                Record.objects.create(parent_name=parent_name, child_name=child_name, email=email, phone_number=phone,
                                      lesson=lesson)
                send_record(selected_course, selected_day, selected_time, parent_name, child_name, email, phone)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Something went wrong in record process.{e}'})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

