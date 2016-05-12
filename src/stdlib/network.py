#!/usr/bin/python

class Net: 
    def __init__(self, batch_size = 0, time_steps = 1, num_subgroups = 1):
    	self.ensembles = []
        self.ensembles_map = {}

        self.buffers = ({},{})
        self.curr_buffer_set = 1

        #self.forward_tasks = TaskSet()
        #self.backward_tasks= TaskSet()
        #self.update_tasks = []
        #self.signal = np.array(1, dtype = int)

        self.params = []
        self.run_where = -1

        self.batch_size = batch_size

        self.train_epoch = 1
        self.test_epoch = 1

        self.curr_time_step = 0
        self.time_steps = time_steps

        self.num_subgroups = num_subgroups
        #ensemble_send_list
        

