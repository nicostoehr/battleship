import socket
import os
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


colorama_init()

CHAR_MAP = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
}
INT_MAP = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
    8: "i",
}


# DONE
def strm(str_in):
    if str_in == "-": return "-"
    elif str_in == "#": return f"{Fore.GREEN}#{Style.RESET_ALL}"
    elif str_in == "O": return f"{Fore.BLUE}O{Style.RESET_ALL}"
    elif str_in == "X": return f"{Fore.RED}X{Style.RESET_ALL}"
    elif str_in == "M": return f"{Fore.BLUE}M{Style.RESET_ALL}"
    elif str_in == "+": return f"{Fore.RED}+{Style.RESET_ALL}"
    else: return "u"


# DONE
def print_board(own_dict, riv_dict=None):
    if riv_dict is None:
        riv_dict = {}
    riv_len = len(riv_dict)
    board_matrix = [["-" for _ in range(18)] for _ in range(9)]

    for ship, pos in own_dict.items():
        if type(pos) is str and pos != "" and len(pos) == 3:
            if pos[2] == "n":
                if ship[0] == "s":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]+1] = "#"
                elif ship[0] == "m":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]+1] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]+2] = "#"
                elif ship[0] == "l":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]+1] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]+2] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]+3] = "#"

            elif pos[2] == "r":
                if ship[0] == "s":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])+1][CHAR_MAP[pos[0]]] = "#"
                elif ship[0] == "m":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])+1][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])+2][CHAR_MAP[pos[0]]] = "#"
                elif ship[0] == "l":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])+1][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])+2][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])+3][CHAR_MAP[pos[0]]] = "#"
        elif ship == "misses":
            for cord in pos:
                board_matrix[int(cord[1])][CHAR_MAP[cord[0]]] = "M"
        elif ship == "hits":
            for cord in pos:
                board_matrix[int(cord[1])][CHAR_MAP[cord[0]]] = "+"

    for ship, pos in riv_dict.items():
        if ship == "misses":
            for cord in pos:
                board_matrix[int(cord[1])][CHAR_MAP[cord[0]]+9] = "O"
        elif ship == "hits":
            for cord in pos:
                board_matrix[int(cord[1])][CHAR_MAP[cord[0]]+9] = "X"

    index = 0
    os.system("cls")
    print("============================", end="")
    if riv_len > 0: print("======================================")
    else: print("")
    print("       YOUR BOARD           ", end="")
    if riv_len > 0: print("                   ENEMY BOARD")
    else: print("")
    print("============================", end="")
    if riv_len > 0: print("======================================")
    else: print("")
    print("  A  B  C  D  E  F  G  H  I ", end="")
    if riv_len > 0: print("            A  B  C  D  E  F  G  H  I")
    else: print("")

    for row in board_matrix:

        print(f"{index} {strm(row[0])}  {strm(row[1])}  {strm(row[2])}  {strm(row[3])}  {strm(row[4])}  {strm(row[5])}  {strm(row[6])}  {strm(row[7])}  {strm(row[8])}", end="")
        if riv_len > 0: print(f"           {index} {strm(row[9])}  {strm(row[10])}  {strm(row[11])}  {strm(row[12])}  {strm(row[13])}  {strm(row[14])}  {strm(row[15])}  {strm(row[16])}  {strm(row[17])}")
        else: print("")
        index += 1

    print("============================", end="")
    if riv_len > 0:
        print("======================================")
    else:
        print("")


