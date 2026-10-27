# Qiskit-Programming

Solutions for **QIS-NET Project 1: Qiskit Foundations (Build, Validate, Design)**,
a set of six Qiskit tasks covering state preparation, teleportation, error correction
and circuit design, plus the autograder used to score them locally.

## Contents

| File | Description |
|------|-------------|
| `submission.py` | The six task implementations |
| `grade_project1.py` | Deterministic autograder (100 points) |
| `results.json` | Output of the most recent grader run |
| `src/qiskit_programming/` | Package source directory |

## Tasks

| Task | Function | Description |
|------|----------|-------------|
| T1 | `environment_check()` | Reports Qiskit version, Aer availability and student ID |
| T2 | `bell_state()` | 2-qubit circuit preparing \|Φ+⟩ = (\|00⟩ + \|11⟩)/√2 |
| T3 | `ghz_circuit(n)` | n-qubit GHZ state with depth ≤ n+1 |
| T4 | `teleport_circuit(theta, phi)` | Teleports Rz(φ)Ry(θ)\|0⟩ from qubit 0 to qubit 2 using classically-conditioned X/Z corrections |
| T5 | `repetition_logical_error_rate(p_phys, shots)` | Simulates the 3-qubit bit-flip repetition code under Pauli-X noise (Aer, `seed_simulator=42`), decoded by majority vote |
| T6 | `design_challenge()` | 3-qubit W state (\|001⟩ + \|010⟩ + \|100⟩)/√3 in at most 8 gates |

## Requirements

- Python 3.10+
- `qiskit`
- `qiskit-aer`
- `numpy`

```bash
pip install qiskit qiskit-aer numpy
```

## Usage

Run the autograder against the submission:

```bash
python3 grade_project1.py submission.py
```

Optional flags:

```bash
python3 grade_project1.py submission.py --json results.json --csv grades.csv --username <name>
```

The grader prints a per-test breakdown and writes a Submitty-style JSON report
(and optionally a one-row CSV for Blackboard import).

## How grading works

| Task | Points | Check |
|------|--------|-------|
| T1 | 10 | Correct keys/types, `aer_available` is `True` |
| T2 | 20 | Statevector fidelity to \|Φ+⟩ |
| T3 | 15 | Fidelity for n = 2, 3, 5, 8, plus a depth bound |
| T4 | 25 | Teleportation fidelity over four (θ, φ) pairs, plus structural checks |
| T5 | 20 | Logical error rate vs. theory 3p²(1−p) + p³
