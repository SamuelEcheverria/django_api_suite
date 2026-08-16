import os
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import firebase_admin
from firebase_admin import credentials, db


def get_firebase_db():
    key_path = os.path.join(settings.BASE_DIR, 'firebase_key.json')
    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://landing-92a81-default-rtdb.firebaseio.com/'
        })
    return db


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        try:
            firebase_db = get_firebase_db()
            ref = firebase_db.reference('/')
            data = ref.get()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al conectar con Firebase: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            if not data:
                return Response({'error': 'No se proporcionaron datos para guardar.'}, status=status.HTTP_400_BAD_REQUEST)

            firebase_db = get_firebase_db()
            # Guardar en el nodo 'mensajes' o en la colección enviada en el payload
            target_node = data.get('node', 'mensajes')
            ref = firebase_db.reference(target_node)
            new_ref = ref.push(data)

            return Response({
                'message': 'Dato guardado exitosamente en Firebase.',
                'id': new_ref.key,
                'data': data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al guardar en Firebase: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item (Firebase)"

    def get(self, request, item_id):
        try:
            firebase_db = get_firebase_db()
            ref = firebase_db.reference(f'mensajes/{item_id}')
            data = ref.get()
            if data is None:
                ref = firebase_db.reference(f'landing/{item_id}')
                data = ref.get()
            if data is None:
                return Response({'error': 'Elemento no encontrado en Firebase.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
