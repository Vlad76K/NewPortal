# Create your models here.
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Sum
from django.db import utils
from django.contrib.auth.models import User
import datetime

from django.urls import reverse

article = 'A'
news = 'N'
POSTTYPE = [(article, 'Статья'),
            (news, 'Новость')]


# Модель, содержащая объекты всех авторов.
class Author(models.Model):
    # Имеет следующие поля:
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)  # - cвязь «один к одному» с встроенной моделью пользователей User;
    author_rating = models.IntegerField(default=0)                      # - рейтинг пользователя.Ниже будет дано описание того, как этот рейтинг можно посчитать.
    # _author_rating = models.IntegerField(default=0, db_column='author_rating') # - рейтинг пользователя.Ниже будет дано описание того, как этот рейтинг можно посчитать.

    # def get_author_name(self):
    #     a = Author.objects.filter(pk=self.author_user).values('author_user_id').first()
    #     u = User.objects.filter(pk=a.values()).values('username')
    #     for u_name in u[0].values():
    #         return u_name

    def get_best_author(self):
        # определяем автора с максимальным рейтингом и вытаскиваем его Id (ключ Author - User)
        QS_ba = Author.objects.all().order_by('-author_rating').values('author_user_id')
        items0 = []
        for val_ba in QS_ba[0].values():  # берем первый элемент из QuerySet (Id автора с максимальным рейтингом)
            QS_a = Author.objects.filter(author_user_id=val_ba).values('author_rating')
            for a_rating in QS_a[0].values():  # получим рейтинг - нулевой элемент списка, представленный в виде справочника
                QS_u = User.objects.filter(pk=val_ba).values('username')
                for u_name in QS_u[0].values(): # получим полное имя автора - нулевой элемент списка, представленный в виде справочника
                    items0.append({
                        'author_rating': a_rating,
                        'username': u_name
                    })
        return items0

    # обновление рейтингов авторов
    @property
    def update_rating(self):
        post_rating_sum = 0
        comments_author_rating_sum = 0
        comments_post_rating_sum = 0

        # Рейтинг состоит из следующего:
        # - суммарный рейтинг каждой статьи автора умножается на 3;
        QS1 = Post.objects.filter(post_author=self.pk).aggregate(Sum('post_rating'))
        for val_p in QS1.values():
            post_rating_sum += val_p

        # - суммарный рейтинг всех комментариев автора;
        QS2 = Comment.objects.filter(comment_user_id=self.author_user).aggregate(Sum('comment_rating'))
        for val_com in QS2.values():
            comments_author_rating_sum += val_com

        # - суммарный рейтинг всех комментариев к статьям автора.
        QS3 = Post.objects.filter(post_author_id=self.pk).values('pk')  # < QuerySet[{'pk': 1}, {'pk': 3}] >
        for i in range(len(QS3)):
            for val_cp in QS3[i].values():
                QS3_1 = Comment.objects.filter(comment_post_id=val_cp).aggregate(Sum('comment_rating'))
                for val_con in QS3_1.values():
                    comments_post_rating_sum += val_con

        self.author_rating = post_rating_sum*3 + comments_author_rating_sum + comments_post_rating_sum
        self.save()

    def __str__(self):
        return self.author_user.username


class Category(models.Model):
    # Категории новостей / статей — темы, которые они отражают(спорт, политика, образование и т.д.).
    # Имеет единственное поле (должно быть уникальным (в определении поля необходимо написать параметр unique = True)):
    category_name = models.CharField(max_length=50, unique=True)  # - название категории.

    def __str__(self):
        return self.category_name

# Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
class Post(models.Model):
    # Модель должна включать следующие поля:
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)          # - связь «один ко многим» с моделью Author;
    post_type = models.CharField(max_length=2, choices=POSTTYPE) #, default='N')  # - поле с выбором — «статья» или «новость»;
    post_date = models.DateTimeField(auto_now_add=datetime.datetime.now())     # - автоматически добавляемая дата и время создания;
    post_category = models.ManyToManyField(Category, through='PostCategory')   # - связь «многие ко многим» с моделью Category(с дополнительной моделью PostCategory);
    post_title = models.CharField(max_length=124)                              # - заголовок статьи / новости;
    post_text = models.TextField()                                             # - текст статьи / новости;
    post_rating = models.IntegerField()                # - рейтинг статьи / новости.

    # - Метод like() увеличивает рейтинг на единицу.
    @property
    def like(self):
        self.post_rating += 1
        self.save()

    # - Метод dislike() уменьшает рейтинг на единицу.
    @property
    def dislike(self):
        self.post_rating -= 1
        self.save()

    # - Метод preview(), который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):
        return str(self.post_text)[0:125] + '...'

    @property
    def paginator(self):
        pass

    # Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
    # основываясь на лайках / дислайках к этой статье.
    def post_info(self):
        items0 = []
        QS1 = Post.objects.all().order_by('-post_rating').values('post_author', 'post_date', 'post_rating', 'post_title', 'pk')
        post_au = QS1[0].get('post_author', -1)    # автор поста
        post_rt = QS1[0].get('post_rating', -999)  # рэйтинг поста
        post_tt = QS1[0].get('post_title', '-')    # заголовок поста
        post_dt = QS1[0].get('post_date', None)    # дата поста
        post_pk = QS1[0].get('pk', -1)             # первичный ключ поста

        author_name = '-'
        if post_au != -1:
            author_name = User.objects.filter(pk=post_au).values('username')[0].get('username')

        post_prw = '-'
        if post_pk != -1:
            p = Post.objects.get(pk=post_pk)
            post_prw = p.preview()

        items0.append({
            'username': author_name,  # фио автора
            'post_rating': post_rt,   # рэйтинг поста
            'post_title': post_tt,    # заголовок поста
            'post_prw': post_prw,     # превью поста
            'post_dt': post_dt        # дата поста
        })
        return items0

    # def __str__(self):
    #     return f'{self.post_text.title()}: {self.post_title[:10]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    # Вывести все комментарии(дата, пользователь, рейтинг, текст) к статье.
    def post_all_comments(self):
        items0 = []
        QS1 = Post.objects.all().order_by('-post_rating').values('pk')
        post_pk = QS1[0].get('pk', -1)

        QS3 = Comment.objects.filter(comment_post_id=post_pk).values('comment_datetime', 'comment_user', 'comment_rating', 'comment_text')
        for i in range(len(QS3)):
            comm_user_id = QS3[i].get('comment_user', -1)

            comm_dt = QS3[i].get('comment_datetime')
            comm_ur = User.objects.filter(pk=comm_user_id).values('username')[0].get('username', -1)
            comm_rt = QS3[i].get('comment_rating', -1)
            comm_tx = QS3[i].get('comment_text', '-')

            items0.append({
                'comment_datetime': comm_dt,  # дата комента
                'comment_user': comm_ur,      # автор комента
                'comment_rating': comm_rt,    # рэйтинг комента
                'comment_text': comm_tx       # текст комента
            })

        return items0

    # def PostListView(self):
    #     serv_list = self.objects.all().order_by('name')
    #     return render(request, 'posts.html', {'serv_list': serv_list})
    #     pass


# Промежуточная модель для связи «многие ко многим»:
class PostCategory(models.Model):
    # - связь «один ко многим» с моделью Post;
    post_connection = models.ForeignKey(Post, on_delete=models.CASCADE)
    # - связь «один ко многим» с моделью Category.
    category_connection = models.ForeignKey(Category, on_delete=models.CASCADE)


# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
class Comment(models.Model):
    # Модель будет иметь следующие поля:
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE) # - связь «один ко многим» с моделью Post;
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE) # - связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    comment_text = models.TextField()                                # - текст комментария;
    comment_datetime = models.DateTimeField(auto_now_add=datetime.datetime.now()) # - дата и время создания комментария;
    comment_rating = models.IntegerField()                           # - рейтинг комментария

    # - Метод like() увеличивает рейтинг на единицу.
    @property
    def like(self):
        self.comment_rating += 1
        self.save()

    # - Метод dislike() уменьшает рейтинг на единицу.
    @property
    def dislike(self):
        self.comment_rating -= 1
        self.save()

