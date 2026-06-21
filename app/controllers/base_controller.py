import os


class BaseController:
    def __init__(self, app):
        self.app = app
        self.upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')

    def allowed_file(self, filename):
        from app.config import ALLOWED_EXTENSIONS
        return "." in filename and \
               filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_upload(self, file):
        import uuid
        if file and file.filename:
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(self.upload_folder, filename)
            os.makedirs(self.upload_folder, exist_ok=True)
            file.save(filepath)
            return filename
        return None

    def delete_upload(self, filename):
        if filename:
            filepath = os.path.join(self.upload_folder, filename)
            if os.path.exists(filepath):
                os.remove(filepath)