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

from typing import Dict, List
import utils


class BitField(object):
    def __init__(self, name='', desc='', reset=0, width=1, lsb=0, access='rw'):
        self.name = name
        self.desc = desc
        self.reset = reset
        self.width = width
        self.lsb = lsb
        self.access = access
        self.enum = []

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            raise TypeError(
                f'Failed to compare {repr(self)} with {repr(other)}!')
        else:
            return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        if self.__class__ != other.__class__:
            raise TypeError(
                f'Failed to compare {repr(self)} with {repr(other)}!')
        else:
            return not self.__eq__(other)

    def __repr__(self):
        return f'BitField({repr(self.name)})'

    def __str__(self):
        return self.as_str()

    def __len__(self):
        """calculate number of enum inside bitfield"""
        return len(self.enum)

    def __iter__(self):
        """create iterator over enum"""
        return iter(self.enum)

    def __getitem__(self, key):
        """get enum by name or index"""
        try:
            if utils.is_str(key):
                return next(enum for enum in self if enum.name == key)
            else:
                return self.enum[key]
        except Exception as error:
            info = f"there is no enum with the name/index '{key}'"
            info += f" in the '{self.name}' bitfield!"
            raise KeyError(info) from error

    def __setitem__(self, key, value):
        """set enum by key"""
        info = f"Not able to set '{key}' enum directly in the '{self.name}!"
        info += " Try to use addenum() method."
        raise KeyError(info)

    def as_str(self, idt=''):
        """create an indented string with the bit field information"""
        indent = idt + '  '
        bf_str = f'{indent}{self.name}: {self.desc}\n'
        bf_str += f'{indent}reset = {str(self.reset)}\n'
        bf_str += f'{indent}wdith = {str(self.width)}\n'
        bf_str += f'{indent}lsb = {str(self.lsb)}\n'
        bf_str += f'{indent}access = {str(self.access)}\n'
        bf_str += f'{indent}enum:\n'
        enum = [enum.as_str(indent + indent) for enum in self.enum]
        bf_str += '\n'.join(enum) if enum else indent + 'empty'
        return bf_str

    def as_dict(self):
        """create a dictionary with the key attributes of the bit field"""
        d = {
            'name': self.name,
            'desc': self.desc,
            'reset': self.reset,
            'width': self.width,
            'lsb': self.lsb,
            'access': self.access,
            'enum': [enum.as_dict() for enum in self.enum]
        }

        return d

    @property
    def name(self) -> str:
        """name of the bit field"""
        return self._name

    @name.setter
    def name(self, value: str):
        if not utils.is_str(value):
            res = "'name' attribute has to be 'str', "
            res += f"but '{type(value)}' provided for the bitfield!"
            raise ValueError(res)
        self._name = value

    @property
    def desc(self) -> str:
        """desc of the bit field"""
        return self._desc

    @desc.setter
    def desc(self, value: str):
        if not utils.is_str(value):
            res = "'desc' attribute has to be 'str', "
            res += f"but '{type(value)}' provided for the bitfield!"
            raise ValueError(res)
        self._desc = value

    @property
    def reset(self) -> int:
        """reset of the bit field"""
        return self._reset

    @reset.setter
    def reset(self, value: int):
        if not utils.is_int(value):
            res = "'reset' attribute has to be 'int', "
            res += f"but '{type(value)}' provided for the bitfield!"
            raise ValueError(res)
        self._reset = value

    @property
    def width(self) -> int:
        """width of the bit field"""
        return self._width

    @width.setter
    def width(self, value: int):
        if not utils.is_int(value):
            res = "'width' attribute has to be 'int', "
            res += f"but '{type(value)}' provided for the bitfield!"
            raise ValueError(res)
        self._width = value

    @property
    def lsb(self) -> int:
        """lsb of the bit field"""
        return self._lsb

    @lsb.setter
    def lsb(self, value: int):
        if not utils.is_int(value):
            res = "'lsb' attribute has to be 'int', "
            res += f"but '{type(value)}' provided for the bitfield!"
            raise ValueError(res)
        self._lsb = value

    @property
    def msb(self) -> int:
        """position of most significant bit (MSB) of the field"""
        return self.lsb + self.width - 1

    @property
    def byte_strobes(self) -> Dict[int, Dict[str, int]]:
        """dictionary for the every byte in the write data bus"""
        strb = {}
        first = self.lsb // 8
        last = self.msb // 8
        for i in range(first, last + 1):
            # per every byte strobe
            wdata_lsb = self.lsb if i == first else i * 8
            wdata_msb = (i + 1) * 8 - 1 if (
                (i + 1) * 8 - 1 - self.msb) < 0 else self.msb
            bf_lsb = wdata_lsb - self.lsb
            bf_msb = wdata_msb - self.lsb
            strb[i] = {
                'bf_lsb': bf_lsb,
                'bf_msb': bf_msb,
                'wdata_lsb': wdata_lsb,
                'wdata_msb': wdata_msb
            }
        return strb

    @property
    def access(self) -> str:
        """access of the bit field"""
        return self._access

    @access.setter
    def access(self, value: str):
        if not utils.is_str(value):
            res = "'access' attribute has to be 'str', "
            res += f"but '{type(value)}' provided for the bitfield!"
            raise ValueError(res)
        self._access = value

    @property
    def enum_names(self):
        """list with all enum names."""
        return [enum.name for enum in self]

    @property
    def bits(self) -> List[int]:
        """all positions of the bits represented by the bit field"""
        return list(range(self.lsb, self.msb + 1))

    @property
    def mask(self) -> int:
        """bit mask for the field"""
        return (2**(self.width) - 1) << self.lsb

    def is_vector(self) -> bool:
        """check if the width of the bit field > 1"""
        return True if self.width > 1 else False

    def validate(self):
        """validate parameters of the bit field"""
        # name
        info = "Empty bitfield name is not allowed!"
        assert self.name, info

        info = f"Name value '{self.name}' for is wrong!"
        info += " Must start from a letter."
        assert utils.is_first_letter(self.name), info

        # reset
        info = f"Reset value '{self.reset}' for '{self.name}' is wrong!"
        info += "Only non-negative integers are allowed."
        assert utils.is_non_neg_int(self.reset), info

        # width
        info = "Empty bitfield width is not allowed!"
        assert self.width, info

        info = f"Width value '{self.width}' for '{self.name}' is wrong!"
        info += "Only positive integers are allowed."
        assert utils.is_pos_int(self.width), info

        # lsb
        info = f"LSB value '{self.lsb}' for '{self.name}' is wrong!"
        info += "Only non-negative integers are allowed."
        assert utils.is_non_neg_int(self.lsb), info

        # access
        info = f"Unknown access mode '{self.access}' for '{self.name}' field!"
        assert self.access in [
            'rw', 'rw1c', 'rw1s', 'rw1t', 'ro', 'roc', 'roll', 'rolh', 'wo',
            'wosc'
        ], info
