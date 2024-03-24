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

import utils


class BitField(object):
    def __init__(self,
                 name='',
                 desc='',
                 default=0,
                 width=1,
                 lsb=0,
                 access='rw'):
        self.enum = []
        self.name = name
        self.desc = desc
        self.default = default
        self.width = width
        self.lsb = lsb
        self.access = access

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
        """Calculate number of enum inside bitfield"""
        return len(self.enum)

    def __iter__(self):
        """Create iterator over enum"""
        return iter(self.enum)

    def __getitem__(self, key):
        """Get enum by name or index."""
        try:
            if utils.is_str(key):
                return next(enum for enum in self if enum.name == key)
            else:
                return self.enum[key]
        except Exception as error:
            info = f"There is no enum with the name/index '{key}'"
            info += f" in the '{self.name}' bitfield!"
            raise KeyError(info) from error

    def __setitem__(self, key, value):
        """Set enum by key"""
        info = f"Not able to set '{key}' enum directly in the '{self.name}!"
        info += " Try to use addenum() method."
        raise KeyError(info)

    def as_str(self, idt=''):
        """Create an indented string with the bit field information."""
        indent = idt + '  '
        bf_str = f'{indent}{self.name}: {self.desc}\n'
        bf_str += f'{indent}default = {str(self.default)}\n'
        bf_str += f'{indent}wdith = {str(self.width)}\n'
        bf_str += f'{indent}lsb = {str(self.lsb)}\n'
        bf_str += f'{indent}access = {str(self.access)}\n'
        bf_str += f'{indent}enum:\n'
        enum = [enum.as_str(indent + indent) for enum in self.enum]
        bf_str += '\n'.join(enum) if enum else indent + 'empty'
        return bf_str

    def as_dict(self):
        """Create a dictionary with the key attributes of the bit field."""
        d = {
            'name': self.name,
            'desc': self.desc,
            'default': self.default,
            'width': self.width,
            'lsb': self.lsb,
            'access': self.access,
            'enum': [enum.as_dict() for enum in self.enum]
        }

        return d
