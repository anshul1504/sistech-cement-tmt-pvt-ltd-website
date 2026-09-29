from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from apps.core.views import get_page_or_none

from .models import BlogCategory, BlogPost, GalleryCategory, GalleryItem


def gallery(request):
    items = GalleryItem.objects.filter(is_active=True, category__is_active=True).select_related("category")
    categories = GalleryCategory.objects.filter(is_active=True, items__is_active=True).distinct()
    counts = {key: items.filter(media_type=key).count() for key, _ in GalleryItem.MEDIA_TYPES}
    return render(request, "media_center/gallery.html", {
        "page": get_page_or_none("gallery"), "items": items, "categories": categories,
        "media_counts": counts, "total_items": items.count(), "has_cta_section": False,
    })


def blog_list(request):
    posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED, published_at__lte=timezone.now(), category__is_active=True).select_related("category")
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    featured = posts.filter(is_featured=True).first() if not query and not category_slug else None
    if featured:
        posts = posts.exclude(pk=featured.pk)
    page_obj = Paginator(posts, 9).get_page(request.GET.get("page"))
    return render(request, "media_center/blog_list.html", {
        "page": get_page_or_none("blog"), "posts": page_obj, "page_obj": page_obj,
        "featured": featured if page_obj.number == 1 else None,
        "categories": BlogCategory.objects.filter(is_active=True, posts__status=BlogPost.PUBLISHED).distinct(),
        "query": query, "selected_category": category_slug, "has_cta_section": False,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.select_related("category"), slug=slug, status=BlogPost.PUBLISHED, published_at__lte=timezone.now())
    related = BlogPost.objects.filter(status=BlogPost.PUBLISHED, published_at__lte=timezone.now(), category=post.category).exclude(pk=post.pk)[:3]
    return render(request, "media_center/blog_detail.html", {"post": post, "related_posts": related, "has_cta_section": False})
