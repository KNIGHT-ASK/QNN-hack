# CRITICAL ISSUE: Walsh Decomposition Applied to Non-Diagonal Matrix

## Problem

The current implementation in `qnn_model.py` (lines 120-145) attempts to use `build_optimal_walsh_circuit()` on the transformation matrix V, but **Walsh decomposition only works for DIAGONAL matrices**.

## Current Code (INCORRECT):
```python
# Step 3: Diagonalize U = V @ D @ V†
diag_matrix, transform_matrix = diagonalize_unitary(density_matrix)

# Step 4a: Apply V (transformation to diagonal basis)
# BUG: transform_matrix (V) is NOT diagonal, but Walsh expects diagonal!
transform_circuit = build_optimal_walsh_circuit(torch.tensor(transform_matrix, dtype=torch.complex64))
```

## Why This Fails

1. `diagonalize_unitary()` returns:
   - `D`: diagonal matrix (eigenvalues)
   - `V`: transformation matrix (eigenvectors) - **NOT DIAGONAL**

2. `build_optimal_walsh_circuit()` requires:
   - Input: **DIAGONAL** unitary matrix
   - Output: CNOT + RZ gates that implement the diagonal unitary

3. When we pass non-diagonal V to Walsh decomposition:
   - It extracts the diagonal: `d = np.diag(V)`
   - This loses all off-diagonal information!
   - Reconstruction fails with huge error (1.83 vs expected < 1e-6)

## Test Results

From `test_decomposition.py`:
```
Max absolute difference: 1.83e+00  (HUGE ERROR!)
Relative error: 1.83e+00
```

This confirms V is not being compiled correctly.

## Solution Options

### Option 1: Use Different Decomposition for V (RECOMMENDED)
Instead of Walsh, use a proper unitary decomposition like:
- **Cosine-Sine Decomposition (CSD)**
- **Quantum Shannon Decomposition (QSD)**  
- **Solovay-Kitaev algorithm**

These can decompose ANY unitary (not just diagonal) into gates.

### Option 2: Use Only Diagonal Unitaries (SIMPLER)
Modify the density matrix approach to ensure U is already diagonal:
- Don't use general RBS networks
- Use only diagonal transformations
- Simpler but less expressive

### Option 3: Use PennyLane's Built-in Decomposition
```python
import pennylane as qml

# Let PennyLane decompose V automatically
qml.QubitUnitary(transform_matrix, wires=range(num_qubits))
```

This works but doesn't give us control over gate types.

## What Needs to Be Done

1. **Choose a decomposition method** for non-diagonal unitaries
2. **Implement the decomposition** (or use library)
3. **Test reconstruction**: U_reconstructed ≈ U_original (error < 1e-6)
4. **Update qnn_model.py** to use correct decomposition
5. **Verify end-to-end**: Full QNN training works

## References

- Cosine-Sine Decomposition: https://arxiv.org/abs/quant-ph/0406176
- Quantum Shannon Decomposition: https://arxiv.org/abs/quant-ph/0406176  
- PennyLane decompositions: https://docs.pennylane.ai/en/stable/code/qml_transforms.html

## Priority

**CRITICAL** - This blocks the entire density QNN approach from working correctly.

## Teammate Feedback

> "Test the U = VDV^dag part, alone, by first doing U -> decomp -> RX,CNOTs -> then use matrix multiplication to go back into U, make sure the starting and ending U are not too different."

Current test shows they ARE very different (error = 1.83), confirming this issue.

---

## For Next AI Agent

Please implement a proper unitary decomposition that works for non-diagonal matrices. The Walsh decomposition is correct for D (diagonal part) but we need a different method for V (transformation matrix).

Test your solution with `test_decomposition.py` - the reconstruction error should be < 1e-6.
