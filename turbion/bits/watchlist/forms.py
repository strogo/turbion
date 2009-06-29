from django import forms

from turbion.bits.blogs.models import Post
from turbion.bits import watchlist

class SubscriptionForm(forms.Form):
    action = forms.ChoiceField(choices=[('subs', 'subscribe'), ('unsubs', 'unsubscribe')], widget=forms.HiddenInput())
    post = forms.ModelChoiceField(queryset=Post.published.all(), widget=forms.HiddenInput())
    code = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, user=None, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_code(self):
        code = self.cleaned_data['code']
        if code and code != self.user.get_code():
            raise forms.ValidationError('Wrong code')

        return code

    def process(self):
        action = self.cleaned_data['action']
        post = self.cleaned_data['post']

        if action == 'subs':
            watchlist.subscribe(self.user, 'new_comment', post=post)
        else:
            watchlist.unsubscribe(self.user, 'new_comment', post=post)

        return action, post
