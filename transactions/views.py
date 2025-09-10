import os
import shutil
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from git import Repo

# -------------------------------
# Paths (adjust for local/Render)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Local folder to temporarily store uploaded files
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Local clone of the Render media repo
MEDIA_REPO_PATH = os.environ.get("MEDIA_REPO_PATH", os.path.join(BASE_DIR, "slips-media"))

# Repo URL with GitHub token stored as env variable (never hardcode your token!)
GITHUB_USERNAME = "FitzgeraldChallar"
GITHUB_PAT = os.environ.get("GITHUB_PAT")
MEDIA_REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_PAT}@github.com/FitzgeraldChallar/zinna_files.git"

# Name of the folder inside the repo that Render serves
MEDIA_DIR_NAME = "media"

# -------------------------------
# Helper function
# -------------------------------
def handle_uploaded_file(f):
    import os

    # Step 1: Save locally first
    base_filename = os.path.basename(f.name)  # <-- strip folder names
    local_storage = FileSystemStorage(location=UPLOAD_DIR)
    filename = local_storage.save(base_filename, f)
    file_path = local_storage.path(filename)


    # Step 2: Clone or pull the repo
    if not os.path.exists(MEDIA_REPO_PATH):
        Repo.clone_from(MEDIA_REPO_URL, MEDIA_REPO_PATH)
    repo = Repo(MEDIA_REPO_PATH)
    repo.git.pull()

    # Step 3: Copy file into media folder
    dest_path = os.path.join(MEDIA_REPO_PATH, MEDIA_DIR_NAME, filename)
    shutil.copy(file_path, dest_path)

    # Step 4: Commit & push
    repo.git.add(all=True)
    try:
        repo.git.commit(m=f"Add uploaded file {filename}")
        repo.git.push()
    except:
        # Ignore if nothing to commit
        pass

    # Step 5: Return public URL
    public_url = f"https://zinna-files.onrender.com/media/{filename}"
    return public_url

# -------------------------------
# Upload view
# -------------------------------
@csrf_exempt  # For testing; in production, handle CSRF properly
def upload_view(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        public_url = handle_uploaded_file(uploaded_file)
        return HttpResponse(f"File uploaded! Access it here: <a href='{public_url}' target='_blank'>{public_url}</a>")
    
    # For GET requests, simple message
    return HttpResponse("Send a POST request with a file (form-data key 'file') to upload.")
