import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys, os
import numpy as np
os.chdir(sys.path[0])


if __name__=='__main__':
    dataset = pd.read_csv('C:/Team_Alphaca/0716_miniProject/crawling_data/datasets/24hit_lyrics.csv')

    frequency = {}

    for word in dataset.columns[1:]:
        frequency[word] = sum(dataset[word])

    print(frequency)

    fp = 'C:Windows/Fonts/impact.ttf'
    wc = WordCloud(background_color="white", max_words=100, width=1000, height=800, font_path=fp)
    plt.figure(figsize=(15,15))

    wc = wc.generate_from_frequencies(frequency)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()