# DONE
def host_conn_setup(o_socket):
    mode_chosen = False
    c_mode = ""

    while not mode_chosen:
        os.system("cls")
        c_mode = input("Host (h) or Join (j) game: ").strip().lower()
        if c_mode == "h":
            mode_chosen = True
        elif c_mode == "j":
            mode_chosen = True

    if c_mode == "h":
        print("===========================================")
        print("Host Mode")
        print("===========================================")
        own_port = int(input("Run game at port: "))
        o_socket.bind(("", own_port))
        print("===========================================")
        print(f"Game ist hosted on Port:{own_port}")
        print("===========================================")

        while True:
            rec_data, rec_f_addr = o_socket.recvfrom(1024)
            if rec_data.decode("utf-8") == "PySchiffeVersenkenByNicoConnReq":
                break
        o_socket.sendto("PySchiffeVersenkenByNicoConnAcc".encode("utf-8"), rec_f_addr)
        print("Connected to client!")

        return c_mode, rec_f_addr

    elif c_mode == "j":
        print("===========================================")
        print("Join Host")
        print("===========================================")
        own_port = int(input("Run game at port: "))
        o_socket.bind(("", own_port))
        print("===========================================")
        conn_addr = input("Host IP: ").strip()
        conn_port = int(input("Host port: "))
        print("===========================================")

        o_socket.sendto("PySchiffeVersenkenByNicoConnReq".encode("utf-8"), (conn_addr, conn_port))

        while True:
            rec_data, rec_f_addr = o_socket.recvfrom(1024)
            if rec_data.decode("utf-8") == "PySchiffeVersenkenByNicoConnAcc":
                break
        print("Connected to host!")

        return c_mode, rec_f_addr


# DONE
def fit_ship(ship_dict, try_pos, ship_type):
    board_matrix = [["-" for _ in range(9)] for _ in range(9)]

    for ship, pos in ship_dict.items():
        if type(pos) is str and pos != "" and len(pos) == 3:
            if pos[2] == "n":
                if ship[0] == "s":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]] + 1] = "#"
                elif ship[0] == "m":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]] + 1] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]] + 2] = "#"
                elif ship[0] == "l":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]] + 1] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]] + 2] = "#"
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]] + 3] = "#"
                else: return -1
            elif pos[2] == "r":
                if ship[0] == "s":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1]) + 1][CHAR_MAP[pos[0]]] = "#"
                elif ship[0] == "m":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1]) + 1][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1]) + 2][CHAR_MAP[pos[0]]] = "#"
                elif ship[0] == "l":
                    board_matrix[int(pos[1])][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1]) + 1][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1]) + 2][CHAR_MAP[pos[0]]] = "#"
                    board_matrix[int(pos[1]) + 3][CHAR_MAP[pos[0]]] = "#"
                else: return -1

    if try_pos[2] == "n":
        if ship_type == "s" and try_pos[0] in CHAR_MAP.keys():
            if board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]+1] == "-": return 0
        elif ship_type == "m" and try_pos[0] in CHAR_MAP.keys():
            if board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]+1] == "-" and board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]+2] == "-": return 0
        elif ship_type == "l" and try_pos[0] in CHAR_MAP.keys():
            if board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]+1] == "-" and board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]+2] == "-" and board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]+3] == "-": return 0
        else: return -1
    elif try_pos[2] == "r":
        if ship_type == "s" and try_pos[0] in CHAR_MAP.keys():
            if board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])][
                CHAR_MAP[try_pos[0]]] == "-": return 0
        elif ship_type == "m" and try_pos[0] in CHAR_MAP.keys():
            if board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])+1][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])+2][CHAR_MAP[try_pos[0]]] == "-": return 0
        elif ship_type == "l" and try_pos[0] in CHAR_MAP.keys():
            if board_matrix[int(try_pos[1])][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])+1][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])+2][CHAR_MAP[try_pos[0]]] == "-" and board_matrix[int(try_pos[1])+3][CHAR_MAP[try_pos[0]]] == "-": return 0
        else: return -1
    else: return -1
    return -1


# DONE
def send_ships(own_shipd, send_addr_ships, own_s_sock):
    ships_send_s = "ships"
    for ship, pos in own_shipd.items():
        if len(ship) == 2 and pos != "":
            ships_send_s += ","+ship+":"+pos
    own_s_sock.sendto(ships_send_s.encode("utf-8"), send_addr_ships)


# DONE
def rec_ships(rs_socket):
    riv_s: dict[str, str | list] = {}
    re_data, re_f_addr = rs_socket.recvfrom(1024)
    rec_array = re_data.decode("utf-8").split(",")
    print(rec_array)
    for rec_entry in rec_array:
        if len(rec_entry) == 6:
            rec_split = rec_entry.split(":")
            riv_s[rec_split[0]] = rec_split[1]
    print(riv_s)
    return riv_s


