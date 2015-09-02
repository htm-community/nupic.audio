# Adopted from RNN-RBM deep learning tutorial
# More information at http://deeplearning.net/tutorial/rnnrbm.html

import glob
import os
import sys
import cPickle
import numpy
try:
    import pylab
except ImportError:
    print (
        "pylab isn't available. If you use its functionality, it will crash."
    )
    print "It can be installed with 'pip install -q Pillow'"

from midi.utils import midiread, midiwrite
import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams

# Don't use a python long as this don't work on 32 bits computers.
numpy.random.seed(0xbeef)
rng = RandomStreams(seed=numpy.random.randint(1 << 30))
theano.config.warn.subtensor_merge_bug = False

# Change this to train and test on another dataset
FILEPATH = '/data/Nottingham'


def build_rbm(v, W, bv, bh, k):
    '''Construct a k-step Gibbs chain starting at v for an RBM.

    v : Theano vector or matrix
        If a matrix, multiple chains will be run in parallel (batch).
    W : Theano matrix
        Weight matrix of the RBM.
    bv : Theano vector
        Visible bias vector of the RBM.
    bh : Theano vector
        Hidden bias vector of the RBM.
    k : scalar or Theano scalar
        Length of the Gibbs chain.

    Return a (v_sample, cost, monitor, updates) tuple:

    v_sample : Theano vector or matrix with the same shape as `v`
        Corresponds to the generated sample(s).
    cost : Theano scalar
        Expression whose gradient with respect to W, bv, bh is the CD-k
        approximation to the log-likelihood of `v` (training example) under the
        RBM. The cost is averaged in the batch case.
    monitor: Theano scalar
        Pseudo log-likelihood (also averaged in the batch case).
    updates: dictionary of Theano variable -> Theano variable
        The `updates` object returned by scan.'''

    def gibbs_step(v):
        mean_h = T.nnet.sigmoid(T.dot(v, W) + bh)
        h = rng.binomial(size=mean_h.shape, n=1, p=mean_h,
                         dtype=theano.config.floatX)
        mean_v = T.nnet.sigmoid(T.dot(h, W.T) + bv)
        v = rng.binomial(size=mean_v.shape, n=1, p=mean_v,
                         dtype=theano.config.floatX)
        return mean_v, v

    chain, updates = theano.scan(lambda v: gibbs_step(v)[1], outputs_info=[v],
                                 n_steps=k)
    v_sample = chain[-1]

    mean_v = gibbs_step(v_sample)[0]
    monitor = T.xlogx.xlogy0(v, mean_v) + T.xlogx.xlogy0(1 - v, 1 - mean_v)
    monitor = monitor.sum() / v.shape[0]

    def free_energy(v):
        return -(v * bv).sum() - T.log(1 + T.exp(T.dot(v, W) + bh)).sum()
    cost = (free_energy(v) - free_energy(v_sample)) / v.shape[0]

    return v_sample, cost, monitor, updates


def shared_normal(num_rows, num_cols, scale=1):
    '''Initialize a matrix shared variable with normally distributed
    elements.'''
    return theano.shared(numpy.random.normal(
        scale=scale, size=(num_rows, num_cols)).astype(theano.config.floatX))


def shared_zeros(*shape):
    '''Initialize a vector shared variable with zero elements.'''
    return theano.shared(numpy.zeros(shape, dtype=theano.config.floatX))


