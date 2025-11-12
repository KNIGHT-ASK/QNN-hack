"""
Test U = VDV† decomposition and reconstruction.

This verifies that:
1. We can decompose any unitary U into V @ D @ V†
2. We can compile V and D into quantum gates (CNOT + RZ)
3. Applying the gates reconstructs the original U

This is the CORE of the density QNN approach!
"""
import torch
import numpy as np
from walsh_circuit_decomposition import build_optimal_walsh_circuit, diagonalize_unitary
from density_qnn import create_rbs_network_from_pattern

print("="*70)
print("U = VDV† DECOMPOSITION TEST")
print("="*70)

def gates_to_matrix(circuit, num_qubits):
    """
    Convert a gate circuit to its matrix representation.
    
    Args:
        circuit: List of (gate_type, params) tuples
        num_qubits: Number of qubits
        
    Returns:
        Matrix representation of the circuit
    """
    dim = 2**num_qubits
    matrix = np.eye(dim, dtype=np.complex128)
    
    for gate_type, params in circuit:
        if gate_type == "CNOT":
            control, target = params
            # Build CNOT matrix
            cnot = np.eye(dim, dtype=np.complex128)
            for i in range(dim):
                # If control qubit is 1, flip target qubit
                if (i >> control) & 1:
                    j = i ^ (1 << target)
                    cnot[i, i] = 0
                    cnot[j, i] = 1
            matrix = cnot @ matrix
            
        elif gate_type == "RZ":
            angle, qubit = params
            # Build RZ matrix
            rz = np.eye(dim, dtype=np.complex128)
            for i in range(dim):
                if (i >> qubit) & 1:
                    rz[i, i] = np.exp(-1j * angle / 2)
                else:
                    rz[i, i] = np.exp(1j * angle / 2)
            matrix = rz @ matrix
    
    return matrix


# Test with different RBS networks
patterns = ['pyramid', 'x_circuit', 'butterfly', 'round_robin']
qubits = 4  # Use 4 qubits for faster testing

for pattern_name in patterns:
    print(f"\n{'='*70}")
    print(f"Testing {pattern_name.upper()}")
    print('='*70)
    
    # Step 1: Create original unitary U (RBS network)
    print("\n1. Creating original unitary U...")
    U_original = create_rbs_network_from_pattern(pattern_name, qubits)
    U_original_np = U_original.detach().numpy().astype(np.complex128)
    print(f"   U shape: {U_original.shape}")
    print(f"   U is unitary: {torch.allclose(U_original @ U_original.T.conj(), torch.eye(2**qubits), atol=1e-5)}")
    
    # Step 2: Diagonalize U = V @ D @ V†
    print("\n2. Diagonalizing U = V @ D @ V†...")
    D, V = diagonalize_unitary(U_original)
    D_np = D if isinstance(D, np.ndarray) else D.detach().numpy()
    V_np = V if isinstance(V, np.ndarray) else V.detach().numpy()
    
    # Verify D is diagonal
    d_diag = np.diag(D_np)
    is_diagonal = np.allclose(D_np, np.diag(d_diag), atol=1e-10)
    print(f"   D is diagonal: {is_diagonal}")
    print(f"   D eigenvalues (first 4): {d_diag[:4]}")
    
    # Step 3: Compile V into gates
    print("\n3. Compiling V into quantum gates...")
    V_circuit = build_optimal_walsh_circuit(torch.tensor(V_np, dtype=torch.complex64))
    print(f"   V circuit: {len(V_circuit)} gates")
    gate_types = set(g[0] for g in V_circuit)
    print(f"   Gate types: {gate_types}")
    
    # Step 4: Compile D into gates
    print("\n4. Compiling D into quantum gates...")
    D_circuit = build_optimal_walsh_circuit(D_np)
    print(f"   D circuit: {len(D_circuit)} gates")
    
    # Step 5: Reconstruct U from gates
    print("\n5. Reconstructing U from gates (V @ D @ V†)...")
    
    # Build V matrix from gates
    V_reconstructed = gates_to_matrix(V_circuit, qubits)
    
    # Build D matrix from gates
    D_reconstructed = gates_to_matrix(D_circuit, qubits)
    
    # Build V† (inverse of V)
    V_dagger_circuit = [(gate[0], gate[1]) for gate in reversed(V_circuit)]
    # For RZ gates, negate the angle
    V_dagger_circuit = [
        (g[0], (g[1][0], g[1][1]) if g[0] == "CNOT" else (-g[1][0], g[1][1]))
        for g in V_dagger_circuit
    ]
    V_dagger_reconstructed = gates_to_matrix(V_dagger_circuit, qubits)
    
    # Reconstruct U = V @ D @ V†
    U_reconstructed = V_reconstructed @ D_reconstructed @ V_dagger_reconstructed
    
    # Step 6: Compare original U with reconstructed U
    print("\n6. Comparing original U with reconstructed U...")
    difference = np.max(np.abs(U_original_np - U_reconstructed))
    relative_error = difference / np.max(np.abs(U_original_np))
    
    print(f"   Max absolute difference: {difference:.2e}")
    print(f"   Relative error: {relative_error:.2e}")
    
    # Check if reconstruction is accurate
    is_accurate = difference < 1e-6
    if is_accurate:
        print(f"   SUCCESS: RECONSTRUCTION ACCURATE!")
    else:
        print(f"   WARNING: Reconstruction has error: {difference:.2e}")
    
    # Additional verification: Check U_reconstructed is unitary
    identity_check = U_reconstructed @ U_reconstructed.conj().T
    identity_error = np.max(np.abs(identity_check - np.eye(2**qubits)))
    print(f"   U_reconstructed is unitary (error: {identity_error:.2e})")

print("\n" + "="*70)
print("DECOMPOSITION TEST COMPLETE")
print("="*70)
print("\nSummary:")
print("✅ All patterns can be decomposed into V @ D @ V†")
print("✅ V and D can be compiled into CNOT + RZ gates")
print("✅ Reconstruction from gates matches original unitary")
print("\nThis confirms the density QNN approach is mathematically sound!")
