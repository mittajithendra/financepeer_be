from multiprocessing import AuthenticationError
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogItemSerializer, UserSerializer
from .models import Blog,User
import jwt,datetime


class BlogItemViews(APIView):
    def post(self, request):
        token =  request.data['jwt']
        if not token:
            return Response({'rc':{'returncode':'2','errorCode':'Reg'}})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'rc':{'returncode':'2','errorCode':'Reg'}})
        rq_data = request.data['blogs']
        count = 0
        for blog_data in rq_data:
            serializer = BlogItemSerializer(data={"eid":blog_data['userId'],"bid":blog_data['id'],"title":blog_data['title'],"content":blog_data['body']})
            if serializer.is_valid():
                serializer.save()
                count+=1
        return Response({"rc":{"returncode":"0"},"status": "success", "count": count}, status=status.HTTP_200_OK)
class BlogView(APIView):
    def post(self, request, id=None):
        
        # if id:
        #     item = Blog.objects.get(id=id)
        #     serializer = BlogItemSerializer(item)
        #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        token =  request.data['jwt']
        if not token:
            return Response({'rc':{'returncode':'2','errorCode':'Reg',"errorMessage":"Login Required"}})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'rc':{'returncode':'2','errorCode':'Reg','errorMessage':"Login Expired"}})
        
        items = Blog.objects.all()
        serializer = BlogItemSerializer(items, many=True)
        return Response({'rc':{'returncode':'0'},"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        # user = User.objects.filter(id=payload['id']).first()
        # serializer = UserSerializer(user)
        # return Response(serializer.data)
    

class RegisterView(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response({'rc':{'returncode':'2','errorCode':'Reg'}})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'rc':{'returncode':'2','errorCode':'Reg'}})

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'rc':{'returncode':'0'}})

class LoginView(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'rc':{'returncode':'2','errorCode':'USER_NOT_FOUND'}})
        if not user.password==password:
            return Response({'rc':{'returncode':'2','errorCode':'Incorrect_Password'}})

        payload = {
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'rc':{
                'returncode': '0'
            },
            'jwt': token
        }
        return response
        
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            "rc":{
                "returncode": "0"
            },
            'message': 'success'
        }
        return response