import os
import logging
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
    apply_embossing,
)

# Configure logging for debugging purposes
logger = logging.getLogger(__name__)

def save_filtered_image(photo, filtered_image):
    # Define the save path
    filtered_path = f'photos/filtered/filtered_{photo.original_image.name}'
    filtered_full_path = os.path.join(settings.MEDIA_ROOT, filtered_path)

    # Ensure directories exist
    os.makedirs(os.path.dirname(filtered_full_path), exist_ok=True)

    # Save the filtered image to the defined path
    filtered_image.save(filtered_full_path)

    # Update the model instance
    photo.filtered_image.name = filtered_path
    photo.save()
# Upload photo and apply filters
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()  # Save the form (photo) to the database
            original_path = photo.original_image.path
            filtered_dir = os.path.join(settings.MEDIA_ROOT, 'photos', 'filtered')

            # Ensure the filtered directory exists
            os.makedirs(filtered_dir, exist_ok=True)

            # Apply the selected filter
            filter_type = request.POST.get('filter_type')
            filtered_filename = f"filtered_{os.path.basename(original_path)}"
            filtered_path = os.path.join(filtered_dir, filtered_filename)

            try:
                # Apply the filter based on the selected filter type
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
                    logger.error(f"Unknown filter type: {filter_type}")
                    return render(
                        request,
                        'photo_filter/upload.html',
                        {'form': form, 'error': f"Unknown filter type: {filter_type}"}
                    )

                # Save the filtered image path in the model
                relative_filtered_path = os.path.join('photos', 'filtered', filtered_filename)
                photo.filtered_image.name = relative_filtered_path
                photo.save()  # Save updated photo object with the filtered image path

                # Redirect to the photo detail page
                return redirect('photo_detail', pk=photo.pk)
            except Exception as e:
                logger.error(f"Error applying filter: {e}")
                return render(
                    request,
                    'photo_filter/upload.html',
                    {'form': form, 'error': "An error occurred while applying the filter."}
                )
    else:
        form = PhotoForm()  # Create a new form if it's a GET request

    return render(request, 'photo_filter/upload.html', {'form': form})


# View to show photo details (original and filtered images)
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    # Use default images if the media files are missing
    if not photo.original_image or not photo.original_image.path or not os.path.exists(photo.original_image.path):
        photo.original_image.name = 'photos/originals/default.jpg'

    if not photo.filtered_image or not photo.filtered_image.path or not os.path.exists(photo.filtered_image.path):
        photo.filtered_image.name = 'photos/filtered/default.jpg'

    return render(request, 'photo_filter/detail.html', {'photo': photo})


# About Us page
def about_us(request):
    # Example member images
    default_member_image = "/static/images/default_member.jpg"
    members = [
        {"image_url": "/static/images/member1.jpg", "fullname": "Duman Yessenbay", "id": "210107150", "group": "02-N/07-P"},
        {"image_url": "/static/images/member2.jpg", "fullname": "Omargali Tlepbergenov", "id": "210107016", "group": "02-N/07-P"},
        {"image_url": "/static/images/member3.jpg", "fullname": "Zhassulan Manap", "id": "210103266", "group": "02-N/07-P"},
        {"image_url": "/static/images/member4.jpg", "fullname": "Zanggar Zhazylbekov", "id": "210107070", "group": "02-N/07-P"},
        {"image_url": "/static/images/member5.png", "fullname": "Adilzhan Kuzembayev", "id": "210103451", "group": "02-N/07-P"},
    ]

    # Fallback to a default image if member images are missing
    for member in members:
        if not os.path.exists(os.path.join(settings.BASE_DIR, member['image_url'][1:])):
            member['image_url'] = default_member_image

    documentation_url = "https://docs.google.com/document/d/1SOhjJYOj7Jj860L72wjiwRS_uYtzNOSmA19oQzCE_Iw/edit?tab=t.0"
    return render(request, 'photo_filter/about_us.html', {"members": members, "documentation_url": documentation_url})
