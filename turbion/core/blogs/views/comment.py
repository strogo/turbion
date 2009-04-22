from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django import http

from turbion.core.blogs.decorators import post_view, titled
from turbion.core.blogs.models import Post, Comment
from turbion.core.blogs import signals
from turbion.core.blogs import forms
from turbion.core.profiles import get_profile
from turbion.core.utils.decorators import templated, paged
from turbion.core.utils import antispam

def _do_comment(request, post, defaults={}, comment=None):
    profile = get_profile(request)

    if not post.allow_comment_from(profile):
        return http.HttpResponseRedirect(post.get_absolute_url())#FIXME: add message

    if comment and profile not in (comment.author, post.created_by):
        return http.HttpResponseRedirect(comment.get_absolute_url())

    if request.method == 'POST':
        form = forms.CommentForm(
            data=request.POST,
            request=request,
            instance=comment
        )
        antispam.process_form_init(request, form)

        if form.is_valid():
            new_comment = form.save(False)

            if post:
                new_comment.post = post
            new_comment.__dict__.update(defaults)

            if 'view' in request.POST:
                comment = new_comment
            else:
                if not new_comment.created_by.trusted:
                    new_comment.status = post.get_comment_status(new_comment)

                decision = antispam.process_form_submit(
                    request, form, new_comment, post
                )
                if decision == "spam":
                    new_comment.status = Comment.statuses.spam

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

                new_comment.subscribe_author(email=bool(form.cleaned_data["notify"]))
                new_comment.emit_event()

                if form.need_auth_redirect():
                    return http.HttpResponseRedirect(
                        form.auth_redirect(new_comment.get_absolute_url())
                    )

                return http.HttpResponseRedirect(new_comment.get_absolute_url())
    else:
        form = forms.CommentForm(
            request=request,
            instance=comment
        )
        antispam.process_form_init(request, form)

    return {
        "comment_form": form,
        "comment": comment
    }

@templated('turbion/blogs/edit_comment.html')
@titled(page=_('Add comment to "{{post.title}}"'))
def add(request, post_id):
    post = get_object_or_404(Post.published.all(), pk=post_id)

    if not post.allow_comments:
        return http.HttpResponseRedirect(post.get_absolute_url())#FIXME: add message showing

    context = _do_comment(
        request,
        post=post,
    )

    if isinstance(context, dict):
        context.update({
            "post": post,
        })

    return context

@templated('turbion/blogs/edit_comment.html')
@titled(page=_('Edit comment to "{{post.title}}"'))
def edit(request, comment_id):
    comment = get_object_or_404(
        models.Comment.published.select_related("post"),
        pk=comment_id
    )
    post = comment.post

    context = _do_comment(
        request,
        post=post,
        comment=comment
    )

    if isinstance(context, dict):
        context.update({
            "post": post
        })
    return context

def delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()

    return http.HttpResponseRedirect(request.GET.get("next", "/"))
