# Django functionality
from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic # For generic views.

# Bring in models (db table) you want to represent / render.
from .models import Question, Choice

# For serializing
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer

# Create your views here.
def index(request):
    # Reads in the model data -> converts it to a nice readable output -> Return that output (gets printed)
    latest_question_list = Question.objects.order_by('-pub_date')[:5] # Grab your data from table
    context = {'latest_question_list':latest_question_list} # Link data to a context.
    return render(request, 'polls/index.html', context) # Render a page -> Pass in the context data.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) # Primary key = pk. Ensures you get the correct data object back, or 404.
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id): # After you vote -> It redirects you to results.html
    question = get_object_or_404(Question, pk=question_id) # Gets the question from the poll
    return render(request, 'polls/results.html', {'question': question}) # Renders the html file -> The html files has the results info.

def vote(request, question_id): # Handles the new template.
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# REFACTORING: GENERIC VIEWS
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last 5 published questions
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def vote() we leave the same.

# SERIALIZING: Update the views to use the serializer
# - The api_view will wrap the view so that only HTTP methods that're listed in the decorator (see top of code) will get executed.
@api_view(['GET'])
def get_questions(request):
    # Get the list of questions on the site
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def update_question(request, pk):
    # Get the question that you want to update.
    question = Question.objects.get(id=pk)
    serializer = QuestionSerializer(question, data=request.data, partial=True)

    # Serializer can update the "question_text" field of the "question" entries.
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(status=400, data=serializer.errors)