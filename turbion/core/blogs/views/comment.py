from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from turbion.core.blogs.decorators import post_view, titled
from turbion.core.blogs.models import Post, Comment, CommentAdd
from turbion.core.blogs import signals
from turbion.core.blogs.forms import comment as forms
from turbion.core.profiles import get_profile
from turbion.core.utils.decorators import templated, paged

def add_comment(request, next, defaults={}, post=None,
                comment=None, checker=lambda comment: True,
                status_getter=lambda comment: Comment.statuses.published):
    if comment and not checker(comment):
        return HttpResponseRedirect(next % comment.__dict__)

    if request.method == 'POST':
        form = forms.CommentForm(
                        data=request.POST,
                        request=request,
                        instance=comment
                )

        if form.is_valid():
            new_comment = form.save(False)

            if post:
                new_comment.post = post
            new_comment.__dict__.update(defaults)

            if 'view' in request.POST:
                comment = new_comment
            else:
                if not new_comment.created_by.trusted:
                    new_comment.status = status_getter(new_comment)

                new_comment.save()

                if comment:
                    signal = signals.comment_edited
                else:
                    signal = signals.comment_added

                signal.send(
                        sender=Comment,
                        comment=new_comment,
                        instance=post
                )

                if form.cleaned_data["notify"]:
                    CommentAdd.manager.subscribe(
                        new_comment.created_by,
                        new_comment.post
                    )

                return HttpResponseRedirect(next % new_comment.__dict__)
    else:
        form = forms.CommentForm(
                        request=request,
                        instance=comment
                )

    return {
        "comment_form": form,
        "comment": comment
    }

@templated('turbion/blogs/edit_comment.html')
@titled(page=_('Add comment to "{{post.title}}"'))
def add(request, post_id):
    post = get_object_or_404(Post.published.all(), pk=post_id)

    if not post.allow_comments:
        return HttpResponseRedirect(post.get_absolute_url())#FIXME: add message showing

    context = add_comment(
        request,
        post=post,
        status_getter=post.get_comment_status,
        next=post.get_absolute_url() + "#comment_%(id)s"
    )

    if isinstance(context, dict):
        context.update({
            "post": post,
        })

    return context

@templated('turbion/blogs/edit_comment.html')
@titled(page=_('Edit comment to "{{post.title}}"'))
def edit(request, comment_id):
    comment = get_object_or_404(models.Comment.published.select_related("post"),  pk=comment_id)
    post = comment.post

    context = add_comment(
        request,
        comment=comment,
        redirect=post.get_absolute_url()+"#comment_%(id)s",
        checker=lambda comment: get_profile(request) in (comment.author, post.created_by)
    )

    if isinstance(context, dict):
        context.update({
            "post": post
        })
    return context

def delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()

    return HttpResponseRedirect(request.GET.get("redirect", "/"))
