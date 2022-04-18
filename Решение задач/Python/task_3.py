N = int(input())
for _ in range(N):
    list_input = input().split(',')
    ticket_no = str(list_input[0])
    flight_id = int(list_input[1])

    boarding = str(list_input[2])
    if boarding.startswith('Номер:') == True:
        boarding = boarding.replace('Номер:', '')

    seat_no = str(list_input[3])
    if ';' not in seat_no:
        chars = []
        for i in range(len(seat_no)):
            chars.append(seat_no[i])

        letter = chars.pop()
        chars.append(';')
        chars.append(letter)
        seat_no = ''.join(chars)
        
    print(ticket_no, flight_id, boarding, seat_no, sep=',', end='\n')