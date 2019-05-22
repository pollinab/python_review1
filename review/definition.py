import string
from collections import Counter
import json


def get_code(symbol, key, factor):
    if ord('a') <= ord(symbol) <= ord('z'):
        index = ord(symbol) + key
        if index > ord('z') or index < ord('a'):
            index -= (ord('z') - ord('a') + 1) * factor
        return chr(index)
    elif ord('A') <= ord(symbol) <= ord('Z'):
        index = ord(symbol) + key
        if index > ord('Z') or index < ord('A'):
            index -= (ord('Z') - ord('A') + 1) * factor
        return chr(index)
    else:
        return symbol


def caesar(key, input_text, func_type):
    res = []
    if func_type == 'decode':
        factor = -1
    else:
        factor = 1
    key *= factor
    for symbol in input_text:
        res.append(get_code(symbol, key, factor))
    return "".join(res)


def vigenere(key, input_text, func_type):
    res = []
    length = len(input_text)
    key = key.lower()
    if func_type == 'encode':
        factor = 1
    else:
        factor = -1
    for i in range(length):
        symbol = input_text[i]
        key_value = ord(key[i % len(key)]) - ord('a')
        key_value *= factor
        res.append(get_code(symbol, key_value, factor))
    return "".join(res)


def train(text, file):
    frequency = Counter(s.lower() for s in text if s in string.ascii_letters)
    length = sum(frequency.values())
    for key in frequency:
        frequency[key] /= length
    with open(file, "w") as write_file:
        json.dump(frequency, write_file)


def hack(input_text, model_file):
    with open(model_file, "r") as read_file:
        normal_frequency = json.load(read_file)
    text0 = ''.join(s.lower() for s in input_text
                    if s in string.ascii_letters)
    min_deflection = float("inf")
    min_key = 0
    text = caesar(0, text0, 'decode')
    frequency = Counter(text)
    length = len(text)
    for i in frequency:
        frequency[i] /= length
    for key in range(26):
        deflection = 0
        for symbol in string.ascii_lowercase:
            code_index = ord(symbol) + key
            if code_index > ord('z'):
                code_index -= (ord('z') - ord('a') + 1)
            code = chr(code_index)
            deflection += (frequency[code] - normal_frequency[symbol])**2
        if deflection < min_deflection:
            min_deflection = deflection
            min_key = key
    return caesar(min_key, input_text, 'decode')
