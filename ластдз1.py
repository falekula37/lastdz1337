import tkinter as tk
import sqlite3


conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
""")
conn.commit()
conn.close()

def add_employee():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    full_name = entry_full_name.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    salary = entry_salary.get()
    cursor.execute("INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)",
                   (full_name, phone_number, email, salary))
    conn.commit()
    conn.close()
    refresh_list()

def update_employee():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    selected_id = listbox.curselection()[0]
    employee_id = employee_ids[selected_id]
    full_name = entry_full_name.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    salary = entry_salary.get()
    cursor.execute("UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?",
                   (full_name, phone_number, email, salary, employee_id))
    conn.commit()
    conn.close()
    refresh_list()

def delete_employee():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    selected_id = listbox.curselection()[0]
    employee_id = employee_ids[selected_id]
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    conn.close()
    refresh_list()

def search_employee():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    search_term = entry_search.get()
    cursor.execute("SELECT id, full_name, phone_number, email, salary FROM employees WHERE full_name LIKE ?",
                   ('%' + search_term + '%',))
    employees = cursor.fetchall()
    conn.close()
    listbox.delete(0, tk.END)
    employee_ids.clear()
    for employee in employees:
        employee_ids.append(employee[0])
        listbox.insert(tk.END, f"{employee[1]} ({employee[2]})")

def refresh_list():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, phone_number, email, salary FROM employees")
    employees = cursor.fetchall()
    conn.close()
    listbox.delete(0, tk.END)
    employee_ids.clear()
    for employee in employees:
        employee_ids.append(employee[0])
        listbox.insert(tk.END, f"{employee[1]} ({employee[2]})")


root = tk.Tk()
root.title("Управление сотрудниками")

label_full_name = tk.Label(root, text="ФИО:")
entry_full_name = tk.Entry(root)
label_phone_number = tk.Label(root, text="Номер телефона:")
entry_phone_number = tk.Entry(root)
label_email = tk.Label(root, text="Адрес электронной почты:")
entry_email = tk.Entry(root)
label_salary = tk.Label(root, text="Заработная плата:")
entry_salary = tk.Entry(root)

add_button = tk.Button(root, text="Добавить сотрудника", command=add_employee)
update_button = tk.Button(root, text="Изменить сотрудника", command=update_employee)
delete_button = tk.Button(root, text="Удалить сотрудника", command=delete_employee)
search_label = tk.Label(root, text="Поиск по ФИО:")
entry_search = tk.Entry(root)
search_button = tk.Button(root, text="Найти", command=search_employee)

listbox = tk.Listbox(root)
employee_ids = []

refresh_list()

label_full_name.grid(row=0, column=0)
entry_full_name.grid(row=0, column=1)
label_phone_number.grid(row=1, column=0)
entry_phone_number.grid(row=1, column=1)
label_email.grid(row=2, column=0)
entry_email.grid(row=2, column=1)
label_salary.grid(row=3, column=0)
entry_salary.grid(row=3, column=1)

add_button.grid(row=4, column=0, columnspan=2)
update_button.grid(row=5, column=0, columnspan=2)
delete_button.grid(row=6, column=0, columnspan=2)

search_label.grid(row=7, column=0)
entry_search.grid(row=7, column=1)
search_button.grid(row=8, column=0, columnspan=2)

listbox.grid(row=0, column=2, rowspan=9)


root.mainloop()
