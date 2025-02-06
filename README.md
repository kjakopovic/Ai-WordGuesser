# Ai-WordGuesser

## 🚀 About the Project

The AI WordGuesser project is a college experiment aimed at exploring brain activity patterns through EEG signals in response to letters displayed on a screen. Using a PsychoPy interface, this experiment is recorded and stored for every word that user chooses to experiment himself on. The collected data is then processed using CNN to predict which letter the participant is thinking of based on brainwave activity.

## 🔬 Experiment Workflow

### 1. User Interface (PsychoPy)

The first step in the experiment involves the participant interacting with a PsychoPy interface. The user is asked to write in a word that he wants to think of for the experiment. The interface presents 22 letters, one after another, for each letter that is found in a word he entered.

### 2. EEG Data Collection

While the letters are shown on the screen, the EEG data is recorded using a V-AMP system and a program called Recorder. A MyDAQ device is used to convert serial communication to digital signals for the V-AMP to collect the data about the markers. Each letter shown is marked in an EEG at the time it was on the screen. At the end, the EEG data is saved locally in a designated data folder for further processing.

### 3. Data Processing an AI Model

After recording the EEG data, the focus shifts to data manipulation. Previously, a script calculated the total power for each character's EEG response to identify the strongest stimulus. However, due to time constraints at the end of the semester, the AI model was trained using a simpler approach. Instead of relying on power calculations, the model was fed with the EEG data associated with each timestamp and the corresponding label (the character displayed on the screen).

The model was tasked with predicting the label shown based on the EEG data (features) at each timestamp. While this approach yielded suboptimal results, there was a clear trend: the validation loss decreased over time, indicating that with more data, the model could potentially improve its accuracy.

## 📊 Results & Future Work

The results from the initial model were not as promising as anticipated. The performance was poor, but there was a noticeable improvement in validation loss over time. Given that the dataset was relatively small and if total power would be introduced, it is hypothesized that with more data, the model could produce more accurate predictions.

### Future Improvements:

- **Data Expansion**: Collecting a larger dataset could significantly improve the model’s ability to generalize and make accurate predictions.
- **Feature Engineering**: Exploring alternative ways to extract features from EEG data, such as analyzing power spectral densities or incorporating temporal dynamics, could improve model performance.

## ⚙️ Installation and Setup

To run the experiment and process the data, ensure the following dependencies are installed:

- **PsychoPy** (for the user interface)
- **MyDAQ** drivers and software
- **V-AMP** system setup for EEG recording
- **Python Libraries:**
  - numpy
  - pandas
  - scikit-learn
  - TensorFlow (or other relevant libraries)

## 📙 Structure Explanation

### Docs
All the documents used for developing the hardware and software components can be found in the `docs` folder.

### Data
The data collected during the experiment is stored in the `data` folder. 
The word used in the experiment is part of the filename. For example: `app.vhdr`.

### Old
This folder contains older scripts that were used previously but are no longer necessary for the current process. 
It includes a script where we attempted to calculate the total power across words.

### Scripts
This folder contains scripts that were used in the process

`mydaq.py` has the fully updated code that transmits letters trough serial communication (USB port) into mydaq which it transfers it out trough it's digital ports

`psychopy_script.py` is the script that was used as an UI for our experiment and that connects the first part of the project together

`read_markers.py` is the basic code that is needed to read data from eeg files with mne library

### Utils
This folder contains basic utils funcitons that were needed for data manipulation and ai model training
It also contains `marker_utils.py` which contains all the mappings between characters and integers

## 📧 Contact

[![LinkedIn KJ badge](https://img.shields.io/badge/LinkedIn-kjakopovic-%230A66C2?logo=linkedin&logoColor=white&labelColor=gray)](https://www.linkedin.com/in/karlo-jakopovi%C4%87-24595027a/)
[![LinkedIn Majki badge](https://img.shields.io/badge/LinkedIn-majki-%230A66C2?logo=linkedin&logoColor=white&labelColor=gray)](https://www.linkedin.com/in/marin-mikulec-26b0a829b/)
[![LinkedIn MBrodarac badge](https://img.shields.io/badge/LinkedIn-mbrodarac-196CBF)](https://www.linkedin.com/in/matej-brodarac-b866562ba/)
[![LinkedIn MGolub badge](https://img.shields.io/badge/LinkedIn-mgolub-196CBF)](https://www.linkedin.com/in/matej-golub-70a837235/)

Mentored by v. asist. dr. sc. Ivan Markovinović from RiTeh
