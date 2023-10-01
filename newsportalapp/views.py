from django.http import HttpResponse
from django.views import View

from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes#, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save

from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

# from NewsPortal_django.newsportalapp.my_functions import mail_notification_post_create, subscribe

from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Category, User, SubscribeCategory

from django.utils.decorators import method_decorator

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, SubscribeForm
from datetime import datetime, timedelta
from .filters import PostFilter
from django.conf import settings

from .tasks import mail_notification_post_create

from django.utils.translation import gettext as _  # импортируем функцию для перевода


# Create your views here.
class Index(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = Post.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'index.html', context))


def wms():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week).values_list('post_category', flat=True)
    categories = SubscribeCategory.objects.filter(category_connection_id__in=posts).values_list("subscriber_connection_id", flat=True)
    subscribers = set(User.objects.filter(pk__in=categories).values_list('email', flat=True))
    # ['Korwin@yandex.ru']
    # set(Category.objects.filter(category_name__in=categories).values_list('subscribecategory__email', flat=True))

    # from newsportalapp.models import User, Category, Post, SubscribeCategory
    # a = Post.objects.filter(id__gte=80).values_list('post_category', flat=True)
    # b = SubscribeCategory.objects.filter(category_connection_id__in=a).values_list("subscriber_connection_id", flat=True)
    # c = User.objects.filter('pk__in'=b).values_list('email', flat=True)
    # c

    html_context = render_to_string(
        'weekly_news.html', {
            'link': settings.SITE_URL,
            # 'http://127.0.0.1:8000/news/'
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()


# @receiver(post_save, sender=PostCreate)
def mail_data_fill(request, category, subscribecategory, success_url, post_id):
    client_username_lst = []

    # # отправляем письмо
    recipient_list = []
    qs_postcategory = request.POST['post_category']
    if int(qs_postcategory) > 0:
        _category_name = category.objects.filter(pk=qs_postcategory).values('category_name')
        qs_authorcategory = subscribecategory.objects.filter(category_connection=qs_postcategory).values('subscriber_connection')
        if qs_authorcategory.exists():
            for ac_id in qs_authorcategory.values():
                qs_user = User.objects.filter(pk=ac_id.get('subscriber_connection_id')).values('username', 'email', 'last_name', 'first_name')

                # - И при добавлении новости из этой категории пользователю на email, указанный при регистрации, приходит письмо
                # с HTML-кодом заголовка и первых 50 символов текста статьи.

                client_username = qs_user[0].get("username")  # логин подписчика
                client_username_lst.append(client_username)
                client_fname = qs_user[0].get("first_name")  # имя подписчика
                client_lname = qs_user[0].get("last_name")  # фамилия подписчика
                client_email = qs_user[0].get('email')  # почта подписчика
                category_name = _category_name[0].get("category_name")  # наименование категории нового поста
                # текст письма
                appointment_message = f'Здравствуйте, {client_fname}. Новая статья в Вашем любимом разделе!'
                appointment_message1 = request.POST["post_text"]
                # тема письма
                appointment_subject = f'Изменения в категории  {category_name} от {datetime.now()}. Публикация: {request.POST["post_title"]}'
                # список адресов получателей рассылки
                recipient_list = []
                recipient_list.append(client_email)
                appointment_title = request.POST["post_title"]
                link = f'http://127.0.0.1:8000/news/{post_id}'

                mail_notification_post_create(
                    link, appointment_title, appointment_message, appointment_message1,
                    appointment_subject, recipient_list, client_username)

                # send_mail(
                #     # Категория и дата записи будут в теме для удобства
                #     subject=appointment_subject,
                #     # сообщение с кратким описанием
                #     message=appointment_message,
                #     # здесь указываете почту, с которой будете отправлять
                #     from_email='Kornyushin.Vladislav@yandex.ru',
                #     # здесь список получателей
                #     recipient_list=recipient_list
                # )
    return HttpResponseRedirect(success_url, request)


@login_required
def subscribe(request, pk, category):
    user = request.user
    cat = category.objects.get(id=pk)
    cat.category_subscribe.add(user)

    message = f'Уважаемый, {user}! Вы успешно подписались на рассылку новостей в выбранных категориях!'
    return render(request, 'subscribe.html', {'category': cat, 'message': message})


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

    def get(self, request):
        # . Translators: This message appears on the home page only
        models = Post.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'news.html', context))

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
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


def how_many_posts(request):
    author_id = request.POST['post_author']
    select_posts = Post.objects.filter(post_author=author_id)
    i = 0
    for sp in select_posts.values():
        if sp.get('post_date').day == datetime.now().day\
                and sp.get('post_date').month == datetime.now().month\
                and sp.get('post_date').year == datetime.now().year:
            # print(f'{sp.get("post_date")} == {request.POST["post_date"]} ')
            i += 1
    return i

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

                # отправим подписчикам уведомление о появлении новой публикации
                mail_data_fill(self.request, Category, SubscribeCategory, self.success_url, post_ed.id)

        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     print(how_many_posts(self.request), ' < ', 3)
    #     if self.form_valid and how_many_posts(request) < 3:  # Один пользователь не может публиковать более трёх новостей в сутки
    #         return HttpResponseRedirect(self.success_url, request)
    #
    #     return render(request, '../create', {"form": form})


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

    # Переопределяем функцию получения списка постов
    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'news_category_list.html'
    context_object_name = 'category_news_list'

    def get_gueryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['is_not_subscriber'] = self.request.user not in self.category.category_subscribe.all()
        # context['category'] = self.category
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in Category.objects.all().values('category_subscribe')
        context['category'] = self.model.post_category
        return context


class SubscribeView(CreateView):
    # Указываем нашу разработанную форму
    form_class = SubscribeForm
    # модель категорий подписок
    model = SubscribeCategory
    # и новый шаблон, в котором используется форма.
    template_name = 'client_subscriber.html'
    success_url = '../../../'

    def post(self, request, *args, **kwargs):
        for a in request.POST.getlist('category_connection'):
            cc = SubscribeCategory.objects.filter(category_connection=a)
            for i in cc.values('subscriber_connection'):
                # SubscribeCategory.objects.filter(subscriber_connection=request.user.pk)
                if i.get('subscriber_connection') == request.user.pk:
                    print(f'Для пользователя {i} уже есть такая подписка (категория {a})')
                else:
                    subscribes = SubscribeCategory(category_connection=Category.objects.get(id=a),
                                           subscriber_connection=User.objects.get(pk=request.user.pk), )
                    subscribes.save()
        # subscribe(request, a, Category)

        return HttpResponseRedirect(self.success_url, request)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

