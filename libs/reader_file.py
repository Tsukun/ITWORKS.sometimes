import os
from hashlib import sha1
from libs.reader import BaseReader
import numpy as np
from pydub import AudioSegment
from pydub.utils import audioop


class FileReader(BaseReader):

    def __init__(self, filename):
        super(FileReader, self).__init__(filename)
        self.filename = filename

    def parse_audio(self, limit=None):
        result = None

        songname, extension = os.path.splitext(os.path.basename(self.filename))

        try:
            audiofile = AudioSegment.from_file(self.filename)

            if limit:
                audiofile = audiofile[:limit * 1000]

            data = np.fromstring(audiofile._data, np.int16)

            channels = []
            for chn in range(audiofile.channels):
                channels.append(data[chn::audiofile.channels])

            result = {
                "songname": songname,
                "extension": extension,
                "channels": channels,
                "Fs": audiofile.frame_rate,
                "file_hash": self.parse_file_hash()
            }
        except audioop.error:
            print('audioop.error')
            pass

        return result

    def parse_file_hash(self, blocksize=2 ** 20):
        s = sha1()

        with open(self.filename, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                s.update(buf)

        return s.hexdigest().upper()
