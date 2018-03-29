import pyphen

dic = pyphen.Pyphen(lang='en_US')


def insert_soft_hyphens(text, hyphen='\xad'):
    """Insert the hyphen in breaking pointsaccording to the dictionary.
    
    '\xad' is the Soft Hyphen (SHY) character
    """
    lines = []
    for line in text.splitlines():
        hyph_words = [
            dic.inserted(word, hyphen) for word in line.split()
        ]
        lines.append(' '.join(hyph_words))
    return '\n'.join(lines)
