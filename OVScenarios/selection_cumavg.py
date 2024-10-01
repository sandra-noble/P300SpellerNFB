import numpy as np

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.num_flashes = None
        self.selected = None
        self.candidate = None
        self.prob = None
        self.prob_selected = None
        self.nbInputs = 6
        self.count = np.zeros([(self.nbInputs*2)],int) # counts how many times this row/col has flashed
        self.dimensionLabels = list()
        self.dimensionSizes = list()
        self.streamHeader = None
        self.debugging = False # make true to display messages

    def initialize(self):
        self.num_flashes = int(self.setting['Number of flashes'])
        self.selected = np.zeros([self.num_flashes],int)
        self.candidate = np.zeros([self.num_flashes],int)
        self.prob = np.zeros([self.num_flashes])
        self.prob_selected = np.zeros([self.num_flashes])
        
        #creation of the headers
        self.output[0].append(OVStimulationHeader(0.,0.))

        for i in range(self.num_flashes):
            self.dimensionLabels.append(str(i+1)+' Flashes')
        self.dimensionSizes = [self.num_flashes]

        self.streamHeader = OVStreamedMatrixHeader(0.,0.,self.dimensionSizes,self.dimensionLabels)
        self.output[1].append(self.streamHeader)
        return

    # select the row/col with the highest target probability for each number of flashes between 1 and the actual number used
    # returns the selected row/col for the actual number in first output and for all cumulative flashes in second output
    def process(self):
        # loop through the inputs
        for inputIdx in range(self.nbInputs):
            # go through the classification labels and get target candidates
            for chunkIdx in range(len(self.input[inputIdx])):
                chunk = self.input[inputIdx].pop()
                if(type(chunk)==OVStimulationSet):
                    for stimIdx in range(len(chunk)):
                        stim=chunk.pop()
                        self.count[inputIdx] += 1

                        # to index into candidate array, which contains the cumulative candidates for all flashes
                        flashIdx = self.count[inputIdx]-1
                        
                        if (self.debugging):
                            print('Received label', stim.identifier, 'stamped at', stim.date, 's')
                            print('Counter for this row/col:', self.count[inputIdx])

                        # to make sure that flash to show next letter is not included
                        # no need to check for target classification since the candidate with the highest probability to belong to the target class is chosen
                        # that way, even if nothing was labelled as target we chose the row/col that was closest to being labelled as target
                        if(self.count[inputIdx] <= self.num_flashes):
                            if(self.setting['Row']=='true'):
                                self.candidate[flashIdx] = inputIdx+33025 # row stim label
                            else:
                                self.candidate[flashIdx] = inputIdx+33031 # col stim label

                            if(self.debugging):
                                print('Target candidate:', self.candidate[flashIdx], 'for nFlash=', self.count[inputIdx], 'at', inputIdx)                 
            
            # go through the probs and compare prob of candidate to prob of selection
            probIdx = inputIdx+7
            for chunkIdx in range(len(self.input[probIdx])):
                chunk = self.input[probIdx].pop()
                if(type(chunk)==OVStreamedMatrixBuffer):
                    self.count[probIdx-1] += 1

                    # to index into candidate and selected arrays (there is one more input for all stims, so subtract one from probIdx
                    flashIdx = self.count[probIdx-1]-1 

                    # to make sure that flash to show next letter is not included
                    if(self.count[probIdx-1] <= self.num_flashes):
                        self.prob[flashIdx] = chunk.pop(0) # get the first element of the buffer --> target prob

                        if(self.debugging):
                            print('Candidate:', self.candidate[flashIdx])
                            print('Target prob', self.prob[flashIdx])
                            print('Current selected target:', self.selected[flashIdx])
                            print('Current target prob:', self.prob_selected[flashIdx])

                        # if the current candidate has a higher
                        if(self.prob[flashIdx] >= self.prob_selected[flashIdx]):
                            self.selected[flashIdx] = self.candidate[flashIdx]
                            self.prob_selected[flashIdx] = self.prob[flashIdx]

                        if(self.debugging):
                            print('New target selected:', self.selected[flashIdx], 'for n=', self.count[probIdx-1])
                            print('New prob:', self.prob_selected[flashIdx], 'for n=', self.count[probIdx-1])

                    # send the selections to the outputs once we have reached the number of flashes
                    if(all(elem == self.num_flashes for elem in self.count)):
                        # send last target selection to output 0
                        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
                        stimSet.append(OVStimulation(self.selected[self.num_flashes-1], self.getCurrentTime(), 0.))
                        self.output[0].append(stimSet)

                        # send all selections to output 1
                        streamSet = OVStreamedMatrixBuffer(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock(), self.selected)
                        self.output[1].append(streamSet)

                        if(self.debugging):
                            print('Sent target', self.selected[self.num_flashes-1])
                            print('Selected array', self.selected)
                            print('Prob array', self.prob_selected)


        # go through all stimulations to identify segment start and stop
        for chunkIdx in range(len(self.input[6])):
            chunk = self.input[6].pop()
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
                        self.selected = np.zeros([self.num_flashes],int)
                        self.candidate = np.zeros([self.num_flashes],int)
                        self.prob = np.zeros([self.num_flashes])
                        self.prob_selected = np.zeros([self.num_flashes])
                        self.count = np.zeros([(self.nbInputs*2)],int)

        return

    def uninitialize(self):
        end = self.getCurrentTime()
        self.output[0].append(OVStimulationEnd(end, end))
        self.output[1].append(OVStreamedMatrixEnd(end,end))
        return

box = MyOVBox()
