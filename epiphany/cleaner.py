# cleaner.py

import re

def remove_chat_metadata(chat_export_file):
    date_time = r"(\d+\/\d+\/\d+, \s\d+:\d+)" 
    dash_whitespace = r"\s- \s"
    username = r"([\w\s]+)"
    metadata_end = r" :\s"
    pattern = date_time + dash_whitespace + username + metadata_end

    with open(chat_export_file, "r") as corpus_file:
        content = content_file.read()
    cleaned_corpus = re.sub(pattern, " ", content)
    return tuple(cleaned_corpus.split("\n"))

if __name__ == "__main__":
    print(remove_chat_metadata("chat.text"))
