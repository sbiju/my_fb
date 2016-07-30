from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from datetime import datetime


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    PostModel = instance.__class__
    try:
        new_id = PostModel.objects.order_by("id").last().id + 1
    except:
        PostModel.objects.last() == 0
        new_id = 1
    return "%s/%s" %(new_id, filename)


class BlogPost(models.Model):
    owner = models.ForeignKey(User, related_name='current_user')
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=500, editable=False)
    image = models.FileField(upload_to=upload_location,
            null=True, 
            blank=True, 
           )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Creation date", default=datetime.now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_shared = models.BooleanField(default=False, verbose_name='Share')

    objects = PostManager()

    def __unicode__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_absolute_user(self):
        return reverse('profiles:user_detail', kwargs={'pk': self.pk})


    class Meta:
        ordering = ["-publish", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = BlogPost.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=BlogPost)









