from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import authentication,permissions,viewsets,serializers
from api.serializers import UserSerializer,PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from api.models import Posts,Comments
from django.views.generic import CreateView,FormView,TemplateView
from django.urls import reverse_lazy
from api.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
def appindex(request):
    return render(request, 'app-index.html')
class UserView(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
class PostsView(viewsets.ModelViewSet):
    #authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=PostSerializer
    querset=Posts.objects.all()
    def create(self,request,*args,**kwargs):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def get_queryset(self):
        return Posts.objects.all().exclude(user=self.request.user)
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Posts.objects.get(id=id)
        if request.user==object.user:
            object.delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("permission denied for the user")
    @action(methods=["POST"],detail=True)
    def add_post_like(self,request,*args,**kwargs):
        object=self.get_object()
        user=request.user
        object.post_like.add(user)
        return Response(data="post_like")
    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Posts.objects.get(id=id)
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,post=object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
class CommentsView(viewsets.ModelViewSet):
    #authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CommentSerializer
    queryset=Comments.objects.all()
    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError("method not allowed")
    def list(self,request,*args,**kwargs):
        raise serializers.ValidationError("method not allowed")
    def destroy(self, request, *args, **kwargs):
        object=self.get_object()
        if request.user==object.user:
            object.delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("permission denied for this user")
    @action(methods=["POST"],detail=True)
    def add_comment_like(self,request,*args,**kwargs):
        object=self.get_object()
        user=request.user
        object.comment_like.add(user)
        return Response(data="comment_liked")
class SignupView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self,form):
        messages.success(self.request,"account created successfully")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,"account creation failed")
        return super().form_invalid(form)
class SigninView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("user-home")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"login.html",{"form":form})
class HomeView(TemplateView):
    template_name="base.html"