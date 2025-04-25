import numpy as np
import random

# Define the Agent class
class Agent:
    def __init__(self, layer_id, num_agents, threshold=1.0, weight_init_range=(0.1, 1.0)):
        self.layer_id = layer_id
        self.num_agents = num_agents
        self.threshold = threshold
        self.weights = np.random.uniform(weight_init_range[0], weight_init_range[1], size=(num_agents, num_agents))  # Random initial weights
        self.potential = np.zeros(num_agents)  # Initial potentials are 0
        self.spike_times = np.zeros(num_agents)  # Track spike times for STDP learning

    def process_input(self, input_data):
        # Update potential with incoming signals based on current weights
        self.potential += np.dot(self.weights, input_data)
    
    def check_spike(self):
        # Check which agents spike (potential exceeds threshold)
        spikes = self.potential >= self.threshold
        self.potential[spikes] = 0  # Reset potential after spike
        return spikes

    def learn(self, spikes, learning_rate=0.01):
        # Learning based on Hebbian learning rule
        for i in range(self.num_agents):
            if spikes[i]:
                for j in range(self.num_agents):
                    if self.potential[j] > 0:  # Only adjust if the other agent has fired
                        self.weights[i][j] += learning_rate * self.potential[i] * self.potential[j]
        
    def update_spike_times(self, spikes):
        # Store the spike times for STDP (optional for advanced models)
        self.spike_times += spikes.astype(int)

# Create the layers of agents
def create_network(layers=5, agents_per_layer=80):
    network = []
    for i in range(layers):
        layer = Agent(layer_id=i, num_agents=agents_per_layer)
        network.append(layer)
    return network

# Define the forward pass through the network
def forward_pass(network, input_data):
    for layer in network:
        layer.process_input(input_data)
        spikes = layer.check_spike()
        layer.learn(spikes)
        layer.update_spike_times(spikes)
        input_data = spikes  # Output of this layer is input to the next
    return input_data

# Initialize the network
network = create_network(layers=5, agents_per_layer=80)

# Example input: 400 nodes with random activation levels
input_data = np.random.rand(80)

# Run the network for 10 iterations
for epoch in range(10):
    print(f"Epoch {epoch + 1}")
    output = forward_pass(network, input_data)
    print(f"Output (last layer spikes): {output}")