def build_rnnrbm(n_visible, n_hidden, n_hidden_recurrent):
    '''Construct a symbolic RNN-RBM and initialize parameters.

    n_visible : integer
        Number of visible units.
    n_hidden : integer
        Number of hidden units of the conditional RBMs.
    n_hidden_recurrent : integer
        Number of hidden units of the RNN.

    Return a (v, v_sample, cost, monitor, params, updates_train, v_t,
    updates_generate) tuple:

    v : Theano matrix
        Symbolic variable holding an input sequence (used during training)
    v_sample : Theano matrix
        Symbolic variable holding the negative particles for CD log-likelihood
        gradient estimation (used during training)
    cost : Theano scalar
        Expression whose gradient (considering v_sample constant) corresponds
        to the LL gradient of the RNN-RBM (used during training)
    monitor : Theano scalar
        Frame-level pseudo-likelihood (useful for monitoring during training)
    params : tuple of Theano shared variables
        The parameters of the model to be optimized during training.
    updates_train : dictionary of Theano variable -> Theano variable
        Update object that should be passed to theano.function when compiling
        the training function.
    v_t : Theano matrix
        Symbolic variable holding a generated sequence (used during sampling)
    updates_generate : dictionary of Theano variable -> Theano variable
        Update object that should be passed to theano.function when compiling
        the generation function.'''

    W = shared_normal(n_visible, n_hidden, 0.01)
    bv = shared_zeros(n_visible)
    bh = shared_zeros(n_hidden)
    Wuh = shared_normal(n_hidden_recurrent, n_hidden, 0.0001)
    Wuv = shared_normal(n_hidden_recurrent, n_visible, 0.0001)
    Wvu = shared_normal(n_visible, n_hidden_recurrent, 0.0001)
    Wuu = shared_normal(n_hidden_recurrent, n_hidden_recurrent, 0.0001)
    bu = shared_zeros(n_hidden_recurrent)

    params = W, bv, bh, Wuh, Wuv, Wvu, Wuu, bu  # learned parameters as shared
                                                # variables

    v = T.matrix()  # a training sequence
    u0 = T.zeros((n_hidden_recurrent,))  # initial value for the RNN hidden
                                         # units

    # If `v_t` is given, deterministic recurrence to compute the variable
    # biases bv_t, bh_t at each time step. If `v_t` is None, same recurrence
    # but with a separate Gibbs chain at each time step to sample (generate)
    # from the RNN-RBM. The resulting sample v_t is returned in order to be
    # passed down to the sequence history.
    def recurrence(v_t, u_tm1):
        bv_t = bv + T.dot(u_tm1, Wuv)
        bh_t = bh + T.dot(u_tm1, Wuh)
        generate = v_t is None
        if generate:
            v_t, _, _, updates = build_rbm(T.zeros((n_visible,)), W, bv_t,
                                           bh_t, k=25)
        u_t = T.tanh(bu + T.dot(v_t, Wvu) + T.dot(u_tm1, Wuu))
        return ([v_t, u_t], updates) if generate else [u_t, bv_t, bh_t]

    # For training, the deterministic recurrence is used to compute all the
    # {bv_t, bh_t, 1 <= t <= T} given v. Conditional RBMs can then be trained
    # in batches using those parameters.
    (u_t, bv_t, bh_t), updates_train = theano.scan(
        lambda v_t, u_tm1, *_: recurrence(v_t, u_tm1),
        sequences=v, outputs_info=[u0, None, None], non_sequences=params)
    v_sample, cost, monitor, updates_rbm = build_rbm(v, W, bv_t[:], bh_t[:],
                                                     k=15)
    updates_train.update(updates_rbm)

    # symbolic loop for sequence generation
    (v_t, u_t), updates_generate = theano.scan(
        lambda u_tm1, *_: recurrence(None, u_tm1),
        outputs_info=[None, u0], non_sequences=params, n_steps=200)

    print "RBM has been built!"
    return (v, v_sample, cost, monitor, params, updates_train, v_t,
            updates_generate)


