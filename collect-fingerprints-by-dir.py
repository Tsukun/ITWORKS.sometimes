#!/usr/bin/python
import os

import libs.fingerprint as fingerprint
from libs.db_sqlite import SqliteDatabase
from libs.reader_file import FileReader

if __name__ == '__main__':

    db = SqliteDatabase()
    path = "music/"

    # fingerprint all files in a directory

    for filename in os.listdir(path):
        if filename.endswith(".mp3"):
            readonly_filename = os.path.splitext(filename)[0]
            reader = FileReader(path + filename)
            audio = reader.parse_audio()

            song = db.get_song_by_filehash(audio['file_hash'])
            song_id = db.add_song(filename, audio['file_hash'])

            if song:
                hash_count = db.get_song_hashes_count(song_id)

                if hash_count > 0:
                    print(f"already exist {readonly_filename}")
                    continue

            print("new song, analyze...")
            print(readonly_filename)

            hashes = set()
            channel_amount = len(audio['channels'])

            for channel_n, channel in enumerate(audio['channels']):
                print(f"fingerprinting channel {channel_n + 1} of {channel_amount}")

                channel_hashes = fingerprint.fingerprint(channel, Fs=audio['Fs'])
                channel_hashes = set(channel_hashes)

                print(f"fingerprinting channel {channel_n + 1} of {channel_amount}, got {len(channel_hashes)} hashes")

                hashes |= channel_hashes

            values = []
            for hash, offset in hashes:
                values.append((song_id, hash, offset))

            print(f"storing {len(values)} hashes in db")

            print(values)
            db.store_fingerprints(values)

    print("Finish")
