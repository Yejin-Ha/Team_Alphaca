# import pandas as pd
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS
# import sys, os
# import numpy as np
# os.chdir(sys.path[0])




if __name__=='__main__':
    dataset = pd.read_csv('C:/Team_Alphaca/0716_miniProject/crawling_data/datasets/24hit_lyrics.csv')

    frequency = {}

    for word in dataset.columns[1:]:
        frequency[word] = sum(dataset[word])

    black_mage_mask = 