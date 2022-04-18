N = int(input())
list_output = [1, 2]
for i in range(N):
    list_input = input().split(',')
    ticket_no = str(list_input[0])
    flight_id = int(list_input[1])
    if ticket_no == list_output[0] and flight_id == list_output[1]:
        continue
    
    boarding = str(list_input[2])
    seat_no = str(list_input[3])

    list_output = [ticket_no, flight_id, boarding, seat_no]

    print(*list_output, sep=',', end='\n')