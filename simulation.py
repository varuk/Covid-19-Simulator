
from scipy.stats import lognorm
import random
from matplotlib import pyplot as plt


transmission = {"H":0.2,"W":0.1,"S":0.05}  #transmission probabilities for household, work and school contact edge
class Agent:        #agents class 
    def __init__(self,id,state="S"):
        self.id = id
        
        
        self.state = state
        self.contacts = []
        self.infectedtill = 0 # till what time agent remains infected 
        self.exposedtill = 0 # till what time agent remains exposed and become infected
        
    def insert(self,contact,agent):
        self.contacts.append((contact,agent))
        
    #update state of agent
    def update(self,time,Agents):
        if self.state== "S" :
            if(random.uniform(0,1)<=self.getprob(Agents)):
                self.state = "E"
                self.exposedtill = int(random.lognormvariate(4.6,4.8))+time
            
        elif self.state=="E"and time>=self.exposedtill:
            self.state = "I"
            self.infectedtill = time+int(random.lognormvariate(5,2))
            
        elif self.state=="I" and time>=self.infectedtill:
            self.state = "R"
            
    #get transmission probability        
    def getprob(self,Agents):
        B=1
        for L in self.contacts:
            if Agents[L[0]].state=="I":
                B = B*(1-transmission[L[1]])
                
       
        return 1-B
                
        

class datagenerator:   #generates a contact graph of agents and initial list of infected and suspected individuals
    def __init__(self, numagents=50, meancontacts=4,infected=5):
        self.numagents=numagents    # total number of agents
        self.meancontacts=meancontacts   #mean of contacts per person
        self.infected=infected      #number of infected people at the beginning
        self.agents=[Agent(i) for i in range(numagents)]   #list of all agents 
    def create(self):
        Infected=[]
        Susceptible=[]
        Exposed=[]
        Recovered=[]
        for i in range(self.infected):
            rand= random.randint(0,self.numagents-1) #randomly picking a subset of patients to mark as infected
            time= int(random.lognormvariate(8,2)) #creating a number for how many days the person remains infected
            self.agents[rand].state="I"
            self.agents[rand].infectedtill=time
            if not(rand in Infected):
                Infected.append(rand)
        dict = {1:"H",2:"S",3:"W"}
        for i in range(self.numagents):
            if (self.agents[i].state=='S'):
                Susceptible.append(i)
            rand = int(random.gauss(self.meancontacts,2)) #gauss distribution for calculating number of contacts for that person
            for j in range(rand):
                if(len(self.agents[i].contacts)>=rand):
                    break
                randj= random.randint(0,self.numagents-1)
                typ= random.randint(1,3)  #type of contact : school, work, household
                if not((randj,dict[typ]) in self.agents[i].contacts):
                    if(randj !=i):
                        self.agents[i].contacts.append((randj,dict[typ]))
                        self.agents[randj].contacts.append((i,dict[typ]))
        return self.agents,Infected,Susceptible,Exposed,Recovered

Agents , Infected,Susceptible,Exposed,Recovered = datagenerator(5000,20,50).create()

class Simulation:
    def __init__(self,time,Agents,Susceptible,Infected,Recovered,Exposed):
        self.stats=[]
        self.Time = time #number of days to run
        self.Susceptible = Susceptible  
        self.Infected = Infected
        self.Exposed = Exposed
        self.Recovered = Recovered
        self.Agents = Agents
    
    
      
    def run(self):
   
      for time in range(self.Time):
        
        
        for i in Exposed:
            self.Agents[i].update(time,self.Agents)
            if self.Agents[i].state=="I":
                Exposed.remove(i)
                Infected.append(i)
        for i in Infected:
            self.Agents[i].update(time,self.Agents)
            if self.Agents[i].state=="R":
                Infected.remove(i)
                Recovered.append(i)
        for i in Susceptible:
            self.Agents[i].update(time,self.Agents)
            if self.Agents[i].state=="E":
                Susceptible.remove(i)
                Exposed.append(i)
        self.stats.append([len(Susceptible),len(Exposed),len(Infected),len(Recovered)])
    def plot(self):
        plt.plot([i for i in range(len(self.stats))],[l[0] for l in self.stats],label="Susceptible")
        plt.plot([i for i in range(len(self.stats))],[l[1] for l in self.stats],label="Exposed")
        plt.plot([i for i in range(len(self.stats))],[l[2] for l in self.stats],label="Infected")
        plt.plot([i for i in range(len(self.stats))],[l[3] for l in self.stats],label="Recovered")
        plt.xlabel('Days')
        plt.ylabel('No of agents')

        plt.title('Transmission')

        plt.legend()

        plt.show()
        
    
if __name__ == "__main__":
    
    Model = Simulation(200,Agents,Susceptible,Infected,Recovered,Exposed) #sample case
    Model.run()
    Model.plot()