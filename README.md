# Video-Based Traffic Analysis for Capacity Reduction Due to Roadside Friction

A computer vision-based traffic monitoring system that analyzes road videos to detect, classify, track, and count vehicles, estimate vehicle speeds, and identify traffic violations such as wrong-way driving and illegal parking. The project aims to analyze how roadside friction affects traffic flow and road capacity.

## 1. Project Overview

Traffic congestion is increasing due to roadside activities such as illegal parking, street vending, unauthorized stopping, and vehicles moving in the wrong direction. These activities can reduce the effective road width, disturb vehicle movement, and decrease road capacity.

This project develops a video-based traffic analysis system using computer vision and deep learning. It processes recorded traffic videos to detect and classify vehicles, count traffic volume, estimate vehicle speeds, and analyze vehicle movements to identify potential traffic violations and roadside friction.

The system aims to provide useful traffic statistics and insights that can support congestion analysis, road capacity assessment, and improved traffic management.

## 2. Objectives

* Develop a vehicle detection and classification system using YOLOv8.
* Count vehicles passing through a predefined Region of Interest (ROI).
* Track vehicle movements across consecutive video frames.
* Estimate vehicle speeds using video-based tracking.
* Identify wrong-way driving using vehicle trajectory analysis.
* Detect stationary vehicles that may indicate illegal parking.
* Analyze traffic conditions and assess the effects of roadside friction on road capacity.

## 3. Technologies Used

| Technology      | Purpose                                    |
| --------------- | ------------------------------------------ |
| Python          | Main programming language                  |
| YOLOv8          | Vehicle detection and classification       |
| ByteTrack       | Multi-object tracking across video frames  |
| OpenCV          | Video processing and frame analysis        |
| NumPy           | Numerical calculations and data processing |
| Computer Vision | Vehicle movement and traffic analysis      |
| Deep Learning   | Automated object detection                 |

## 4. Key Features

### Vehicle Detection and Classification

Detects vehicles in traffic videos and classifies them into supported categories, such as cars, motorcycles, buses, trucks, and auto-rickshaws.

### Vehicle Counting

Counts detected vehicles within a predefined Region of Interest (ROI) to analyze traffic volume.

### Vehicle Tracking

Uses ByteTrack to maintain vehicle identities across consecutive frames and analyze movement trajectories.

### Speed Estimation

Estimates vehicle speeds based on their movement across video frames. Accuracy depends on frame rate, camera calibration, and scene conditions.

### Wrong-Way Driving Detection

Analyzes vehicle trajectories to identify vehicles moving against the expected direction of traffic.

### Illegal Parking Detection

Monitors stationary vehicles over a specified period to identify potential parking violations. Reliable identification requires suitable parking-zone definitions and scene configuration.

### Traffic Analysis

Displays vehicle counts and other available traffic statistics to help understand traffic flow and congestion patterns.

## 5. Project Workflow

1. Input a recorded traffic video.
2. Extract and process video frames using OpenCV.
3. Detect and classify vehicles using YOLOv8.
4. Track detected vehicles using ByteTrack.
5. Count vehicles within the defined ROI.
6. Estimate vehicle speeds from tracked movements.
7. Analyze vehicle trajectories to identify potential wrong-way driving.
8. Monitor stationary vehicles to identify potential illegal parking.
9. Display traffic statistics and detected roadside issues.

## 6. Installation and Setup

### Prerequisites

* Python 3.x
* Git
* pip package manager
* Required Python libraries
* A compatible traffic video for analysis

### Step 1: Clone the Repository

```bash
git clone https://github.com/akashkl001/Video-Based-traffic-Analysis-for-Capacity-Reduction-due-to-Roadside-Friction.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Video-Based-traffic-Analysis-for-Capacity-Reduction-due-to-Roadside-Friction
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

If a `requirements.txt` file is available, install the required libraries:

```bash
pip install -r requirements.txt
```

If the dependency file is not included, install the libraries specified by your project code.

### Step 5: Run the Project

If the main entry-point file is named `main.py`, run:

```bash
python main.py
```

If your project uses a different entry-point filename, execute the appropriate Python file.

### Step 6: Analyze a Traffic Video

Provide a compatible traffic video using the input method configured in the project. The system will process the video and display the supported vehicle detection and traffic analysis results.

## 7. Dataset

The traffic video dataset used for this project is available at the following link:

**[Access the Traffic Video Dataset](https://drive.google.com/file/d/1UpThRqghx9eUW-QhEhWuEwGeu6JZ3PQ0/view?usp=sharing)**

Download the dataset and configure the video input path according to the project implementation.

## 8. Project Scope

The project focuses on video-based traffic monitoring and the analysis of roadside friction that can affect traffic movement and road capacity. It can help identify congestion patterns, measure traffic volume, analyze vehicle speeds, and investigate the effects of roadside disturbances.

The system's performance depends on video resolution, camera angle, lighting conditions, occlusion, frame rate, and available computing resources. Accurate speed estimation and violation detection may also require camera calibration and suitable scene-specific configurations.

## 9. Future Enhancements

* Improve vehicle detection under different lighting and weather conditions.
* Enhance speed estimation through camera calibration.
* Detect additional roadside obstructions and traffic violations.
* Identify parking violations using defined no-parking zones.
* Integrate real-time traffic camera feeds.
* Develop a dashboard for live traffic statistics and visualization.
* Investigate adaptive traffic signal timing based on traffic density.
* Quantify road capacity reduction associated with roadside friction.

## 10. Conclusion

This project presents a computer vision-based approach to traffic monitoring by integrating vehicle detection, classification, tracking, counting, speed estimation, and roadside friction analysis. By extracting meaningful information from traffic videos, the system aims to support congestion assessment, road capacity analysis, and data-driven traffic management.

## 11. Author

**Akash KL**

GitHub: [@akashkl001](https://github.com/akashkl001)
