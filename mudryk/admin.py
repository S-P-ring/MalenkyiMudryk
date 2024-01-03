from django.contrib import admin
from django.utils.safestring import mark_safe
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from mudryk.models import MainPageInfo, ReasonToChoose, Advantage, Discount, SmallDescription, InfoForParents, \
    TeamMember, Faq, TextForCourse, Course, TextWithListForCourse, ListItemForText, Feedback, Proposal, Lesson, Record, \
    Phone, Contact


class ReasonToChooseInline(admin.TabularInline):
    model = ReasonToChoose
    extra = 1
    min_num = 1
    validate_min = True

class AdvantageInline(admin.TabularInline):
    model = Advantage
    extra = 1
    min_num = 1
    validate_min = True

class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1
    min_num = 1
    validate_min = True

class SmallDescriptionInline(admin.TabularInline):
    model = SmallDescription
    extra = 1
    min_num = 1
    validate_min = True

class InfoForParentsInline(admin.TabularInline):
    model = InfoForParents
    extra = 1
    min_num = 1
    validate_min = True


class MainPageInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tagline',)
    list_display_links = ('id', 'tagline',)
    fields = ('tagline', 'center_mission',)
    inlines = [ReasonToChooseInline, AdvantageInline, DiscountInline, SmallDescriptionInline, InfoForParentsInline]


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'get_html_photo')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    fields = ('name', 'description', 'photo', 'get_html_photo')
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=200>")
        else:
            return mark_safe(f"<h4>Фото поки що немає<h4>")


class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer',)
    list_display_links = ('id', 'question')
    search_fields = ('question',)
    fields = ('question', 'answer',)


class ListItemForTextInline(NestedStackedInline):
    model = ListItemForText
    extra = 0
    min_num = 1
    validate_min = True


class TextWithListForCourseInline(NestedStackedInline):
    model = TextWithListForCourse
    extra = 0
    min_num = 1
    validate_min = True
    inlines = [ListItemForTextInline]


class TextForCourseInline(NestedStackedInline):
    model = TextForCourse
    extra = 0
    min_num = 1
    validate_min = True


class CoursesAdmin(NestedModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    fields = ('name', 'price', 'max_members')
    inlines = [TextForCourseInline, TextWithListForCourseInline]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_published', 'created_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'created_date')
    fields = ('name', 'email', 'feedback_text', 'phone_number', 'is_published', 'created_date')
    readonly_fields = ('created_date',)


class ProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'created_date')
    fields = ('name', 'email', 'proposal_text', 'phone_number', 'created_date')
    readonly_fields = ('created_date',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'datetime_start', 'current_participants')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'datetime_start', 'current_participants')
    fields = ('title', 'datetime_start', 'max_participants', 'current_participants')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_name', 'child_name', 'email', 'phone_number', 'lesson')
    list_display_links = ('id', 'parent_name', 'child_name')
    search_fields = ('parent_name', 'child_name', 'email', 'phone_number', 'lesson')
    fields = ('parent_name', 'child_name', 'email', 'phone_number', 'lesson')


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    min_num = 1
    validate_min = True


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
    list_display_links = ('id', 'email',)
    fields = ('email', 'facebook_link', 'instagram_link', 'address')
    inlines = [PhoneInline]


admin.site.register(MainPageInfo, MainPageInfoAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Course, CoursesAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Contact, ContactAdmin)
