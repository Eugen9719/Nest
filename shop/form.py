from django import forms

from shop.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-group', 'placeholder': 'Напиши отзыв'}))

    class Meta:
        model = ProductReview
        fields = ['review']