from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profilepics",null=True)
    bio=models.CharField(max_length=200,null=True)
    following=models.ManyToManyField(User)
    timeline_pic=models.ImageField(upload_to="timelinepics",null=True)
class Posts(models.Model):
    title=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(null=True,upload_to="images")
    post_like=models.ManyToManyField(User,related_name="post_like")
    def __str__(self):
        return self.title
    @property
    def post_like_count(self):
        return self.post_like.all().count()
    @property
    def post_comments(self):
        return self.comments_set.all()    
class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=250)
    date=models.DateTimeField(auto_now_add=True)
    comment_like=models.ManyToManyField(User,related_name="comment_like")
    def __str__(self):
        return self.Comment
    @property
    def comment_like_count(self):
        return self.comment_like.all().count()
        