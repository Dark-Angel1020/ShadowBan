# 🚫 ShadowBan

Welcome to ShadowBan, a Python-based utility for searching, managing, and editing IP address allocations stored in  MySQL database.

## 📌 Features
- 🔎 **Search IP**: Find the country of an IP address from the database.
- 🌍 **List Ranges by Country**: Display all IP ranges allocated to a specific country.
- ➕ **Add IP Range**: Insert a new range of IPs.
- 🖥️ **Add Single IP**: Add a single IP to the database.
- ✏️ **Edit IP Range**: Modify an existing IP range.
- ❌ **Delete IP Range**: Remove an IP range from the database.

## 📂 Repository Structure
```
📁 ShadowBan/
 ├── 📜 Shadow.py           # Main script to interact with the database
 ├── 📜 Data.sql            # MySQL database dump
 ├── 📜 requirements.txt    # Required Python libraries
 ├── 📜 country.csv         # Country code mappings
 ├── 📜 README.md           # This fabulous documentation 😎
```

## ⚡ Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Dark-Angel1020/ShadowBan.git
cd ShadowBan
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Setup MySQL Database
Import the provided **Data.sql** file into your MySQL database:
```sh
mysql -u root -p ip_database < Data.sql
```
Modify `db_config` in `main.py` if necessary to match your MySQL settings.

### 4️⃣ Run the Script
```sh
python Shadow.py
```

## 🛠️ How to Use

You'll be presented with a menu where you can:

1️⃣ Search for an IP

2️⃣ List all IP ranges for a country

3️⃣ Add new IP ranges

4️⃣ Add Single IP address

5️⃣ Edit existing IP allocations 

6️⃣ Delete existing IP allocations


Simply enter the corresponding option number and follow the prompts!

## 📝 Example Usage
### Searching for an IP
```
Enter choice: 1
Enter IP to search: 192.168.1.1

IP 192.168.1.1 is from India
From the range of 192.168.1.0 - 192.168.1.255
```

### Listing All IP Ranges for a Country
```
Enter choice: 2
Enter country code: US

IP ranges for United States:
192.168.0.0 - 192.168.255.255
172.16.0.0 - 172.31.255.255
```

## 📌 Contributions
Got an idea or a bug fix? Feel free to fork and submit a pull request! 🚀

## 📜 License
This project is open-source and available under the **MIT License**.

🌟 Star this repository if you found it useful! ⭐ Happy coding! 😃

