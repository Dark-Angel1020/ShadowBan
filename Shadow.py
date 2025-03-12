import mysql.connector
import ipaddress
import csv

# MySQL connection settings
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root", # username
    "password": "**********", # Put your mysql password 
    "database": "ip_database"
}

# Load country codes and names from CSV
country_mapping = {}

def load_country_data():
    """Load country codes and names from country.csv into a dictionary."""
    global country_mapping
    try:
        with open("country.csv", mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                if len(row) >= 2:
                    country_mapping[row[1].strip().upper()] = row[0].strip() 
    except FileNotFoundError:
        print("[ERROR] country.csv file not found. Country names may not be available.")

load_country_data() 

def connect_db():
    """Establish a connection to the MySQL database."""
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"[ERROR] Database connection error: {err}")
        return None

def search_ip(ip):
    """Search for an IP in the database and return the country name."""
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    ip_obj = ipaddress.IPv4Address(ip)
    
    cursor.execute("SELECT start_ip, end_ip, country_code FROM ip_allocations")
    for start_ip, end_ip, country_code in cursor.fetchall():
        if ipaddress.IPv4Address(start_ip) <= ip_obj <= ipaddress.IPv4Address(end_ip):
            country_name = country_mapping.get(country_code.upper(), "Unknown Country")
            print(f"\nIP {ip} is from {country_name}\nFrom the range of {start_ip} - {end_ip}")
            cursor.close()
            conn.close()
            return
    
    print("IP not found in any range.")
    cursor.close()
    conn.close()

def list_ranges_by_country(country_code):
    """List all IP ranges allocated to a specific country."""
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    
    country_name = country_mapping.get(country_code.upper(), "Unknown Country")
    cursor.execute("SELECT start_ip, end_ip FROM ip_allocations WHERE country_code = %s", (country_code,))
    ranges = cursor.fetchall()
    
    if not ranges:
        print(f"No ranges found for {country_name} ({country_code}).")
    else:
        print(f"IP ranges for {country_name} ({country_code}):")
        for start_ip, end_ip in ranges:
            print(f"{start_ip} - {end_ip}")
    
    cursor.close()
    conn.close()

def add_ip_range(start_ip, end_ip, country_code):
    """Add a new IP range to the database."""
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ip_allocations (start_ip, end_ip, country_code) VALUES (%s, %s, %s)", (start_ip, end_ip, country_code))
    conn.commit()
    print("IP range added successfully!")
    cursor.close()
    conn.close()

def add_single_ip(ip, country_code):
    """Add a single IP to the database."""
    add_ip_range(ip, ip, country_code)

def edit_ip_range(old_start_ip, old_end_ip, new_start_ip, new_end_ip, country_code):
    """Edit an existing IP range in the database."""
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("UPDATE ip_allocations SET start_ip = %s, end_ip = %s, country_code = %s WHERE start_ip = %s AND end_ip = %s", 
                   (new_start_ip, new_end_ip, country_code, old_start_ip, old_end_ip))
    conn.commit()
    print("IP range updated successfully!")
    cursor.close()
    conn.close()

def delete_ip_range(start_ip, end_ip):
    """Delete an IP range from the database."""
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ip_allocations WHERE start_ip = %s AND end_ip = %s", (start_ip, end_ip))
    conn.commit()
    print("IP range deleted successfully!")
    cursor.close()
    conn.close()

def main():
    """Main menu for user interaction."""
    while True:
        print("\n1. Search IP")
        print("2. List IP ranges by country")
        print("3. Add IP range")
        print("4. Add single IP")
        print("5. Edit IP range")
        print("6. Delete IP range")
        print("7. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            ip = input("Enter IP to search: ")
            search_ip(ip)
        elif choice == "2":
            country_code = input("Enter country code: ").upper()
            list_ranges_by_country(country_code)
        elif choice == "3":
            start_ip = input("Enter start IP: ")
            end_ip = input("Enter end IP: ")
            country_code = input("Enter country code: ").upper()
            add_ip_range(start_ip, end_ip, country_code)
        elif choice == "4":
            ip = input("Enter IP: ")
            country_code = input("Enter country code: ").upper()
            add_single_ip(ip, country_code)
        elif choice == "5":
            old_start_ip = input("Enter old start IP: ")
            old_end_ip = input("Enter old end IP: ")
            new_start_ip = input("Enter new start IP: ")
            new_end_ip = input("Enter new end IP: ")
            country_code = input("Enter country code: ").upper()
            edit_ip_range(old_start_ip, old_end_ip, new_start_ip, new_end_ip, country_code)
        elif choice == "6":
            start_ip = input("Enter start IP to delete: ")
            end_ip = input("Enter end IP to delete: ")
            delete_ip_range(start_ip, end_ip)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main()
