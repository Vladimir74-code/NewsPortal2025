from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.news_set.aggregate(postRating=Sum('rating'))
        pRat = postRat.get('postRating', 0) or 0
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = commentRat.get('commentRating', 0) or 0
        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return self.authorUser.username

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True, verbose_name="Подписчики")

    def __str__(self):
        return self.name

class News(models.Model):
    TYPE_CHOICES = [
        ('news', 'Новость'),
        ('article', 'Статья'),
    ]
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='news', verbose_name='Тип')
    rating = models.SmallIntegerField(default=0)
    categories = models.ManyToManyField(Category, through='NewsCategory', blank=True, verbose_name='Категории')

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Новость/Статья'
        verbose_name_plural = 'Новости/Статьи'

class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(News, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def post_com(self):
        return f'Комментарий к статье:\n Дата: {self.dateCreation}\nПользователь: {self.commentUser}\n Рейтинг: {self.rating}\n Комментарий: {self.text}'

@receiver(post_save, sender=News)
def send_new_article_email(sender, instance, created, **kwargs):
    if created:
        category = instance.categories.first()  # Берем первую категорию (можно доработать для нескольких)
        if category:
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                subject = f'Новая статья в категории {category.name}'
                message = f'Новая статья: {instance.title}\nКраткое содержание: {instance.content[:100]}...\nЧитать полностью: {reverse("news:news_detail", args=[instance.id])}'
                send_mail(
                    subject,
                    message,
                    'from@example.com',  # Замени на DEFAULT_FROM_EMAIL
                    [subscriber.email],
                    fail_silently=True,
                )