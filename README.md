
# 🌿 Green Energy Dashboard – AWS Deployment

An interactive data visualization platform built with **Streamlit** to analyze renewable energy trends. This project showcases the full lifecycle of a data application, from local development to cloud deployment on **AWS EC2**.

### 🔗 Quick Links

* **Live Demo:** [View Dashboard](http://3.88.140.192:8501)
* **Repository:** [GitHub Source](https://github.com/Akshita1395/green-energy-dashboard-aws-deployment)

---

## 📖 Description

The **Green Energy Dashboard** provides a user-friendly interface to explore and visualize complex renewable energy datasets. By leveraging Python’s powerful data ecosystem, it transforms raw data into actionable insights through dynamic charts and filters.

## 🛠️ Technologies Used

* **Frontend/App Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Visualization:** [Plotly](https://plotly.com/)
* **Cloud Hosting:** [AWS EC2](https://aws.amazon.com/ec2/) (Ubuntu Instance)
* **Version Control:** Git & GitHub

## 🚀 Deployment Steps

To deploy this dashboard on an AWS EC2 instance, follow these steps:

1. **Provision Instance:** Launch an **Ubuntu** EC2 instance via the AWS Management Console.
2. **Network Configuration:** Edit Security Group rules to allow:
* **Port 22:** For SSH access.
* **Port 8501:** The default port for Streamlit applications.


3. **Environment Setup:** Update the package manager and install dependencies:
```bash
sudo apt update
sudo apt install python3-pip git

```


4. **Clone & Install:**
```bash
git clone https://github.com/Akshita1395/green-energy-dashboard-aws-deployment.git
cd green-energy-dashboard-aws-deployment
pip install -r requirements.txt

```


5. **Launch:** Run the application using the Streamlit CLI:
```bash
streamlit run app.py

```



## 📸 Screenshots

You can find visual walkthroughs of the deployment process and the final dashboard interface in the [`/screenshots`](https://www.google.com/search?q=%5Bhttps://github.com/Akshita1395/green-energy-dashboard-aws-deployment%5D(https://github.com/Akshita1395/green-energy-dashboard-aws-deployment)) folder.

---

## 👤 Author

**Akshita**
[GitHub Profile](https://github.com/Akshita1395)

---
