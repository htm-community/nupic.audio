#! /usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
#
# ----------------------------------------------------------------------

# TODO:
"""


"""

# IMPORTS: ###########################
import glob
import os
import sys
import cPickle
import numpy
import utils
import model_params

try:
    import pylab
except ImportError:
    print (
        "pylab isn't available. If you use its functionality, it will crash."
    )
    print "It can be installed with 'pip install -q Pillow'"

from midi.utils import midiread, midiwrite

#############################

# Data-Processing Functions: ###################

###############################################

# Generation Functions: ###############################

###########################################

# Data-Processing Functions: ###################

###############################################


# MAIN ###############################################


if __name__ == '__main__':
    
    print " This will train on the given dataset and generate 20, hopefully enjoyable, sequences..."
    
    # Function Calls: 


############    
    #saving or loading? 

    saving = True #set true if saving is wanted 
    loading = False #set True if immidiatly continiung is wanted 

    # Plotting ? 
    plotting = False

#######

    
    if saving == True:
        model, files, costst = test_rnnrbm()
        print "Saving current learning!" 
        save = model, costst
        cPickle.dump(save,  open( "save_learning_progress2Nott.p", "wb" ) )
        print "Data saved!"
        print "Proceeding with the model's Sample generation..."
        
    elif loading == True: 
        print "Loading the current Model and proceeding to learn..."
        saved = cPickle.load( open( "save_learning_progress.p", "rb" ) )
        modelsaved, coststsaved = saved
        #proceed learning:
        print "Model loaded. Begin learning."
        model, files, costst = test_rnnrbm(modelin = modelsaved, costsold = coststsaved)
        print "Saving current learning status!" 
        save = model, costst
        cPickle.dump(save,  open( "save_learning_progress2Nott.p", "wb" ) )
        print "Data saved!"
        print "Proceeding with the model's Sample generation..."
    
    else: 
        print "Error: Please select either loading or saving to start the model!"


###########  Pianoroll Plotting:  
    if plotting:
        import matplotlib.pyplot as plt 
        plt.plot(costst)
        plt.title('Cost function')
        plt.ylabel('Mean Energy-Cost')
        plt.xlabel('Training iterations')
        plt.show()
    
        model.generate('sample1.mid')
        model.generate('sample2.mid')
        model.generate('sample3.mid')
        model.generate('sample4.mid')
        model.generate('sample5.mid')
        model.generate('sample6.mid')
        model.generate('sample7.mid')
        model.generate('sample8.mid')
        model.generate('sample9.mid')
        model.generate('sample10.mid')
        model.generate('sample11.mid')
        model.generate('sample12.mid')
        model.generate('sample13.mid')
        model.generate('sample14.mid')
        model.generate('sample15.mid')
        model.generate('sample16.mid')
        model.generate('sample17.mid')
        model.generate('sample18.mid')
        model.generate('sample19.mid')
        model.generate('sample20.mid')
        pylab.show()




#########################################
