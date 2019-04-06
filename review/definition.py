import string
from collections import Counter
import json


def caesar(key, input_text, func_type):
    res = ''
    if func_type == 'decode':
        factor = -1
    else:
        factor = 1
    key *= factor
    for symbol in input_text:
        if ord('a') <= ord(symbol) <= ord('z'):
            index = ord(symbol) + key
            if index > ord('z') or index < ord('a'):
                index -= (ord('z') - ord('a') + 1) * factor
            res += chr(index)
        elif ord('A') <= ord(symbol) <= ord('Z'):
            index = ord(symbol) + key
            if index > ord('Z') or index < ord('A'):
                index -= (ord('Z') - ord('A') + 1) * factor
            res += chr(index)
        else:
            res += symbol
    return res


def vigenere(key, input_text, func_type):
    res = ''
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
        if ord('a') <= ord(symbol) <= ord('z'):
            index = ord(symbol) + key_value
            if index < ord('a') or index > ord('z'):
                index -= (ord('z') - ord('a') + 1) * factor
            res += chr(index)
        elif ord('A') <= ord(symbol) <= ord('Z'):
            index = ord(symbol) + key_value
            if index < ord('A') or index > ord('Z'):
                index -= (ord('Z') - ord('A') + 1) * factor
            res += chr(index)
        else:
            res += symbol
    return res


def train_function(text, file):
    frequency = Counter([s.lower() for s in text
                         if s in string.ascii_letters])
    length = 0
    for key in frequency:
        length += frequency[key]
    for key in frequency:
        frequency[key] /= length
    for s in string.ascii_lowercase:
        if frequency.get(s) is None:
            frequency[s] = 0
    with open(file, "w") as write_file:
        json.dump(frequency, write_file)


def hack_function(input_text, model_file):
    with open(model_file, "r") as read_file:
        normal_frequency = json.load(read_file)
    text0 = ''.join(s.lower() for s in input_text
                    if s in string.ascii_letters)
    min_deflection = float("inf")
    min_key = 0
    for key in range(26):
        text = caesar(key, text0, 'decode')
        frequency = Counter(text)
        length = len(text)
        for i in frequency:
            frequency[i] /= length
        deflection = 0
        for s in string.ascii_lowercase:
            if frequency.get(s) is None:
                frequency[s] = 0
            deflection += (frequency[s] - normal_frequency[s])**2
        if deflection < min_deflection:
            min_deflection = deflection
            min_key = key
    return caesar(min_key, input_text, 'decode')
