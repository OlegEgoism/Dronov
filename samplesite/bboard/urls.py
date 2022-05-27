from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BbCreateView, BbDetailView, by_rubric, BbEditView, \
    BbMonthArchiveView, index, delete, edit, rubrics, bbs, Login, Logout, SLPasswordResetView, search, \
    formset_processing, imgadd, get_email, api_rubrics, api_rubric_detail, APIRubrics, APIRubricDetail, APIRubricList, \
    APIRubricViewSet, APIRubricViewSetRe

router = DefaultRouter()
router.register('rubset', APIRubricViewSet)
router.register('rubsetre', APIRubricViewSetRe)

urlpatterns = [
    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),

    path('rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),
    # path('<int:pk>/', BbByRubricView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('detail/<int:pk>/edit/', BbEditView.as_view(), name='edit'),
    path('edit/<int:pk>', edit, name='edit'),

    path('delete/<int:pk>', delete, name='delete'),
    # path('detail/<int:pk>/delete/', BbDeleteView.as_view(), name='delete'),

    path('<int:year>/<int:month>/', BbMonthArchiveView.as_view()),

    # path('login/', get_login, name='login'),
    # path('logout/', get_logout, name='logout'),
    # вход/выход на сайт (ГЛАВА 15)
    path('accounts/login', Login.as_view(), name='login'),
    path('accounts/logout', Logout.as_view(), name='logout'),
    # смена пароля
    path('accounts/password_change/', PasswordChangeView.as_view(
        template_name='registration/change_password.html'),
         name='password_change'),
    # уведомление об успешном изменении пароля
    path('accounts/ch_pass/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_changed.html'),
         name='password_change_done'),
    # отправка письма для сброса пароля
    # path('accounts/password_reset/', PasswordResetView.as_view(
    #     template_name='registration/password_reset.html',
    #     subject_template_name='registration/reset_subject.txt',
    #     email_template_name='registration/reset_email.txt'),
    #      name='password_reset'),
    path('accounts/password_reset/', SLPasswordResetView.as_view(), name='password_reset'),

    # уведомление об отправки письма для сброса пароля
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/email_sent.html'),
         name='password_reset_done'),
    # сброс пароля
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/confirm_password.html'),
         name='password_reset_confirm'),
    # уведомление об успешном сбросе
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_confirmed.html'),
         name='password_reset_complete'),

    path('search/', search, name='search'),
    path('formset_processing/', formset_processing, name='formset_processing'),

    path('img', imgadd, name='img'),

    path('mail/', get_email, name='mail'),

    path('api/rubrics/', api_rubrics),
    path('api/rubrics/<int:pk>', api_rubric_detail),
    path('api/rubricss/', APIRubrics.as_view()),  # исправление рубрик
    path('api/rubricss/<int:pk>', APIRubricDetail.as_view()),
    path('api/rublist/', APIRubricList.as_view()),
    path('', include(router.urls)),  # http://127.0.0.1:8000/rubset/   http://127.0.0.1:8000/rubsetre/


    # path('add', add_and_save, name='add'),
    # path('add/', FormView.as_view(), name='add'),
]
