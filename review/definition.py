import string
from collections import Counter
import json


def encode_caesar(key, input_text):
    res = ''
    for symbol in input_text:
        if ord('a') <= ord(symbol) <= ord('z'):
            index = ord(symbol) + key
            if index > ord('z'):
                index -= ord('z') - ord('a') + 1
            res += chr(index)
        elif ord('A') <= ord(symbol) <= ord('Z'):
            index = ord(symbol) + key
            if index > ord('Z'):
                index -= ord('Z') - ord('A') + 1
            res += chr(index)
        else:
            res += symbol
    return res


def encode_vigenere(key, input_text):
    res = ''
    length = len(input_text)
    key = key.lower()
    for i in range(length):
        symbol = input_text[i]
        key_value = ord(key[i % len(key)]) - ord('a')
        if ord('a') <= ord(symbol) <= ord('z'):
            index = ord(symbol) + key_value
            if index > ord('z'):
                index -= ord('z') - ord('a') + 1
            res += chr(index)
        elif ord('A') <= ord(symbol) <= ord('Z'):
            index = ord(symbol) + key_value
            if index > ord('Z'):
                index -= ord('Z') - ord('A') + 1
            res += chr(index)
        else:
            res += symbol
    return res


def decode_caesar(key, input_text):
    res = ''
    for symbol in input_text:
        if ord('a') <= ord(symbol) <= ord('z'):
            index = ord(symbol) - key
            if index < ord('a'):
                index += ord('z') - ord('a') + 1
            res += chr(index)
        elif ord('A') <= ord(symbol) <= ord('Z'):
            index = ord(symbol) - key
            if index < ord('A'):
                index += ord('Z') - ord('A') + 1
            res += chr(index)
        else:
            res += symbol
    return res


def decode_vigenere(key, input_text):
    res = ''
    length = len(input_text)
    key = key.lower()
    for i in range(length):
        symbol = input_text[i]
        key_value = ord(key[i % len(key)]) - ord('a')
        if ord('a') <= ord(symbol) <= ord('z'):
            index = ord(symbol) - key_value
            if index < ord('a'):
                index += ord('z') - ord('a') + 1
            res += chr(index)
        elif ord('A') <= ord(symbol) <= ord('Z'):
            index = ord(symbol) - key_value
            if index < ord('A'):
                index += ord('Z') - ord('A') + 1
            res += chr(index)
        else:
            res += symbol
    return res


def train_function(text, file):
    text = text.lower()
    text = ''.join(s for s in text if s in string.ascii_lowercase)
    frequency = dict(Counter(text))
    length = len(text)
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
    text0 = input_text.lower()
    text0 = ''.join(s for s in text0 if s in string.ascii_lowercase)
    min_deflection = -1
    min_key = 0
    for key in range(26):
        text = decode_caesar(key, text0)
        frequency = dict(Counter(text))
        length = len(text)
        for i in frequency:
            frequency[i] /= length
        deflection = 0
        for s in string.ascii_lowercase:
            if frequency.get(s) is None:
                frequency[s] = 0
            deflection += (frequency[s] - normal_frequency[s])**2
        if min_deflection == -1 or deflection < min_deflection:
            min_deflection = deflection
            min_key = key
    return decode_caesar(min_key, input_text)
