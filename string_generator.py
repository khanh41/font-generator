import random
import random as rnd
import re
import string

import requests
from bs4 import BeautifulSoup


def create_strings_from_file(filename, count):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, "r", encoding="utf8") as f:
        lines = [l[0:200] for l in f.read().splitlines() if len(l) > 0]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) >= count - len(strings):
                strings.extend(lines[0: count - len(strings)])
            else:
                strings.extend(lines)

    return strings


def create_strings_from_dict(length, allow_variable, count, lang_dict):
    """
        Create all strings by picking X random word in the dictionnary
    """

    dict_len = len(lang_dict)
    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            current_string += lang_dict[rnd.randrange(dict_len)]
            current_string += " "
        strings.append(current_string[:-1])
    return strings


def create_strings_from_wikipedia(minimum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    temp_regex = "[a-z0-9A-Z_àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ/,]+"
    pages = ["https://vi.wikipedia.org/wiki/L%E1%BB%8Bch_s%E1%BB%AD_Vi%E1%BB%87t_Nam",
             "https://vi.wikipedia.org/wiki/Vi%E1%BB%87t_Nam_th%E1%BB%9Di_ti%E1%BB%81n_s%E1%BB%AD",
             "https://vi.wikipedia.org/wiki/H%E1%BB%93ng_B%C3%A0ng",
             "https://vi.wikipedia.org/wiki/An_D%C6%B0%C6%A1ng_V%C6%B0%C6%A1ng",
             "https://vi.wikipedia.org/wiki/Th%E1%BB%9Di_k%E1%BB%B3_B%E1%BA%AFc_thu%E1%BB%99c_l%E1%BA%A7n_th%E1%BB%A9_nh%E1%BA%A5t",
             "https://vi.wikipedia.org/wiki/%C4%90%E1%BA%A1i_Vi%E1%BB%87t_s%E1%BB%AD_k%C3%BD_to%C3%A0n_th%C6%B0",
             "https://vi.wikipedia.org/wiki/Hai_B%C3%A0_Tr%C6%B0ng",
             "https://vi.wikipedia.org/wiki/Th%E1%BB%9Di_k%E1%BB%B3_B%E1%BA%AFc_thu%E1%BB%99c_l%E1%BA%A7n_th%E1%BB%A9_hai",
             "https://vi.wikipedia.org/wiki/Tri%E1%BB%87u_Vi%E1%BB%87t_V%C6%B0%C6%A1ng",
             "https://vi.wikipedia.org/wiki/Th%E1%BB%9Di_k%E1%BB%B3_B%E1%BA%AFc_thu%E1%BB%99c_l%E1%BA%A7n_th%E1%BB%A9_ba",
             "https://vi.wikipedia.org/wiki/Th%E1%BB%9Di_k%E1%BB%B3_t%E1%BB%B1_ch%E1%BB%A7_Vi%E1%BB%87t_Nam",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_Ng%C3%B4",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_%C4%90inh",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_Ti%E1%BB%81n_L%C3%AA",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_L%C3%BD",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_Tr%E1%BA%A7n",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_H%E1%BB%93",
             "https://vi.wikipedia.org/wiki/Th%E1%BB%9Di_k%E1%BB%B3_B%E1%BA%AFc_thu%E1%BB%99c_l%E1%BA%A7n_th%E1%BB%A9_t%C6%B0",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_H%E1%BA%ADu_L%C3%AA",
             "https://vi.wikipedia.org/wiki/Vi%E1%BB%87t_Nam",
             "https://vi.wikipedia.org/wiki/Chi%E1%BA%BFn_tranh_%C4%90%C3%B4ng_D%C6%B0%C6%A1ng",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_Nguy%E1%BB%85n",
             "https://vi.wikipedia.org/wiki/Nh%C3%A0_T%C3%A2y_S%C6%A1n"
             ]

    while len(sentences) < count:
        # We fetch a random page

        # page_url = "https://{}.wikipedia.org/wiki/Special:Random".format(lang)
        try:
            page = requests.get(random.choice(pages), timeout=3.0)  # take into account timeouts
        except requests.exceptions.Timeout:
            continue

        soup = BeautifulSoup(page.text, "html.parser")
        soup = soup.find("div", {"id": "mw-content-text"})

        text = soup.get_text(" ")
        text = text.replace("\n", " ").replace("\xa0", " ").replace(" , ", ", ").replace(" / ", "/")
        text = " ".join(re.findall(temp_regex, text))
        text = " " + " ".join(text.split())

        new_lines = []
        before_index = 0
        while True:
            random_start = random.randint(15, 50)
            end_index = text.find(" ", random_start + before_index)

            if end_index - before_index < 10:
                break

            temp = text[before_index + 1: end_index]

            new_lines.append(temp)
            before_index = end_index

        # Remove the last lines that talks about contributing
        sentences.extend(new_lines[0: max([1, len(new_lines) - 5])])

    sentences = list(set(sentences))
    new_sentences = []
    for i in range(count):
        temp = random.choices(sentences, k=random.randint(10, 20))
        new_sentences.append(temp)

    return new_sentences


def create_strings_randomly(length, allow_variable, count, let, num, sym, lang):
    """
        Create all strings by randomly sampling from a pool of characters.
    """

    # If none specified, use all three
    if True not in (let, num, sym):
        let, num, sym = True, True, True

    pool = ""
    if let:
        if lang == "cn":
            pool += "".join(
                [chr(i) for i in range(19968, 40908)]
            )  # Unicode range of CHK characters
        elif lang == "ja":
            pool += "".join(
                [chr(i) for i in range(12288, 12351)]
            )  # unicode range for japanese-style punctuation
            pool += "".join(
                [chr(i) for i in range(12352, 12447)]
            )  # unicode range for Hiragana
            pool += "".join(
                [chr(i) for i in range(12448, 12543)]
            )  # unicode range for Katakana
            pool += "".join(
                [chr(i) for i in range(65280, 65519)]
            )  # unicode range for Full-width roman characters and half-width katakana
            pool += "".join(
                [chr(i) for i in range(19968, 40908)]
            )  # unicode range for common and uncommon kanji
            # https://stackoverflow.com/questions/19899554/unicode-range-for-japanese
        else:
            pool += string.ascii_letters
    if num:
        pool += "0123456789"
    if sym:
        pool += "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~"

    if lang == "cn":
        min_seq_len = 1
        max_seq_len = 2
    elif lang == "ja":
        min_seq_len = 1
        max_seq_len = 2
    else:
        min_seq_len = 2
        max_seq_len = 10

    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, rnd.randint(1, length) if allow_variable else length):
            seq_len = rnd.randint(min_seq_len, max_seq_len)
            current_string += "".join([rnd.choice(pool) for _ in range(seq_len)])
            current_string += " "
        strings.append(current_string[:-1])
    return strings
