# Evaluation - Tests
This directory contains the test suite for the project. The tests are organized into several files:

- **e2e_test.py:** This file contains end-to-end tests for the entire pipeline, from audio to pitch estimation to MIDI generation. It uses sample audio and MIDI files from the Datasets directory for testing.

- **evaluation.py:** This module contains functions for evaluating the performance of the system, such as comparing MIDI files and assessing pitch accuracy.

- **midi2pitch.py:** This module provides functionality for converting MIDI files to pitch annotations and vice versa.

- **visualizations.py:** This module contains functions for visualizing evaluation results, such as plots of F0 curves and MIDI note comparisons.

- **outputs:** This directory is intended for storing output files generated during testing.

- **Datasets:** This directory contains sample audio and MIDI files used for testing purposes.

# Running Tests
To run the test suite, execute the e2e_test.py file using Python:

```python
python tests/e2e_test.py
