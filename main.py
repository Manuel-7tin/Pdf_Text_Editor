# import os
import fitz

# This project is aimed at reading a company's drafted email in pdf, editing
# and personalizing the message for  their vip clients


def edit_word(sentence: bytes, old_word: str, new_word: str, separator: str = "\n") -> str:
    """Takes in a byte string, replaces target word and returns the output as a string"""
    # if isinstance(sentence, bytes):
    sentence = sentence.decode("utf-8")  # decode byte string
    sentence_list = sentence.split("\n")  # split string into list of  single sentences (for multiline strings)
    for i in range(len(sentence_list)):
        word_list = sentence_list[i].split()  # split sentence into list of words
        for word in word_list:
            if word.lower() == old_word.lower():  # identify the target word in the word list
                index = word_list.index(word)  # determine target word location in the list
                word_list[index] = new_word  # replace target word with substitute word
        sentence_list[i] = " ".join(word_list)  # convert word-list back into a sentence (string)

    return separator.join(sentence_list)  # return new string


filenames = ["company_christmas_letter", "company_new-year_letter"]
# Read and store vip names
with open("vip_names.txt") as vips:
    names = vips.read()
    vip_names = names.split(", ")
for file in filenames:
    # Open, read original documents and write new ones
    doc = fitz.open(f"./old_greet_letters/{file}.pdf")  # open a document
    for page in doc:  # iterate the document pages
        print("typoooo", type(page.get_text()))
        text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
        company_text = edit_word(text, "d_company", "Python-Company")  # replace target word
        for name in vip_names:
            text = edit_word(company_text.encode("utf8"), "vip_customer,", name, "\n\n")  # replace target word
            print("nn", name, "mm")
            docu = fitz.open()  # create empty pdf
            new_page = docu.new_page()  # create empty page
            print("Texte below\n", text)
            new_page.insert_text((50, 72), text)  # insert the data
            docu.save(f"./new_greet_letters/{file}_to_{name.split()[1]}.pdf")  # save pdf document
