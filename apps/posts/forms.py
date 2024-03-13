from django import forms

from apps.posts.models import Post


class PostLikeForm(forms.Form):
    """
    Django Form for validation
    """

    post = forms.IntegerField()
    action = forms.ChoiceField(
        choices=(
            ("like", "like"),
            ("unlike", "unlike"),
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        post_id = cleaned_data.get("post")
        try:
            post = Post.objects.get(id=post_id)
            cleaned_data["post"] = post
        except Post.DoesNotExist:
            self.add_error(
                "post", forms.ValidationError("Post does not exist")
            )
        return cleaned_data
