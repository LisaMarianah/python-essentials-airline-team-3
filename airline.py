# SKYLINK RESERVATIONS
# Airline Reservation System


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

# Cancels an existing booking and frees the passenger's seat.
def cancel_booking():
    booking_id = input("Booking ID: ").strip().upper()

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
        "Cancelled", booking_id + ":",
        passenger_id,
        "on", flight_id,
        "seat", seat_label
    )

    promote_from_waitlist(flights, flight_id)


def change_seat():
    



# Workstream C - Waitlist & Reports


def join_waitlist():
    


def promote_from_waitlist():
    


def flight_manifest():
    


def revenue_report():
    



# Main Menu


def main():
    


if __name__ == "__main__":
    main()
