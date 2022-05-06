from django.urls import path
from django.views.generic.edit import FormView

from .views import BbCreateView, BbDetailView, by_rubric, add_and_save, BbEditView, BbIndexView, \
    BbMonthArchiveView, index, delete, edit

urlpatterns = [
    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),

    path('rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    # path('<int:pk>/', BbByRubricView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('detail/<int:pk>/edit/', BbEditView.as_view(), name='edit'),
    path('edit/<int:pk>', edit, name='edit'),

    path('delete/<int:pk>', delete, name='delete'),
    # path('detail/<int:pk>/delete/', BbDeleteView.as_view(), name='delete'),

    path('<int:year>/<int:month>/', BbMonthArchiveView.as_view()),

    # path('add', add_and_save, name='add'),
    # path('add/', FormView.as_view(), name='add'),

]

# '<slug:pk>/amp'
# post/<int:pk>/