class RnnRbm:
    '''Simple class to train an RNN-RBM from MIDI files and to generate sample
    sequences.'''
    
    # MODEL TWEAKS HERE // Maybe a Particle swarm optimisation?
    def __init__(
        self,
        n_hidden=200,  # default: 150
        n_hidden_recurrent=50, # default: 100
        lr=0.005, # default: 0.001
        r=(21, 109),
        dt=0.3 # default: 0.3 
    ):
        '''Constructs and compiles Theano functions for training and sequence
        generation.

        n_hidden : integer
            Number of hidden units of the conditional RBMs.
        n_hidden_recurrent : integer
            Number of hidden units of the RNN.
        lr : float
            Learning rate
        r : (integer, integer) tuple
            Specifies the pitch range of the piano-roll in MIDI note numbers,
            including r[0] but not r[1], such that r[1]-r[0] is the number of
            visible units of the RBM at a given time step. The default (21,
            109) corresponds to the full range of piano (88 notes).
        dt : float
            Sampling period when converting the MIDI files into piano-rolls, or
            equivalently the time difference between consecutive time steps.'''

        self.r = r
        self.dt = dt
        (v, v_sample, cost, monitor, params, updates_train, v_t,
            updates_generate) = build_rnnrbm(
                r[1] - r[0],
                n_hidden,
                n_hidden_recurrent
            )

        gradient = T.grad(cost, params, consider_constant=[v_sample])
        updates_train.update(
            ((p, p - lr * g) for p, g in zip(params, gradient))
        )
        self.train_function = theano.function(
            [v],
            monitor,
            updates=updates_train
        )
        self.generate_function = theano.function(
            [],
            v_t,
            updates=updates_generate
        )

    def train(self, files, batch_size=100, num_epochs=200):
        '''Train the RNN-RBM via stochastic gradient descent (SGD) using MIDI
        files converted to piano-rolls.

        files : list of strings
            List of MIDI files that will be loaded as piano-rolls for training.
        batch_size : integer
            Training sequences will be split into subsequences of at most this
            size before applying the SGD updates.
        num_epochs : integer
            Number of epochs (pass over the training set) performed. The user
            can safely interrupt training with Ctrl+C at any time.'''

        assert len(files) > 0, 'Training set is empty!' \
                               ' (did you download the data files?)'
        dataset = [midiread(f, self.r,
                            self.dt).piano_roll.astype(theano.config.floatX)
                   for f in files]
        print "Start training process of the recurrent network RBM machine with the given dataset..." ,
        print "Lenght of the Dataset: ", len(files)
        print "Interrupt if necessariy by pressing Ctrl+C",
        print "...Might take some time :) ..."
        costst = []
        try:
            for epoch in xrange(num_epochs):
                numpy.random.shuffle(dataset)
                costs = []

                for s, sequence in enumerate(dataset):
                    for i in xrange(0, len(sequence), batch_size):
                        cost = self.train_function(sequence[i:i + batch_size])
                        costs.append(cost)

                print 'Epoch %i/%i' % (epoch + 1, num_epochs),
                print "Current mean Energy cost:", numpy.mean(costs)
                costst.append(numpy.mean(costs))
                print "Training %i percent done; interrupt training by pressing Crtl+C." % (float((float(epoch) + 1.0)*100.0 / float(num_epochs)))
                sys.stdout.flush()

        except KeyboardInterrupt:
            print 'Training Interrupted.'
            
        return self, files, costst

    def generate(self, filename, show=True):
        '''Generate a sample sequence, plot the resulting piano-roll and save
        it as a MIDI file.

        filename : string
            A MIDI file will be created at this location.
        show : boolean
            If True, a piano-roll of the generated sequence will be shown.'''

        piano_roll = self.generate_function()
        print "Sample generated!"
        midiwrite(filename, piano_roll, self.r, self.dt)
        if show:
            extent = (0, self.dt * len(piano_roll)) + self.r
            pylab.figure()
            pylab.imshow(piano_roll.T, origin='lower', aspect='auto',
                         interpolation='nearest', cmap=pylab.cm.gray_r,
                         extent=extent)
            pylab.xlabel('time (s)')
            pylab.ylabel('MIDI note number (corresponds to piano keys)')
            pylab.title('generated piano-roll')
            pylab.savefig('Piano_Roll_'+str(filename)) #
            
        return piano_roll #
            
##############

        
####### hf-implementation code: 

def gauss_newton_product(cost, p, v, s):  # this computes the product Gv = J'HJv (G is the Gauss-Newton matrix)
  Jv = T.Rop(s, p, v)
  HJv = T.grad(T.sum(T.grad(cost, s)*Jv), s, consider_constant=[Jv], disconnected_inputs='ignore')
  Gv = T.grad(T.sum(HJv*s), p, consider_constant=[HJv, Jv], disconnected_inputs='ignore')
  Gv = map(T.as_tensor_variable, Gv)  # for CudaNdarray
  return Gv


