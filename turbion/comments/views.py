# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from turbion.comments.models import Comment, CommentAdd
from turbion.comments import signals
from turbion.comments import forms

def add_comment(request, next, defaults={}, connection=None,
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

            if connection:
                new_comment.connection = connection
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
                        instance=connection
                )

                if form.cleaned_data["notify"]:
                    CommentAdd.instance.subscribe(new_comment.created_by, new_comment.connection)

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

edit_comment = add_comment

def delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()

    return HttpResponseRedirect(request.GET.get("redirect", "/"))
