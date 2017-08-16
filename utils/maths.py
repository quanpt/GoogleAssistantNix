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