class hf_optimizer:
  '''Black-box Theano-based Hessian-free optimizer.
See (Martens, ICML 2010) and (Martens & Sutskever, ICML 2011) for details.

Useful functions:
__init__ :
    Compiles necessary Theano functions from symbolic expressions.
train :
    Performs HF optimization following the above references.'''

  def __init__(self, p, inputs, s, costs, h=None, ha=None):
    '''Constructs and compiles the necessary Theano functions.

  p : list of Theano shared variables
      Parameters of the model to be optimized.
  inputs : list of Theano variables
      Symbolic variables that are inputs to your graph (they should also
      include your model 'output'). Your training examples must fit these.
  s : Theano variable
    Symbolic variable with respect to which the Hessian of the objective is
    positive-definite, implicitly defining the Gauss-Newton matrix. Typically,
    it is the activation of the output layer.
  costs : list of Theano variables
      Monitoring costs, the first of which will be the optimized objective.
  h: Theano variable or None
      Structural damping is applied to this variable (typically the hidden units
      of an RNN).
  ha: Theano variable or None
    Symbolic variable that implicitly defines the Gauss-Newton matrix for the
    structural damping term (typically the activation of the hidden layer). If
    None, it will be set to `h`.'''

    self.p = p
    self.shapes = [i.get_value().shape for i in p]
    self.sizes = map(numpy.prod, self.shapes)
    self.positions = numpy.cumsum([0] + self.sizes)[:-1]

    g = T.grad(costs[0], p)
    g = map(T.as_tensor_variable, g)  # for CudaNdarray
    self.f_gc = theano.function(inputs, g + costs, on_unused_input='ignore')  # during gradient computation
    self.f_cost = theano.function(inputs, costs, on_unused_input='ignore')  # for quick cost evaluation

    symbolic_types = T.scalar, T.vector, T.matrix, T.tensor3, T.tensor4

    v = [symbolic_types[len(i)]() for i in self.shapes]
    Gv = gauss_newton_product(costs[0], p, v, s)

    coefficient = T.scalar()  # this is lambda*mu    
    if h is not None:  # structural damping with cross-entropy
      h_constant = symbolic_types[h.ndim]()  # T.Rop does not support `consider_constant` yet, so use `givens`
      structural_damping = coefficient * (-h_constant*T.log(h + 1e-10) - (1-h_constant)*T.log((1-h) + 1e-10)).sum() / h.shape[0]
      if ha is None: ha = h
      Gv_damping = gauss_newton_product(structural_damping, p, v, ha)
      Gv = [a + b for a, b in zip(Gv, Gv_damping)]
      givens = {h_constant: h}
    else:
      givens = {}

    self.function_Gv = theano.function(inputs + v + [coefficient], Gv, givens=givens,
                                       on_unused_input='ignore')

  def quick_cost(self, delta=0):
    # quickly evaluate objective (costs[0]) over the CG batch
    # for `current params` + delta
    # delta can be a flat vector or a list (else it is not used)
    if isinstance(delta, numpy.ndarray):
      delta = self.flat_to_list(delta)

    if type(delta) in (list, tuple):
      for i, d in zip(self.p, delta):
        i.set_value(i.get_value() + d)

    cost = numpy.mean([self.f_cost(*i)[0] for i in self.cg_dataset.iterate(update=False)])

    if type(delta) in (list, tuple):
      for i, d in zip(self.p, delta):
        i.set_value(i.get_value() - d)

    return cost


  def cg(self, b):
    if self.preconditioner:
      M = self.lambda_ * numpy.ones_like(b)
      for inputs in self.cg_dataset.iterate(update=False):
        M += self.list_to_flat(self.f_gc(*inputs)[:len(self.p)])**2  # / self.cg_dataset.number_batches**2
      # print 'precond~%.3f,' % (M - self.lambda_).mean(),
      M **= -0.75  # actually 1/M
      sys.stdout.flush()
    else:
      M = 1.0

    x = self.cg_last_x if hasattr(self, 'cg_last_x') else numpy.zeros_like(b)  # sharing information between CG runs
    r = b - self.batch_Gv(x)
    d = M*r
    delta_new = numpy.dot(r, d)
    phi = []
    backtracking = []
    backspaces = 0

    for i in xrange(1, 1 + self.max_cg_iterations):
      # adapted from http://www.cs.cmu.edu/~quake-papers/painless-conjugate-gradient.pdf (p.51)
      q = self.batch_Gv(d)
      dq = numpy.dot(d, q)
      # assert dq > 0, 'negative curvature'
      alpha = delta_new / dq
      x = x + alpha*d
      r = r - alpha*q
      s = M*r
      delta_old = delta_new
      delta_new = numpy.dot(r, s)
      d = s + (delta_new / delta_old) * d

      if i >= int(numpy.ceil(1.3**len(backtracking))):
        backtracking.append((self.quick_cost(x), x.copy(), i))

      phi_i = -0.5 * numpy.dot(x, r + b)
      phi.append(phi_i)

      progress = ' [CG iter %i, phi=%+.5f, cost=%.5f]' % (i, phi_i, backtracking[-1][0])
      sys.stdout.write('\b'*backspaces + progress)
      sys.stdout.flush()
      backspaces = len(progress)

      k = max(10, i/10)
      if i > k and phi_i < 0 and (phi_i - phi[-k-1]) / phi_i < k*0.0005:
        break

    self.cg_last_x = x.copy()

    if self.global_backtracking:
      j = numpy.argmin([bt[0] for bt in backtracking])
    else:
      j = len(backtracking) - 1
      while j > 0 and backtracking[j-1][0] < backtracking[j][0]:
        j -= 1
    print ' backtracked %i/%i' % (backtracking[j][2], i),
    sys.stdout.flush()

    return backtracking[j] + (i,)

  def flat_to_list(self, vector):
    return [vector[position:position + size].reshape(shape) for shape, size, position in zip(self.shapes, self.sizes, self.positions)]

  def list_to_flat(self, l):
    return numpy.concatenate([i.flatten() for i in l])

  def batch_Gv(self, vector, lambda_=None):
    v = self.flat_to_list(vector)
    if lambda_ is None: lambda_ = self.lambda_
    result = lambda_*vector  # Tikhonov damping
    for inputs in self.cg_dataset.iterate(False):
      result += self.list_to_flat(self.function_Gv(*(inputs + v + [lambda_*self.mu]))) / self.cg_dataset.number_batches
    return result

  def trainhf(self, gradient_dataset, cg_dataset, initial_lambda=0.1, mu=0.03, global_backtracking=False, preconditioner=False, max_cg_iterations=250, num_updates=100, validation=None, validation_frequency=1, patience=numpy.inf, save_progress='hftrainingTEMP'):
    '''Performs HF training.

  gradient_dataset : SequenceDataset-like object
      Defines batches used to compute the gradient.
      The `iterate(update=True)` method should yield shuffled training examples
      (tuples of variables matching your graph inputs).
      The same examples MUST be returned between multiple calls to iterator(),
      unless update is True, in which case the next batch should be different.
  cg_dataset : SequenceDataset-like object
      Defines batches used to compute CG iterations.
  initial_lambda : float
      Initial value of the Tikhonov damping coefficient.
  mu : float
      Coefficient for structural damping.
  global_backtracking : Boolean
      If True, backtracks as much as necessary to find the global minimum among
      all CG iterates. Else, Martens' heuristic is used.
  preconditioner : Boolean
      Whether to use Martens' preconditioner.
  max_cg_iterations : int
      CG stops after this many iterations regardless of the stopping criterion.
  num_updates : int
      Training stops after this many parameter updates regardless of `patience`.
  validation: SequenceDataset object, (lambda : tuple) callback, or None
      If a SequenceDataset object is provided, the training monitoring costs
      will be evaluated on that validation dataset.
      If a callback is provided, it should return a list of validation costs
      for monitoring, the first of which is also used for early stopping.
      If None, no early stopping nor validation monitoring is performed.
  validation_frequency: int
      Validation is performed every `validation_frequency` updates.
  patience: int
      Training stops after `patience` updates without improvement in validation
      cost.
  save_progress: string or None
      A checkpoint is automatically saved at this location after each update.
      Call the `train` function again with the same parameters to resume
      training.'''

    self.lambda_ = initial_lambda
    self.mu = mu
    self.global_backtracking = global_backtracking
    self.cg_dataset = cg_dataset
    self.preconditioner = preconditioner
    self.max_cg_iterations = max_cg_iterations
    best = [0, numpy.inf, None]  # iteration, cost, params
    first_iteration = 1

    if isinstance(save_progress, str) and os.path.isfile(save_progress):
      save = cPickle.load(file(save_progress))
      self.cg_last_x, best, self.lambda_, first_iteration, init_p = save
      first_iteration += 1
      for i, j in zip(self.p, init_p): i.set_value(j)
      print '* recovered saved model'
    
    try:
      for u in xrange(first_iteration, 1 + num_updates):
        print 'update %i/%i,' % (u, num_updates),
        sys.stdout.flush()

        gradient = numpy.zeros(sum(self.sizes), dtype=theano.config.floatX)
        costs = []
        for inputs in gradient_dataset.iterate(update=True):
          result = self.f_gc(*inputs)
          gradient += self.list_to_flat(result[:len(self.p)]) / gradient_dataset.number_batches
          costs.append(result[len(self.p):])

        print 'cost=', numpy.mean(costs, axis=0),
        print 'lambda=%.5f,' % self.lambda_,
        sys.stdout.flush()

        after_cost, flat_delta, backtracking, num_cg_iterations = self.cg(-gradient)
        delta_cost = numpy.dot(flat_delta, gradient + 0.5*self.batch_Gv(flat_delta, lambda_=0))  # disable damping
        before_cost = self.quick_cost()
        for i, delta in zip(self.p, self.flat_to_list(flat_delta)):
          i.set_value(i.get_value() + delta)
        cg_dataset.update()

        rho = (after_cost - before_cost) / delta_cost  # Levenberg-Marquardt
        # print 'rho=%f' %rho,
        if rho < 0.25:
          self.lambda_ *= 1.5
        elif rho > 0.75:
          self.lambda_ /= 1.5
        
        if validation is not None and u % validation_frequency == 0:
          if hasattr(validation, 'iterate'):
            costs = numpy.mean([self.f_cost(*i) for i in validation.iterate()], axis=0)
          elif callable(validation):
            costs = validation()
          print 'validation=', costs,
          if costs[0] < best[1]:
            best = u, costs[0], [i.get_value().copy() for i in self.p]
            print '*NEW BEST',

        if isinstance(save_progress, str):
          # do not save dataset states
          save = self.cg_last_x, best, self.lambda_, u, [i.get_value().copy() for i in self.p]
          cPickle.dump(save, file(save_progress, 'wb'), cPickle.HIGHEST_PROTOCOL)
        
        if u - best[0] > patience:
          print 'PATIENCE ELAPSED, BAILING OUT'
          break
        
        print
        sys.stdout.flush()
    except KeyboardInterrupt:
      print 'Interrupted by user.'
    
    if best[2] is None:
      best[2] = [i.get_value().copy() for i in self.p]
    return best[2]
    
    
    def generate(self, filename, show=True):
        '''Generate a sample sequence, plot the resulting piano-roll and save
        it as a MIDI file.

        filename : string
            A MIDI file will be created at this location.
        show : boolean
            If True, a piano-roll of the generated sequence will be shown.'''

        piano_roll = self.generate_function()
        print "Sample generated!"
        midiwrite(filename, piano_roll, self.r, self.dt)
        if show:
            extent = (0, self.dt * len(piano_roll)) + self.r
            pylab.figure()
            pylab.imshow(piano_roll.T, origin='lower', aspect='auto',
                         interpolation='nearest', cmap=pylab.cm.gray_r,
                         extent=extent)
            pylab.xlabel('time (s)')
            pylab.ylabel('MIDI note number (corresponds to piano keys)')
            pylab.title('generated piano-roll')
            pylab.savefig('Piano_Roll_'+str(filename))
            


