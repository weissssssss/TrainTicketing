import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# Core Classes (unchanged from original)
class Train:
    def __init__(self, train_no, name, source, destination, seats, fare):
        self.train_no = train_no
        self.name = name
        self.source = source
        self.destination = destination
        self.seats = seats
        self.available_seats = list(range(1, seats + 1))
        self.fare = fare

class TicketingSystem:
    def __init__(self):
        self.trains = []
        self.bookings = []

    def add_train(self, train):
        self.trains.append(train)

    def find_train(self, train_no):
        for train in self.trains:
            if train.train_no == train_no:
                return train
        return None

    def book_ticket(self, passenger_name, train_no):
        train = self.find_train(train_no)
        if train:
            if train.available_seats:
                seat_no = train.available_seats.pop(0)
                ticket_id = f"TICKET{random.randint(1000, 9999)}"
                booking = {
                    'ticket_id': ticket_id,
                    'passenger_name': passenger_name,
                    'train_name': train.name,
                    'train_no': train.train_no,
                    'seat_no': seat_no,
                    'fare': train.fare
                }
                self.bookings.append(booking)
                return booking
            else:
                return "No seats available."
        else:
            return "Train not found."

    def cancel_ticket(self, ticket_id):
        for booking in self.bookings:
            if booking['ticket_id'] == ticket_id:
                train = self.find_train(booking['train_no'])
                if train:
                    train.available_seats.append(booking['seat_no'])
                    train.available_seats.sort()
                self.bookings.remove(booking)
                return True
        return False

    def export_bookings(self):
        if not self.bookings:
            return "No bookings to export."
        result = ""
        for booking in self.bookings:
            result += f"{booking['ticket_id']} - {booking['passenger_name']} - {booking['train_name']} - Seat {booking['seat_no']} - Ksh{booking['fare']}\n"
        return result

    def view_ticket_details(self, ticket_id):
        for booking in self.bookings:
            if booking['ticket_id'] == ticket_id:
                return f"Ticket ID: {booking['ticket_id']}\nPassenger: {booking['passenger_name']}\nTrain: {booking['train_name']} (Seat {booking['seat_no']})\nFare: Ksh{booking['fare']}"
        return "Ticket not found."

    def view_available_seats(self, train_no):
        train = self.find_train(train_no)
        if train:
            return f"Available Seats: {', '.join(map(str, train.available_seats))}"
        else:
            return "Train not found."

