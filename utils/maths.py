# Copyright (C) 2017 Tran Quan Pham
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


# Code taken from https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers

def text2int(text_num, num_words={}):
    if not num_words:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        num_words["and"] = (1, 0)
        for idx, word in enumerate(units):    num_words[word] = (1, idx)
        for idx, word in enumerate(tens):     num_words[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   num_words[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in text_num.split():
        if word not in num_words:
            raise Exception("Illegal word: " + word)

        scale, increment = num_words[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