class SequenceDataset:
  '''Slices, shuffles and manages a small dataset for the HF optimizer.'''

  def __init__(self, data, batch_size, number_batches, minimum_size=10):
    '''SequenceDataset __init__

  data : list of lists of numpy arrays
    Your dataset will be provided as a list (one list for each graph input) of
    variable-length tensors that will be used as mini-batches. Typically, each
    tensor is a sequence or a set of examples.
  batch_size : int or None
    If an int, the mini-batches will be further split in chunks of length
    `batch_size`. This is useful for slicing subsequences or provide the full
    dataset in a single tensor to be split here. All tensors in `data` must
    then have the same leading dimension.
  number_batches : int
    Number of mini-batches over which you iterate to compute a gradient or
    Gauss-Newton matrix product.
  minimum_size : int
    Reject all mini-batches that end up smaller than this length.'''
    self.current_batch = 0
    self.number_batches = number_batches
    self.items = []

    for i_sequence in xrange(len(data[0])):
      if batch_size is None:
        self.items.append([data[i][i_sequence] for i in xrange(len(data))])
      else:
        for i_step in xrange(0, len(data[0][i_sequence]) - minimum_size + 1, batch_size):
          self.items.append([data[i][i_sequence][i_step:i_step + batch_size] for i in xrange(len(data))])
          
    self.shuffle()
  
  def shuffle(self):
    numpy.random.shuffle(self.items)

  def iterate(self, update=True):
    for b in xrange(self.number_batches):
      yield self.items[(self.current_batch + b) % len(self.items)]
    if update: self.update()

  def update(self):
    if self.current_batch + self.number_batches >= len(self.items):
      self.shuffle()
      self.current_batch = 0
    else:
      self.current_batch += self.number_batches

          
