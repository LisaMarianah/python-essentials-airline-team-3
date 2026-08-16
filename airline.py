# SKYLINK RESERVATIONS
# Airline Reservation System


# Starting data
flights = {}
passengers = {}
bookings = {}

# ID counters  
next_flight_number = 1
next_passenger_number = 1
next_booking_number = 1


# Workstream A - Flights & Seats
#Adds a new flight with a validated seat map.
def add_flight(flights):
    global next_flight_number

    origin = input("Enter origin: ").strip()
    if origin == "":
        print("Origin cannot be blank.")
        return

    destination = input("Enter destination: ").strip()
    if destination == "":
        print("Destination cannot be blank.")
        return

    while True:
        try:
            price = float(input("Enter flight price: "))
            if price <= 0:
                print("Price must be greater than 0.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            rows = int(input("Enter number of rows: "))
            if rows < 1 or rows > 9:
                print("Please enter a number between 1 and 9. ")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    while True:
        try:
            seats_per_row = int(input("Enter seats per row: "))
            if seats_per_row < 1 or seats_per_row > 6:
                print("Please enter a number between 1 and 6. ")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    seats = []
    for row in range(rows):
        seat_row = []
        for seat in range(seats_per_row):
            seat_row.append(" ")
        seats.append(seat_row)

    flight_id = "F" + str(next_flight_number)
    flights[flight_id] = {
        "origin": origin,
        "dest": destination,
        "price": price,
        "seats": seats,
        "waitlist": []
    }

    next_flight_number = next_flight_number + 1
    print(
        "Added", flight_id + ":",
        origin, "->", destination,
        "| R" + format(price, ".2f"),
        "|", str(rows), "rows x", str(seats_per_row), "seats"
    )

# Workstream A - Flights & Seats
# Converts a seat label such as 2C into row and column indexes.
def seat_label_to_indexes(seat_label):
    seat_label = seat_label.strip().upper()

    if len(seat_label) < 2:
        return None, None

    row_part = seat_label[:-1]
    column_letter = seat_label[-1]

    try:
        row_number = int(row_part)
    except ValueError:
        return None, None

    if column_letter < "A" or column_letter > "F":
        return None,None
    if row_number < 1:
        return None, None

    row_index = row_number - 1 
    column_index = ord(column_letter) - ord("A")
    return row_index, column_index

# Workstream A - Flights & Seats
# Displays a flight's seat map and occupancy.
def render_seat_map(flights, flight_id):
    seats = flights[flight_id]["seats"]

    print(
        "Flight", flight_id + ":",
        flights[flight_id]["origin"],
        "->",
        flights[flight_id]["dest"],
        "| R" + format(flights[flight_id]["price"], ".2f"),
        "|",
        str(len(seats)),
        "rows x",
        str(len(seats[0])),
        "seats"
    )
    print(" ", end="")

    for column in range(len(seats[0])):
        print(chr(ord("A") + column), end="   ")

    print()

    row_number = 1

    for row in seats:
        print(row_number, end=" ")

        for seat in row:
            if seat == "X":
                print("[X]", end=" ")
            else:
                print("[ ]", end=" ")

    
        print()
        row_number = row_number + 1
    taken, total = seat_counts(flights, flight_id)
    percentage = (taken / total) * 100
    print(
        "Seats taken:",
        taken,
        "of",
        total,
        "(" + format(percentage, ".1f") + "% full)"
    )

# Workstream A - Flights & Seats
# Counts the taken and total seats for a flight.
def seat_counts(flights, flight_id):
    seats = flights[flight_id]["seats"]

    total = 0 
    taken = 0 

    for row in seats:
        for seat in row:
            total = total + 1

            if seat == "X":
                taken = taken + 1
    return taken, total           


# Workstream B - People & Bookings
# Registers a new passenger with a unique passenger ID.
def register_passenger():
    global next_passenger_number

    name = input("Enter passenger names: ").strip()

    if name == "":
        print("Passenger name cannot be blank.")
        return

    passenger_id = "P" + str(next_passenger_number)

    passengers[passenger_id] = {
        "name": name
    }

    next_passenger_number = next_passenger_number + 1

    print("Registered", passenger_id + ":", name)

# Workstream B - People & Bookings
# Books a passenger into an available seat on a flight.
def book_seat():
    global next_booking_number

    passenger_id = input("Passenger ID: ").strip()

    if passenger_id not in passengers:
        print("No such passenger.")
        return

    flight_id = input("Flight ID: ").strip()

    if flight_id not in flights:
        print("No such flight.")
        return

    taken, total = seat_counts(flights, flight_id)

    if taken == total:
        answer = input(
            "Flight " + flight_id +
            " is FULL. Add " + passenger_id +
            " to the waitlist? (y/n): "
        ).strip().lower()

        if answer == "y":
            join_waitlist(flights, flight_id, passenger_id)
        return

    seat_label = input("Seat: ").strip().upper()

    row_index, column_index = seat_label_to_indexes(seat_label)

    if row_index is None:
        print("Invalid seat format.")
        return

    seats = flights[flight_id]["seats"]

    if row_index >= len(seats) or column_index >= len(seats[0]):
        print("Seat does not exist on this flight.")
        return

    if seats[row_index][column_index] == "X":
        print("Seat is already taken.")
        return

    for booking in bookings.values():
        if (
            booking["passenger"] == passenger_id
            and booking["flight"] == flight_id
        ):
            print("Passenger is already booked on this flight.")
            return

    seats[row_index][column_index] = "X"

    booking_id = "BK" + str(next_booking_number)

    bookings[booking_id] = {
        "passenger": passenger_id,
        "flight": flight_id,
        "seat": seat_label
    }

    next_booking_number = next_booking_number + 1

    print(
        "Booked", booking_id + ":",
        passenger_id,
        "on", flight_id,
        "seat", seat_label,
        "| R" + format(flights[flight_id]["price"], ".2f")
    )

# Workstream B - People & Bookings
# Cancels an existing booking and frees the passenger's seat.
def cancel_booking():
    booking_id = input("Booking ID: ").strip().upper()

    if booking_id == "":
        print("Booking ID cannot be blank.")
        return

    if booking_id not in bookings:
        print("No such booking.")
        return

    booking = bookings[booking_id]

    passenger_id = booking["passenger"]
    flight_id = booking["flight"]
    seat_label = booking["seat"]

    row_index, column_index = seat_label_to_indexes(seat_label)

    flights[flight_id]["seats"][row_index][column_index] = " "


    del bookings[booking_id]

    print(
        "Booking", booking_id,
        "cancelled. Seat", seat_label,
        "on", flight_id, "is free."
    )

    promote_from_waitlist(flights, flight_id)

# Workstream B - People & Bookings
# Changes a passenger's seat on a flight.
def change_seat():
    booking_id = input("Booking ID: ").strip().upper()

    if booking_id == "":
        print("Booking ID cannot be blank.")
        return

    if booking_id not in bookings:
        print("No such booking.")
        return

    booking = bookings[booking_id]

    flight_id = booking["flight"]
    old_seat = booking["seat"]

    new_seat = input("New seat: ").strip().upper()

    if new_seat == "":
        print("Seat cannot be blank.")
        return

    row_index, column_index = seat_label_to_indexes(new_seat)

    if row_index is None:
        print("Invalid seat format.")
        return

    seats = flights[flight_id]["seats"]

    if row_index >= len(seats) or column_index >= len(seats[0]):
        print("Seat does not exist on this flight.")
        return

    if seats[row_index][column_index] == "X":
        print("Seat is already taken.")
        return

    old_row, old_column = seat_label_to_indexes(old_seat)

    seats[old_row][old_column] = " "
    seats[row_index][column_index] = "X"

    booking["seat"] = new_seat

    print(booking_id + ": seat changed from", old_seat, "to", new_seat)
    

# Workstream C - Waitlist & Reports
# Adds a passenger to a flight's waitlist

def join_waitlist(flights, flight_id, passenger_id):
    waitlist = flights[flight_id]["waitlist"]

    if passenger_id in waitlist:
        print("Passenger is already on the waitlist.")
        return

    for booking in bookings.values():
        if (
            booking["passenger"] == passenger_id
            and booking["flight"] == flight_id
        ):
            print("Passenger is already booked on this flight.")
            return

    waitlist.append(passenger_id)
    
    position = len(waitlist)

    print(
        "Added", passenger_id,
        "to the waitlist for", flight_id,
        "at position", position

    )

# Workstream C - Waitlist & Reports
# Promotes the first passenger on the waitlist when a seat becomes available.
def promote_from_waitlist(flights, flight_id):
    waitlist = flights[flight_id]["waitlist"]

    if len(waitlist) == 0:
        return

    passenger_id = waitlist.pop(0)

    seats = flights[flight_id]["seats"]

    for row_index in range(len(seats)):
        for column_index in range(len(seats[row_index])):
            if seats[row_index][column_index] == " ":

                seats[row_index][column_index] = "X"

                seat_label = (
                    str(row_index + 1) +
                    chr(ord("A") + column_index)
                )

                global next_booking_number

                booking_id = "BK" + str(next_booking_number)

                bookings[booking_id] = {
                    "passenger": passenger_id,
                    "flight": flight_id,
                    "seat": seat_label
                }

                next_booking_number = next_booking_number + 1

                print(
                    "Promoted", passenger_id,
                    "from waitlist.",
                    "Booked", booking_id + ":",
                    "seat", seat_label
                )

                return

# Workstream C - Waitlist & Reports
# Displays all passengers booked on a flight.
def flight_manifest():
    flight_id = input("Flight ID: ").strip().upper()

    if flight_id == "":
        print("Flight ID cannot be blank.")
        return

    if flight_id not in flights:
        print("No such flight.")
        return

    print()
    print(
        "Manifest for", flight_id + ":",
        flights[flight_id]["origin"],
        "->",
        flights[flight_id]["dest"]
    )

    flight_bookings = []

    for booking_id, booking in bookings.items():
        if booking["flight"] == flight_id:
            flight_bookings.append(
                (booking["seat"], booking_id, booking["passenger"])
            )

    flight_bookings.sort()

    if len(flight_bookings) == 0:
        print("No passengers booked on this flight.")
    else:
        for seat, booking_id, passenger_id in flight_bookings:
            passenger_name = passengers[passenger_id]["name"]

            print(
                booking_id,
                "|",
                seat,
                "|",
                passenger_id,
                "-",
                passenger_name
            )

    waitlist = flights[flight_id]["waitlist"]

    print()
    print("Waitlist:")

    if len(waitlist) == 0:
        print("(waitlist empty)")
    else:
        for passenger_id in waitlist:
            passenger_name = passengers[passenger_id]["name"]

            print(
                passenger_id,
                "-",
                passenger_name
            )

# Workstream C - Waitlist & Report
# Calculates occupancy information for a flight.
def flight_occupancy(flights, flight_id):
    taken, total = seat_counts(flights, flight_id)

    if total == 0:
        percentage = 0
    else:
        percentage = (taken / total) * 100

    return taken, total, percentage

# Workstream C - Waitlist & Reports
# Finds the flight with the highest occupancy.
def find_fullest_flight(flights):
    fullest_flight = None
    highest_occupancy = -1

    for flight_id in flights:
        taken, total, percentage = flight_occupancy(
            flights,
            flight_id
        )

        if percentage > highest_occupancy:
            highest_occupancy = percentage
            fullest_flight = flight_id

    return fullest_flight, highest_occupancy

# Workstream C - Waitlist & Reports
# Calculates and displays total revenue from bookings.
def revenue_report():
    print()
    print("Revenue Report")

    total_revenue = 0
    total_waitlisted = 0
    
    if len(flights) == 0:
        print("No flights available.")
        print("Total revenue: R0.00")
        print("Fullest flight: None")
        print("Total passengers on waitlists: 0")
        return
        
    fullest_flight, _ = find_fullest_flight(flights)

    for flight_id, flight in flights.items():

        taken, total, occupancy = flight_occupancy(flights, flight_id)        

        revenue = taken * flight["price"]

        total_revenue = total_revenue + revenue
        total_waitlisted = total_waitlisted + len(flight["waitlist"])

        print(
            flight_id,
            "|",
            flight["origin"],
            "->",
            flight["dest"],
            "|",
            str(taken) + "/" + str(total),
            "seats",
            "|",
            format(occupancy, ".1f") + "%",
            "|",
            "R" + format(revenue, ".2f")
        )

    print()
    print("Total revenue: R" + format(total_revenue, ".2f"))
    print("Fullest flight:", fullest_flight)
    print("Total passengers on waitlists:", total_waitlisted)
    

# Main Menu
def main():
    while True:
        print()
        print("===== SKYLINK RESERVATIONS =====")
        print("1. Add Flight")
        print("2. Register a passenger")
        print("3. View seat map")
        print("4. Book a Seat")
        print("5. Cancel a Booking")
        print("6. Change a Seat")
        print("7. Flight manifest")
        print("8. Revenue report")
        print("9. Exit")
    

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            add_flight(flights)

        elif choice == "2":
            register_passenger()

        elif choice == "3":
            flight_id = input("Flight ID: ").strip().upper()

            if flight_id == "":
                print("Flight ID cannot be blank.")
            elif flight_id not in flights:
                print("No such flight.")
            else:
                render_seat_map(flights, flight_id)

        elif choice == "4":
            book_seat()

        elif choice == "5":
            cancel_booking()

        elif choice == "6":
            change_seat()

        elif choice == "7":
            flight_manifest()

        elif choice == "8":
            revenue_report()

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please enter 1-9.")

if __name__ == "__main__":
    main()
