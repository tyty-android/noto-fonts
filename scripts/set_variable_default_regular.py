#!/usr/bin/python
# coding=UTF-8
#
# Copyright 2025 Yuan Tong. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Set the default instance of variable font to Regular."""

import sys

from fontTools import ttLib
from fontTools.varLib import instancer


def process_ttf(font, extra_axis):
    for name in font['name'].names:
        extra_light = 'ExtraLight'.encode('utf-16be')
        regular = 'Regular'.encode('utf-16be')
        targets = [
            2,   # fontSubfamily
            3,   # uniqueID
            6,   # postScriptName
            17,  # preferredSubfamily
        ]
        if name.nameID in targets:
            name.string = name.string.replace(extra_light, regular)

    axes_map = {axis.axisTag: idx for idx, axis in enumerate(font['fvar'].axes)}
    all_axis = {'wght': 400.0, **extra_axis}
    axisLimits = {}
    for axis, value in all_axis.items():
        fvar = font['fvar'].axes[axes_map[axis]]
        axisLimits[axis] = (fvar.minValue, value, fvar.maxValue)
    instancer.instantiateVariableFont(font, axisLimits, inplace=True, optimize=True)


def main(argv):
    """Set the default instance of variable font to Regular."""

    source_file_name = argv[1]
    target_file_name = argv[2]
    pairs = (entry.split('=') for entry in argv[3:])
    extra_axis = {axis: float(value) for axis, value in pairs}

    if source_file_name.endswith('.ttc') or source_file_name.endswith('.otc'):
        ttc = ttLib.ttCollection.TTCollection(source_file_name)
        for font in ttc:
            print("Processing", font)
            process_ttf(font, extra_axis)
        ttc.save(target_file_name)
    else:
        font = ttLib.TTFont(source_file_name)
        process_ttf(font, extra_axis)
        font.save(target_file_name)

if __name__ == '__main__':
    main(sys.argv)
