from datetime import datetime
import csv

import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="pass@word1",
        database="parking_db"
    )

# ---------------- CRUD Functions ----------------
def vehicle_entry():
    number = input("Enter vehicle number: ").strip()
    v_type = input("Enter vehicle type (Car/Bike): ").strip().capitalize()

    if v_type not in ["Car", "Bike"]:
        print("Invalid vehicle type! Must be 'Car' or 'Bike'.")
        return

    entry = datetime.now()

    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO parking (vehicle_number, vehicle_type, entry_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (number, v_type, entry))
    conn.commit()
    conn.close()
    print("Vehicle entry recorded!")

def filter_by_date():
    date_str = input("Enter date (YYYY-MM-DD): ")
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM parking WHERE DATE(entry_time) = %s"
    cursor.execute(query, (date_str,))
    rows = cursor.fetchall()
    conn.close()

    print(f"\n--- Records for {date_str} ---")
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Number: {row[1]}, Type: {row[2]}, Entry: {row[3]}, Exit: {row[4]}, Fee: ₹{row[5]}")
    else:
        print("No records found for this date.")

def dashboard_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM parking")
    total_vehicles = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(parking_fee) FROM parking")
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM parking WHERE exit_time IS NULL")
    currently_parked = cursor.fetchone()[0]

    conn.close()

    print("\n--- Dashboard Summary ---")
    print(f"Total Vehicles: {total_vehicles}")
    print(f"Total Revenue: ₹{round(total_revenue, 2)}")
    print(f"Currently Parked Vehicles: {currently_parked}")

def vehicle_exit():
    vid = int(input("Enter parking ID for exit: "))
    exit_time = datetime.now()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT entry_time, vehicle_type FROM parking WHERE id = %s", (vid,))
    result = cursor.fetchone()

    if result:
        entry_time, v_type = result
        duration = (exit_time - entry_time).total_seconds() / 3600  # hours

        rate = 30 if v_type.lower() == "car" else 15  # ₹30/hr for Car, ₹15/hr for Bike
        fee = round(duration * rate, 2)

        query = "UPDATE parking SET exit_time = %s, parking_fee = %s WHERE id = %s"
        cursor.execute(query, (exit_time, fee, vid))
        conn.commit()
        print(f"Vehicle exited. Parking fee: ₹{fee}")
    else:
        print("Invalid parking ID.")

    conn.close()


def view_parking():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking")
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Parking Records ---")
    for row in rows:
        try:
            print(f"ID: {row[0]}, Number: {row[1]}, Type: {row[2]}, Entry: {row[3]}, Exit: {row[4]}, Fee: ₹{row[5]}")
        except Exception as e:
            print(f"Error printing row: {row} — {e}")

def search_vehicle():
    keyword = input("Enter vehicle number to search: ")
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM parking WHERE vehicle_number LIKE %s"
    cursor.execute(query, (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Search Results ---")
    for row in rows:
        print(f"ID: {row[0]}, Number: {row[1]}, Type: {row[2]}, Entry: {row[3]}, Exit: {row[4]}, Fee: ₹{row[5]}")

def export_parking():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking")
    rows = cursor.fetchall()
    conn.close()

    with open("C:\\Users\\Administrator\\Desktop\\parking_records.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Vehicle Number", "Type", "Entry Time", "Exit Time", "Fee"])
        writer.writerows(rows)
        print("Data exported to parking_records.csv")

# ---------------- Main Menu ----------------
def main_menu():
    while True:
        print("\n===== Parking Management System =====")
        print("1. Vehicle Entry")
        print("2. Vehicle Exit")
        print("3. View Parking Records")
        print("4. Search Vehicle")
        print("5. Export Records to CSV")
        print("6. Filter Records by Date")
        print("7. Dashboard Summary")
        print("8. Help / Instructions")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_entry()
        elif choice == "2":
            vehicle_exit()
        elif choice == "3":
            view_parking()
        elif choice == "4":
            search_vehicle()
        elif choice == "5":
            export_parking()
        elif choice == "6":
            filter_by_date()
        elif choice == "7":
            dashboard_summary()
        elif choice == "8":
            print("\nInstructions:")
            print("- Use 'Vehicle Entry' to log a new vehicle.")
            print("- Use 'Vehicle Exit' to calculate fee and close the record.")
            print("- Use 'Dashboard Summary' for quick stats.")
            print("- Use 'Export' to save records to CSV.")
        elif choice == "9":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()
