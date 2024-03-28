#!/bin/python

# Copyright (c) 2023 Beijing Institute of Open Source Chip
# csrgen is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#             http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.


def is_str(val):
    """check if value is string"""
    return isinstance(val, str)


def is_int(val):
    """check if value is int"""
    return isinstance(val, int)


def is_first_letter(val):
    """check if string starts from a letter"""
    return ord(val[0].lower()) in range(ord('a'), ord('z') + 1)


def is_non_neg_int(val):
    """check if value is non negative integer"""
    return isinstance(val, int) and val >= 0


def is_pos_int(val):
    """check if value is positive integer"""
    return isinstance(val, int) and val > 0