###################### Example NN implementation: 

#import numpy, sys
#import theano
#import theano.tensor as T
#
#from hf import hf_optimizer, SequenceDataset
#
#
#def test_cg(n=500):
#  '''Attempt to solve a linear system using the CG function in hf_optimizer.'''
#
#  A = numpy.random.uniform(-1, 1, (n, n))
#  A = numpy.dot(A.T, A)
#  val, vec = numpy.linalg.eig(A)
#  val = numpy.random.uniform(1, 5000, (n, 1))
#  A = numpy.dot(vec.T, val*vec)
#
#  # hack into a fake hf_optimizer object
#  x = theano.shared(0.0)
#  s = 2.0*x
#  hf = hf_optimizer([x], [], s, [s**2])
#  hf.quick_cost = lambda *args, **kwargs: 0.0
#  hf.global_backtracking = False
#  hf.preconditioner = False
#  hf.max_cg_iterations = 300
#  hf.batch_Gv = lambda v: numpy.dot(A, v)
#  b = numpy.random.random(n)
#  c, x, j, i = hf.cg(b)
#  print
#
#  print 'error on b =', abs(numpy.dot(A, x) - b).mean()
#  print 'error on x =', abs(numpy.linalg.solve(A, b) - x).mean()
#
#
#def sgd_optimizer(p, inputs, costs, train_set, lr=1e-4):
#  '''SGD optimizer with a similar interface to hf_optimizer.'''
#
#  g = [T.grad(costs[0], i) for i in p]
#  updates = dict((i, i - lr*j) for i, j in zip(p, g))
#  f = theano.function(inputs, costs, updates=updates)
#  
#  try:
#    for u in xrange(1000):
#      cost = []
#      for i in train_set.iterate(True):
#        cost.append(f(*i))
#      print 'update %i, cost=' %u, numpy.mean(cost, axis=0)
#      sys.stdout.flush()
#
#  except KeyboardInterrupt: 
#    print 'Training interrupted.'
#
#
## feed-forward neural network with sigmoidal output
#def simple_NN(sizes=(784, 100, 10)):
#  x = T.matrix()
#  t = T.matrix()
#
#  p = []
#  y = x
#
#  for i in xrange(len(sizes)-1):
#    a, b = sizes[i:i+2]
#    Wi = theano.shared((10./numpy.sqrt(a+b) * numpy.random.uniform(-1, 1, size=(a, b))).astype(theano.config.floatX))
#    bi = theano.shared(numpy.zeros(b, dtype=theano.config.floatX))
#    p += [Wi, bi]
#
#    s = T.dot(y,Wi) + bi
#    y = T.nnet.sigmoid(s)
#
#  c = (-t* T.log(y) - (1-t)* T.log(1-y)).mean()
#  acc = T.neq(T.round(y), t).mean()
#
#  return p, [x, t], s, [c, acc]
#
#
#def example_NN(hf=True):
#  p, inputs, s, costs = simple_NN((2, 50, 40, 30, 1))
#
#  xor_dataset = [[], []]
#  for i in xrange(50000):
#    x = numpy.random.randint(0, 2, (50, 2))
#    t = (x[:, 0:1] ^ x[:, 1:2]).astype(theano.config.floatX)
#    x = x.astype(theano.config.floatX)
#    xor_dataset[0].append(x)
#    xor_dataset[1].append(t)
#
#  training_examples = len(xor_dataset[0]) * 3/4
#  train = [xor_dataset[0][:training_examples], xor_dataset[1][:training_examples]]
#  valid = [xor_dataset[0][training_examples:], xor_dataset[1][training_examples:]]
#
#  gradient_dataset = SequenceDataset(train, batch_size=None, number_batches=10000)
#  cg_dataset = SequenceDataset(train, batch_size=None, number_batches=5000)
#  valid_dataset = SequenceDataset(valid, batch_size=None, number_batches=5000)
#  
#  if hf:
#    hf_optimizer(p, inputs, s, costs).train(gradient_dataset, cg_dataset, initial_lambda=1.0, preconditioner=True, validation=valid_dataset)
#  else:
#    sgd_optimizer(p, inputs, costs, gradient_dataset, lr=1e-3)
#    
#
## single-layer recurrent neural network with sigmoid output, only last time-step output is significant
#def simple_RNN(nh):
#  Wx = theano.shared(0.2 * numpy.random.uniform(-1.0, 1.0, (1, nh)).astype(theano.config.floatX))
#  Wh = theano.shared(0.2 * numpy.random.uniform(-1.0, 1.0, (nh, nh)).astype(theano.config.floatX))
#  Wy = theano.shared(0.2 * numpy.random.uniform(-1.0, 1.0, (nh, 1)).astype(theano.config.floatX))
#  bh = theano.shared(numpy.zeros(nh, dtype=theano.config.floatX))
#  by = theano.shared(numpy.zeros(1, dtype=theano.config.floatX))
#  h0 = theano.shared(numpy.zeros(nh, dtype=theano.config.floatX))
#  p = [Wx, Wh, Wy, bh, by, h0]
#
#  x = T.matrix()
#
#  def recurrence(x_t, h_tm1):
#    ha_t = T.dot(x_t, Wx) + T.dot(h_tm1, Wh) + bh
#    h_t = T.tanh(ha_t)
#    s_t = T.dot(h_t, Wy) + by
#    return [ha_t, h_t, s_t]
#
#  ([ha, h, activations], updates) = theano.scan(fn=recurrence, sequences=x, outputs_info=[dict(), h0, dict()])
#
#  h = T.tanh(ha)  # so it is differentiable with respect to ha
#  t = x[0, 0]
#  s = activations[-1, 0]
#  y = T.nnet.sigmoid(s)
#  loss = -t*T.log(y + 1e-14) - (1-t)*T.log((1-y) + 1e-14)
#  acc = T.neq(T.round(y), t)
#  
#  return p, [x], s, [loss, acc], h, ha
#
#
#def example_RNN(hf=True):
#  p, inputs, s, costs, h, ha = simple_RNN(100)
#
#  memorization_dataset = [[]]  # memorize the first unit for 100 time-steps with binary noise
#  for i in xrange(100000):
#    memorization_dataset[0].append(numpy.random.randint(2, size=(100, 1)).astype(theano.config.floatX))
#
#  train = [memorization_dataset[0][:-1000]]
#  valid = [memorization_dataset[0][-1000:]]
#  
#  gradient_dataset = SequenceDataset(train, batch_size=None, number_batches=5000)
#  cg_dataset = SequenceDataset(train, batch_size=None, number_batches=1000)
#  valid_dataset = SequenceDataset(valid, batch_size=None, number_batches=1000)
#
#  if hf:
#    hf_optimizer(p, inputs, s, costs, 0.5*(h + 1), ha).train(gradient_dataset, cg_dataset, initial_lambda=0.5, mu=1.0, preconditioner=False, validation=valid_dataset)
#  else:
#    sgd_optimizer(p, inputs, costs, gradient_dataset, lr=5e-5)    
#

