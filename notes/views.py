from .models import Note
from .serializers import CreateNoteSerializer, NoteSerializer
from accounts.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note_view(request):
    if request.method == 'POST':
        user = request.user

        serializer = CreateNoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)

            return Response(
                {
                    'success':True,
                    'data':serializer.data
                }, status=status.HTTP_201_CREATED
            )

        return Response (
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_user_notes_view(request):
    if request.method == 'GET':
        notes = Note.objects.filter(user=request.user)

        serializer = NoteSerializer(notes, many=True)

        return Response (
            {
                'success':True,
                'data':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return Response ({'error':'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoteSerializer(note)

        return Response (
            {
                'success':True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = NoteSerializer(note, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'data':serializer.data
                }, status=status.HTTP_200_OK
            )

        return Response (
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        note.delete()

        return Response (
            {
                'success':True,
                'message':'Note has been deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )