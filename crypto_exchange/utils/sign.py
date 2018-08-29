# -*- coding: utf-8 -*-
import secrets
import string

"""
secrets 包:
    - 只存在 python3.6 中, 
    - 低版本, 可以移植该lib代码, 很简短

"""


def generate_secret_key(length=48):
    """生成64位随机数: (数字+大小写字母+安全符号)

        示例:
            - 2xIh1zpD71ZGiWpHYlG9OcoXtDmaeQinq_lae4z_H7r4etaKkl9Kvc8bKAxtTYqX
            - 6Y3RKdcdpfz9mogLzvSwpzD3eZvV6F1S01hI5Fio9FSYUliT03nrln1ENNg3xj3O

    :param length:
    :return:
    """
    return secrets.token_urlsafe(length)


def generate_secret_key_hex(length=32):
    """生成64位随机数: (16进制数)

        示例:
            - ff110c13b2d34ca68a1bc3d7e560e987cdc9428cf4d37d16a2a27f466883da43
            - a6608e63ae186258e5ca2b1fdec9bf39893dd4f3665082806fe5557004d01533

    :param length:
    :return:
    """
    return secrets.token_hex(length)


def generate_secret_key_v2(length=64):
    """ 生成64位随机数: (数字+字母大小写)

        - string.ascii_letters: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        - string.punctuation:  '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    :param length:
    :return:
    """
    alphabet = string.ascii_letters + string.digits

    key = ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )

    # while True:
    #     key = ''.join(secrets.choice(alphabet) for _ in range(64))
    #
    #     if (any(c.islower() for c in key)
    #         and sum(c.isupper() for c in key) == 3
    #         and sum(c.isdigit() for c in key) > 2):
    #         break

    return key
