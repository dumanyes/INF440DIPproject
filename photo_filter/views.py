import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import PhotoForm
from .models import Photo
from .utils import (
    apply_grayscale,
    apply_edge_detection,
    apply_gaussian_blur,
    apply_sepia,
    apply_sharpening,
    apply_embossing
)

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            original_path = photo.original_image.path
            filtered_dir = os.path.join(settings.MEDIA_ROOT, 'photos', 'filtered')

            # Ensure the filtered directory exists
            if not os.path.exists(filtered_dir):
                os.makedirs(filtered_dir)

            # Apply the selected filter
            filter_type = request.POST.get('filter_type')
            filtered_filename = f"filtered_{os.path.basename(original_path)}"
            filtered_path = os.path.join(filtered_dir, filtered_filename)

            if filter_type == 'grayscale':
                apply_grayscale(original_path, filtered_path)
            elif filter_type == 'edge_detection':
                apply_edge_detection(original_path, filtered_path)
            elif filter_type == 'gaussian_blur':
                apply_gaussian_blur(original_path, filtered_path)
            elif filter_type == 'sepia':
                apply_sepia(original_path, filtered_path)
            elif filter_type == 'sharpening':
                apply_sharpening(original_path, filtered_path)
            elif filter_type == 'embossing':
                apply_embossing(original_path, filtered_path)
            else:
                print(f"Unknown filter type: {filter_type}")  # Debugging

            # Save the filtered image path in the model
            relative_filtered_path = os.path.join('photos', 'filtered', filtered_filename)
            photo.filtered_image.name = relative_filtered_path
            photo.save()

            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()

    return render(request, 'photo_filter/upload.html', {'form': form})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo_filter/detail.html', {'photo': photo})


def about_us(request):
    members = [
        {"image_url": "/static/images/member1.jpg", "fullname": "Duman Yessenbay", "id": "210107150", "group": "02-N/07-P"},
        {"image_url": "/static/images/member2.jpg", "fullname": "Omargali Tlepbergenov", "id": "210107016", "group": "02-N/07-P"},
        {"image_url": "/static/images/member3.jpg", "fullname": "Zhassulan Manap", "id": "210103266", "group": "02-N/07-P"},
        {"image_url": "/static/images/member4.jpg", "fullname": "Zanggar Zhazylbekov", "id": "210107070", "group": "02-N/07-P"},
        {"image_url": "/static/images/member5.png", "fullname": "Adilzhan Kuzembayev", "id": "210103451", "group": "02-N/07-P"},
    ]
    documentation_url = "https://docs.google.com/document/d/1SOhjJYOj7Jj860L72wjiwRS_uYtzNOSmA19oQzCE_Iw/edit?tab=t.0"
    return render(request, 'photo_filter/about_us.html', {"members": members, "documentation_url": documentation_url})