# Tkinter GUI with Proper Centering
class TicketApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Train Ticketing System")
        self.root.geometry("700x600")
        self.root.config(bg="#000000")  # Black background
        
        # Configure root to center everything
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Main container frame
        self.main_frame = tk.Frame(self.root, bg="#000000")  # Black background
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # Header - centered
        header_frame = tk.Frame(self.main_frame, bg="#000000")  # Black background
        header_frame.grid(row=0, column=0, sticky="ew", pady=(20, 30))
        header_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(header_frame, text="Train Ticketing System",
                 font=('Arial', 24, 'bold'), fg='#FFFFFF', bg='#000000') \
          .grid(row=0, column=0)

        # Button frame - centered
        button_frame = tk.Frame(self.main_frame, bg="#000000")  # Black background
        button_frame.grid(row=1, column=0, sticky="", pady=10)
        button_frame.grid_columnconfigure(0, weight=1)

        # Buttons - centered in their frame
        buttons = [
            ("View Trains", self.view_trains),
            ("Book Ticket", self.book_ticket_window),
            ("View Bookings", self.view_bookings),
            ("Cancel Ticket", self.cancel_ticket_window),
            ("Export Bookings", self.export_bookings),
            ("View Available Seats", self.view_available_seats_window),
            ("View Ticket Details", self.view_ticket_details_window)
        ]

        for i, (text, command) in enumerate(buttons):
            btn_frame = tk.Frame(button_frame, bg="#000000")  # Black background
            btn_frame.grid(row=i, column=0, pady=5, sticky="ew")
            btn_frame.grid_columnconfigure(0, weight=1)
            
            tk.Button(btn_frame, text=text, command=command, font=('Arial', 12, 'bold'), bg="#3498DB", fg="white", activebackground="#2980B9", relief="flat", width=20, height=2) \
                .grid(row=0, column=0, sticky="")

    # Pop-up customization
    def show_custom_popup(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.config(bg="#000000")
        popup.geometry("300x150")

        label = tk.Label(popup, text=message, font=('Arial', 12), fg='#FFFFFF', bg='#000000')
        label.pack(pady=20)

        button = tk.Button(popup, text="OK", command=popup.destroy, font=('Arial', 12, 'bold'), bg="#3498DB", fg="white", relief="flat")
        button.pack()

    def view_trains(self):
        train_info = ""
        for train in self.system.trains:
            train_info += f"{train.train_no} - {train.name} | {train.source} -> {train.destination} | Fare: Ksh{train.fare} | Available Seats: {len(train.available_seats)}\n"
        if train_info:
            self.show_custom_popup("Available Trains", train_info)
        else:
            self.show_custom_popup("Available Trains", "No trains available.")

    def view_bookings(self):
        if not self.system.bookings:
            self.show_custom_popup("Bookings", "No bookings yet.")
        else:
            booking_info = ""
            for booking in self.system.bookings:
                booking_info += f"Ticket ID: {booking['ticket_id']}\nPassenger: {booking['passenger_name']}\nTrain: {booking['train_name']} (Seat {booking['seat_no']})\nFare: Ksh{booking['fare']}\n\n"
            self.show_custom_popup("Booked Tickets", booking_info)

    def cancel_ticket_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Cancel Ticket")
        self.new_window.config(bg="#000000")
        self.new_window.grid_columnconfigure(0, weight=1)
        
        content_frame = tk.Frame(self.new_window, bg="#000000")
        content_frame.grid(row=0, column=0, padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)

        tk.Label(content_frame, text="Enter Ticket ID to Cancel:", 
                font=('Arial', 14), fg="#3498DB", bg="#000000").grid(row=0, column=0, pady=10)
        self.ticket_id_entry = tk.Entry(content_frame, font=('Arial', 12), width=30)
        self.ticket_id_entry.grid(row=1, column=0, pady=10)
        
        btn_frame = tk.Frame(content_frame, bg="#000000")
        btn_frame.grid(row=2, column=0, pady=10)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        tk.Button(btn_frame, text="Cancel Ticket", 
                 command=self.cancel_ticket_action, font=('Arial', 12, 'bold'), bg="#3498DB", fg="white", relief="flat").grid(row=0, column=0)

    def cancel_ticket_action(self):
        ticket_id = self.ticket_id_entry.get()
        if not ticket_id:
            self.show_custom_popup("Error", "Please enter a valid ticket ID!")
            return

        if self.system.cancel_ticket(ticket_id):
            self.show_custom_popup("Success", "Ticket successfully canceled!")
            self.new_window.destroy()
        else:
            self.show_custom_popup("Error", "Ticket ID not found.")

    def export_bookings(self):
        result = self.system.export_bookings()
        self.show_custom_popup("Export Success", result)

    def view_available_seats_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("View Available Seats")
        self.new_window.config(bg="#000000")
        self.new_window.grid_columnconfigure(0, weight=1)
        
        content_frame = tk.Frame(self.new_window, bg="#000000")
        content_frame.grid(row=0, column=0, padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)

        tk.Label(content_frame, text="Select Train:", 
                font=('Arial', 14), fg="#3498DB", bg="#000000").grid(row=0, column=0, pady=10)
        
        train_list = [f"{train.train_no} - {train.name}" for train in self.system.trains]
        self.train_selection = ttk.Combobox(content_frame, values=train_list, state="readonly", font=('Arial', 12))
        self.train_selection.grid(row=1, column=0, pady=10)
        
        btn_frame = tk.Frame(content_frame, bg="#000000")
        btn_frame.grid(row=2, column=0, pady=10)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        tk.Button(btn_frame, text="View Available Seats", 
                 command=self.view_available_seats_action, font=('Arial', 12, 'bold'), bg="#3498DB", fg="white", relief="flat").grid(row=0, column=0)

    def view_available_seats_action(self):
        selected_train = self.train_selection.get()
        if not selected_train:
            self.show_custom_popup("Error", "Please select a train!")
            return

        train_no = selected_train.split(' ')[0]
        result = self.system.view_available_seats(train_no)
        self.show_custom_popup("Available Seats", result)

    def view_ticket_details_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("View Ticket Details")
        self.new_window.config(bg="#000000")
        self.new_window.grid_columnconfigure(0, weight=1)
        
        content_frame = tk.Frame(self.new_window, bg="#000000")
        content_frame.grid(row=0, column=0, padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)

        tk.Label(content_frame, text="Enter Ticket ID:", 
                font=('Arial', 14), fg="#3498DB", bg="#000000").grid(row=0, column=0, pady=10)
        self.ticket_id_entry = tk.Entry(content_frame, font=('Arial', 12), width=30)
        self.ticket_id_entry.grid(row=1, column=0, pady=10)
        
        btn_frame = tk.Frame(content_frame, bg="#000000")
        btn_frame.grid(row=2, column=0, pady=10)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        tk.Button(btn_frame, text="View Ticket", 
                 command=self.view_ticket_details_action, font=('Arial', 12, 'bold'), bg="#3498DB", fg="white", relief="flat").grid(row=0, column=0)

    def view_ticket_details_action(self):
        ticket_id = self.ticket_id_entry.get()
        if not ticket_id:
            self.show_custom_popup("Error", "Please enter a valid ticket ID!")
            return
        
        result = self.system.view_ticket_details(ticket_id)
        self.show_custom_popup("Ticket Details", result)

    def book_ticket_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Book Ticket")
        self.new_window.config(bg="#000000")
        self.new_window.grid_columnconfigure(0, weight=1)
        
        content_frame = tk.Frame(self.new_window, bg="#000000")
        content_frame.grid(row=0, column=0, padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)

        tk.Label(content_frame, text="Enter Passenger Name:", 
                font=('Arial', 14), fg="#3498DB", bg="#000000").grid(row=0, column=0, pady=10)
        
        self.passenger_name_entry = tk.Entry(content_frame, font=('Arial', 12), width=30)
        self.passenger_name_entry.grid(row=1, column=0, pady=10)

        tk.Label(content_frame, text="Select Train:", 
                 font=('Arial', 14), fg="#3498DB", bg="#000000").grid(row=2, column=0, pady=10)

        train_list = [f"{train.train_no} - {train.name}" for train in self.system.trains]
        self.train_selection = ttk.Combobox(content_frame, values=train_list, state="readonly", font=('Arial', 12))
        self.train_selection.grid(row=3, column=0, pady=10)

        btn_frame = tk.Frame(content_frame, bg="#000000")
        btn_frame.grid(row=4, column=0, pady=10)
        btn_frame.grid_columnconfigure(0, weight=1)
        
        tk.Button(btn_frame, text="Book Ticket", 
                  command=self.book_ticket_action, font=('Arial', 12, 'bold'), bg="#3498DB", fg="white", relief="flat").grid(row=0, column=0)

    def book_ticket_action(self):
        passenger_name = self.passenger_name_entry.get()
        selected_train = self.train_selection.get()
        
        if not passenger_name or not selected_train:
            self.show_custom_popup("Error", "Please fill in all fields!")
            return
        
        train_no = selected_train.split(' ')[0]
        result = self.system.book_ticket(passenger_name, train_no)
        if isinstance(result, dict):  # Successful booking
            ticket_details = f"Ticket ID: {result['ticket_id']}\nPassenger: {result['passenger_name']}\nTrain: {result['train_name']} (Seat {result['seat_no']})\nFare: Ksh{result['fare']}"
            self.show_custom_popup("Booking Successful", ticket_details)
            self.new_window.destroy()
        else:
            self.show_custom_popup("Error", result)

# Sample Train Data
system = TicketingSystem()

train1 = Train("001", "Express 101", "Nairobi", "Mombasa", 50, 1500)
train2 = Train("002", "SuperFast 202", "Mombasa", "Nakuru", 50, 1200)

system.add_train(train1)
system.add_train(train2)

# Running the Tkinter App
root = tk.Tk()
app = TicketApp(root, system)
root.mainloop()
