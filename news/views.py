from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import News, Author, Category
from .forms import NewsForm, AuthorProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils import timezone

# Общие представления
def about(request):
    return render(request, 'about.html')

def news_list(request):
    news_items = News.objects.all().order_by('-published_date')
    categories = Category.objects.all()

    # Поиск
    query = request.GET.get('q')
    if query:
        news_items = news_items.filter(title__icontains=query) | news_items.filter(content__icontains=query)

    # Пагинация
    paginator = Paginator(news_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

def news_detail(request, pk):
    news = get_object_or_404(News, id=pk)
    return render(request, 'news/news_detail.html', {'news': news})

def news_search(request):
    news_list = News.objects.all()
    filter = NewsFilter(request.GET, queryset=news_list)
    paginator = Paginator(filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_search.html', {'filter': filter, 'page_obj': page_obj})

def category_news(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    is_subscribed = request.user in category.subscribers.all() if request.user.is_authenticated else False
    return render(request, 'category_news.html', {
        'category': category,
        'is_subscribed': is_subscribed
    })

# Представления для подписки/отписки
@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    messages.success(request, f'Вы подписались на категорию "{category.name}".')
    return redirect('news:category_news', category_id=category_id)

@login_required
def unsubscribe_from_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    messages.success(request, f'Вы отписались от категории "{category.name}".')
    return redirect('news:category_news', category_id=category_id)

# Представление для становления автором
@login_required
def become_author(request):
    user_has_author = hasattr(request.user, 'author')
    if request.method == 'POST' and not user_has_author:
        try:
            Author.objects.create(authorUser=request.user)
            messages.success(request, 'Вы стали автором!')
        except Exception as e:
            messages.error(request, f'Ошибка при создании автора: {str(e)}')
        return redirect('news:news_list')
    return render(request, 'news/become_author.html', {'user_has_author': user_has_author})

# Классовые представления
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_news'
    model = News
    form_class = NewsForm
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        # Проверка, является ли пользователь автором
        return self.request.user.is_authenticated and hasattr(self.request.user, 'author')

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        form.instance.type = 'news'
        today = timezone.now().date()
        news_count = News.objects.filter(author=self.request.user.author, published_date__date=today).count()
        if news_count >= 3:
            messages.error(self.request, 'Вы не можете публиковать более 3 новостей в сутки.')
            return redirect('news:news_list')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не зарегистрированы как автор. Станьте автором перед созданием новости.')
        return redirect('news:become_author')

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_news'
    model = News
    form_class = NewsForm
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'author')

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        form.instance.type = 'article'
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для создания статей. Станьте автором.')
        return redirect('news:become_author')

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_news'
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        news = self.get_object()
        return self.request.user.is_authenticated and (news.author.authorUser == self.request.user or self.request.user.is_staff)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этой записи.')
        return redirect('news:news_list')

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_news'
    model = News
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        news = self.get_object()
        return self.request.user.is_authenticated and (news.author.authorUser == self.request.user or self.request.user.is_staff)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этой записи.')
        return redirect('news:news_list')

class AuthorProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorProfileForm
    template_name = 'news/author_profile_edit.html'
    success_url = reverse_lazy('news:news_list')

    def get_object(self, queryset=None):
        return self.request.user.author