from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random

from .models import Problem, ParticipantProgress, EventConfig


class LevelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, level_number):
        user = request.user

        # 1. Check event is live
        config = EventConfig.objects.first()
        now = timezone.now()
        if now < config.started_at:
            return Response({'error': 'Event has not started yet'}, status=status.HTTP_403_FORBIDDEN)
        if now > config.ending_time:
            return Response({'error': 'Event has ended'}, status=status.HTTP_403_FORBIDDEN)

        # 2. Check previous level completed (skip for level 1)
        if level_number > 1:
            prev_done = ParticipantProgress.objects.filter(
                user=user, user_level=level_number - 1, status=True
            ).exists()
            if not prev_done:
                return Response({'error': 'Complete the previous level first'}, status=status.HTTP_403_FORBIDDEN)

        # 3. Check if this level was already assigned
        existing = ParticipantProgress.objects.filter(user=user, user_level=level_number).first()
        if existing:
            return Response({
                'problem_id': existing.problem.id,
                'title': existing.problem.title,
                'description': existing.problem.description,
            }, status=status.HTTP_200_OK)

        # 4. Find patterns already seen by this user
        seen_categories = ParticipantProgress.objects.filter(user=user).values_list('problem__category', flat=True)

        # 5. Pick a random problem matching this level, excluding seen patterns
        available_problems = Problem.objects.filter(difficulty=level_number).exclude(category__in=seen_categories)
        if not available_problems.exists():
            return Response({'error': 'No problems available for this level'}, status=status.HTTP_404_NOT_FOUND)
        problem = random.choice(list(available_problems))

        # 6. Create the ParticipantProgress row to lock in this assignment
        ParticipantProgress.objects.create(user=user, problem=problem, user_level=level_number)

        return Response({
            'problem_id': problem.id,
            'title': problem.title,
            'description': problem.description,
        }, status=status.HTTP_200_OK)
    


from .services import validate_answer
from .models import Submission

class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        problem_id = request.data.get('problem_id')
        submitted_answer = request.data.get('answer')

        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return Response({'error': 'Problem not found'}, status=status.HTTP_404_NOT_FOUND)

        is_correct = validate_answer(problem.expected_answer, submitted_answer)

        Submission.objects.create(
            user=user,
            problem=problem,
            submitted_answer=submitted_answer,
            is_correct=is_correct,
        )

        if is_correct:
            progress = ParticipantProgress.objects.get(user=user, problem=problem)
            progress.status = True
            progress.completed_at = timezone.now()
            progress.save()

            return Response({'result': 'correct', 'message': 'Level complete!'}, status=status.HTTP_200_OK)

        return Response({'result': 'incorrect', 'message': 'Try again'}, status=status.HTTP_200_OK)