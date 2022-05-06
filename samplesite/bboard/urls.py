from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from django.views.generic.edit import FormView

from .views import BbCreateView, BbDetailView, by_rubric, add_and_save, BbEditView, BbIndexView, \
    BbMonthArchiveView, index, delete, edit, rubrics, bbs, Login, Logout

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
    path('accounts/login', Login.as_view(), name='login'),
    path('accounts/logout', Logout.as_view(), name='logout'),
    # смена пароля (глава 15 стр. 303)
    path('accounts/change_password/', PasswordChangeView.as_view(template_name='registration/change_password.html',
                                                                 success_url=reverse_lazy('bboard:password_change_done')),
                                                                 name='password_change'),
    # уведомление об успешном изменении пароля (глава 15 стр. 303)
    path('accounts/change_password/done/', PasswordChangeDoneView.as_view(template_name='registration/password_changed.html'),
                                                                          name='password_change_done'),



    # path('add', add_and_save, name='add'),
    # path('add/', FormView.as_view(), name='add'),

]
