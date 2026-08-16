import os
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import credentials, db


def get_firebase_db():
    key_path = os.path.join(settings.BASE_DIR, 'firebase_key.json')
    if not os.path.exists(key_path):
        key_path = os.path.join(settings.BASE_DIR.parent, 'firebase_key.json')
    if not os.path.exists(key_path):
        raise FileNotFoundError("No se encontró el archivo firebase_key.json en la raíz del proyecto.")
    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://landing-92a81-default-rtdb.firebaseio.com/'
        })
    return db


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing"

    def get(self, request, collection=None):
        try:
            firebase_db = get_firebase_db()
            # Si acceden a index/ o landing/, consultar la raíz '/' de Firebase para incluir mensajes y noticias
            if collection in [None, 'index', 'landing']:
                ref = firebase_db.reference('/')
            else:
                ref = firebase_db.reference(f'{collection}')
            
            data = ref.get()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al obtener datos de Firebase: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, collection=None):
        try:
            data = request.data
            firebase_db = get_firebase_db()
            target_collection = collection if collection else self.collection_name
            # Referencia a la colección
            ref = firebase_db.reference(f'{target_collection}')

            current_time = datetime.now()
            custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')

            if isinstance(data, dict):
                data.update({"timestamp": custom_format})
            else:
                data = {"payload": data, "timestamp": custom_format}

            # push: Guarda el objeto en la colección
            new_resource = ref.push(data)
            # Devuelve el id del objeto guardado
            return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al guardar en Firebase: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
