#!/usr/bin/python
import libs.fingerprint as fingerprint
from libs.reader_file import FileReader
from libs.db_sqlite import SqliteDatabase
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in zip_longest(fillvalue=fillvalue, *args))


def align_matches(matches):
    diff_counter = {}
    largest_count = 0
    song_id = -1

    for tup in matches:
      sid, diff = tup

      if diff not in diff_counter:
        diff_counter[diff] = {}

      if sid not in diff_counter[diff]:
        diff_counter[diff][sid] = 0

      diff_counter[diff][sid] += 1

      if diff_counter[diff][sid] > largest_count:
        largest_count = diff_counter[diff][sid]
        song_id = sid

    songM = db.get_song_by_id(song_id)

    return songM


def return_matches(hashes):
    mapper = {}
    for hash, offset in hashes:
        mapper[hash.upper()] = offset
    values = mapper.keys()
    count = 0


    for split_values in grouper(values, 50):
        query = """
            SELECT upper(hash), song_fk, offset
            FROM fingerprints
            WHERE upper(hash) IN (%s)
        """

        split_values = [y for y in split_values]
        query = query % ', '.join('?' * len(split_values))

        x = db.executeAll(query, split_values)

        matches_found = len(x)


        if matches_found > 0:
            msg = 'found hash matches'
            count += 1
            if count > 3:
                break
        else:
            msg = 'not hash matches found'

        print(msg)
        for hash, sid, offset in x:
            yield (sid, offset - mapper[hash])


def find_matches(samples, fs=fingerprint.DEFAULT_FS):
    hashes = fingerprint.fingerprint(samples, fs)
    return return_matches(hashes)


if __name__ == "__main__":
    db = SqliteDatabase()

    r = FileReader("testtest.mp3")
    audio = r.parse_audio()

    Fs = audio['Fs']
    channel_amount = len(audio['channels'])

    result = set()
    matches = []
    msg = None

    for channeln, channel in enumerate(audio['channels']):
        matches.extend(find_matches(channel))

    total_matches_found = len(matches)

    if total_matches_found > 0:
        print("Success")
        song = align_matches(matches)
        print(song[1])
    else:
        print("Cant find song")

