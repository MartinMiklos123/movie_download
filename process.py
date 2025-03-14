import subprocess
import os
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import ffmpeg

# TS_SOURCE is a locator for .m3u8 file, which contains decrypted .ts links

TS_SOURCE = "index-v1-a1"

# KEY_SOURCE is a locator for encryption key

KEY_SOURCE = "encryption.key"

M3U8 = ".m3u8"

# Define the Node.js script file path
js_script = "script.js"

# change the path to ffmpeg

ffmpeg_path = r"C:\Users\martin2\Downloads\ffmpeg-2025-03-10-git-87e5da9067-full_build\ffmpeg-2025-03-10-git-87e5da9067-full_build\bin\ffmpeg.exe"

# change this path to where the .mp4 file will be downloaded

merge_path = r"C:\Users\martin2\Videos"


def url_file_loaded():
    return os.path.isfile('captured_urls.txt')


def process_urls():
    """
    function which filters urls that are not important for us
    we are essentially looking for urls containing encryption.key and
    index v1-a1 or "master"
    :return: returns list of urls which contains encrypt key or .m3u8 file
    """

    if url_file_loaded():
        print("stream links loaded successfully")
        print("-------------------------------------")
    else:
        print("something went wrong check script.js")
        return

    with open("captured_urls.txt", "r") as f:
        url_lst = list(filter(lambda x: (KEY_SOURCE in x or TS_SOURCE in x or M3U8 in x), f.read().split()))

    return url_lst


def process_ts_files():
    urls = process_urls()

    file_m3u8 = None
    decrypt_key = None

    for url in urls:
        if TS_SOURCE in url:
            file_m3u8 = url
        elif KEY_SOURCE in url:
            decrypt_key = url

    if file_m3u8 is None:
        print(f"m3u8 file not located :( , urls: {urls}")
        return False

    elif decrypt_key is None:
        print(f"decrypt key not found - this sometimes happens\n just reload the script")
        return False

    # [5:] - we skip the previously assigned decrypt key and proceed to
    # filter out garbage from the .ts urls

    content_file = requests.get(file_m3u8).text.split()[5:]
    content_file = list(filter(lambda x: "https" in x, content_file))

    return content_file, decrypt_key


def decrypt_ts_files():
    result = process_ts_files()

    if not result:
        print("Movie is not available")
        return False

    content_urls, key_url = result

    key_response = requests.get(key_url).content
    cipher = AES.new(key_response, AES.MODE_CBC)

    print("decrypting data")
    print("-------------------------------------")

    for i in range(len(content_urls)):
        print("decrypting file " + str(i) + " from " + str(len(content_urls)))

        segment_content = requests.get(content_urls[i]).content

        # magically decrypts the data for me :)

        decrypted_data = unpad(cipher.decrypt(segment_content), AES.block_size)

        with open(str(i) + '.decryptedSegment.ts', 'wb') as f:
            f.write(decrypted_data)


def remove_garbage_after_merge(ts_list):
    print("removing garbage")
    print("-------------------------------------")
    for del_file in ts_list:
        if os.path.isfile(del_file):
            os.remove(del_file)

    # some problems happened when it wasn't removed, so
    # I remove it after every merge

    if os.path.isfile("captured_urls.txt"):
        os.remove("captured_urls.txt")

    if os.path.isfile("filelist.txt"):
        os.remove("filelist.txt")


def merge_ts_files(name):
    decrypt_ts_files()

    # sorts decrypted files in order from <0.xxxx.ts, len - 1.xxxx.ts)

    print("sorting ts files for proper merge")
    print("-------------------------------------")

    ts_list = [f for f in os.listdir() if ".ts" in f]
    ts_list = [f.split(".") for f in ts_list]
    ts_list = sorted(ts_list, key=lambda x: int(x[0]))
    ts_list = [".".join(f) for f in ts_list]

    with open("filelist.txt", "w") as f:
        for ts in ts_list:
            f.write(f"file '{ts}'\n")

    # Use FFmpeg to merge the TS files into an MP4

    print("merging .ts files")
    print("-------------------------------------")

    path = merge_path + "\\" + name + ".mp4"
    ffmpeg.input("filelist.txt", format="concat", safe=0).output(path, c="copy").run(cmd=ffmpeg_path)

    print("Merging complete: output.mp4")
    print("-------------------------------------")

    # removes now useless .ts elements from folder

    remove_garbage_after_merge(ts_list)


def launch_script(link, name):
    if os.path.isfile(f"{name}.mp4"):
        print("file already exists")
        return

    result = subprocess.run(['node', js_script, link], capture_output=True, text=True)
    print("Errors from Node.js:\n", result.stderr)
    merge_ts_files(name)
