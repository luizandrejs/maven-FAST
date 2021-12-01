# FAST-parameterized

This repository is a modification of the [FAST Approaches to Scalable Similarity-based Test Case Prioritization](https://github.com/icse18-FAST/FAST) project, it is based on the following publication:

> Breno Miranda, Emilio Cruciani, Roberto Verdecchia, and Antonia Bertolino. 2018. FAST Approaches to Scalable Similarity-based Test Case Prioritization. In *Proceedings of ICSE’18: 40th International Conference on Software Engineering, Gothenburg, Sweden, May 27-June 3, 2018 (ICSE’18)*, 11 pages. DOI: [10.1145/3180155.3180210](http://dx.doi.org/10.1145/3180155.3180210)


It contains materials needed to perform FAST project prioritization for projects developed using Java in conjunction with [Maven](https://maven.apache.org/)


Project Replication
---------------
In order to replicate the project follow these steps:

### Getting started

1. Clone the repository
   - `git clone https://github.com/DinoSaulo/FAST-parameterized`

2. Install the additional python packages required:
   - `pip3 install -r requirements.txt`

### Perform prioritization with different FAST algorithms

1. Execute the `prioritize.py` script
   - `python3 py/prioritize.py <subject> <algorithm>`

      Example: `python3 py/prioritize.py /home/user/projects/truth FAST-pw`

      The `<subject>` is the path to the project, some examples are: '/home/user/projects/truth' or '../my-projects/calculator'

      The possible values for `<algorithm>` are: FAST-pw, FAST-one, FAST-log, FAST-sqrt and FAST-all.

2. View output results stored in folder `<subject>/.fast/output/`

3. Access the project repository

   Example: `cd /home/user/projects/truth`

4. Run the project tests

   - `mvn test`

### Project source code instrumentation (OPTIONAL)
   When running the tests prioritized by the `FASTPrioritizedSuite.java` file, the report generated at runtime of the tests displayed by Maven is no longer displayed due to tool settings.

   To make a workarround it is necessary to instrument the project by adding the file [FASTTestWatcher.java](tools/TestWatcher/FASTTestWatcher.java) to the project and adding the following lines to the project's test classes:

   ```java
      import org.junit.jupiter.api.extension.ExtendWith;
      import fast.FASTTestWatcher;

      ...

      @ExtendWith(FASTTestWatcher.class)
   ```

   #### Adding the instrumentation

   To automatically add instrumentation to the project, just run the command
    - `python3 tools/project-instrumentation.py <subject> add_instrumentation_to_the_project`

   Example: `python3 tools/project-instrumentation.py /home/user/projects/truth add_instrumentation_to_the_project`

   #### Removendo a instrumentação

   To automatically remove instrumentation from the project, just run the command
    - `python3 tools/project-instrumentation.py <subject> remove_instrumentation_from_the_project`

   Example: `python3 tools/project-instrumentation.py /home/user/projects/truth remove_instrumentation_from_the_project`

### Clean preprocessed input files

 1. Run the script `clean-preprocessed-input.py` to clean preprocessed input files for repeating the prioritization in a clean environment.

    - `python3 tools/clean-preprocessed-input.py <subject>`

   Example: `python3 tools/clean-preprocessed-input.py /home/user/projects/truth`


Directory Structure
---------------
This is the root directory of the repository. The directory is structured as follows:

    FAST
     .
     |
     |--- py/            Implementation of the algorithms and scripts to execute the project.
     |
     |--- tools/         Util scripts, e.g. clean environment, project instrumentation.
