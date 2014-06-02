
import pandas
import numpy
import matplotlib.pyplot as plt

def run_fun():
    numpy.random.seed(seed = 69)
    dat = pandas.DataFrame(numpy.random.randn(5, 2), 
                           index = [letter for letter in 'abcde'],
                           columns = [0, 1])

    color_a = ["#7F8392", "#B08B47", "#52A479", "#C6778A", "#CF7B5E"]
    color_b = ["#829554", "#A78071", "#AD8AB2", "#679486", "#65A1BC"]

    fig = plt.figure()
    ax = plt.subplot2grid((1,1), (0,0))
    xploded_barchart(ax, dat[0], dat[1], 'd', color_a, color_b)
    
    
def xploded_barchart(ax, series, x_series, x_label, color_a, color_b):
    def draw_rect(x, y, bottom, color, lw, label):
        return ax.bar(x, y, bottom = bottom, color = color, 
            align = 'center', width = 0.5, lw = lw, label = label)

    #create the line width series and "darken" the exploded series
    lw = [0.5 for val in series.index]
    lw[series.index.get_loc(x_label)] = 3.0
    
    #holders for the starting point of other other values
    neg_sum = series[series < 0].sum()
    pos_sum = 0.
    r_dict = {}

    for i, val in enumerate(series):
        if val < 0:
            neg_sum -= val
            r_dict[series.index[i]] = draw_rect(0, val, 
                bottom = neg_sum, color = color_a[i],
                lw = lw[i], label = series.index[i])
        else:
            r_dict[series.index[i]] = draw_rect(0, val, 
                bottom = pos_sum, color = color_a[i], 
                lw = lw[i], label = series.index[i])
            pos_sum += val
        
    #This Rectangle Needs to be redrawn b/c of overlap
    x_ind = series.index.get_loc(x_label)
    draw_rect(0, series[x_label], bottom = r_dict[x_label][0].get_y(), 
              lw = 4.0, color = color_a[x_ind], label = x_label)

    #create the second series
    neg_sum = x_series[x_series < 0].sum()
    yc = neg_sum
    pos_sum = 0.
    rx_dict = {}
    for i, val in enumerate(x_series):
        if val < 0:
            neg_sum -= val
            rx_dict[x_series.index[i]] = draw_rect(1, val, 
                bottom = neg_sum, color = color_b[i],
                lw = 0.5, label = series.index[i])
        else:
            rx_dict[x_series.index[i]] = draw_rect(1, val, 
                bottom = pos_sum, color = color_b[i], 
                lw = 0.5, label = x_series.index[i])
            pos_sum += val
    
    x1 = r_dict[x_label][0].get_x() + 0.501
    x2 = rx_dict[x_series.index[0]][0].get_x() - .01
    ya = r_dict[x_label][0].get_y()
    yb = ya + series[x_label]
    yd = pos_sum

    ax.plot([x1, x2], [ya, yc], color = 'k', ls = '--', lw = 1.0)        
    ax.plot([x1, x2], [yb, yd], color = 'k', ls = '--', lw = 1.0)
    return None

def stacked_barchart(ax, tick, series, colors):
    neg_sum = series[series < 0].sum()
    pos_sum = 0.
    for i, val in enumerate(series):
        if val < 0:
            neg_sum -= val
            ax.bar(tick, val, bottom = neg_sum, color = colors[i],
                   align = 'center', width = 0.5, 
                   lw = .25, label = series.index[i])
        else:
            ax.bar(tick, val, bottom = pos_sum, align = 'center',
                   width = 0.5, color = colors[i], 
                   label = series.index[i], lw = .5)
            pos_sum += val
    return ax

