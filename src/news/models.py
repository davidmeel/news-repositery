from django.db import models
from general.models import BaseModel
from users.models import User




class PostCategory(BaseModel):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Post(BaseModel):
    title = models.CharField(max_length=64)
    description = models.TextField()
    
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class PostFiles(BaseModel):
    file = models.FileField(upload_to="files/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.file.name) 
    
    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

        
class PostComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=48)

    def __str__(self):
        return f"Commented by {self.user} on {self.post}"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class PostFavorites(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Added by {self.user} on {self.post}"
    
    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_favorite')
        ]
