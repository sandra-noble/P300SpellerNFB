import numpy as np

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.in_segment = False
        self.counter = 0
        self.numFlash = 0
        self.nComp = 0 # number of channels
        self.nSamples = 75 # number of samples per buffer (75 for eego and 76 for generic oscillator)
        self.cumsum = np.zeros([self.nComp*self.nSamples])
        self.cumavg = np.zeros([self.nComp*self.nSamples])
        self.dimensionLabels = list()
        self.dimensionSizes = list()
        self.streamHeader = None
        self.debugging = False # make true to display messages

    def initialize(self):
        self.numFlash = int(self.setting['Number of flashes'])
        self.nComp = int(self.setting['Number of channels'])
        #creation of the signal header
        for i in range(self.nComp):
            self.dimensionLabels.append( 'Component'+str(i) )
        self.dimensionLabels += self.nSamples*['']
        self.dimensionSizes = [self.nComp,self.nSamples]

        self.streamHeader = OVStreamedMatrixHeader(0.,0.,self.dimensionSizes,self.dimensionLabels)
        self.output[0].append(self.streamHeader)
        return

    def process(self):
        # go through the input signal
        for chunkIdx in range(len(self.input[0])):
            chunk = self.input[0].pop()

            if(type(chunk)==OVSignalBuffer):
                self.counter += 1

                if(self.debugging):
                    print(len(chunk))
                    print('Old sum', self.cumsum[1:5])

                # only add the current epoch if it is not greater than the number of flashes to avoid counting the display of the next target letter
                if(self.counter <= self.numFlash):
                    # add current epoch to the cumulative sum for each component
                    self.cumsum += np.array(chunk)

                    # divide the cumsum by the counter to get the cumulative average
                    self.cumavg = np.divide(self.cumsum,self.counter)

                    # send the cumulative average
                    streamSet = OVStreamedMatrixBuffer(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock(), self.cumavg.tolist())
                    self.output[0].append(streamSet)

                # can check that all cumulative averages are sent --> self.counter should go up to the number of flashes and label is the row or column label
                if(self.debugging):
                    print('Sent avg chunk', self.counter, 'label', self.setting['Label'])
                    print('New chunk', np.array(chunk)[1:5])
                    print('New sum', self.cumsum[1:5])
                    print('Avg', self.cumavg[1:5])

        # go through all stimulations to identify segment start and stop
        for chunkIdx in range(len(self.input[1])):
            chunk = self.input[1].pop()
            if(type(chunk)==OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop()
                    if(stim.identifier==32774):
                        if(self.debugging):
                            print('Segment stop')
                        
                    elif(stim.identifier==32773):
                        if(self.debugging):
                            print('Segment start, reset variables')

                        # reset variables
                        self.counter = 0
                        self.cumsum = np.zeros([self.nComp*self.nSamples])
                        self.cumavg = np.zeros([self.nComp*self.nSamples])
        return

    def uninitialize(self):
        end = self.getCurrentTime()
        self.output[0].append(OVStreamedMatrixEnd(end, end))
        return

box = MyOVBox()
