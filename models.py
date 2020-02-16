# Ryan McCrory
# NLP Assignment 1

import math


def perp(sum_lines, total):
    exp = sum_lines * (-1 / total)
    perp = math.pow(2, exp)
    return perp


# ------------- smoothing --------------
def smooth(x1, x2, x3, dic1, dic2, dic3, file_name, total):
    sum_lines = 0
    file = open(file_name, 'r', encoding='utf8')
    # iterate through file
    for j, line in enumerate(file, 0):
        # j is position, line is the line, file is file
        x = line.split()
        # add START to beginning
        p1 = ['<START>']
        x = p1 + x
        x.append('<STOP>')
        sum_toks = 0
        for i, tok in enumerate(x, 0):
            # i is position, tok is word, x is line
            if x[i] in dic1:
                this_does_nothing = 4
            else:
                x[i] = '<UNK>'
            if x[i-1] in dic1:
                this_does_nothing = 4
            else:
                x[i-1] = '<UNK>'
            if x[i-2] in dic1:
                this_does_nothing = 4
            else:
                x[i-2] = '<UNK>'
            # unigram -----------------
            if x[i] == '<START>':
                continue
            elif x[i] in dic1:
                prob1 = (dic1[x[i]]) / total
            else:
                prob1 = dic1['<UNK>'] / total
            # bigram -------------------
            if (x[i - 1], x[i]) in dic2:
                prob2 = (dic2[(x[i - 1], x[i])]) / dic1[x[i-1]]
            else:
                prob2 = 0
            # trigram ------------------
            if (x[i - 2], x[i-1], x[i]) in dic3:
                prob3 = (dic3[(x[i - 2], x[i-1], x[i])]) / dic2[(x[i-2], x[i-1])]
            else:
                prob3 = 0
            # multiply by weights (x1, x2, x3)
            prob1 = prob1 * x1
            prob2 = prob2 * x2
            prob3 = prob3 * x3
            sum_prob = prob1 + prob2 + prob3
            log = math.log(sum_prob, 2)
            sum_toks += log
        sum_lines += sum_toks
    perp1 = perp(sum_lines, total)
    file.close()
    print(file_name, 'smoothed perplexity:', perp1)


def find_total(file_name):
    file = open(file_name, 'r', encoding='utf8')
    total = 0
    for lines in file:
        x = lines.split()
        for tok in x:
            total += 1
    file.close()
    return total


# unigram perplexity
def unigram_perp(file_name, total, dic1):
    file = open(file_name, 'r', encoding='utf8')
    # sum of prob of sentence
    sum_lines1 = 0
    for line in file:
        x = line.split()
        x.append('<STOP>')
        # sum of prob of tok
        sum_toks1 = 0
        for tok in x:
            if tok in dic1:
                prob1 = (dic1[tok]) / total
            else:
                prob1 = (dic1['<UNK>']) / total
            log = math.log(prob1, 2)
            sum_toks1 += log
        sum_lines1 += sum_toks1
    perp1 = perp(sum_lines1, total)
    file.close()
    print(file_name, 'unigram perplexity:', perp1)

# Bigram perplexity
def bigram_perp(file_name, total, need_to_remove, dic1, dic2):
    file = open(file_name, 'r', encoding='utf8')
    sum_lines2 = 0
    for j, line in enumerate(file, 0):
        x = line.split()
        # add START to beginning
        p1 = ['<START>']
        x = p1 + x
        x.append('<STOP>')
        sum_toks2 = 0
        for i, tok in enumerate(x, 0):
            if tok in need_to_remove:
                tok = '<UNK>'
            if x[i - 1] in need_to_remove:
                x[i - 1] = '<UNK>'
            if (x[i - 1], tok) in dic2:
                prob2 = (dic2[(x[i - 1], tok)]) / dic1[x[i-1]]
            else:
                prob2 = 0
            if prob2 == 0:
                log = -1000
            else:
                log = math.log(prob2, 2)
            sum_toks2 += log
        sum_lines2 += sum_toks2
    perp2 = perp(sum_lines2, total)
    file.close()
    print(file_name, 'bigram perplexity:', perp2)

# Trigram perplexity
def trigram_perp(file_name, total, need_to_remove, dic2, dic3):
    file = open(file_name, 'r', encoding='utf8')
    sum_lines3 = 0
    for j, line in enumerate(file, 0):
        x = line.split()
        # add START to beginning
        p1 = ['<START>']
        x = p1 + x
        x.append('<STOP>')
        sum_toks3 = 0
        for i, tok in enumerate(x, 0):
            if tok in need_to_remove:
                tok = '<UNK>'
            if x[i - 1] in need_to_remove:
                x[i - 1] = '<UNK>'
            if x[i - 2] in need_to_remove:
                x[i - 2] = '<UNK>'
            if (x[i - 2], x[i-1], tok) in dic3:
                prob3 = (dic3[(x[i - 2], x[i-1], tok)]) / dic2[(x[i-2], x[i-1])]
            else:
                prob3 = 0
            if prob3 == 0:
                log = -1000
            else:
                log = math.log(prob3, 2)
            sum_toks3 += log
        sum_lines3 += sum_toks3
    perp3 = perp(sum_lines3, total)
    file.close()
    print(file_name, 'trigram perplexity:', perp3)

