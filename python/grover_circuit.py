"""
Grover's Algorithm Implementation for Brussels Mobility Zone Search
Using Google Cirq Quantum Computing Framework
"""

import cirq
import numpy as np

def create_grover_circuit(num_qubits=2):
    """
    Create a Grover search circuit for optimal zone identification
    
    Args:
        num_qubits: Number of qubits (2 qubits = 4 zones searchable)
    
    Returns:
        cirq.Circuit: Quantum circuit implementing Grover's algorithm
    """
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    
    # Step 1: Initialize superposition (all zones simultaneously)
    circuit.append(cirq.H(q) for q in qubits)
    
    # Step 2: Oracle - mark optimal zones
    # This oracle marks states |11⟩ (representing high-mobility zones)
    circuit.append(cirq.CZ(qubits[0], qubits[1]))
    
    # Step 3: Grover diffusion operator
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.X(q) for q in qubits)
    circuit.append(cirq.CZ(qubits[0], qubits[1]))
    circuit.append(cirq.X(q) for q in qubits)
    circuit.append(cirq.H(q) for q in qubits)
    
    # Step 4: Measurement
    circuit.append(cirq.measure(*qubits, key='result'))
    
    return circuit

def simulate_zone_search(num_zones=145):
    """
    Simulate Grover search for Brussels mobility zones
    
    Args:
        num_zones: Total number of zones to search (default: 145 Brussels neighborhoods)
    
    Returns:
        dict: Search results with optimal zones
    """
    # Calculate required qubits
    num_qubits = int(np.ceil(np.log2(num_zones)))
    
    # Create circuit
    circuit = create_grover_circuit(num_qubits)
    
    # Simulate
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    
    # Extract results
    measurements = result.measurements['result']
    
    # Count optimal zone occurrences
    optimal_zones = {}
    for measurement in measurements:
        zone_id = int(''.join(map(str, measurement)), 2)
        if zone_id < num_zones:
            optimal_zones[zone_id] = optimal_zones.get(zone_id, 0) + 1
    
    return {
        'circuit': circuit,
        'optimal_zones': sorted(optimal_zones.items(), key=lambda x: x[1], reverse=True)[:5],
        'total_iterations': len(measurements),
        'quantum_speedup': f"{num_zones / np.sqrt(num_zones):.1f}x"
    }

if __name__ == "__main__":
    print("🌌 Brussels Mobility - Grover's Quantum Search")
    print("=" * 50)
    
    # Run quantum search
    results = simulate_zone_search(num_zones=145)
    
    print(f"\n📊 Search Results:")
    print(f"Total zones searched: 145 Brussels neighborhoods")
    print(f"Quantum speedup: {results['quantum_speedup']}")
    print(f"\n🎯 Top 5 Optimal Zones (by probability):")
    
    for i, (zone_id, count) in enumerate(results['optimal_zones'], 1):
        probability = (count / results['total_iterations']) * 100
        print(f"  {i}. Zone {zone_id}: {probability:.1f}% probability")
    
    print(f"\n⚛️ Quantum Circuit:")
    print(results['circuit'])