############## Example ends here.


################# hf ends here


########## CALLS:

def test_rnnrbm(modelin=None, costsold=None, batch_size=100, num_epochs=100): #defaulfs: batchsize: 100 (60s) and epochs: 200
    
    if modelin == None:
        model = RnnRbm()
        model, files, costst = model.train(glob.glob(str(os.path.dirname(__file__))+ FILEPATH +'/train/*.mid'), batch_size=batch_size, num_epochs=num_epochs)
    
    elif modelin != None:
        model, files, costst = modelin.train(glob.glob(str(os.path.dirname(__file__))+ FILEPATH + '/train/*.mid'), batch_size=batch_size, num_epochs=num_epochs)
        costst= costsold.append(costst)
        
        if not (len(costsold) > 0):
            print "failed to load old cost-matrix!"
                
    return model, files, costst



##################################################################################
#################################################################################


if __name__ == '__main__':
    print " This will train on the given dataset and generate 20, hopefully enjoyable, sequences..."
    
############ CONFIG
    saving = True #set true if saving is wanted 
    save_filename = 'save_learning_progress2Nott.p'
    loading = False #set True if immediatly continiung is wanted 
###########

    
    if saving == True:
        model, files, costst = test_rnnrbm()
        print "Saving current learning!"  
        cPickle.dump((model, costst), file(save_filename)) #open( save_filename, "wb" ) )
        print "Data saved!"
        print "Proceeding with the model's Sample generation..."
        
    elif loading == True: 
        print "Loading the current Model and proceeding to learn..."
        saved = cPickle.load(file(save_filename)) #open( save_filename, "rb" ) )
        modelsaved, coststsaved = saved
        print "Model loaded. Proceed learning."
        model, files, costst = test_rnnrbm(modelin=modelsaved, costsold=coststsaved)
        print "Saving current learning status!" 
        cPickle.dump((model, costst), file(save_filename)) #open( save_filename, "wb" ) )
        print "Data saved!"
        print "Proceeding with the model's Sample generation..."
    else: 
        print "Error: Please select either loading or saving to start the model!"


