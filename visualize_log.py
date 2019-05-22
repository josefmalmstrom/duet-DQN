import argparse
import json

import matplotlib.pyplot as plt

name_dict = {"episode_reward": "episode reward",
             "mean_q": "mean Q-value"}


def visualize_log(filename, figsize=None, output=None):
    with open(filename, 'r') as f:
        data = json.load(f)
    if 'episode' not in data:
        raise ValueError('Log file "{}" does not contain the "episode" key.'.format(filename))
    episodes = data['episode']

    # Get value keys. The x axis is shared and is the number of episodes.
    keys = sorted(list(set(data.keys()).difference(set(['episode']))))

    for idx, key in enumerate(keys):
        if key in name_dict.keys():
            plt.figure(figsize=(15.0, 5.0))
            plt.plot(episodes, data[key])
            plt.xlabel('training episodes')
            plt.ylabel(name_dict[key])
            plt.savefig(output + name_dict[key] + ".pdf")


parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='The filename of the JSON log generated during training.')
parser.add_argument('--output', type=str, default=None, help='The output file. If not specified, the log will only be displayed.')
parser.add_argument('--figsize', nargs=2, type=float, default=None, help='The size of the figure in `width height` format specified in points.')
args = parser.parse_args()

# You can use visualize_log to easily view the stats that were recorded during training. Simply
# provide the filename of the `FileLogger` that was used in `FileLogger`.
visualize_log(args.filename, output=args.output, figsize=args.figsize)
