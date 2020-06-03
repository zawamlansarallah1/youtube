import os
import time
import traceback

from youtube_upload.auth import GoogleAuth
from youtube_upload.youtube import Youtube

from ..config import Config
from ..translations import Messages as tr


class Uploader:

    def __init__(self, file, title=None):
        
        self.file = file
        self.title = title


    async def start(self, progress=None, *args):
        self.progress = progress
        self.args = args

        await self._upload()

        return self.status, self.message


    async def _upload(self):
        try:

            auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
            
            if not os.path.isfile(Config.CRED_FILE):
                self.status = False
                
                self.message = "فشل الرفع بسبب عدم توثيق البوت بالقناه اليوتيوب الخاصه بك."
                
                return

            auth.LoadCredentialsFile(Config.CRED_FILE)

            google = auth.authorize()

            properties = dict(
                title = self.title if self.title else os.path.basename(self.file),
                description = 'تم رفع الفديو بواسطة بوت قناة زوامل انصار الله ,
                category = 27,
                privacyStatus = 'public'
            )

            youtube = Youtube(google)

            self.start_time = time.time()
            self.last_time = self.start_time

            r = await youtube.upload_video(video = self.file, properties = properties)

            self.status = True
            self.message = f"رابط الفديو على اليوتيوب هنا\n\n https://youtu.be/{r['id']}"
        except Exception as e:
            traceback.print_exc()
            self.status = False
            self.message = f"خطأ أثناء الرفع.\تفاصيل الخطأ: {e}"
        return

