#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2019, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

# Copy the Free Spoken Digit Dataset wav files and organize into a directory 
# structure required by the Tensorflow training script

import os, shutil, fnmatch

src_dir = "../free-spoken-digit-dataset/recordings"
dst_dir = "./data/"

if __name__ == "__main__":

    if not os.path.isdir(src_dir):
        print("Free spoken digit dataset not found!")
        exit()

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    keywords = ("zero", "one", "two", "three")

    for i, keyword in enumerate(keywords):

        dst = os.path.join(dst_dir, keyword)
        if not os.path.isdir(dst):
            os.makedirs(dst)

        matches = []
        for root, dirnames, filenames in os.walk(src_dir):
            for filename in fnmatch.filter(filenames, "{}_jackson_*.wav".format(i)):
                matches.append(os.path.join(root, filename))

        for match in matches:
            shutil.copy2(match, dst)
