import flickrapi
import urllib
import os

# Set up your Flickr API credentials
api_key = "03b014788a34e150d0f1f75c9a643806"
api_secret = "a8abdbeb2f5e16db"

# Set up the Flickr API client
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Define your search parameters
search_keywords = ['portrait', 'face']  # Example search keywords
num_images_per_keyword = 100  # Number of images to download per keyword

# Create a directory to save the downloaded images
save_dir = 'facedataset'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Search and download images for each keyword
for keyword in search_keywords:
    photos = flickr.photos.search(text=keyword, per_page=num_images_per_keyword)

    # Download each image
    for idx, photo in enumerate(photos['photos']['photo']):
        photo_id = photo['id']
        farm_id = photo['farm']
        server_id = photo['server']
        photo_secret = photo['secret']
        photo_url = f"https://farm{farm_id}.staticflickr.com/{server_id}/{photo_id}_{photo_secret}.jpg"

        # Save the image locally
        save_path = os.path.join(save_dir, f"{keyword}_{idx}.jpg")
        urllib.request.urlretrieve(photo_url, save_path)

        print(f"Downloaded image {idx + 1} for keyword: {keyword}")

print("Image collection complete!")
