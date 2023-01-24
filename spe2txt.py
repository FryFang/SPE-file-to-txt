import glob
import numpy as np

def read_spe(filename):
    f = np.genfromtxt(filename, dtype = None, delimiter = '\n', encoding = None)
    for i in range (len(f)):
        if f[i] == '$MEAS_TIM:':
            time_info = f[i+1].split(' ')
            meas_time = int(time_info[0])
            real_time = int(time_info[1])
            dead_time = (1- meas_time/real_time)*100
            # print(meas_time, real_time, dead_time)
        if f[i] == '$DATA:':
            data_start_line = i+2
        if f[i] == '$ROI:':
            data_end_line = i
    counts = []
    for i in range(data_start_line, data_end_line):
        counts.append(int(f[i]))
    # print(counts[0], counts[-1], len(counts))
    return meas_time, real_time, dead_time, np.array(counts)

def spe2txt(meas_time, real_time, dead_time, counts_array,filename):
    channel_array = np.arange(8192)
    np.savetxt('../txt/'+filename[:-3]+'txt', np.transpose([channel_array, counts_array]), header = 'measure time [s], real time [s], dead time [s]\n {} {} {:.2f}\n channel counts'.format(meas_time, real_time, dead_time), fmt = '%9i')
    return None

def main():
    files = glob.glob('./*.Spe')
    for file in files:
        meas_time, real_time, dead_time, counts = read_spe(str(file)[2:])
        spe2txt(meas_time, real_time, dead_time, counts,str(file)[2:])

if __name__ == "__main__":
    main()