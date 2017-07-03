from __future__ import print_function

import os, math
import torch
from tree import Tree
from vocab import Vocab

# loading GLOVE word vectors
# if .pth file is found, will load that
# else will load from .txt file & save
def load_word_vectors(path):
    if os.path.isfile(path+'.pth') and os.path.isfile(path+'.vocab'):
        print('==> File found, loading to memory')
        vectors = torch.load(path+'.pth')
        vocab = Vocab(filename=path+'.vocab')
        return vocab, vectors
    # saved file not found, read from txt file
    # and create tensors for word vectors
    print('==> File not found, preparing, be patient')
    count = sum(1 for line in open(path+'.txt'))
    with open(path+'.txt','r') as f:
        contents = f.readline().rstrip('\n').split(' ')
        dim = len(contents[1:])
    words = [None]*(count)
    vectors = torch.zeros(count,dim)
    with open(path+'.txt','r') as f:
        idx = 0
        for line in f:
            contents = line.rstrip('\n').split(' ')
            words[idx] = contents[0]
            vectors[idx] = torch.Tensor(map(float, contents[1:]))
            idx += 1
    with open(path+'.vocab','w') as f:
        for word in words:
            f.write(word+'\n')
    vocab = Vocab(filename=path+'.vocab')
    torch.save(vectors, path+'.pth')
    return vocab, vectors


# write unique words from a set of files to a new file
def build_vocab(filenames, vocabfile):
    vocab = set()
    for filename in filenames:
        with open(filename,'r', encoding='utf-8') as f:
            for line in f:
                tokens = line.rstrip('\n').split(' ')
                vocab |= set(tokens)
    with open(vocabfile,'w', encoding='utf-8') as f:
        for token in vocab:
            f.write(token+'\n')


def map_label_to_target_sentiment(label, num_classes = 3):
    # num_classes not use yet
    target = torch.LongTensor(1)
    target[0] = int(label) # nothing to do here as we preprocess data
    return target


def count_param(model):
    print('_param count_')
    params = list(model.parameters())
    sum_param = 0
    for p in params:
        sum_param+= p.numel()
        print (p.size())
    # emb_sum = params[0].numel()
    # sum_param-= emb_sum
    print ('sum', sum_param)
    print('____________')