# DONE
def setup_ships(conn_mode_setup, send_addr_setup, setup_socket):
    os.system("cls")
    own_ship_dict: dict[str, str | list] = {
        "s1": "",
        "s2": "",
        "m1": "",
        "m2": "",
        "l1": "",
        "l2": "",
    }

    for ship, pos in own_ship_dict.items():
        ship_set = False
        false_set = False
        while not ship_set:
            print_board(own_ship_dict)
            if false_set: print("That doesn't work. Try again! ", end="")
            print("Choose a position for ", end="")
            if ship.startswith("s"):
                print("(small, len 2) ", end="")
            elif ship.startswith("m"):
                print("(medium, len 3) ", end="")
            elif ship.startswith("l"):
                print("(large, len 4) ", end="")
            print("ship like (e4, e4r, ..): ", end="")

            try_pos = input("").strip().lower()

            if 2 <= len(try_pos) <= 3:
                if len(try_pos) == 2:
                    if fit_ship(own_ship_dict, try_pos+"n", ship[0]) == 0:
                        own_ship_dict[ship] = try_pos+"n"
                        ship_set = True
                    else: false_set = True
                else:
                    if fit_ship(own_ship_dict, try_pos, ship[0]) == 0:
                        own_ship_dict[ship] = try_pos
                        ship_set = True
                    else:
                        false_set = True
            else: false_set = True

    # GET RIV SHIPS
    setup_socket.sendto((conn_mode_setup + "SetupDone").encode("utf-8"), send_addr_setup)
    os.system("cls")
    print_board(own_ship_dict)
    print("Waiting for other player to finish setup...")
    r_data, rec_f_addr = setup_socket.recvfrom(1024)

    if r_data.decode("utf-8") == "hSetupDone":
        riv_ship_dict = rec_ships(setup_socket)
        send_ships(own_ship_dict, send_addr_setup, setup_socket)
        own_ship_dict["misses"] = []
        riv_ship_dict["misses"] = []
        own_ship_dict["hits"] = []
        riv_ship_dict["hits"] = []
        return own_ship_dict, riv_ship_dict

    elif r_data.decode("utf-8") == "jSetupDone":
        send_ships(own_ship_dict, send_addr_setup, setup_socket)
        riv_ship_dict = rec_ships(setup_socket)
        own_ship_dict["misses"] = []
        riv_ship_dict["misses"] = []
        own_ship_dict["hits"] = []
        riv_ship_dict["hits"] = []
        return own_ship_dict, riv_ship_dict


# DONE
def legal_shot(shot_req, riv_b_dict):
    if len(shot_req) == 2 and shot_req[0] in CHAR_MAP.keys() and int(shot_req[1]) in INT_MAP.keys():
        if shot_req not in riv_b_dict["hits"] and shot_req not in riv_b_dict["misses"]: return True
        else: return False
    else: return False


# DONE
def transmit_check_shot(shot, riv_dict, send_addr, transmit_socket):
    shot_int = int(shot[1])
    ship_hit = False
    for ship, pos in riv_dict.items():
        if len(ship) == 2:
            if ship[0] == "s":
                if pos[2] == "n":
                    if pos[1] == shot[1]: # number is equal
                        if pos[0] == shot[0] or INT_MAP[CHAR_MAP[pos[0]]+1] == shot[0]: # char is equal
                            ship_hit = True
                elif pos[2] == "r":
                    if pos[0] == shot[0]: # char is equal
                        if int(pos[1]) == shot_int or int(pos[1])+1 == shot_int: # number is equal
                            ship_hit = True
            elif ship[0] == "m":
                if pos[2] == "n":
                    if pos[1] == shot[1]: # number is equal
                        if pos[0] == shot[0] or INT_MAP[CHAR_MAP[pos[0]]+1] == shot[0] or INT_MAP[CHAR_MAP[pos[0]]+2] == shot[0]: # char is equal
                            ship_hit = True
                elif pos[2] == "r":
                    if pos[0] == shot[0]: # char is equal
                        if int(pos[1]) == shot_int or int(pos[1])+1 == shot_int or int(pos[1])+2 == shot_int: # number is equal
                            ship_hit = True
            elif ship[0] == "l":
                if pos[2] == "n":
                    if pos[1] == shot[1]: # number is equal
                        if pos[0] == shot[0] or INT_MAP[CHAR_MAP[pos[0]]+1] == shot[0] or INT_MAP[CHAR_MAP[pos[0]]+2] == shot[0] or INT_MAP[CHAR_MAP[pos[0]]+3] == shot[0]: # char is equal
                            ship_hit = True
                elif pos[2] == "r":
                    if pos[0] == shot[0]: # char is equal
                        if int(pos[1]) == shot_int or int(pos[1])+1 == shot_int or int(pos[1])+2 == shot_int or int(pos[1])+3 == shot_int: # number is equal
                            ship_hit = True

    if ship_hit:
        send_hit(shot, send_addr, transmit_socket)
        riv_dict["hits"].append(shot)
    else:
        send_miss(shot, send_addr, transmit_socket)
        riv_dict["misses"].append(shot)

    return ship_hit, riv_dict


