from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['original_image', 'description']  # Include description if you want users to input it

    # Optionally, you can add custom validation or file handling logic for the original image if needed
    def clean_original_image(self):
        # Here you can add any custom validation if needed
        image = self.cleaned_data.get('original_image')
        # Example: Check if the file is too large or if the format is incorrect
        return image
