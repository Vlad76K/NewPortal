from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from datetime import datetime
from .filters import PostFilter


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['next_action'] = "Творческий вечер в среду!"
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'new'

# def create_post(request):
#     form = PostForm()
#
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('../')
#
#     return render(request, 'news_edit.html', {'form': form})

# Добавляем новое представление для создания постов.
class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель постов
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'
    success_url = '../../../'

    permission_required = ('newsportalapp.add_post', )

    def form_valid(self, form):
        if form.is_valid():
            post_ed = form.save(commit=False)
            if self.request.method == 'POST':
                path_url = self.request.META['PATH_INFO']
                if path_url == '/news/new/create/':
                    post_ed.post_type = 'N'
                elif path_url == '/news/article/create/':
                    post_ed.post_type = 'A'
                else:
                    post_ed.post_type = 'U'
                post_ed.save(self)

        return super().form_valid(form)


# Добавляем представление для изменения товара.
@method_decorator(login_required, name='dispatch')
class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('newsportalapp.change_post', )

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    # template_name = 'prodected_page.html'
    success_url = '../../../'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_date'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю должны быть показаны наши объекты
    template_name = 'news_search.html'
    # Это имя списка, в котором будут лежать все объекты. Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 3  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context