# DONE
def send_hit(send_shot, addr, send_socket):
    send_socket.sendto(f"h:{send_shot}".encode("utf-8"), addr)


# DONE
def send_miss(send_shot, addr, send_socket):
    send_socket.sendto(f"m:{send_shot}".encode("utf-8"), addr)


# MAIN
if __name__ == "__main__":

    # CREATE OWN SOCKET
    own_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # DEFINE CONN MODE
    conn_mode, send_addr = host_conn_setup(own_socket)

    # DEFINE SHIP POSITIONS
    own_ships, riv_ships = setup_ships(conn_mode, send_addr, own_socket)

    # BEGIN GAME
    hosts_turn = True
    while len(own_ships["hits"]) < 18 and len(riv_ships["hits"]) < 18:

        # ROUND START HOST TURN
        if hosts_turn:

            # ROUND IF HOST
            if conn_mode == "h":
                valid_shot = False
                while not valid_shot:
                    os.system("cls")
                    print_board(own_ships, riv_ships)
                    req_shot = input("Choose a field to shoot: ")
                    if legal_shot(req_shot.strip().lower(), riv_ships):
                        shot_result, riv_ships = transmit_check_shot(req_shot, riv_ships, send_addr, own_socket)
                        valid_shot = True
                        if shot_result: # shoot another round
                            continue
                        else: # other player turn
                            hosts_turn = False
                            continue
            # ROUND IF CLIENT
            elif conn_mode == "j":
                os.system("cls")
                print_board(own_ships, riv_ships)
                print("Waiting for other player to shoot...")
                rec_data, rec_f_addr = own_socket.recvfrom(1024)
                shot_data = rec_data.decode("utf-8")
                if shot_data[0] == "h": # other player shoot another round
                    own_ships["hits"].append(shot_data[2:])
                    continue
                else: # client turn
                    hosts_turn = False
                    own_ships["misses"].append(shot_data[2:])
                    continue

        # ROUND START CLIENT TURN
        else:

            # ROUND IF HOST
            if conn_mode == "h":
                os.system("cls")
                print_board(own_ships, riv_ships)
                print("Waiting for other player to shoot...")
                rec_data, rec_f_addr = own_socket.recvfrom(1024)
                shot_data = rec_data.decode("utf-8")
                if shot_data[0] == "h":  # other player shoot another round
                    own_ships["hits"].append(shot_data[2:])
                    continue
                else:  # client turn
                    hosts_turn = True
                    own_ships["misses"].append(shot_data[2:])
                    continue

            # ROUND IF CLIENT
            elif conn_mode == "j":
                valid_shot = False
                while not valid_shot:
                    os.system("cls")
                    print_board(own_ships, riv_ships)
                    req_shot = input("Choose a field to shoot: ")
                    if legal_shot(req_shot.strip().lower(), riv_ships):
                        shot_result, riv_ships = transmit_check_shot(req_shot, riv_ships, send_addr, own_socket)
                        valid_shot = True
                        if shot_result:  # shoot another round
                            continue
                        else:  # other player turn
                            hosts_turn = True
                            continue

    os.system("cls")
    if len(riv_ships["hits"]) == 18:
        print("===============================")
        print("            YOU WON!           ")
        print("===============================")
    elif len(own_ships["hits"]) == 18:
        print("===============================")
        print("            YOU LOST           ")
        print("===============================")
    game_done = input("")
    exit()




