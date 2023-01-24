import glob
import numpy as np

def read_spe(filename):
    f = np.genfromtxt(filename, dtype = None, delimiter = '\n', encoding = None)
    for i in range (len(f)):
        if f[i] == '$MEAS_TIM:':
            time_info = f[i+1].split(' ')
            meas_time = int(time_info[0]) # get measurement time
            real_time = int(time_info[1]) # get real time
            dead_time = (1- meas_time/real_time)*100 # calculate dead time in percentage
            # print(meas_time, real_time, dead_time)
        if f[i] == '$DATA:': # start parsing through the spectrum
            data_start_line = i+2 # start index of actual data
        if f[i] == '$ROI:':
            data_end_line = i # end indexo f actual data
    counts = []
    for i in range(data_start_line, data_end_line):
        counts.append(int(f[i]))
    # print(counts[0], counts[-1], len(counts))
    # return measurement time, real time, dead time in percentage, and an array of counts for each channel
    return meas_time, real_time, dead_time, np.array(counts)

def spe2txt(meas_time, real_time, dead_time, counts_array,filename):
    channel_array = np.arange(8192) # your ADC or MCA channel number
    np.savetxt('../txt/'+filename[:-3]+'txt', np.transpose([channel_array, counts_array]), header = 'measure time [s], real time [s], dead time [s]\n {} {} {:.2f}\n channel counts'.format(meas_time, real_time, dead_time), fmt = '%9i')
    return None

def main():
    files = glob.glob('./*.Spe')
    for file in files:
        meas_time, real_time, dead_time, counts = read_spe(str(file)[2:])
        spe2txt(meas_time, real_time, dead_time, counts,str(file)[2:])

if __name__ == "__main__":
    main()
