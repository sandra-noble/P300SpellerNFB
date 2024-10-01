import numpy as np

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.num_flashes = 0
        self.selected_rows = 0
        self.selected_cols = 0
        self.next_target_row = 0
        self.next_target_col = 0
        self.target_row = 0
        self.target_col = 0

        self.file = None # file to save accuracies to

        self.score = 0
        self.segment_count = 0
        self.accuracy = 0
        self.debugging = False # make true to display messages
        
    def initialize(self):
        self.num_flashes = int(self.setting['Number of flashes'])
        self.selected_rows = np.zeros(self.num_flashes,int)
        self.selected_cols = np.zeros(self.num_flashes,int)

        self.file = open(self.setting['Save to file'],'a') # open file
        self.score = np.zeros(self.num_flashes,int)
        self.accuracy = np.zeros(self.num_flashes,float)
        return

    def process(self):
        # get the selected rows
        for chunkIdx in range(len(self.input[0])):
            chunk = self.input[0].pop()
            if(type(chunk)==OVStreamedMatrixBuffer):
##                for stimIdx in range(len(chunk)):
##                    stim=chunk.pop()
                self.selected_rows = np.array(chunk)
                if(self.debugging):
                    print('Selected rows', self.selected_rows)
        
        # get the selected columns
        for chunkIdx in range(len(self.input[1])):
            chunk = self.input[1].pop()
            if(type(chunk)==OVStreamedMatrixBuffer):
##                for stimIdx in range(len(chunk)):
##                    stim=chunk.pop()
                self.selected_cols = np.array(chunk)
                if(self.debugging):
                    print('Selected columns', self.selected_cols)


        # get the target row and column
        for chunkIdx in range(len(self.input[2])):
            chunk = self.input[2].pop()
            if(type(chunk)==OVStimulationSet):
                if(len(chunk)>0):
                    stim_row = chunk.pop(0)
                    self.next_target_row = stim_row.identifier
                    stim_col = chunk.pop()
                    self.next_target_col = stim_col.identifier

                    if(self.debugging):
                        print('Next target row:', self.next_target_row)
                        print('Next target col:', self.next_target_col)

        # check where we are in experiment
        for chunkIdx in range(len(self.input[3])):
            chunk = self.input[3].pop()
            if(type(chunk)==OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop()
                    if(stim.identifier==32774):
                        if(self.debugging):
                            print('Segment stop')

                        # increment segment (letter) count
                        self.segment_count += 1;
                        
                        if(self.debugging):
                            print('Segment count:', self.segment_count)

                    elif(stim.identifier==32773):
                        if(self.debugging):
                            print('Segment start')

                        # increment score if prediction for previous segment was correct
                        if(self.segment_count >= 1):
                            for n in range(len(self.selected_rows)):
                                if(self.selected_rows[n]==self.target_row) and (self.selected_cols[n]==self.target_col):
                                    self.score[n] += 1;

                        if(self.debugging):
                            print('Scores:', self.score)
                        
                        # next target now becomes the target
                        self.target_row = self.next_target_row
                        self.target_col = self.next_target_col

                        if(self.debugging):
                            print('Current target row:', self.target_row)
                            print('Current target col:', self.target_col)
                        

                    # calculate accuracy at the end of the experiment
                    elif(stim.identifier==32770):
                        # increment score if prediction for previous segment was correct
                        if(self.segment_count >= 1):
                            for n in range(len(self.selected_rows)):
                                if(self.selected_rows[n]==self.target_row) and (self.selected_cols[n]==self.target_col):
                                    self.score[n] += 1;

                        if(self.debugging):
                            print('Scores:', self.score)

                        # calculate accuracy
                        for n in range(len(self.accuracy)):
                            self.accuracy[n] = 100 * (self.score[n]/self.segment_count)

                        # write accuracies to a file - enough to do this only in uninitialize function?
                        #self.file.write(str(self.accuracy)+'\n')
                        
                        if(self.debugging):
                            print('Spelling accuracies:', self.accuracy)

        return

    def uninitialize(self):
        for n in range(len(self.accuracy)):
            self.accuracy[n] = round(100. * (self.score[n]/self.segment_count), 2)
            
        if(self.debugging):
            print('Scores:', self.score)
            print('Segment count:', self.segment_count)

        # write accuracies to a file
        self.file.write(str(self.accuracy)+'\n')
        self.file.close()
        
        print('Spelling accuracies:', self.accuracy)
        return

box = MyOVBox()
