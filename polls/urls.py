from django.urls import path
from . import views

# Note: All the views are converted to generic ones, except the "vote" view)
# Essentially: These are all different views / pages user can go to.
app_name = 'polls' # When you're inside the "polls" app -> You have access to all of these URLS.
urlpatterns = [
    # Ex: /polls/
    path('', views.IndexView.as_view(), name='index'), # On empty path, takes you to the 'index' (home) page.

    # Ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name = "detail"), 

    # Ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name = "results"), # When navigating to .../results/ = You'll open the view "results" inside of "views.py"

    # Ex: /polls/5/vote/
    #path('<int:question_id>/vote/', views.detail, name = "vote"),

    # Handles form submitted data (non-generic view)
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # Want API responses to have JSON objects.
    path('api/questions/', views.get_questions, name='get_questions'),

    # Allow serializer to update questions
    path('api/question/<int:pk>', views.update_question, name="update_question"),
]