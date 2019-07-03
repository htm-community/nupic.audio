#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simple Model of Spiking Neurons
# IEEE Transactions on Neural Networks(2003) 14:1569 - 1572
#  Eugene M. Izhikevich
# https://www.izhikevich.org/publications/spikes.htm

# http://www.maths.dit.ie/~johnbutler/Izhikevich/IzhikevichModel.html
# https://extropynow.weebly.com/izhikevich-model-on-python.html

from numpy import *
from pylab import *


# Izhikevich neuron model

class IzhNeuron:
  # - The parameter a 􏰇describes the time scale of the recovery variable u.
  #   Smaller values result in slower recovery. A typical value is a = 0.02
  # - The parameter b 􏰈describes the sensitivity of the recovery variable u
  #   to the subthreshold fluctuations of the membrane potential v.
  #   Greater values couple u and v more strongly resulting in possible
  #   subthreshold oscillations and low-threshold spiking dynamics.
  #   A typical value is b = 0.2 The case b < a(b > a) corresponds to
  #   saddle-node (Andronov–Hopf) bifurcation of the resting state.
  # - The parameter c 􏰉describes the after-spike reset value of the membrane
  #   potential v caused by the fast high-threshold K+ conductances.
  #   A typical value is c = -65 mV
  # - The parameter d describes after-spike reset of the recovery variable 􏰓􏰓
  #   u caused by slow high-threshold Na+ and K+ conductances.
  #   A typical value is d = 2
  #
  # Membrane potential v has mV scale and the time t has ms scale
  #

  def __init__(self, label, a, b, c, d, v0, u0=None):
    self.label = label
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.v = v0
    self.u = u0 if u0 is not None else b*v0


class IzhSim:
  def __init__(self, n, T, dt=0.25):
    self.neuron = n
    self.dt = dt
    self.t = t = arange(0, T+dt, dt)
    self.stim = zeros(len(t))
    self.x = 5
    self.y = 140
    self.du = lambda a, b, v, u: a*(b*v - u)

  def integrate(self, n=None):
    if n is None:
      n = self.neuron

    trace = zeros((2, len(self.t)))
    for i, j in enumerate(self.stim):
      n.v += self.dt * (0.04*n.v**2 + self.x*n.v + self.y - n.u + self.stim[i])
      n.u += self.dt * self.du(n.a, n.b, n.v, n.u)
      if n.v < 30:
        trace[0, i] = n.v
        trace[1, i] = n.u
      else:
        # Produce spike, and reset membrane voltage (v) and recovery (u)
        trace[0, i] = 30
        n.v = n.c
        n.u += n.d
    return trace


def main():
  sims = []

  # a = decay rate of u(t)
  # b = sensitivity of u(t)
  # c = reset of v(t)
  # d = reset of u(t)

  # b = 0.2, c = −65, and
  # d = 8, a = 0.02 for excitatory neurons and
  # d = 2, a = 0.1 for inhibitory neurons

  # n = IzhNeuron("(A) tonic spiking", a=0.02, b=0.2, c=-65, d=6, v0=-70)
  # s = IzhSim(n, T=100)
  # for i, t in enumerate(s.t):
  #   s.stim[i] = 14 if t > 10 else 0
  # sims.append(s)
  #
  # n = IzhNeuron("(B) phasic spiking", a=0.02, b=0.25, c=-65, d=6, v0=-64)
  # s = IzhSim(n, T=200)
  # for i, t in enumerate(s.t):
  #   s.stim[i] = 0.5 if t > 20 else 0
  # sims.append(s)

  n = IzhNeuron("(RS) regular spiking", a=0.02, b=0.2, c=-65, d=8, v0=-64)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 5 if t > 20 else 0
  sims.append(s)

  n = IzhNeuron("(IB) intrinsically bursting", a=0.02, b=0.2, c=-55, d=4, v0=-64)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 5 if t > 20 else 0
  sims.append(s)

  n = IzhNeuron("(CH) chattering", a=0.02, b=0.2, c=-50, d=2, v0=-64)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 5 if t > 20 else 0
  sims.append(s)

  n = IzhNeuron("(FS) fast spiking", a=0.1, b=0.2, c=-65, d=2, v0=-64)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 5 if t > 20 else 0
  sims.append(s)

  n = IzhNeuron("(TC) thalmo-cortical", a=0.02, b=0.25, c=-65, d=0.05, v0=-63)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 5 if t > 20 else 0
  sims.append(s)

  n = IzhNeuron("(TC) thalamo-cortical", a=0.02, b=0.25, c=-65, d=0.05, v0=-87)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 0 if t > 20 else -5
  sims.append(s)

  # Parameters not correct, doesn't resonate properly
  n = IzhNeuron("(RZ) resonator", a=0.1, b=0.26, c=-65, d=2, v0=-64)
  s = IzhSim(n, T=100)
  for i, t in enumerate(s.t):
    s.stim[i] = 0 if t > 20 else -5
    s.stim[i] = 5 if t > 50 and t < 60 else s.stim[i]
  sims.append(s)

  n = IzhNeuron("(LTS) low-threshold", a=0.02, b=0.25, c=-65, d=2, v0=-64)
  s = IzhSim(n, T=200)
  for i, t in enumerate(s.t):
    s.stim[i] = 5 if t > 20 else 0
  sims.append(s)

  # Simulate
  fig = figure()
  fig.suptitle('Izhikevich neuron models')

  for i, s in enumerate(sims):
    res = s.integrate()

    ax = subplot(2, 4, i+1)
    ax.plot(s.t, res[0], s.t, -95 + ((s.stim - min(s.stim))/(max(s.stim) - min(s.stim)))*10)

    ax.set_xlim([0, s.t[-1]])
    ax.set_ylim([-100, 35])

    ax.set_title(s.neuron.label, size="small")

    ax.set_xticklabels([])
    ax.set_yticklabels([])

  show()


if __name__ == "__main__":
    main()