###########    
    
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



###TODO: implement the hessian free algorithm for faster learning.
#
# 
#    modelhf = hf_optimizer(model, files, test,  costs)                
#    modelhf.trainhf(glob.glob(str(os.path.dirname(__file__)) + FILEPATH + '/train/*.mid'), glob.glob(str(os.path.dirname(__file__)) + FILEPATH + '/test/*.mid'))
#   
#    modelhf.generate('sample1.mid')
#    modelhf.generate('sample2.mid')
#    modelhf.generate('sample3.mid')
#    modelhf.generate('sample4.mid')
#    modelhf.generate('sample5.mid')
#    modelhf.generate('sample6.mid')
#    modelhf.generate('sample7.mid')
#    modelhf.generate('sample8.mid')
#    modelhf.generate('sample9.mid')
#    modelhf.generate('sample10.mid')
#    modelhf.generate('sample11.mid')
#    modelhf.generate('sample12.mid')
#    modelhf.generate('sample13.mid')
#    modelhf.generate('sample14.mid')
#    modelhf.generate('sample15.mid')
#    modelhf.generate('sample16.mid')
#    modelhf.generate('sample17.mid')
#    modelhf.generate('sample18.mid')
#    modelhf.generate('sample19.mid')
#    modelhf.generate('sample20.mid')
#    pylab.show()  
#    
#    
########
