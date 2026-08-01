from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid


data_list = []


data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})  # Ejemplo de item inactivo


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get_item_by_id(self, item_id):
        for item in data_list:
            if item.get('id') == item_id:
                return item
        return None

    def put(self, request, item_id):
        item = self.get_item_by_id(item_id)
        if item is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'id' not in data or data.get('id') != item_id:
            return Response({'error': 'El campo id es obligatorio y debe coincidir con la ruta.'}, status=status.HTTP_400_BAD_REQUEST)

        updated_item = {
            'id': item_id,
            'name': data.get('name'),
            'email': data.get('email'),
            'is_active': data.get('is_active', item.get('is_active', True)),
        }

        index = data_list.index(item)
        data_list[index] = updated_item

        return Response({'message': 'Elemento reemplazado correctamente.', 'data': updated_item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        item = self.get_item_by_id(item_id)
        if item is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        for key, value in data.items():
            if key == 'id':
                continue
            item[key] = value

        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = self.get_item_by_id(item_id)
        if item is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False

        return Response({'message': 'Elemento eliminado lógicamente.', 'data': item}, status=status.HTTP_200_OK)
