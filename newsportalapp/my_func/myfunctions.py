def send_mail_weekly():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers = ['Korwin@yandex.ru']
        # set(Category.objects.filter(category_name__in=categories).values_list('subscribecategory__email', flat=True))

    html_context = render_to_string(
        'weekly_news.html', {
            'link': 'http://127.0.0.1:8000/news/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='Kornyushin.Vladislav@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()


