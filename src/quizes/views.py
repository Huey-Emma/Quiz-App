from json import loads
from typing import Optional
from django.shortcuts import render, Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.generic import ListView
from .models import Quiz
from questions.models import Question, Answer
from results.models import Result


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'
    context_object_name = 'quiz_list'


def quiz_view(request, pk) -> HttpResponse:
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        raise Http404

    return render(request, 'quizes/quiz.html', {
        'quiz': quiz
    })


@require_http_methods(['GET'])
def quiz_data_view(request, pk) -> JsonResponse:
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        raise Http404

    questions = []
    for question in quiz.get_questions():
        answers = []
        for answer in question.get_answers():
            answers.append(answer.text)
        questions.append({
            str(question.text): answers
        })

    return JsonResponse(data={
        'data': questions,
        'time': quiz.time,
    })


@require_http_methods(['POST'])
def quiz_save_view(request, pk) -> JsonResponse:
    body_data = loads(request.body)
    questions = []

    for question_text in body_data.keys():
        question = Question.objects.get(text=question_text)
        questions.append(question)

    user = request.user
    quiz = Quiz.objects.get(pk=pk)
    score: int = 0
    multiplier: float = 100 / quiz.num_of_questions
    results = []
    correct_answer: Optional[str] = None

    for question_ in questions:
        selected_answer = body_data.get(question_.text)

        if selected_answer is not None:
            answers = Answer.objects.filter(question=question_)
            for answer in answers:
                if answer.correct and answer.text == selected_answer:
                    score += 1
                    correct_answer = answer.text
                else:
                    correct_answer = answer.text

            results.append({
                question_.text: {
                    'correct_answer': correct_answer,
                    'answered': selected_answer
                }
            })
        else:
            results.append({
                question_.text: None
            })

    score_ = score * multiplier
    Result.objects.create(quiz=quiz, user=user, score=score_)

    if score_ >= quiz.pass_score:
        return JsonResponse(status=201, data={
            'passed': True,
            'score': score_,
            'results': results
        })
    else:
        return JsonResponse(status=201, data={
            'passed': False,
            'score': score_,
            'results': results
        })

