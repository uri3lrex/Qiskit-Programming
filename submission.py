"""
QIS-NET Project 1 — Qiskit Foundations: Build, Validate, Design
Student: HERA KHAN   ID: 22312194

Implement the six functions below. Do NOT rename them, change signatures,
print, read/write files, or import anything beyond qiskit / qiskit_aer / numpy.
AI-use declaration (per module policy): <state tool & extent, or "none">
"""

import qiskit
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
import numpy as np

# Safetyy??: if qiskit_aer isn't installed, it shouldn't crash the file
try:
    from qiskit_aer import AerSimulator
    import qiskit_aer
    aer_available = True
except ImportError:
    aer_available = False

student_id = "22312194"


def environment_check() -> dict:
    """T1: return environment info. See specification."""
    return {
        "qiskit_version": qiskit.__version__,
        "aer_available": aer_available,
        "student_id": student_id
    }


def bell_state() -> QuantumCircuit:
    """T2: return a 2-qubit circuit preparing |Phi+> = (|00>+|11>)/sqrt(2).
    No measurements."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def ghz_circuit(n: int) -> QuantumCircuit:
    """T3: return an n-qubit circuit preparing the GHZ state
    (|0...0> + |1...1>)/sqrt(2). No measurements. Depth <= n+1."""
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n-1): #forgot range and out of bounds error
      qc.cx(i,i+1)
    return qc


def teleport_circuit(theta: float, phi: float) -> QuantumCircuit:
    """T4: 3 qubits + 2 classical bits.
    - Prepare Ry(theta) Rz(phi) |0> on qubit 0.
    - Create an ebit on qubits 1-2.
    - Bell-measure qubits 0-1 into the classical bits.
    - Apply classically-conditioned X and Z corrections on qubit 2.
    No gates after the measurements other than the conditioned corrections.
    """

    # set up the classical and qubit registers
    qr = QuantumRegister(3,name="q")
    cr = ClassicalRegister(2, name="c")
    qc = QuantumCircuit(qr,cr)

    # prepare the states of qc

    qc.ry(theta,0)
    qc.rz(phi,0)

    # create ebit -> entangled bit
    qc.h(1)
    qc.cx(1,2)

    # apply bell measure on classical bits
    qc.cx(0,1)
    qc.h(0)

    #classical conditioned corrections on qubits??
    qc.measure(0,0)
    qc.measure(1,1)

    #check the values
    #if classical bit 1 is set, turn qubit 2 with X
    if qc.if_test((cr[1],1)):
      qc.x(2)
    #if classical bit 0 is set, turn qubit 2 with Z
    if qc.if_test((cr[1],0)):
      qc.z(2)

    return qc
    # TODO
    raise NotImplementedError


def repetition_logical_error_rate(p_phys: float, shots: int) -> float:
    """T5: simulate the 3-qubit bit-flip repetition code protecting logical |0>
    under a bit-flip noise model with per-qubit flip probability p_phys
    applied after encoding. Decode with majority-vote syndrome correction.
    Return the logical error rate over `shots` shots with seed_simulator=42.
    Must use qiskit_aer."""

    from qiskit import transpile
    from qiskit_aer.noise import NoiseModel, pauli_error

    qc = QuantumCircuit(3, 3)  # 3 qubits, 3 classical bits for logical measurement

    # create a bit flip error model
    error = pauli_error([('X', p_phys), ('I', 1 - p_phys)])
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ['id'])  # apply to identity gates

    # apply a noisy identity gate to each qubit after encoding
    for q in range(3):
        qc.id(q)

    # apply majority vote decoding and measure the logical qubit
    qc.measure([0, 1, 2], [0,1,2])  # measure all qubits into classical bits

    # run simulator with noise model and return logical error rate
    #sim = AerSimulator(method="statevector", seed_simulator=42) <- not working, noisiness is not being applied
    sim = AerSimulator(method="density_matrix", seed_simulator=42)

    compiled_circuit = transpile(qc, sim, optimization_level=0)
    counts = sim.run(compiled_circuit, shots=shots, noise_model=noise_model).result().get_counts()

    # decode by majority vote and calculate logical error rate
    logical_errors = 0

    for outcome, count in counts.items():
        # majority vote decoding
        if outcome.count('1') > 1:  # more than one '1' means logical error
            logical_errors += count

    logical_error_rate = logical_errors / shots
    return logical_error_rate


    # TODO
    raise NotImplementedError


def design_challenge() -> QuantumCircuit:
    """T6: 3-qubit circuit preparing |W> = (|001>+|010>+|100>)/sqrt(3)
    with at most 8 gates. No measurements."""

    qc = QuantumCircuit(3)
    #rotate qubit 0 to create superposition
    x = 1/np.sqrt(3)
    theta = 2 * np.acos(x)
    qc.ry(theta, 0)
    #controlled hadamard gate on qubit 1 controlled by qubit 0
    qc.ch(0, 1)
    #apply CNOT gates to create the W state
    qc.cx(1, 2)
    qc.cx(0, 2)
    #flip qubit 0 to ensure correct state
    qc.x(0)
    return qc


    # TODO
    raise NotImplementedError
