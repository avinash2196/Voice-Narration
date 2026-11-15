# Enrollment evaluator prerequisites

Use CPython 3.13.17 x64 and the existing developer harness. General setup remains
in developer-setup.md. The additional manifest installs only the reviewed
webrtcvad-wheels 2.0.14.post1 binary; it does not install dev extras or weights.
Supported prerequisite targets are Windows x64 and Linux glibc x86_64.
Do not fall back to a source build, another detector or another wheel hash.

After approval of initial-build Implementation Plan 009, from the repository root:

    .\.venv\Scripts\python.exe -m pip install --no-deps --only-binary=:all: --require-hashes -r requirements-evaluator.txt
    .\.venv\Scripts\python.exe -m pip check
    .\.venv\Scripts\python.exe tools/evaluator_readiness.py
    .\.venv\Scripts\python.exe tools/evaluator_readiness.py

For an already prepared Linux general harness, use its selected Python interpreter:

    python -m pip install --no-deps --only-binary=:all: --require-hashes -r requirements-evaluator.txt
    python -m pip check
    python tools/evaluator_readiness.py
    python tools/evaluator_readiness.py

The existing dependency Dockerfile also installs this manifest. Run the probe
with the existing image and network disabled, mounting only the probe read-only;
exact Windows/Linux command forms and evidence gates are in Implementation Plan009.
No application, database schema, enrollment setting or calibration is created.

Retain the complete installed distribution LICENSE when redistributing the wheel
or a derived image. It contains MIT wrapper and native WebRTC BSD3 notices,
including copyright, conditions, disclaimer and non-endorsement restriction.
PyPI's short MIT label does not replace the native notice.

The source release tree does not include PATENTS/AUTHORS, although native headers
refer to them. The exact reviewed source identity, official upstream notice
references, package/wheel hashes and limits of the evidence are recorded in
docs/.ai/initial-build/009_Implementation_Plan_Enrollment_Evaluator_Prerequisites.md.
They are provenance records, not model commercial clearance or patent guarantees.
Keep the packaged LICENSE; report missing or changed notices rather than silently
substituting another distribution. No extra runtime Python dependencies are
declared without the dev extra. Native/system libraries still require actual
successful import and invocation on each supported target.

The probe reports versions, installed-file hashes, FFmpeg library identities and
deterministic synthetic nonvoice results. It denies Python socket operations and
accepts no private recording input. Linux container execution adds network
isolation. No result measures speech quality, language performance, acoustic
threshold correctness, calibration or production readiness. Enrollment remains
subject to its separate reviewed RED/GREEN and calibration milestones.
