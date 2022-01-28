import numpy as np

Data = np.genfromtxt("results/results.txt", dtype=float,
                    encoding=None, delimiter=",")

(unique, counts) = np.unique(Data, return_counts=True)
frequencies = np.asarray((unique, counts)).T
# Sort 2D numpy array by 2nd Column
sorted_freqs = frequencies[frequencies[:,1].argsort()]
sorted_freqs = sorted_freqs.astype(int)
most_probable_bpm = sorted_freqs[frequencies.shape[0] - 1][0]
second_probable_bpm = sorted_freqs[frequencies.shape[0] - 2][0]
estimation = (most_probable_bpm + second_probable_bpm) / 2
print(Data)
print("--FREQUENCIES--")
print(frequencies)
print('--SORTED--')
print(sorted_freqs)
sorted_freqs[sorted_freqs[:,0] == 72 ] -= 100
print('meoww' + str( sorted_freqs[sorted_freqs[:,0] == 42 ]))
print('meoww ' + str( sorted_freqs[sorted_freqs[:,0] == 48]))
print('max ' + str(most_probable_bpm))
print('second max ' + str(second_probable_bpm))
print('estimation: ' + str(estimation))
den = 0
nom = 0
for i in range(sorted_freqs.shape[0]):
    den += sorted_freqs[i][0]
    nom += sorted_freqs[i][1] * sorted_freqs[i][0]
print(nom/den)