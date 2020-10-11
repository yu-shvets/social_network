from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . serializers import UserSerializer, PostSerializer, MyTokenObtainPairSerializer
from . models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreate(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PostCreateApiView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikesUpdateApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.likes += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostDisLikesUpdateApiView(PostLikesUpdateApiView):

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.dislikes += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnalyticsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        posts = Post.objects.filter(created__date__range=(date_from, date_to)).values('created__date', 'likes')
        analytics = {}
        for post in posts:
            date = str(post['created__date'])
            if date not in analytics.keys():
                analytics[date] = post['likes']
            else:
                analytics[date] += post['likes']
        return Response(analytics, status=status.HTTP_200_OK)


class UserAnalyticsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        response = {
            'user_id': user.id,
            'user_username': user.username,
            'user_email': user.email,
            'user_last_login': user.last_login
        }
        return Response(response, status=status.HTTP_200_OK)
