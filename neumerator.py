# CREATED: 6/20/15 4:56 PM by Justin Salamon <justin.salamon@nyu.edu>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse, os
import imread


def melodia_neumerator(audio_file):

    command = '../sonic_annotator/sonic-annotator -d vamp:mtg-melodia:melodia:melody ' + audio_file + ' -w csv --csv-force'
    os.system(command)

    csv_file = audio_file.replace(os.path.basename(audio_file), os.path.basename(audio_file)[:-4] + '_vamp_mtg-melodia_melodia_melody.csv')
    neumerator(csv_file)
    os.remove(csv_file)


def make_neume_chart(times, pitches, basename):

    # background_file = 'images/neumy A.bmp'
    # background_file = 'images/neumy text 3.bmp'
    # background_file = 'images/neumy neumy neumy.bmp'
    # background_file = 'images/neumy uni.bmp'
    background_file = 'images/big uni.bmp'
    manuscript = imread.imread(background_file)

    # small version: works
    # my_dpi = 30
    # plt.figure(figsize=(577/my_dpi,216/my_dpi), dpi=my_dpi, frameon=False)
    # plt.imshow(manuscript)
    # note_start = 100
    # note_end = 520
    # pitch_offset = 220
    # pitch_scale = 2.5
    # # plt.plot([note_start, note_start],[100,150],'r')
    # # plt.plot([note_end, note_end],[100,150],'r')

    my_dpi = 72
    plt.figure(figsize=(2401/my_dpi,901/my_dpi), dpi=my_dpi, frameon=False)
    plt.imshow(manuscript)
    note_start = 350
    note_end = 2100
    pitch_offset = 220
    pitch_scale = 8
    plt.plot([note_start, note_start],[100,500],'r')
    plt.plot([note_end, note_end],[100,500],'r')

    pitch_time_range = times[-1] - times[0]
    manuscript_time_range = note_end - note_start

    times_scaled = (times - times[0]) * (manuscript_time_range/pitch_time_range) + note_start

    # E (lowest line is pitch value 26)

    # small works
    # pitches_scaled = 136 - (np.array(pitches)-26) * pitch_scale

    pitches_scaled = 565 - (np.array(pitches)-26) * pitch_scale

    # small works
    # plt.plot(times_scaled, pitches_scaled, 'ks', markersize=12)

    plt.plot(times_scaled, pitches_scaled, 'ks', markersize=24)

    # plt.plot([100, 200],[136,136],'r')
    # plt.plot([100, 200],[127,127],'r')

    # plt.show()

    plt.axis([0,2400,900,0])
    plt.axis('off')
    plt.tight_layout()


    # plt.savefig('images/generated/' + basename.replace('csv','png'), dpi=my_dpi * 10)
    plt.savefig('images/generated/' + basename.replace('csv','png'), dpi=my_dpi)


def pitch_changes(times, cents):
    ts = []
    ps = []
    prevp = None
    for t, p in zip(times, cents):
        if p!=prevp:
            ts.append(t)
            ps.append(p)
            prevp = p
    return ts, ps


def majorityfilt(x, n):
    half_win = n // 2
    y = x.copy()
    for i in range(half_win, len(x)-half_win):
        data = x[i-half_win:i+half_win]
        counts = np.bincount(data)
        y[i] = np.argmax(counts)
    return y


def neumerator(csv_file):

    pitch = pd.read_csv(csv_file, header=None)
    cents_semi = 12*np.log2(pitch[1]/55.)
    cents_semi_round = np.round(cents_semi)

    time_nan = pitch[0][~np.isnan(cents_semi_round)]
    cents_semi_nan = cents_semi_round[~np.isnan(cents_semi_round)]

    cents_semi_maj = majorityfilt(np.array([int(c) for c in cents_semi_nan]), 300)

    # plt.figure(figsize=(18,6))
    # plt.plot(time_nan, cents_semi_maj)
    # plt.axis([0, 25, 20, 40])
    # plt.show()

    ts, ps = pitch_changes(time_nan, cents_semi_maj)

    # plt.figure(figsize=(18,6))
    # plt.plot(ts, ps, 'o')
    # plt.axis([0, 25, 20, 40])
    # plt.show()

    make_neume_chart(ts, ps, os.path.basename(csv_file))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")

    args = parser.parse_args()

    melodia_neumerator(args.csv_file)

    # neumerator(args.csv_file)