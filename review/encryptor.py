from definition import decode_caesar, decode_vigenere, hack_function
from definition import encode_vigenere, encode_caesar, train_function
import argparse
import sys

parser = argparse.ArgumentParser()

subs = parser.add_subparsers()
encode_parser = subs.add_parser('encode')
decode_parser = subs.add_parser('decode')
train_parser = subs.add_parser('train')
hack_parser = subs.add_parser('hack')

encode_parser.set_defaults(method='encode')
decode_parser.set_defaults(method='decode')
train_parser.set_defaults(method='train')
hack_parser.set_defaults(method='hack')

encode_parser.add_argument('--cipher', required=True,
                           choices=('caesar', 'vigenere'))

encode_parser.add_argument('--key', required=True)
encode_parser.add_argument('--input-file', type=argparse.FileType('r'),
                           default=sys.stdin)
encode_parser.add_argument('--output-file', type=argparse.FileType('w'),
                           default=sys.stdout)
decode_parser.add_argument('--cipher', required=True,
                           choices=('caesar', 'vigenere'))
decode_parser.add_argument('--key', required=True)
decode_parser.add_argument('--input-file', type=argparse.FileType('r'),
                           default=sys.stdin)
decode_parser.add_argument('--output-file', type=argparse.FileType('w'),
                           default=sys.stdout)
train_parser.add_argument('--text-file', type=argparse.FileType('r'),
                          default=sys.stdin)
train_parser.add_argument('--model-file', required=True)
hack_parser.add_argument('--input-file', type=argparse.FileType('r'),
                         default=sys.stdin)
hack_parser.add_argument('--output-file', type=argparse.FileType('w'),
                         default=sys.stdout)
hack_parser.add_argument('--model-file', required=True)


args = parser.parse_args()
if args.method == 'encode':
    text = args.input_file.read()
    if args.cipher == 'caesar':
        args.output_file.write(encode_caesar(int(args.key), text))
    else:
        args.output_file.write(encode_vigenere(args.key, text))
elif args.method == 'decode':
    text = args.input_file.read()
    if args.cipher == 'caesar':
        args.output_file.write(decode_caesar(int(args.key), text))
    else:
        args.output_file.write(decode_vigenere(args.key, text))
elif args.method == 'train':
    text = args.text_file.read()
    train_function(text, args.model_file)
elif args.method == 'hack':
    text = args.input_file.read()
    args.output_file.write(hack_function(text, args.model_file))
