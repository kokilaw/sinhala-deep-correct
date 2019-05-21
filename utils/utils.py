import re

sinhala_punctuation_marks = [".", ",", "!", "?"]

short_forms = {
    "ඒ.": "aa",
    "බී.": "bb",
    "සී.": "cc",
    "ඩී.": "dd",
    "ඊ.": "ee",
    "එෆ්.": "ff",
    "ජී.": "gg",
    "එච්.": "hh",
    "අයි.": "ii",
    "ජේ.": "jj",
    "කේ.": "kk",
    "එල්.": "ll",
    "එම්.": "mm",
    "එන්.": "nn",
    "ඕ.": "oo",
    "පී.": "pp",
    "කිව්.": "qq",
    "ආර්.": "rr",
    "එස්.": "ss",
    "ටී.": "tt",
    "යූ.": "uu",
    "ඩබ්.": "WW",
    "ඩබ්ලිව්.": "ww",
    "එක්ස්.": "xx",
    "වයි.": "yy",
    "ඉසෙඩ්.": "zz",
    "පෙ.": "pe",
    "ව.": "wa",
    "ප.": "pa",
    "රු.": "ru",
    "0.": "0dot", "1.": "1dot", "2.": "2dot", "3.": "3dot", "4.": "4dot", "5.": "5dot",
    "6.": "6dot", "7.": "7dot", "8.": "8dot", "9.": "dot"
}

short_form_identifier = "\u0D80"


def encode_short_form_with_escape_values(text):
    encode_text = text
    for short_form, escape_form in short_forms.items():
        encode_text = encode_text.replace(short_form, escape_form)

    return encode_text


def decode_short_form_with_escape_values(text):
    decode_text = text

    for short_form, escape_form in short_forms.items():
        decode_text = decode_text.replace(escape_form, short_form)

    return decode_text


def tokenize_sinhala_text(text):
    escape_encoded_text = encode_short_form_with_escape_values(text)

    escape_encoded_text = re.sub(r"([.!?])", r"\1\t", escape_encoded_text)
    sentences = escape_encoded_text.split("\t")

    if '' in sentences:
        sentences.remove('')

    decoded_sentences = []

    for sentence in sentences:
        decoded_sentence = decode_short_form_with_escape_values(sentence)
        decoded_sentences.append(decoded_sentence)

    return decoded_sentences


def split(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default seperator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


if __name__ == "__main__":
    text = "මම පෙ.ව. 10ට එතැනට පැමිණියෙමි. මම පෙ.ව. 10ට එතැනට පැමිණියෙමි. මම පෙ.ව. 10ට එතැනට පැමිණියෙමි."
    print(tokenize_sinhala_text(text))