# ---------------------- Add all words in language to dictionary ---------------------------
def fill_dictionaries(file_name):
    # create dictionary's
    dic1 = {}
    dic2 = {}
    dic3 = {}
    # open file
    file = open(file_name, 'r', encoding='utf8')
    # iterate through file and add words to dictionary
    # i = 0
    for line in file:
        # i += 1
        # if i == 30765:
        #     break
        x = line.split()
        x.append('<STOP>')
        for tok in x:
            # unigram below
            # if token exists, increment instance s in dict by 1
            if tok in dic1:
                dic1[tok] += 1
            # if it doesnt exist, set it to 1
            else:
                dic1[tok] = 1
    file.close()
    # edit dictionary to adjust for UNKs
    dic1['<UNK>'] = 0
    need_to_remove = set([])
    keys = dic1.keys()
    for x in keys:
        if dic1[x] == 1:
            dic1['<UNK>'] += 1
            need_to_remove.add(x)
        elif dic1[x] == 2:
            dic1['<UNK>'] += 2
            need_to_remove.add(x)
        # part 2.4, make UNK < 5 occurences
        # elif dic1[x] == 3:
        #     dic1['<UNK>'] += 3
        #     need_to_remove.add(x)
        # elif dic1[x] == 4:
        #     dic1['<UNK>'] += 4
        #     need_to_remove.add(x)
    for x in need_to_remove:
        del dic1[x]
    # determine total number of tokens
    keys = dic1.keys()
    total = 0
    for x in keys:
        total += dic1[x]

    # loop through file again for bi/trigams
    file = open(file_name, 'r', encoding='utf8')
    # iterate through file and add words to dictionary
    # i = 0
    for j, line in enumerate(file, 0):
        # i += 1
        # if i == 30765:
        #     break
        x = line.split()
        # add START to beginning
        p1 = ['<START>']
        x = p1 + x
        x.append('<STOP>')
        for i, tok in enumerate(x, 0):
            if tok in need_to_remove:
                tok = '<UNK>'
            if x[i-1] in need_to_remove:
                x[i-1] = '<UNK>'
            if x[i-2] in need_to_remove:
                x[i-2] = '<UNK>'
            # bigram
            if (x[i - 1], tok) in dic2:
                dic2[x[i - 1], tok] += 1
            else:
                dic2[x[i - 1], tok] = 1
            # trigram
            if (x[i - 2], x[i - 1], tok) in dic3:
                dic3[x[i - 2], x[i - 1], tok] += 1
            else:
                dic3[x[i - 2], x[i - 1], tok] = 1
    file.close()

    # All dictionaries are filled

    unigram_perp('1b_benchmark.train.tokens', total, dic1)
    # # add START to Dictionary, is necessary for bigram and trigram but will not affect unigram
    dic1['<START>'] = dic1['<STOP>']
    bigram_perp('1b_benchmark.train.tokens', total, need_to_remove, dic1, dic2)
    trigram_perp('1b_benchmark.train.tokens', total, need_to_remove, dic2, dic3)
    print()
    del dic1['<START>']

    # find perplexities of the dev set
    total2 = find_total('1b_benchmark.dev.tokens')
    unigram_perp('1b_benchmark.dev.tokens', total2, dic1)
    dic1['<START>'] = dic1['<STOP>']
    bigram_perp('1b_benchmark.dev.tokens', total2, need_to_remove, dic1, dic2)
    trigram_perp('1b_benchmark.dev.tokens', total2, need_to_remove, dic2, dic3)
    print()
    del dic1['<START>']

    # find perplexities of the test set
    total3 = find_total('1b_benchmark.test.tokens')
    unigram_perp('1b_benchmark.test.tokens', total3, dic1)
    dic1['<START>'] = dic1['<STOP>']
    bigram_perp('1b_benchmark.test.tokens', total3, need_to_remove, dic1, dic2)
    trigram_perp('1b_benchmark.test.tokens', total3, need_to_remove, dic2, dic3)
    print()

    print('Smoothing below\n')
    # These are the best hyperparmeters I found while doing a grid search
    x1 = 0.6
    x2 = 0.3
    x3 = 0.1
    smooth(x1, x2, x3, dic1, dic2, dic3, '1b_benchmark.train.tokens', total)
    smooth(x1, x2, x3, dic1, dic2, dic3, '1b_benchmark.dev.tokens', total2)
    smooth(x1, x2, x3, dic1, dic2, dic3, '1b_benchmark.test.tokens', total3)


# ------------- MAIN METHOD --------------
fill_dictionaries('1b_benchmark.train.tokens')
