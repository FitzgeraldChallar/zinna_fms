import os
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from git import Repo

# Path to your local clone of the Render media repo
MEDIA_REPO_PATH = 'C:\Users\Fitzgerald Challar\Desktop\slips-media'

# URL of your media repo
MEDIA_REPO_URL = f"https://FitzgeraldChallar:{os.environ['GITHUB_PAT']}@github.com/FitzgeraldChallar/zinna_files.git"

# Directory inside the repo that Render serves
MEDIA_DIR_NAME = 'media'


def handle_uploaded_file(f):
    # Step 1: Save file locally first
    local_storage = FileSystemStorage(location=r"C:\Users\Fitzgerald Challar\Desktop\uploads")
    filename = local_storage.save(f.name, f)
    file_path = local_storage.path(filename)

    # Step 2: Clone the Render media repo (or pull if already cloned)
    if not os.path.exists(MEDIA_REPO_PATH):
        Repo.clone_from(MEDIA_REPO_URL, MEDIA_REPO_PATH)
    repo = Repo(MEDIA_REPO_PATH)
    repo.git.pull()

    # Step 3: Copy uploaded file into media folder
    dest_path = os.path.join(MEDIA_REPO_PATH, MEDIA_DIR_NAME, filename)
    shutil.copy(file_path, dest_path)

    # Step 4: Commit & push to GitHub
    repo.git.add(all=True)
    repo.git.commit(m=f'Add uploaded file {filename}')
    repo.git.push()

    # Step 5: Return public URL for user
    public_url = f'https://zinna-files.onrender.com/{filename}'
    return public_url
