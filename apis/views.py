from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from apis.models import Group,Images,GroupImage
from apis.serializers import GroupSerializer,GroupImageSerializer,ImagesSerializer
from apis.filters import ImagesFilter


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            })

class Logout(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        return Response({"success": "Successfully logged out."},
                        status=200)


class GroupList(APIView):

    def get(self,request):
        groups = Group.objects.filter(user=request.user)
        page = request.GET.get('page', 1)
        paginator = PageNumberPagination()
        groups = paginator.paginate_queryset(groups, request)
        serializer = GroupSerializer(groups, many=True)
        return paginator.get_paginated_response(serializer.data)


class GroupDetail(APIView):
    def get(self, request, id, format=None):
        group = Group.objects.get(id=id).group_images.all()
        page = request.GET.get('page', 1)
        paginator = PageNumberPagination()
        group = paginator.paginate_queryset(group, request)
        serializer = GroupImageSerializer(group,many=True)
        return paginator.get_paginated_response(serializer.data)

class PhotosList(APIView):
    def get(self, request, format=None):

        photos = ImagesFilter(request.GET,queryset=Images.objects.all())
        page = request.GET.get('page', 1)
        paginator = PageNumberPagination()
        photos = paginator.paginate_queryset(photos.qs, request)
        serializer = ImagesSerializer(photos, many=True)
        return paginator.get_paginated_response(serializer.data)


class PhotosDetail(APIView):
    def get(self,request,id):
        image = Images.objects.get(id=id)
        serializer = ImagesSerializer(image)

        return Response(serializer.data)

