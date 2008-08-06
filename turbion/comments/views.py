# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import *

from turbion.blogs.models import Comment
from turbion.comments import signals
from turbion.comments import forms

def add_comment(request,
                defaults={},
                redirect=None,
                connection=None,
                comment=None,
                checker=lambda comment: True):
    if comment and not checker(comment):
        return HttpResponseRedirect(redirect and redirect or new_comment.get_absolute_url())

    if request.method == 'POST':
        form = forms.CommentForm(data=request.POST,
                                request=request,
                                instance=comment)

        if form.is_valid():
            new_comment = form.save(False)

            if 'view' in request.POST:
                comment = new_comment
            else:
                if connection:
                    new_comment.connection = connection
                new_comment.__dict__.update(defaults)
                new_comment.save()

                if comment:
                    signal = signals.comment_edited
                else:
                    signal = signals.comment_added

                signal.send(sender=Comment,
                            comment=new_comment,
                            instance=connectio
                        )

                return HttpResponseRedirect(redirect and redirect or new_comment.get_absolute_url())
    else:
        form = forms.CommentForm(request=request,
                                instance=comment)

    return { "comment_form": form,
             "comment"     : comment
            }

edit_comment = add_comment

def delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()

    return HttpResponseRedirect(request.GET.get("redirect", "/"))
