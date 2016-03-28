"""A wallycore version of https://github.com/trezor/python-mnemonic"""
import wallycore
from ctypes import create_string_buffer
from os import urandom

BIP39_ENTROPY_LEN_128 = wallycore.BIP39_ENTROPY_LEN_128
BIP39_ENTROPY_LEN_160 = wallycore.BIP39_ENTROPY_LEN_160
BIP39_ENTROPY_LEN_192 = wallycore.BIP39_ENTROPY_LEN_192
BIP39_ENTROPY_LEN_224 = wallycore.BIP39_ENTROPY_LEN_224
BIP39_ENTROPY_LEN_256 = wallycore.BIP39_ENTROPY_LEN_256

class Mnemonic(object):

    def __init__(self, language):
        self.wordlist = wallycore.bip39_get_wordlist(language)


    def list_languages(self):
        return wallycore.bip39_get_languages().split()


    def generate(self, strength = wallycore.BIP39_ENTROPY_LEN_128):
        if strength not in [BIP39_ENTROPY_LEN_128, BIP39_ENTROPY_LEN_160,
                            BIP39_ENTROPY_LEN_192, BIP39_ENTROPY_LEN_224,
                            BIP39_ENTROPY_LEN_256]:
            raise ValueError('Invalid strength %d.' % strength)

        buf = create_string_buffer(urandom(strength), strength)
        return wallycore.bip39_mnemonic_from_bytes(self.wordlist, buf)


    def to_entropy(self, words):
        if isinstance(words, list):
            words = ' '.join(words)
        buf = create_string_buffer(BIP39_ENTROPY_LEN_256)
        length = wallycore.bip39_mnemonic_to_bytes(self.wordlist, words, buf)
        if length <= 0:
            raise ValueError('Invalid word list. %s' % words)
        return bytearray(buf)[0:length]


    def to_mnemonic(self, data):
        return wallycore.bip39_mnemonic_from_bytes(self.wordlist, data)


    def check(self, mnemonic):
        return wallycore.bip39_mnemonic_is_valid(self.wordlist, mnemonic)


    def to_seed(self, mnemonic, passphrase = ''):
        buf = create_string_buffer(wallycore.BIP39_SEED_LEN_512)
        if wallycore.bip39_mnemonic_to_seed(mnemonic, passphrase, buf) == 0:
            raise ValueError('Unable to create seed')
        return bytearray(buf)[0:wallycore.BIP39_SEED_LEN_512]