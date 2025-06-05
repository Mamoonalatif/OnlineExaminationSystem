# 🐼 PandaProctor-Online-examination-system
PandaProctor is a secure client-server online examination platform featuring AI-powered face detection, user authentication, and real-time monitoring. Designed for both students and educators, it ensures academic integrity during assessments while providing a streamlined quiz management system.

## 📖 Overview
PandaProctor is an online examination platform with:
- **Role-based access** (Admin/Student)
- **AI face detection** during exams
- **Real-time question management**
- **Performance analytics dashboard**
- **Secure TCP-based client-server architecture**

## ✨ Key Features
### 👨‍🏫 Admin Portal
- Create/edit/delete questions with metadata (difficulty, concept, course)
- Track student performance through visual analytics
- Manage multiple courses (DSA, OOP, PF)

### 🎓 Student Experience
- Secure login with face verification during exams
- Course-specific quizzes with instant feedback
- Progress tracking dashboard

### 🔒 Security
- Facial presence monitoring during exams
- Encrypted client-server communication
- Role-based authentication system

## ⚙️ Tech Stack
| Component       | Technologies                          |
|-----------------|---------------------------------------|
| **Frontend**    | Streamlit, Matplotlib, PIL            |
| **Backend**     | Python (Socket, Threading)            |
| **Face Auth**   | OpenCV, Flask, Haarcascade Classifier |
| **Data**        | Pandas, JSON                          |

## 🚀 Installation
1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/pandaproctor.git
   cd pandaproctor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download Haar Cascade file:
   ```bash
   wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
   ```

## 🖥️ Usage
1. Start the **backend server**:
   ```bash
   python server.py
   ```

2. Start the **face detection service**:
   ```bash
   python face.py
   ```

3. Launch the **main application**:
   ```bash
   streamlit run main.py
   ```

## 📂 Project Structure
```
pandaproctor/
├── main.py            # Streamlit frontend
├── server.py          # TCP question/score server
├── face.py            # Face detection service
├── haarcascade_frontalface_default.xml
├── Admin.txt
├── questions.csv
├── student_scores.csv
└── Student.txt        # Student credentials
```

### Project Description  
**PandaProctor** addresses the growing need for reliable online examination systems with these core capabilities:

1. **Dual User System**  
   - *Admins*: Create/manage questions with metadata tagging (difficulty, course, concept)  
   - *Students*: Take proctored exams with real-time face verification  

2. **Anti-Cheating Protections**  
   - Continuous facial presence detection using OpenCV  
   - Webcam monitoring throughout the examination  

3. **Data Management**  
   - TCP server handles all data operations  
   - Persistent storage of questions/scores in CSV format  
   - Real-time synchronization between components  

4. **Analytics & Reporting**  
   - Visual score distribution charts  
   - Performance tracking per student/course  
   - Exportable result data  

5. **Intuitive UI**  
   - Streamlit-based responsive interface  
   - Course-themed visual design  
   - Interactive dashboards for both roles  

The system uses a microservice architecture where:  
- The **Streamlit frontend** provides the user interface  
- The **TCP server** (server.py) handles data operations  
- The **Flask face service** (face.py) provides proctoring capabilities  


