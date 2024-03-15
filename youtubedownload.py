from pytube import YouTube

# Initialize an empty list to hold the URLs
urls = []

while True:
    # Ask the user for a YouTube URL
    url = input("Enter a YouTube URL (or 'quit' to finish): ")
    
    # If the user enters 'quit', break the loop
    if url.lower() == 'quit':
        break
    
    # Otherwise, add the URL to the list
    urls.append(url)

# Now loop through the URLs and download each one
for url in urls:
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Filter out all the files with "mp4" extension
        mp4files = yt.streams.filter(file_extension='mp4')

        # Get the video with the extension and resolution
        d_video = mp4files[-1].download()

        print(f'Download of {url} complete!')
    except Exception as e:
        print(f'Error occurred: {str(e)}')
