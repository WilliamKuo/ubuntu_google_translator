#!/usr/bin/env python3
import os
import argparse
import traceback
from time import sleep
from pprint import pprint

import googletrans


BOX_LENGTH = 80
BOX_CHAR = '@'
BOX_FRAME = BOX_CHAR * BOX_LENGTH
INNER_BOX_CHAR = '*'
INNER_BOX_FRAME = INNER_BOX_CHAR * BOX_LENGTH


def box_text(text, rule='^', BOX_CHAR=BOX_CHAR):
    # TODO: not truncating too long string
    print('{BOX_CHAR}{0:{rule}{BOX_LENGTH}}{BOX_CHAR}'.format(
        text, rule=rule, BOX_CHAR=BOX_CHAR, BOX_LENGTH=BOX_LENGTH-2))


def terminal_head(**kwarg):
    print(BOX_FRAME)
    box_text('GOOGLE TRANSLATOR TOOL')
    # TODO: more beautiful way?
    box_text('ctrl-c to exit')
    box_text('now translate "{}" to "{}"'.format(
        kwarg['input'], kwarg['output']))
    print(BOX_FRAME)


def terminal_result(mouse_hls_str, translated_str, extra=list()):
    print(INNER_BOX_FRAME)
    box_text('SOURCE TEXT:', BOX_CHAR=INNER_BOX_CHAR)
    print(INNER_BOX_FRAME)
    print('\n{0:^{BOX_LENGTH}}\n'.format(mouse_hls_str, BOX_LENGTH=BOX_LENGTH))
    print(INNER_BOX_FRAME)
    box_text('TRANSE TEXT:', BOX_CHAR=INNER_BOX_CHAR)
    print(INNER_BOX_FRAME)
    print('\n{:^{BOX_LENGTH}}\n'.format(translated_str, BOX_LENGTH=BOX_LENGTH))

    if translated_str != '' and translated_str != 'translated fail':
        print('EXTRA:')
        try:
            if not len(extra['possible-translations'][0][2]):
                raise
            for t in extra['possible-translations'][0][2]:
                print('\t{}'.format(t[0]))
        except Exception:
            print('\tnone')
    print(BOX_FRAME)
    box_text('BOTTOM')
    print(BOX_FRAME)


def main(**kwarg):
    translator = googletrans.Translator()
    cache = '@@init@@magic@@:)'
    while True:
        # get height light text by mouse
        try:
            mouse_hls_str = os.popen('xsel').read()
            if '-\n' in mouse_hls_str:
                mouse_hls_str = mouse_hls_str.replace('-\n', '')
        except Exception:
            mouse_hls_str = ''

        if mouse_hls_str == cache:
            # no new text
            sleep(1)
            continue
        else:
            cache = mouse_hls_str
            os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal
            terminal_head(**kwarg)

        # do translate
        try:
            result = translator.translate(
                mouse_hls_str,
                src=kwarg['input'],
                dest=kwarg['output'])
            translated_str = result.text
        except Exception:
            translated_str = mouse_hls_str

        if mouse_hls_str == '':
            mouse_hls_str = 'no select input data !!!'
            translated_str = ''
        elif mouse_hls_str == translated_str:
            translated_str = 'translated fail'

        # print result
        terminal_result(mouse_hls_str, translated_str, extra=result.extra_data)

        # sleep for ctrl-c
        sleep(1)


if __name__ == '__main__':
    _ap = argparse.ArgumentParser(
        prog='google_translator',
        description='translate selected text in mouse',
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=27
        )
    )

    _ap.add_argument(
        '-i',
        '--input',
        help='input google translator language key (default is auto)')
    _ap.add_argument(
        '-o',
        '--output',
        help='output google translator language key (default is zh-tw)')

    _ap.add_argument(
        '-l',
        '--list',
        action='store_true',
        help='list all google translator language key')
    _args = _ap.parse_args()

    _input = vars(_args)['input']
    _output = vars(_args)['output']
    _list = vars(_args)['list']

    if _list:
        pprint(googletrans.LANGUAGES)
        exit(0)

    kwarg = dict()
    kwarg['input'] = _input if _input else 'auto'
    kwarg['output'] = _output if _output else 'zh-tw'
    try:
        main(**kwarg)
    except Exception as e:
        print('TOOL ERROR:\n{}'.format(e))
        print(traceback.format_exc())

exit(0)
