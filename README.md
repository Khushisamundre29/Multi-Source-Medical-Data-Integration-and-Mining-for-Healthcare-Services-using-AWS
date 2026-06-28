# Multi-Source Medical Data Integration and Mining for Healthcare Services

A cloud-native healthcare platform built using **AWS**, **Python**, and **MySQL** that securely integrates medical data from multiple healthcare sources into a centralized system. The platform enables healthcare professionals to manage patients, appointments, prescriptions, and medical records while maintaining strong privacy and security through **Privacy-Preserving Data Fusion and Mining (PDFM)** techniques.

---

# Project Overview

Healthcare organizations generate massive amounts of data from Electronic Health Records (EHRs), medical imaging systems, laboratory reports, IoT devices, and genetic databases. These datasets often exist in isolated systems, making it difficult to obtain a unified patient view.

This project addresses that challenge by providing a secure cloud-based platform that:

- Integrates medical data from multiple healthcare sources
- Stores healthcare records securely on AWS
- Provides role-based access for different users
- Supports healthcare data analysis and mining
- Protects sensitive patient information using Privacy-Preserving Data Fusion and Mining (PDFM)

---

# Key Features

##  Multi-Source Medical Data Integration

- Electronic Health Records (EHR)
- Medical Imaging Records
- Genetic Information
- Laboratory Reports
- IoT Healthcare Device Data

##  Secure Cloud Storage

- AWS S3 for secure medical document storage
- AWS RDS for structured healthcare data
- Secure access using AWS IAM
- Data encryption at rest and in transit

##  Role-Based Access Control (RBAC)

The platform provides separate portals for:

- Admin
- Doctor
- Patient
- Internet of Health (IoH)

Each user can access only the information relevant to their role.

##  Healthcare Data Mining

- Analyze disease patterns
- Mine healthcare data for insights
- Support medicine recommendations
- Improve clinical decision-making

##  Appointment Management

- Book appointments
- Manage schedules
- Track appointment history
- Doctor-patient coordination

##  Privacy-Preserving Data Fusion and Mining (PDFM)

Securely integrates healthcare data from multiple sources while preserving patient privacy and confidentiality.

---

#  System Modules

##  Admin

- Register and manage doctors
- Register and manage patients
- Manage medicine inventory
- Approve medicine requests
- Monitor appointments
- Oversee the complete healthcare system

---

##  Doctor

- View patient appointments
- Access complete medical history
- Issue prescriptions
- Recommend treatments
- Update patient records

---

##  Patient

- Register and log in
- Book appointments
- View prescriptions
- Access personal medical history
- Track healthcare updates

---

## Internet of Health (IoH)

- Connect external healthcare devices
- Upload real-time health data
- Analyze disease patterns
- Suggest relevant medicines
- Feed integrated healthcare data into the platform

---

#  Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask / Django

## Database

- MySQL
- AWS RDS

## Cloud Services (AWS)

| Service | Purpose |
|----------|---------|
| Amazon S3 | Secure storage of medical records and reports |
| Amazon RDS | Managed relational database |
| AWS Lambda | Serverless event-driven processing |
| AWS Glue | ETL pipeline for integrating healthcare data |
| AWS IAM | Identity and access management |

---

#  Project Architecture

```text
                +-------------------------+
                |   Healthcare Data       |
                +-------------------------+
                  /      |      |      \
                 /       |      |       \
             EHR     Imaging   IoT   Genetic Data
                 \       |      |       /
                  \      |      |      /
                    AWS Glue (ETL)
                           |
                           |
                     Amazon RDS
                           |
                  +----------------+
                  | Python Backend |
                  +----------------+
                           |
       -----------------------------------------
       |             |             |            |
     Admin        Doctor        Patient       IoH
                           |
                      Amazon S3
```

---

#  Security Features

- Role-Based Access Control (RBAC)
- End-to-end encryption
- HTTPS/TLS secure communication
- AWS S3 Server-Side Encryption (SSE)
- AWS IAM permission policies
- Secure authentication
- Privacy-Preserving Data Fusion and Mining (PDFM)

---

#  Database

The platform stores:

- Patient Information
- Doctor Information
- Appointments
- Prescriptions
- Medicine Inventory
- Medical Reports
- IoT Health Data

---

#  Installation

## Prerequisites

- Python 3.8+
- MySQL Server
- AWS Account
- AWS CLI (Optional)

---

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcare-aws.git

cd healthcare-aws
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure the Database

```bash
mysql -u root -p < database.sql
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=yourpassword
DB_NAME=your_database_name 

AWS_ACCESS_KEY_ID=xxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxx
AWS_REGION=ap-south-1
AWS_BUCKET_NAME=your-bucket
```

> **Note:** Never commit your `.env` file or AWS credentials to GitHub. Use AWS Secrets Manager or environment variables in production.

---

## 5. Run the Application

```bash
python app.py
```

The application will run on:

```text
http://localhost:5000
```

---

#  UML Diagrams

The project includes the following UML diagrams:

- Use Case Diagram
- Class Diagram
- Activity Diagram
- Collaboration Diagram
- Deployment Diagram

These diagrams illustrate the overall system architecture, workflows, object relationships, and cloud deployment.

---

#  Future Enhancements

- AI-powered disease prediction
- Machine Learning for healthcare analytics
- HL7/FHIR interoperability
- Wearable device integration
- Audit logging and compliance dashboard
- Real-time health monitoring
- Microservices architecture
- Docker & Kubernetes deployment

---

#  Recognition

** 1st Place – SPARK 2024 National Level Project Competition**

This project was recognized for its innovative implementation of secure cloud computing and healthcare data integration using AWS.

---

#  Author

**Khushi Samundre**
