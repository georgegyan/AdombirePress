from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Category
from .forms import CommentForm, ContactForm, PostForm

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # For saving many-to-many relationships (tags)
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-publish_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentForm()  # Reset form after submission
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category, status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
def post_search(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query),
            status='published'
        ).order_by('-publish_date')
    
    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results
    })

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification
            send_mail(
                f"New Contact Message: {contact_message.subject}",
                f"You have received a new message from {contact_message.name} ({contact_message.email}):\n\n{contact_message.message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            return render(request, 'blog/contact_success.html')
    else:
        form = ContactForm()
    
    return render(request, 'blog/contact.html', {'form': form})