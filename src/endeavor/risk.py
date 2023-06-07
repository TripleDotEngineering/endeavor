import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml

from .jinja_tools import env, render

def load_risks(fpath):
    with open(fpath) as f:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def score(p, s, A, B):
    """A and B are the likelihood and consequence multipliers respectively"""
    return A*p + B*s

def risk_matrix(data, fig, cmap, A, B):

    meta = data['RiskAssessment']
    risks = data['Risks']

    # Build the data frame
    df = pd.DataFrame({
        'id': [ risk['id'] for risk in risks ],
        'text': [ risk['text'] for risk in risks ],
        'likelihood': [ risk['likelihood'] for risk in risks ],
        'consequence': [ risk['consequence'] for risk in risks ],
        'score': [ risk['score'] for risk in risks ]
    })

    # scale info
    y_scale = meta['likelihood']
    x_scale = meta['consequence']
    y_lo = y_scale[0]
    y_hi = y_scale[1]
    x_lo = x_scale[0]
    x_hi = x_scale[1]
    yn = [ i for i in range(1, y_hi - y_lo + 2) ]
    xn = [ i for i in range(1, x_hi - x_lo + 2) ]
    # specify bin borders and respective positions
    likelihood_bins = [ i for i in range(y_lo, y_hi+1) ]
    positions = yn
    for position, likelihood in zip(positions, likelihood_bins):
        df.loc[df['likelihood']>=likelihood, 'y'] = position

    # generate x-positions from severity column
    df['x'] = df['consequence'] #.replace({'High':2, 'Medium':1, 'Low':0})

    # default offset for x -position
    x_offset = -0.4

    # generate risk matrix and display as image
    matrix = np.zeros((xn[-1]+1, yn[-1]+1))
    for i in range(0, len(xn)+1):
        for j in range(0, len(yn)+1):
            matrix[i][j] = score(i+1, j+1, A, B)
    #print(matrix)

    plt.imshow(matrix, cmap=cmap)

    # write individual components on it
    # as some components will end up in hte same bin,
    # caculate y-offset on the fly
    for group in df.groupby(['x', 'y']):
        y_offset = -0.1
        for ix, row in group[1].iterrows():

            plt.annotate(
                row['id'],
                xy=(
                    row['x']+x_offset,
                    row['y']+y_offset
                    )
                )
            y_offset +=.15 # update y_offset

    plt.xlabel('Consequence')
    plt.ylabel('Likelihood')
    plt.xlim([x_lo - 0.5, x_hi + 0.5])
    plt.ylim([y_lo - 0.5, y_hi + 0.5])
    plt.xticks(xn)
    plt.yticks(yn)
    #plt.show()
    plt.savefig(fig)


def risk_writeup(data, out):
    risks = data['Risks']
    print(risks)
    result = render('risks.jinja.md', risks=risks)
    with open(out, 'w') as f:
        f.write(result)

def compute_scores(risks, a, b):
    """a and b are the likelihood and consequence multipliers respectively"""
    for risk in risks:
        risk['score'] = score(risk['likelihood'], risk['consequence'], a, b)

def validate_risk_data(data):
    risks = data['Risks']
    ids = [ r['id'] for r in risks ]
    if len(ids) != len(set(ids)):
        raise Exception("Duplicate IDs found in risk data.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='The risk data YAML file')
    parser.add_argument('--outfile-png', default="risks.png", help='The risk matrix output path')
    parser.add_argument('--outfile-md', default="risks.md", help='The risk write up output path')
    parser.add_argument('--cmap', default='RdYlGn_r', help="Any valid matplotlib cmap should work")
    parser.add_argument('--l-multiplier', type=float, default=1.0, help="The likelihood multiplier used in scoring")
    parser.add_argument('--c-multiplier', type=float, default=1.2, help="The consequence multiplier used in scoring")
    args = parser.parse_args()
    data = load_risks(args.input)
    validate_risk_data(data)
    compute_scores(data['Risks'], args.l_multiplier, args.c_multiplier)
    risk_matrix(data, args.outfile_png, args.cmap, args.l_multiplier, args.c_multiplier)
    risk_writeup(data, args.outfile_md)


if __name__ == '__main__':
    main()
