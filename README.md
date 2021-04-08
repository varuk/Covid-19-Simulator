# Covid-19-Simulator
Here we present a simple simulation of the spread of COVID-19 given a starting population and
a contact graph with the help of an stochastic discrete-time step SEIR(susceptible, exposed,
infected, recovered) agent based model. The model is coded in python and the parameters are
hardcoded but may be specified by the user. One time step is given by one day.

● There are three classes- agent, datagenerator and model. Datagenerator class generates a
random contact graph of agents and the model class describes the simulation model.

● The parameters such as number of days, transmission probabilities can be specified by
the user in model class.

● The transition from susceptible to exposed is given by transmission probabilities if they
come in contact.

● Transmission probabilities are defined for household, work and school edges in graph,
assuming more transmission rate for contacts within a household. 

● The transition from exposed to infectious state is given by log-normal distribution with
mean 4.6 days.

● The recovery times for infected individuals are given by a log-normal distribution with
mean 8 days.

● Once recovered, the agents don't change their state. (the model does not consider the
chances of re-infection).

● The number of total agents infected and total agents recovered can be plotted with time.

